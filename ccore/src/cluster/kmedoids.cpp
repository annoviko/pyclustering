#include "cluster/kmedoids.hpp"

#include "utils.hpp"

#include <limits>


namespace cluster {


kmedoids_data::kmedoids_data(void) :
        cluster_data(),
        m_medoids(std::vector<size_t>())
{ }


kmedoids_data::kmedoids_data(const kmedoids_data & p_other) :
        cluster_data(p_other),
        m_medoids(p_other.m_medoids)
{ }


kmedoids_data::kmedoids_data(kmedoids_data && p_other) :
        cluster_data(p_other),
        m_medoids(std::move(p_other.m_medoids))
{ }


kmedoids_data::~kmedoids_data(void) { }


std::vector<size_t> & kmedoids_data::medoids(void) { return m_medoids; }


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


void kmedoids::process(const cluster_algorithm::input_data & p_data, kmedoids_data & p_result) {
    m_data_ptr = &p_data;
    m_result_ptr = &p_result;

    std::vector<size_t> & medoids = m_result_ptr->medoids();
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
    std::vector<cluster_data::cluster> & clusters = m_result_ptr->clusters();

    clusters.clear();
    clusters.resize(m_result_ptr->medoids().size());

    for (size_t index_point = 0; index_point < m_data_ptr->size(); index_point++) {
        size_t index_optim = 0;
        double dist_optim = 0.0;

        for (size_t index = 0; index < m_result_ptr->medoids().size(); index++) {
            const size_t index_medoid = m_result_ptr->medoids()[index];
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


void kmedoids::erase_empty_clusters(std::vector<cluster_data::cluster> & p_clusters) {
    for (size_t index_cluster = p_clusters.size() - 1; index_cluster != (size_t) -1; index_cluster--) {
        if (p_clusters[index_cluster].empty()) {
            p_clusters.erase(p_clusters.begin() + index_cluster);
        }
    }
}


void kmedoids::calculate_medoids(std::vector<size_t> & p_medoids) {
    std::vector<size_t> & medoids = m_result_ptr->medoids();

    medoids.clear();
    medoids.resize(m_result_ptr->clusters().size());

    for (size_t index = 0; index < medoids.size(); index++) {
        medoids[index] = calculate_cluster_medoid(m_result_ptr->clusters()[index]);
    }
}


size_t kmedoids::calculate_cluster_medoid(const cluster_data::cluster & p_cluster) const {
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


double kmedoids::calculate_changes(const std::vector<size_t> & p_medoids) const {
    double maximum_difference = 0.0;
    for (size_t index = 0; index < p_medoids.size(); index++) {
        const size_t index_point1 = p_medoids[index];
        const size_t index_point2 = m_result_ptr->medoids()[index];

        const double distance = euclidean_distance_sqrt( &(*m_data_ptr)[index_point1], &(*m_data_ptr)[index_point2] );
        if (distance > maximum_difference) {
            maximum_difference = distance;
        }
    }

    return maximum_difference;
}


}
