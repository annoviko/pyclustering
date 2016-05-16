/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#include "cluster/kmedoids.hpp"

#include "utils.hpp"

#include <limits>


namespace cluster_analysis {


kmedoids::kmedoids(void) :
        m_data_ptr(nullptr),
        m_result_ptr(nullptr),
        m_initial_medoids(std::vector<size_t>()),
        m_tolerance(0.0)
{ }


kmedoids::kmedoids(const std::vector<size_t> & p_initial_medoids, const double p_tolerance) :
        m_data_ptr(nullptr),
        m_result_ptr(nullptr),
        m_initial_medoids(p_initial_medoids),
        m_tolerance(p_tolerance)
{ }


kmedoids::~kmedoids(void) { }


void kmedoids::process(const dataset & p_data, cluster_data & p_result) {
    m_data_ptr = &p_data;
    m_result_ptr = (kmedoids_data *) &p_result;

    medoid_sequence & medoids = *(m_result_ptr->medoids());
    medoids.assign(m_initial_medoids.begin(), m_initial_medoids.end());

    double changes = 0.0;
    do {
        update_clusters();

        std::vector<size_t> updated_medoids;
        calculate_medoids(updated_medoids);

        changes = calculate_changes(updated_medoids);

        medoids.swap(updated_medoids);
    }
    while (changes > m_tolerance);

    m_data_ptr = nullptr;
    m_result_ptr = nullptr;
}


void kmedoids::update_clusters(void) {
    cluster_sequence & clusters = *(m_result_ptr->clusters());
    medoid_sequence & medoids = *(m_result_ptr->medoids());

    clusters.clear();
    clusters.resize(medoids.size());

    for (size_t index_point = 0; index_point < m_data_ptr->size(); index_point++) {
        size_t index_optim = 0;
        double dist_optim = 0.0;

        for (size_t index = 0; index < medoids.size(); index++) {
            const size_t index_medoid = medoids[index];
            const double distance = euclidean_distance_sqrt(&(*m_data_ptr)[index_point], &(*m_data_ptr)[index_medoid]);

            if ( (distance < dist_optim) || (index == 0) ) {
                index_optim = index;
                dist_optim = distance;
            }
        }

        clusters[index_optim].push_back(index_point);
    }

    erase_empty_clusters(clusters);
}


void kmedoids::erase_empty_clusters(cluster_sequence & p_clusters) {
    for (size_t index_cluster = p_clusters.size() - 1; index_cluster != (size_t) -1; index_cluster--) {
        if (p_clusters[index_cluster].empty()) {
            p_clusters.erase(p_clusters.begin() + index_cluster);
        }
    }
}


void kmedoids::calculate_medoids(std::vector<size_t> & p_medoids) {
    cluster_sequence & clusters = *(m_result_ptr->clusters());

    p_medoids.clear();
    p_medoids.resize(clusters.size());

    for (size_t index = 0; index < clusters.size(); index++) {
        p_medoids[index] = calculate_cluster_medoid(clusters[index]);
    }
}


size_t kmedoids::calculate_cluster_medoid(const cluster & p_cluster) const {
    size_t index_medoid = 0;
    double distance = std::numeric_limits<double>::max();

    for (auto index_candidate : p_cluster) {
        double distance_candidate = 0.0;
        for (auto index_point : p_cluster) {
            distance_candidate += euclidean_distance_sqrt( &(*m_data_ptr)[index_point], &(*m_data_ptr)[index_candidate] );
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
        const size_t index_point2 = (*m_result_ptr->medoids())[index];

        const double distance = euclidean_distance_sqrt( &(*m_data_ptr)[index_point1], &(*m_data_ptr)[index_point2] );
        if (distance > maximum_difference) {
            maximum_difference = distance;
        }
    }

    return maximum_difference;
}


}
