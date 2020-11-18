/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/cluster/cluster_data.hpp>


namespace pyclustering {

namespace clst {


cluster_sequence & cluster_data::clusters() { return m_clusters; }


const cluster_sequence & cluster_data::clusters() const { return m_clusters; }


size_t cluster_data::size() const { return m_clusters.size(); }


cluster & cluster_data::operator[](const size_t p_index) { return m_clusters[p_index]; }


const cluster & cluster_data::operator[](const size_t p_index) const { return m_clusters[p_index]; }


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

}