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

#include "cluster/kmedians.hpp"

#include "utils.hpp"


namespace cluster_analysis {


kmedians::kmedians(void) :
    m_tolerance(0.025),
    m_initial_medians(0, point()),
    m_ptr_result(nullptr),
    m_ptr_data(nullptr) { }


kmedians::kmedians(const dataset & initial_medians, const double tolerance) :
    m_tolerance(tolerance),
    m_initial_medians(initial_medians),
    m_ptr_result(nullptr),
    m_ptr_data(nullptr) { }


kmedians::~kmedians(void) { }


void kmedians::process(const dataset & data, cluster_data & output_result) {
    m_ptr_data = &data;
    m_ptr_result = (kmedians_data *) &output_result;

    if (data[0].size() != m_initial_medians[0].size()) {
        throw std::runtime_error("CCORE [kmedians]: dimension of the input data and dimension of the initial cluster medians must be equal.");
    }

    m_ptr_result->medians()->assign(m_initial_medians.begin(), m_initial_medians.end());

    double stop_condition = m_tolerance * m_tolerance;
    double changes = 0.0;
    double prev_changes = 0.0;

    size_t counter_repeaters = 0;

    do {
        update_clusters(*m_ptr_result->medians(), *m_ptr_result->clusters());
        changes = update_medians(*m_ptr_result->clusters(), *m_ptr_result->medians());

        double change_difference = abs(changes - prev_changes);
        if (change_difference < 0.000001) {
            counter_repeaters++;
        }
        else {
            counter_repeaters = 0;
        }

        prev_changes = changes;
    }
    while ((changes > stop_condition) && (counter_repeaters < 10));

    m_ptr_data = nullptr;
    m_ptr_result = nullptr;
}


void kmedians::update_clusters(const dataset & medians, cluster_sequence & clusters) {
    const dataset & data = *m_ptr_data;

    clusters.clear();
    clusters.resize(medians.size());

    for (size_t index_point = 0; index_point < data.size(); index_point++) {
        size_t index_cluster_optim = 0;
        double distance_optim = std::numeric_limits<double>::max();

        for (size_t index_cluster = 0; index_cluster < medians.size(); index_cluster++) {
            double distance = euclidean_distance_sqrt(&data[index_point], &medians[index_cluster]);
            if (distance < distance_optim) {
                index_cluster_optim = index_cluster;
                distance_optim = distance;
            }
        }

        clusters[index_cluster_optim].push_back(index_point);
    }

    erase_empty_clusters(clusters);
}


void kmedians::erase_empty_clusters(cluster_sequence & p_clusters) {
    for (size_t index_cluster = p_clusters.size() - 1; index_cluster != (size_t) -1; index_cluster--) {
        if (p_clusters[index_cluster].empty()) {
            p_clusters.erase(p_clusters.begin() + index_cluster);
        }
    }
}


double kmedians::update_medians(cluster_sequence & clusters, dataset & medians) {
    const dataset & data = *m_ptr_data;
    const size_t dimension = data[0].size();

    std::vector<point> prev_medians(medians);

    medians.clear();
    medians.resize(clusters.size(), point(dimension, 0.0));

    double maximum_change = 0.0;

    for (size_t index_cluster = 0; index_cluster < clusters.size(); index_cluster++) {
        for (size_t index_dimension = 0; index_dimension < dimension; index_dimension++) {
            cluster & current_cluster = clusters[index_cluster];
            std::sort(current_cluster.begin(), current_cluster.end(), 
                [this](unsigned int index_object1, unsigned int index_object2) 
            {
                return (*m_ptr_data)[index_object1] > (*m_ptr_data)[index_object2];
            });

            size_t relative_index_median = (size_t) floor(current_cluster.size() / 2.0);
            size_t index_median = current_cluster[relative_index_median];

            if ( (current_cluster.size() % 2) && (relative_index_median + 1 < current_cluster.size()) ) {
                size_t index_median_second = current_cluster[relative_index_median + 1];
                medians[index_cluster][index_dimension] = (data[index_median][index_dimension] + data[index_median_second][index_dimension]) / 2.0;
            }
            else {
                medians[index_cluster][index_dimension] = data[index_median][index_dimension];
            }
        }

        double change = euclidean_distance_sqrt(&prev_medians[index_cluster], &medians[index_cluster]);
        if (change > maximum_change) {
            maximum_change = change;
        }
    }

    return maximum_change;
}


}
