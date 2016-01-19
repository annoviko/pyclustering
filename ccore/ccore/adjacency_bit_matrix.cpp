#include "adjacency_bit_matrix.h"


const size_t adjacency_bit_matrix::DEFAULT_EXISTANCE_CONNECTION_VALUE = 0x01;
const size_t adjacency_bit_matrix::DEFAULT_NON_EXISTANCE_CONNECTION_VALUE = 0x00;


adjacency_bit_matrix::adjacency_bit_matrix(const adjacency_bit_matrix & another_matrix) {
    m_adjacency = another_matrix.m_adjacency;
}


adjacency_bit_matrix::adjacency_bit_matrix(adjacency_bit_matrix && another_matrix) {
    m_adjacency = std::move(another_matrix.m_adjacency);
}


adjacency_bit_matrix::adjacency_bit_matrix(const size_t node_amount) : m_adjacency(node_amount, std::vector<size_t>(node_amount, 0)) { }


adjacency_bit_matrix::~adjacency_bit_matrix(void) { }


void adjacency_bit_matrix::set_connection(const size_t node_index1, const size_t node_index2) {
    update_connection(node_index1, node_index2, DEFAULT_EXISTANCE_CONNECTION_VALUE);
}


void adjacency_bit_matrix::erase_connection(const size_t node_index1, const size_t node_index2) {
    update_connection(node_index1, node_index2, DEFAULT_NON_EXISTANCE_CONNECTION_VALUE);
}


bool adjacency_bit_matrix::has_connection(const size_t node_index1, const size_t node_index2) const {
    const size_t index_element = node_index2 / (sizeof(size_t) << 3);
    const size_t bit_number = node_index2 - (index_element * (sizeof(size_t) << 3));

    const size_t bit_value = (m_adjacency[node_index1][index_element] >> bit_number) & (size_t) DEFAULT_EXISTANCE_CONNECTION_VALUE;

    return (bit_value > 0);
}


void adjacency_bit_matrix::get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const {
    node_neighbors.clear();
    
    for (size_t neighbor_index = 0; neighbor_index != m_adjacency.size(); neighbor_index++) {
        if (has_connection(node_index, neighbor_index)) {
            node_neighbors.push_back(neighbor_index);
        }
    }    
}


void adjacency_bit_matrix::update_connection(const size_t node_index1, const size_t node_index2, const size_t state_connection) {
    size_t bit_value = 0x00;

    if (state_connection > 0) {
        bit_value = 0x01;
    }

    size_t index_element = node_index2 / (sizeof(size_t) << 3);
    size_t bit_number = node_index2 % (sizeof(size_t) << 3);

    m_adjacency[node_index1][index_element] = m_adjacency[node_index1][index_element] | ((size_t) bit_value << bit_number);
}