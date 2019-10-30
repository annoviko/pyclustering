/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#pragma once


#include <pyclustering/cluster/elbow_data.hpp>
#include <pyclustering/cluster/kmeans.hpp>
#include <pyclustering/cluster/kmeans_plus_plus.hpp>

#include <pyclustering/parallel/parallel.hpp>

#include <pyclustering/utils/metric.hpp>

#include <pyclustering/definitions.hpp>


using namespace pyclustering::parallel;
using namespace pyclustering::utils::metric;


namespace pyclustering {

namespace clst {


template <class TypeInitializer = kmeans_plus_plus>
class elbow {
private:
    std::size_t   m_kmin      = 0;
    std::size_t   m_kmax      = 0;

    std::vector<double> m_elbow = { };

    const dataset * m_data      = nullptr;
    elbow_data    * m_result    = nullptr;      /* temporary pointer to output result   */

public:
    elbow() = default;

    elbow(const std::size_t p_kmin, const std::size_t p_kmax) : m_kmin(p_kmin), m_kmax(p_kmax) { verify(); }

    elbow(const elbow & p_other) = default;

    elbow(elbow && p_other) = default;

    ~elbow() = default;

public:
    void process(const dataset & p_data, elbow_data & p_result) {
        if (p_data.size() < m_kmax) {
            throw std::invalid_argument("K max value '" + std::to_string(m_kmax) 
              + "' is greater than amount of data points '" + std::to_string(p_data.size()) + "'.");
        }

        m_data   = &p_data;
        m_result = &p_result;

        m_result->get_wce().resize(m_kmax - m_kmin);

        parallel_for(m_kmin, m_kmax, [this](const std::size_t p_index){
            calculate_wce(p_index);
        });

        calculate_elbows();
        m_result->set_amount(find_optimal_kvalue());
    }

private:
    template<class CenterInitializer = TypeInitializer>
    typename std::enable_if<std::is_same<CenterInitializer, kmeans_plus_plus>::value, void>::type
    static prepare_centers(const std::size_t p_amount, const dataset & p_data, dataset & p_initial_centers) {
        kmeans_plus_plus(p_amount, kmeans_plus_plus::FARTHEST_CENTER_CANDIDATE).initialize(p_data, p_initial_centers);
    }

    template<class CenterInitializer = TypeInitializer>
    typename std::enable_if<!std::is_same<CenterInitializer, kmeans_plus_plus>::value, void>::type
    static prepare_centers(const std::size_t p_amount, const dataset & p_data, dataset & p_initial_centers) {
        TypeInitializer(p_amount).initialize(p_data, p_initial_centers);
    }

    void calculate_wce(const std::size_t p_amount) {
        dataset initial_centers;
        prepare_centers(p_amount, *m_data, initial_centers);

        kmeans_data result;
        kmeans instance(initial_centers, kmeans::DEFAULT_TOLERANCE);
        instance.process(*m_data, result);

        m_result->get_wce().at(p_amount - m_kmin) = result.wce();
    }

    void verify() {
        if (m_kmax < 3 + m_kmin) {
            throw std::invalid_argument("Amount of K '" + std::to_string(m_kmax - m_kmin) + "' is too small for analysis.");
        }
    }

    void calculate_elbows() {
        const wce_sequence & wce = m_result->get_wce();

        const double x0 = 0.0;
        const double y0 = wce.front();

        const double x1 = static_cast<double>(wce.size());
        const double y1 = wce.back();

        const double norm = euclidean_distance(point({ x0, y0 }), point({ x1, y1 }));

        m_elbow.resize(wce.size() - 2, 0.0);

        for (std::size_t index_elbow = 1; index_elbow < m_result->get_wce().size() - 1; index_elbow++) {
            const double x = static_cast<double>(index_elbow);
            const double y = wce.at(index_elbow);

            const double segment = std::abs((y0 - y1) * x + (x1 - x0) * y + (x0 * y1 - x1 * y0));
            
            m_elbow[index_elbow - 1] = segment / norm;
        }
    }

    std::size_t find_optimal_kvalue() {
        auto optimal_elbow_iter = std::max_element(m_elbow.cbegin(), m_elbow.cend());
        return std::distance(m_elbow.cbegin(), optimal_elbow_iter) + 1 + m_kmin;
    }
};


}

}