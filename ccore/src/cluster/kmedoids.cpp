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

#include <pyclustering/cluster/kmedoids.hpp>

#include <algorithm>
#include <limits>

#include <pyclustering/parallel/parallel.hpp>


using namespace pyclustering::parallel;


namespace pyclustering {

namespace clst {


const std::size_t kmedoids::OBJECT_ALREADY_CONTAINED = std::numeric_limits<std::size_t>::max();


const double             kmedoids::DEFAULT_TOLERANCE                       = 0.001;

const std::size_t        kmedoids::DEFAULT_ITERMAX                         = 100;


kmedoids::kmedoids(const medoid_sequence & p_initial_medoids,
                   const double p_tolerance,
                   const std::size_t p_itermax,
                   const distance_metric<point> & p_metric) :
    m_data_ptr(nullptr),
    m_result_ptr(nullptr),
    m_initial_medoids(p_initial_medoids),
    m_tolerance(p_tolerance),
    m_itermax(p_itermax),
    m_metric(p_metric)
{ }


kmedoids::~kmedoids() { }


void kmedoids::process(const dataset & p_data, cluster_data & p_result) {
    process(p_data, kmedoids_data_t::POINTS, p_result);
}


void kmedoids::process(const dataset & p_data, const kmedoids_data_t p_type, cluster_data & p_result) {
    m_data_ptr = &p_data;
    m_result_ptr = (kmedoids_data *) &p_result;
    m_calculator = create_distance_calculator(p_type);

    medoid_sequence & medoids = m_result_ptr->medoids();
    medoids.assign(m_initial_medoids.begin(), m_initial_medoids.end());

    double changes = std::numeric_limits<double>::max();
    for (std::size_t iteration = 0; (iteration < m_itermax) && (changes > m_tolerance); iteration++) {
        update_clusters();

        std::vector<size_t> updated_medoids;
        calculate_medoids(updated_medoids);

        changes = calculate_changes(updated_medoids);

        medoids.swap(updated_medoids);
    }

    m_data_ptr = nullptr;
    m_result_ptr = nullptr;
}


void kmedoids::update_clusters() {
    cluster_sequence & clusters = m_result_ptr->clusters();
    medoid_sequence & medoids = m_result_ptr->medoids();

    clusters.clear();
    clusters.resize(medoids.size());

    for (std::size_t i = 0; i < medoids.size(); i++) {
        clusters[i].push_back(medoids[i]);
    }

    std::vector<std::size_t> cluster_markers(m_data_ptr->size());
    parallel_for(std::size_t(0), m_data_ptr->size(), [this, &medoids, &cluster_markers](const std::size_t p_index) {
        cluster_markers[p_index] = find_appropriate_cluster(p_index, medoids);
    });

    for (std::size_t index_point = 0; index_point < m_data_ptr->size(); index_point++) {
        const std::size_t index_optim = cluster_markers[index_point];
        if (index_optim != OBJECT_ALREADY_CONTAINED) {
            clusters[index_optim].push_back(index_point);
        }
    }
}


void kmedoids::calculate_medoids(cluster & p_medoids) {
    cluster_sequence & clusters = m_result_ptr->clusters();

    p_medoids.clear();
    p_medoids.resize(clusters.size());

    parallel_for(std::size_t(0), clusters.size(), [this, &p_medoids, &clusters](const std::size_t index) {
        p_medoids[index] = calculate_cluster_medoid(clusters[index]);
    });
}


size_t kmedoids::calculate_cluster_medoid(const cluster & p_cluster) const {
    size_t index_medoid = 0;
    double distance = std::numeric_limits<double>::max();

    for (auto index_candidate : p_cluster) {
        double distance_candidate = 0.0;
        for (auto index_point : p_cluster) {
            distance_candidate += m_calculator(index_point, index_candidate);
        }

        if (distance_candidate < distance) {
            index_medoid = index_candidate;
            distance = distance_candidate;
        }
    }

    return index_medoid;
}


double kmedoids::calculate_changes(const medoid_sequence & p_medoids) const {
    double maximum_difference = 0.0;
    for (size_t index = 0; index < p_medoids.size(); index++) {
        const size_t index_point1 = p_medoids[index];
        const size_t index_point2 = m_result_ptr->medoids()[index];

        const double distance = m_calculator(index_point1, index_point2);
        if (distance > maximum_difference) {
            maximum_difference = distance;
        }
    }

    return maximum_difference;
}


kmedoids::distance_calculator kmedoids::create_distance_calculator(const kmedoids_data_t p_type) {
    if (p_type == kmedoids_data_t::POINTS) {
        return [this](const std::size_t index1, const std::size_t index2) {
          return m_metric((*m_data_ptr)[index1], (*m_data_ptr)[index2]); 
        };
    }
    else if (p_type == kmedoids_data_t::DISTANCE_MATRIX) {
        return [this](const std::size_t index1, const std::size_t index2) {
          return (*m_data_ptr)[index1][index2];
        };
    }
    else {
        throw std::invalid_argument("Unknown type data is specified");
    }
}


std::size_t kmedoids::find_appropriate_cluster(const std::size_t p_index, medoid_sequence & p_medoids) {
    if (std::find(p_medoids.begin(), p_medoids.end(), p_index) != p_medoids.cend()) {
        return OBJECT_ALREADY_CONTAINED;
    }

    size_t index_optim = 0;
    double dist_optim = m_calculator(p_index, p_medoids[index_optim]);

    for (size_t index = 1; index < p_medoids.size(); index++) {
        const size_t index_medoid = p_medoids[index];
        const double distance = m_calculator(p_index, index_medoid);

        if (distance < dist_optim) {
            index_optim = index;
            dist_optim = distance;
        }
    }

    return index_optim;
}


}

}
