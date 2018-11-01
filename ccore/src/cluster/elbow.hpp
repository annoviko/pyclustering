/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


#include "cluster/elbow_data.hpp"
#include "cluster/kmeans.hpp"
#include "cluster/kmeans_plus_plus.hpp"

#include "utils/metric.hpp"

#include "definitions.hpp"


using namespace ccore::utils::metric;


namespace ccore {

namespace clst {


template <class TypeInitializer = kmeans_plus_plus>
class elbow {
private:
    std::size_t   m_kmin      = 0;
    std::size_t   m_kmax      = 0;

    std::vector<double> m_elbow = { };

    elbow_data    * m_result  = nullptr;      /* temporary pointer to output result   */

public:
    elbow(void) = default;

    elbow(const std::size_t p_kmin, const std::size_t p_kmax) :
        m_kmin(p_kmin), m_kmax(p_kmax)
    { verify(); }

    elbow(const elbow & p_other) = default;

    elbow(elbow && p_other) = default;

    ~elbow(void) = default;

public:
    void process(const dataset & p_data, elbow_data & p_result) {
        if (p_data.size() < m_kmax) {
            throw std::invalid_argument("K max value '" + std::to_string(m_kmax) 
              + "' is greater than amount of data points '" + std::to_string(p_data.size()) + "'.");
        }

        m_result = &p_result;
        m_elbow.clear();

        for (std::size_t i = m_kmin; i < m_kmax; i++) {
            dataset initial_centers;
            TypeInitializer(i).initialize(p_data, initial_centers);

            kmeans_data result;
            kmeans instance(initial_centers, 0.0001);
            instance.process(p_data, result);

            m_result->get_wce().push_back(result.wce());
        }

        calculate_elbows();
        m_result->set_amount(find_optimal_kvalue());
    }

private:
    void verify(void) {
        if (m_kmax < 3 + m_kmin) {
            throw std::invalid_argument("Amount of K '" + std::to_string(m_kmax - m_kmin) + "' is too small for analysis.");
        }
    }

    void calculate_elbows(void) {
        const double x0 = 0.0;
        const double y0 = m_result->get_wce().front();

        const double x1 = (double) m_result->get_wce().size();
        const double y1 = m_result->get_wce().back();

        for (std::size_t index_elbow = 1; index_elbow < m_result->get_wce().size() - 1; index_elbow++) {
            const double x = (double) index_elbow;
            const double y = m_result->get_wce().at(index_elbow);

            const double segment = std::abs((y0 - y1) * x + (x1 - x0) * y + (x0 * y1 - x1 * y0));
            const double norm = euclidean_distance(point({ x0, y0 }), point({ x1, y1 }));
            m_elbow.push_back(segment / norm);
        }
    }

    std::size_t find_optimal_kvalue(void) {
        auto optimal_elbow_iter = std::max_element(m_elbow.cbegin(), m_elbow.cend());
        return std::distance(m_elbow.cbegin(), optimal_elbow_iter) + 1 + m_kmin;
    }
};


}

}