#include "adjacency_list_matrix.h"


const size_t adjacency_list_matrix::DEFAULT_EXISTANCE_CONNECTION_VALUE = 1;
const size_t adjacency_list_matrix::DEFAULT_NON_EXISTANCE_CONNECTION_VALUE = 0;


void adjacency_list_matrix::set_connection(const size_t node_index1, const size_t node_index2) {
    m_adjacency[node_index1].insert(node_index2);
}

void adjacency_list_matrix::update_connection(const size_t node_index1, const size_t node_index2, const size_t state_connection) {
    if (state_connection > 0) {
        m_adjacency[node_index1].insert(node_index2);
    }
    else {
        m_adjacency[node_index1].erase(node_index2);
    }
}

size_t adjacency_list_matrix::get_connection(const size_t node_index1, const size_t node_index2) const {
    const std::unordered_set<size_t> & node_neighbors = m_adjacency[node_index1];
    if (node_neighbors.find(node_index2) != node_neighbors.end()) {
        return DEFAULT_EXISTANCE_CONNECTION_VALUE;
    }

    return DEFAULT_NON_EXISTANCE_CONNECTION_VALUE;
}

void adjacency_list_matrix::get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const {
    node_neighbors.resize(m_adjacency[node_index].size());
	std::copy(m_adjacency[node_index].begin(), m_adjacency[node_index].end(), node_neighbors.begin());
}