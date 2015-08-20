#include "agglomerative.h"
#include "support.h"

#include <algorithm>



agglomerative::agglomerative() :
m_number_clusters(1),
m_similarity(SINGLE_LINK),
m_centers(0),
m_clusters(0),
m_ptr_data(nullptr) { }


agglomerative::agglomerative(const unsigned int number_clusters, const type_link link) :
m_number_clusters(number_clusters),
m_similarity(link),
m_centers(0),
m_clusters(0),
m_ptr_data(nullptr) { }


agglomerative::~agglomerative() { }


void agglomerative::initialize(const unsigned int number_clusters, const type_link link) {
    m_number_clusters = number_clusters;
    m_similarity = link;

    m_centers.clear();
    m_clusters.clear();

    m_ptr_data = nullptr;
}


void agglomerative::process(const std::vector<point> & data) {
    m_ptr_data = (std::vector<point> *) &data;

    m_centers.clear();
    m_clusters.clear();

    size_t current_number_clusters = data.size();

    m_centers.resize(current_number_clusters);
    m_clusters.resize(current_number_clusters);

    std::copy(data.begin(), data.end(), m_centers.begin());

    for (size_t i = 0; i < data.size(); i++) {
        m_clusters[i].push_back(i);
    }

    while(current_number_clusters > m_number_clusters) {
        merge_similar_clusters();
        current_number_clusters = m_clusters.size();
    }

    m_ptr_data = nullptr;
}


void agglomerative::merge_similar_clusters(void) {
    switch(m_similarity) {
        case SINGLE_LINK:
            merge_by_signle_link();
            break;
        case COMPLETE_LINK:
            merge_by_complete_link();
            break;
        case AVERAGE_LINK:
            merge_by_average_link();
            break;
        case CENTROID_LINK:
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

    for (size_t index_cluster1 = 0; index_cluster1 < m_clusters.size(); index_cluster1++) {
        for (size_t index_cluster2 = index_cluster1 + 1; index_cluster2 < m_clusters.size(); index_cluster2++) {
            double candidate_average_distance = 0.0;

            for (auto index_object1 : m_clusters[index_cluster1]) {
                for (auto index_object2 : m_clusters[index_cluster2]) {
                    candidate_average_distance += euclidean_distance_sqrt(&data[index_object1], &data[index_object2]);
                }
            }

            candidate_average_distance /= (m_clusters[index_cluster1].size() + m_clusters[index_cluster2].size());

            if (candidate_average_distance < minimum_average_distance) {
                minimum_average_distance = candidate_average_distance;

                index1 = index_cluster1;
                index2 = index_cluster2;
            }
        }
    }

    m_clusters[index1].insert(m_clusters[index1].end(), m_clusters[index2].begin(), m_clusters[index2].end());
    m_clusters.erase(m_clusters.begin() + index2);
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

    m_clusters[index_cluster1].insert(m_clusters[index_cluster1].end(), m_clusters[index_cluster2].begin(), m_clusters[index_cluster2].end());
    calculate_center(m_clusters[index_cluster1], m_centers[index_cluster2]);

    m_clusters.erase(m_clusters.begin() + index_cluster2);
    m_centers.erase(m_centers.begin() + index_cluster2);
}


void agglomerative::merge_by_complete_link(void) {
    double minimum_complete_distance = std::numeric_limits<double>::max();

    size_t index1 = 0;
    size_t index2 = 1;

    const std::vector<point> & data = *m_ptr_data;

    for (size_t index_cluster1 = 0; index_cluster1 < m_clusters.size(); index_cluster1++) {
        for (size_t index_cluster2 = index_cluster1 + 1; index_cluster2 < m_clusters.size(); index_cluster2++) {
            double candidate_maximum_distance = 0.0;

            for (auto index_object1 : m_clusters[index_cluster1]) {
                for (auto index_object2 : m_clusters[index_cluster2]) {
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

    m_clusters[index1].insert(m_clusters[index1].end(), m_clusters[index2].begin(), m_clusters[index2].end());
    m_clusters.erase(m_clusters.begin() + index2);
}


void agglomerative::merge_by_signle_link(void) {
    double minimum_single_distance = std::numeric_limits<double>::max();

    size_t index1 = 0;
    size_t index2 = 1;

    const std::vector<point> & data = *m_ptr_data;

    for (size_t index_cluster1 = 0; index_cluster1 < m_clusters.size(); index_cluster1++) {
        for (size_t index_cluster2 = index_cluster1 + 1; index_cluster2 < m_clusters.size(); index_cluster2++) {
            double candidate_minimum_distance = std::numeric_limits<double>::max();

            for (auto index_object1 : m_clusters[index_cluster1]) {
                for (auto index_object2 : m_clusters[index_cluster2]) {
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

    m_clusters[index1].insert(m_clusters[index1].end(), m_clusters[index2].begin(), m_clusters[index2].end());
    m_clusters.erase(m_clusters.begin() + index2);
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

