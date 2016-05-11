#include "cluster_data.hpp"


namespace cluster {


cluster_data::cluster_data(void) : m_clusters(std::vector<cluster>()) { }


cluster_data::cluster_data(const cluster_data & p_other) : m_clusters(p_other.m_clusters) { }


cluster_data::cluster_data(cluster_data && p_other) : m_clusters(std::move(p_other.m_clusters)) { }


cluster_data::~cluster_data(void) { }


std::vector<cluster_data::cluster> & cluster_data::clusters(void) { return m_clusters; }


size_t cluster_data::size(void) const { return m_clusters.size(); }


cluster_data::cluster & cluster_data::operator[](const size_t p_index) { return m_clusters[p_index]; }


const cluster_data::cluster & cluster_data::operator[](const size_t p_index) const { return m_clusters[p_index]; }


cluster_data & cluster_data::operator=(const cluster_data & p_other) {
    if (this != &p_other) {
        m_clusters = p_other.m_clusters;
    }

    return *this;
}


cluster_data & cluster_data::operator=(cluster_data && p_other) {
    if (this != &p_other) {
        m_clusters = std::move(p_other.m_clusters);
    }

    return *this;
}


bool cluster_data::operator==(const cluster_data & p_other) const {
    return (m_clusters == p_other.m_clusters);
}


bool cluster_data::operator!=(const cluster_data & p_other) const {
    return !(*this == p_other);
}


}
