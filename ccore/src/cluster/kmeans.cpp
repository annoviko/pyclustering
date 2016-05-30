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

#include "cluster/kmeans.hpp"

#include <algorithm>
#include <limits>

#include "utils.hpp"


namespace cluster_analysis {


kmeans::kmeans(void) :
    m_tolerance(0.025),
    m_initial_centers(0, point()),
    m_ptr_result(nullptr),
    m_ptr_data(nullptr) { }


kmeans::kmeans(const dataset & p_initial_centers, const double p_tolerance) :
    m_tolerance(p_tolerance * p_tolerance),
    m_initial_centers(p_initial_centers),
    m_ptr_result(nullptr),
    m_ptr_data(nullptr) { }


kmeans::~kmeans(void) { }


void kmeans::process(const dataset & data, cluster_data & output_result) {
    m_ptr_data = &data;

    output_result = kmeans_data();
    m_ptr_result = (kmeans_data *) &output_result;

    if (data[0].size() != m_initial_centers[0].size()) {
        throw std::runtime_error("CCORE [kmeans]: dimension of the input data and dimension of the initial cluster centers must be equal.");
    }

    m_ptr_result->centers()->assign(m_initial_centers.begin(), m_initial_centers.end());

    double current_change = std::numeric_limits<double>::max();

    while(current_change > m_tolerance) {
        update_clusters(*m_ptr_result->centers(), *m_ptr_result->clusters());
        current_change = update_centers(*m_ptr_result->clusters(), *m_ptr_result->centers());
    }
}


void kmeans::update_clusters(const dataset & centers, cluster_sequence & clusters) {
    const dataset & data = *m_ptr_data;

    clusters.clear();
    clusters.resize(centers.size());

    /* fill clusters again in line with centers. */
    for (size_t index_object = 0; index_object < data.size(); index_object++) {
        double    minimum_distance = std::numeric_limits<double>::max();
        size_t    suitable_index_cluster = 0;

        for (size_t index_cluster = 0; index_cluster < clusters.size(); index_cluster++) {
            double distance = euclidean_distance_sqrt(&centers[index_cluster], &data[index_object]);

            if (distance < minimum_distance) {
                minimum_distance = distance;
                suitable_index_cluster = index_cluster;
            }
        }

        clusters[suitable_index_cluster].push_back(index_object);
    }

    erase_empty_clusters(clusters);
}


void kmeans::erase_empty_clusters(cluster_sequence & p_clusters) {
    for (size_t index_cluster = p_clusters.size() - 1; index_cluster != (size_t) -1; index_cluster--) {
        if (p_clusters[index_cluster].empty()) {
            p_clusters.erase(p_clusters.begin() + index_cluster);
        }
    }
}


double kmeans::update_centers(const cluster_sequence & clusters, dataset & centers) {
    const dataset & data = *m_ptr_data;
    const size_t dimension = data[0].size();

    double maximum_change = 0;

    dataset updated_clusters(clusters.size(), point(dimension, 0.0));

    /* for each cluster */
    for (size_t index_cluster = 0; index_cluster < clusters.size(); index_cluster++) {
        point total(centers[index_cluster].size(), 0.0);

        /* for each object in cluster */
        for (auto object_index : clusters[index_cluster]) {
            /* for each dimension */
            for (size_t dimension = 0; dimension < total.size(); dimension++) {
                total[dimension] += data[object_index][dimension];
            }
        }

        /* average for each dimension */
        for (size_t dimension = 0; dimension < total.size(); dimension++) {
            total[dimension] = total[dimension] / clusters[index_cluster].size();
        }

        double distance = euclidean_distance_sqrt(&centers[index_cluster], &total);

        if (distance > maximum_change) {
            maximum_change = distance;
        }

        updated_clusters[index_cluster] = std::move(total);
    }

    centers.clear();
    centers = std::move(updated_clusters);

    return maximum_change;
}


}
