/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#include <pyclustering/container/adjacency_matrix.hpp>


namespace pyclustering {

namespace container {


const double adjacency_matrix::DEFAULT_EXISTANCE_CONNECTION_VALUE = 1.0;
const double adjacency_matrix::DEFAULT_NON_EXISTANCE_CONNECTION_VALUE = 0.0;


adjacency_matrix::adjacency_matrix(const size_t node_amount) : m_adjacency(node_amount, std::vector<double>(node_amount, DEFAULT_NON_EXISTANCE_CONNECTION_VALUE)) { }


adjacency_matrix::~adjacency_matrix() { }


size_t adjacency_matrix::size() const { return m_adjacency.size(); }


void adjacency_matrix::set_connection(const size_t node_index1, const size_t node_index2) {
    m_adjacency[node_index1][node_index2] = DEFAULT_EXISTANCE_CONNECTION_VALUE;
}


bool adjacency_matrix::has_connection(const size_t node_index1, const size_t node_index2) const {
    return (m_adjacency[node_index1][node_index2] != DEFAULT_NON_EXISTANCE_CONNECTION_VALUE);
}


void adjacency_matrix::erase_connection(const size_t node_index1, const size_t node_index2) {
    m_adjacency[node_index1][node_index2] = DEFAULT_NON_EXISTANCE_CONNECTION_VALUE;
}


void adjacency_matrix::get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const {
    node_neighbors.clear();

    const std::vector<double> & node_neighbor_connections = m_adjacency[node_index];
    for (size_t neighbor_index = 0; neighbor_index != node_neighbor_connections.size(); neighbor_index++) {
        if (node_neighbor_connections[neighbor_index] != DEFAULT_NON_EXISTANCE_CONNECTION_VALUE) {
            node_neighbors.push_back(neighbor_index);
        }
    }
}


void adjacency_matrix::set_connection_weight(const size_t node_index1, const size_t node_index2, const double weight) {
    m_adjacency[node_index1][node_index2] = weight;
}


double adjacency_matrix::get_connection_weight(const size_t node_index1, const size_t node_index2) const {
    return m_adjacency[node_index1][node_index2];
}


void adjacency_matrix::clear() {
    m_adjacency.clear();
}


adjacency_matrix & adjacency_matrix::operator=(const adjacency_matrix & another_collection) {
    if (this != &another_collection) {
        m_adjacency = another_collection.m_adjacency;
    }

    return *this;
}


adjacency_matrix & adjacency_matrix::operator=(adjacency_matrix && another_collection) {
    if (this != &another_collection) {
        m_adjacency = std::move(another_collection.m_adjacency);
    }

    return *this;
}


}

}