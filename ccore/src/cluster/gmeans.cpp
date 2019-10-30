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

#include <algorithm>
#include <limits>
#include <numeric>

#include <pyclustering/cluster/gmeans.hpp>
#include <pyclustering/cluster/kmeans.hpp>
#include <pyclustering/cluster/kmeans_plus_plus.hpp>

#include <pyclustering/parallel/parallel.hpp>

#include <pyclustering/utils/linalg.hpp>
#include <pyclustering/utils/metric.hpp>
#include <pyclustering/utils/stats.hpp>


using namespace pyclustering::parallel;
using namespace pyclustering::utils::linalg;
using namespace pyclustering::utils::metric;
using namespace pyclustering::utils::stats;


namespace pyclustering {

namespace clst {


const double             gmeans::DEFAULT_TOLERANCE      = 0.001;

const std::size_t        gmeans::DEFAULT_REPEAT         = 3;

const std::size_t        gmeans::DEFAULT_CANDIDATES     = 3;


gmeans::gmeans(const std::size_t p_k_initial, const double p_tolerance, const std::size_t p_repeat) :
    m_amount(p_k_initial),
    m_tolerance(p_tolerance),
    m_repeat(p_repeat),
    m_ptr_result(nullptr),
    m_ptr_data(nullptr)
{ }


void gmeans::process(const dataset & p_data, cluster_data & p_result) {
    m_ptr_data = &p_data;
    m_ptr_result = dynamic_cast<gmeans_data *>(&p_result);

    if (!m_ptr_result) {
        throw std::invalid_argument("Invalid result storage is specified: impossible to cast to 'gmeans_data'.");
    }

    search_optimal_parameters(p_data, m_amount, m_ptr_result->clusters(), m_ptr_result->centers());

    while(true) {
        std::size_t current_amount_clusters = m_ptr_result->clusters().size();
        statistical_optimization();

        if (current_amount_clusters == m_ptr_result->centers().size()) {
            break;
        }

        perform_clustering();
    }
}


void gmeans::search_optimal_parameters(const dataset & p_data, const std::size_t p_amount, cluster_sequence & p_clusters, dataset & p_centers) const {
    double           best_wce = std::numeric_limits<double>::infinity();
    cluster_sequence best_clusters = { };
    dataset          best_centers = { };

    for (std::size_t i = 0; i < m_repeat; i++) {
        dataset initial_centers;
        kmeans_plus_plus(p_amount, get_amount_candidates(p_data)).initialize(p_data, initial_centers);

        kmeans_data result;
        kmeans(initial_centers, m_tolerance).process(p_data, result);

        if (result.wce() < best_wce) {
            best_wce = result.wce();
            best_clusters = std::move(result.clusters());
            best_centers = std::move(result.centers());
        }

        if (p_amount == 1) {
            break;      /* No need to rerun clustering for one initial center. */
        }
    }

    p_clusters = std::move(best_clusters);
    p_centers = std::move(best_centers);
}


void gmeans::statistical_optimization() {
    dataset centers;
    for (std::size_t i = 0; i < m_ptr_result->clusters().size(); i++) {
        dataset new_centers;
        split_and_search_optimal(m_ptr_result->clusters().at(i), new_centers);
        
        if (new_centers.empty()) {
            centers.push_back(std::move(m_ptr_result->centers().at(i)));
        }
        else {
            centers.push_back(std::move(new_centers[0]));
            centers.push_back(std::move(new_centers[1]));
        }
    }

    m_ptr_result->centers() = std::move(centers);
}


void gmeans::perform_clustering() {
    kmeans_data result;
    kmeans(m_ptr_result->centers(), m_tolerance).process(*m_ptr_data, result);

    m_ptr_result->clusters() = std::move(result.clusters());
    m_ptr_result->centers() = std::move(result.centers());
    m_ptr_result->wce() = result.wce();
}


void gmeans::split_and_search_optimal(const cluster & p_cluster, dataset & p_centers) const {
    if (p_cluster.size() == 1) {
        return;
    }

    dataset region_points(p_cluster.size());
    for (std::size_t i = 0; i < region_points.size(); i++) {
        region_points[i] = m_ptr_data->at(p_cluster[i]);
    }

    cluster_sequence new_clusters;
    dataset new_centers;

    search_optimal_parameters(region_points, 2, new_clusters, new_centers);
    if (new_centers.size() > 1) {
        if (!is_null_hypothesis(region_points, new_centers[0], new_centers[1])) {
            p_centers = std::move(new_centers);
        }
    }
}


bool gmeans::is_null_hypothesis(const dataset & p_data, const point & p_center1, const point & p_center2) {
    point v = subtract(p_center1, p_center2);
    projection sample = calculate_projection(p_data, v);

    double estimation = anderson(sample);
    std::vector<double> critical = critical_values(sample.size());

    return (estimation < critical.back());  /* true - Gaussian distribution, false - not a Gaussian distribution */
}


std::size_t gmeans::get_amount_candidates(const dataset & p_data) {
    return (p_data.size() > DEFAULT_CANDIDATES) ? DEFAULT_CANDIDATES : p_data.size();
}


gmeans::projection gmeans::calculate_projection(const dataset & p_data, const point & p_vector) {
    double square_norm = sum(multiply(p_vector, p_vector));
    return divide(sum(multiply(p_data, p_vector), 1), square_norm);
}


}

}