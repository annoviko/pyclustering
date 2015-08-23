#include "kmedians.h"
#include "support.h"

kmedians::kmedians() :
m_tolerance(0.025),
m_medians(0),
m_clusters(0),
m_ptr_data(nullptr) { }


kmedians::kmedians(const std::vector<point> & initial_medians, const double tolerance) : 
m_tolerance(tolerance),
m_medians(initial_medians),
m_clusters(initial_medians.size()),
m_ptr_data(nullptr) { }


kmedians::~kmedians(void) { }


void kmedians::initialize(const std::vector<point> & initial_medians, const double tolerance) {
    m_tolerance = tolerance;
    m_medians = initial_medians;
    m_clusters.clear();
    m_ptr_data = nullptr;
}


void kmedians::process(const std::vector<point> & data) {
    m_ptr_data = (std::vector<point> *) &data;
    if (data[0].size() != m_medians[0].size()) {
        throw std::runtime_error("CCORE [kmedians]: dimension of the input data and dimension of the initial cluster medians must be equal.");
    }

    m_clusters.clear();

    double stop_condition = m_tolerance * m_tolerance;
    double changes = 0.0;
    double prev_changes = 0.0;

    size_t counter_repeaters = 0;

    do {
        update_clusters();
        changes = update_medians();

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
}


void kmedians::update_clusters() {
    m_clusters.clear();
    m_clusters.resize(m_medians.size());

    const std::vector<point> & data = *m_ptr_data;

    for (size_t index_point = 0; index_point < data.size(); index_point++) {
        size_t index_cluster_optim = 0;
        double distance_optim = std::numeric_limits<double>::max();

        for (size_t index_cluster = 0; index_cluster < m_medians.size(); index_cluster++) {
            double distance = euclidean_distance_sqrt(&data[index_point], &m_medians[index_cluster]);
            if (distance < distance_optim) {
                index_cluster_optim = index_cluster;
                distance_optim = distance;

            }
        }

        m_clusters[index_cluster_optim].push_back(index_point);
    }

    /* Check for clusters that are not able to capture object */
    for (size_t index_cluster = m_clusters.size() - 1; index_cluster != (size_t) -1; index_cluster--) {
        if (m_clusters[index_cluster].empty()) {
            m_clusters.erase(m_clusters.begin() + index_cluster);
        }
    }
}


double kmedians::update_medians() {
    const std::vector<point> & data = *m_ptr_data;
    const size_t dimension = data[0].size();

    std::vector<point> prev_medians(m_medians);

    m_medians.clear();
    m_medians.resize(m_clusters.size(), point(dimension, 0.0));

    double maximum_change = 0.0;

    for (size_t index_cluster = 0; index_cluster < m_clusters.size(); index_cluster++) {
        for (size_t index_dimension = 0; index_dimension < dimension; index_dimension++) {
            cluster & current_cluster = m_clusters[index_cluster];
            std::sort(current_cluster.begin(), current_cluster.end(), 
                [this](unsigned int index_object1, unsigned int index_object2) 
            {
                return (*m_ptr_data)[index_object1] > (*m_ptr_data)[index_object2];
            });

            size_t relative_index_median = (size_t) floor(current_cluster.size() / 2.0);
            size_t index_median = current_cluster[relative_index_median];

            if (current_cluster.size() % 2) {
                size_t index_median_second = current_cluster[relative_index_median + 1];
                m_medians[index_cluster][index_dimension] = (data[index_median][index_dimension] + data[index_median_second][index_dimension]) / 2.0;
            }
            else {
                m_medians[index_cluster][index_dimension] = data[index_median][index_dimension];
            }
        }

        double change = euclidean_distance_sqrt(&prev_medians[index_cluster], &m_medians[index_cluster]);
        if (change > maximum_change) {
            maximum_change = change;
        }
    }

    return maximum_change;
}
