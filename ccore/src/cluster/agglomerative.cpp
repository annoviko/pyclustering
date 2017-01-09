/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#include "cluster/agglomerative.hpp"

#include <algorithm>

#include "utils.hpp"


namespace cluster_analysis {


agglomerative::agglomerative(void) :
    m_number_clusters(1),
    m_similarity(type_link::SINGLE_LINK),
    m_centers(0),
    m_ptr_clusters(nullptr),
    m_ptr_data(nullptr)
{ }


agglomerative::agglomerative(const size_t number_clusters, const type_link link) :
    m_number_clusters(number_clusters),
    m_similarity(link),
    m_centers(0),
    m_ptr_clusters(nullptr),
    m_ptr_data(nullptr)
{ }


agglomerative::~agglomerative(void) { }


void agglomerative::process(const dataset & data, cluster_data & result) {
    m_ptr_data = &data;
    m_ptr_clusters = result.clusters().get();

    m_centers.clear();
    m_ptr_clusters->clear();

    size_t current_number_clusters = data.size();

    m_centers.resize(current_number_clusters);
    m_ptr_clusters->resize(current_number_clusters);

    std::copy(data.begin(), data.end(), m_centers.begin());

    for (size_t i = 0; i < data.size(); i++) {
        (*m_ptr_clusters)[i].push_back(i);
    }

    while(current_number_clusters > m_number_clusters) {
        merge_similar_clusters();
        current_number_clusters = m_ptr_clusters->size();
    }

    m_ptr_data = nullptr;
}


void agglomerative::merge_similar_clusters(void) {
    switch(m_similarity) {
        case type_link::SINGLE_LINK:
            merge_by_signle_link();
            break;
        case type_link::COMPLETE_LINK:
            merge_by_complete_link();
            break;
        case type_link::AVERAGE_LINK:
            merge_by_average_link();
            break;
        case type_link::CENTROID_LINK:
            merge_by_centroid_link();
            break;
        default:
            throw std::runtime_error("Unknown type of similarity is used.");
    }
}


void agglomerative::merge_by_average_link(void) {
    double minimum_average_distance = std::numeric_limits<double>::max();

    const std::vector<point> & data = *m_ptr_data;

    size_t index1 = 0;
    size_t index2 = 1;

    for (size_t index_cluster1 = 0; index_cluster1 < m_ptr_clusters->size(); index_cluster1++) {
        for (size_t index_cluster2 = index_cluster1 + 1; index_cluster2 < m_ptr_clusters->size(); index_cluster2++) {
            double candidate_average_distance = 0.0;

            for (auto index_object1 : (*m_ptr_clusters)[index_cluster1]) {
                for (auto index_object2 : (*m_ptr_clusters)[index_cluster2]) {
                    candidate_average_distance += euclidean_distance_sqrt(&data[index_object1], &data[index_object2]);
                }
            }

            candidate_average_distance /= ((*m_ptr_clusters)[index_cluster1].size() + (*m_ptr_clusters)[index_cluster2].size());

            if (candidate_average_distance < minimum_average_distance) {
                minimum_average_distance = candidate_average_distance;

                index1 = index_cluster1;
                index2 = index_cluster2;
            }
        }
    }

    (*m_ptr_clusters)[index1].insert((*m_ptr_clusters)[index1].end(), (*m_ptr_clusters)[index2].begin(), (*m_ptr_clusters)[index2].end());
    m_ptr_clusters->erase(m_ptr_clusters->begin() + index2);
}


void agglomerative::merge_by_centroid_link(void) {
    double minimum_average_distance = std::numeric_limits<double>::max();

    size_t index_cluster1 = 0;
    size_t index_cluster2 = 1;

    for (size_t index1 = 0; index1 < m_centers.size(); index1++) {
        for (size_t index2 = index1 + 1; index2 < m_centers.size(); index2++) {
            double distance = euclidean_distance_sqrt(&m_centers[index1], &m_centers[index2]);
            if (distance < minimum_average_distance) {
                minimum_average_distance = distance;

                index_cluster1 = index1;
                index_cluster2 = index2;
            }
        }
    }

    (*m_ptr_clusters)[index_cluster1].insert((*m_ptr_clusters)[index_cluster1].end(), (*m_ptr_clusters)[index_cluster2].begin(), (*m_ptr_clusters)[index_cluster2].end());
    calculate_center((*m_ptr_clusters)[index_cluster1], m_centers[index_cluster2]);

    m_ptr_clusters->erase(m_ptr_clusters->begin() + index_cluster2);
    m_centers.erase(m_centers.begin() + index_cluster2);
}


void agglomerative::merge_by_complete_link(void) {
    double minimum_complete_distance = std::numeric_limits<double>::max();

    size_t index1 = 0;
    size_t index2 = 1;

    const std::vector<point> & data = *m_ptr_data;

    for (size_t index_cluster1 = 0; index_cluster1 < m_ptr_clusters->size(); index_cluster1++) {
        for (size_t index_cluster2 = index_cluster1 + 1; index_cluster2 < m_ptr_clusters->size(); index_cluster2++) {
            double candidate_maximum_distance = 0.0;

            for (auto index_object1 : (*m_ptr_clusters)[index_cluster1]) {
                for (auto index_object2 : (*m_ptr_clusters)[index_cluster2]) {
                    double distance = euclidean_distance_sqrt(&data[index_object1], &data[index_object2]);
                    if (distance > candidate_maximum_distance) {
                        candidate_maximum_distance = distance;
                    }
                }
            }

            if (candidate_maximum_distance < minimum_complete_distance) {
                minimum_complete_distance = candidate_maximum_distance;

                index1 = index_cluster1;
                index2 = index_cluster2;
            }
        }
    }

    (*m_ptr_clusters)[index1].insert((*m_ptr_clusters)[index1].end(), (*m_ptr_clusters)[index2].begin(), (*m_ptr_clusters)[index2].end());
    m_ptr_clusters->erase(m_ptr_clusters->begin() + index2);
}


void agglomerative::merge_by_signle_link(void) {
    double minimum_single_distance = std::numeric_limits<double>::max();

    size_t index1 = 0;
    size_t index2 = 1;

    const std::vector<point> & data = *m_ptr_data;

    for (size_t index_cluster1 = 0; index_cluster1 < m_ptr_clusters->size(); index_cluster1++) {
        for (size_t index_cluster2 = index_cluster1 + 1; index_cluster2 < m_ptr_clusters->size(); index_cluster2++) {
            double candidate_minimum_distance = std::numeric_limits<double>::max();

            for (auto index_object1 : (*m_ptr_clusters)[index_cluster1]) {
                for (auto index_object2 : (*m_ptr_clusters)[index_cluster2]) {
                    double distance = euclidean_distance_sqrt(&data[index_object1], &data[index_object2]);
                    if (distance < candidate_minimum_distance) {
                        candidate_minimum_distance = distance;
                    }
                }
            }

            if (candidate_minimum_distance < minimum_single_distance) {
                minimum_single_distance = candidate_minimum_distance;

                index1 = index_cluster1;
                index2 = index_cluster2;
            }
        }
    }

    (*m_ptr_clusters)[index1].insert((*m_ptr_clusters)[index1].end(), (*m_ptr_clusters)[index2].begin(), (*m_ptr_clusters)[index2].end());
    m_ptr_clusters->erase(m_ptr_clusters->begin() + index2);
}


void agglomerative::calculate_center(const cluster & cluster, point & center) {
    const std::vector<point> & data = *m_ptr_data;

    const size_t dimension = data[0].size();

    center.resize(dimension, 0.0);

    for (auto index_point : cluster) {
        for (size_t index_dimension = 0; index_dimension < dimension; index_dimension++) {
            center[index_dimension] += data[index_point][index_dimension];
        }
    }

    for (size_t index_dimension = 0; index_dimension < dimension; index_dimension++) {
        center[index_dimension] /= cluster.size();
    }
}


}
