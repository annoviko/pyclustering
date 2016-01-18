#include "adjacency_bit_matrix.h"


const size_t adjacency_bit_matrix::DEFAULT_EXISTANCE_CONNECTION_VALUE = 1;
const size_t adjacency_bit_matrix::DEFAULT_NON_EXISTANCE_CONNECTION_VALUE = 0;


void adjacency_bit_matrix::set_connection(const size_t node_index1, const size_t node_index2) {
    update_connection(node_index1, node_index2, DEFAULT_EXISTANCE_CONNECTION_VALUE);
}

void adjacency_bit_matrix::update_connection(const size_t node_index1, const size_t node_index2, const size_t state_connection) {
    if (m_conn_type != DYNAMIC_STRUCTURE) {
        m_conn_type = DYNAMIC_STRUCTURE;
    }

    size_t bit_value = 0x00;

    if (state_connection > 0) {
        bit_value = 0x01;
    }

    size_t index_element = node_index2 / (sizeof(size_t) << 3);
    size_t bit_number = node_index2 % (sizeof(size_t) << 3);

    m_adjacency[node_index1][index_element] = m_adjacency[node_index1][index_element] | ((size_t) bit_value << bit_number);
}

size_t adjacency_bit_matrix::get_connection(const size_t node_index1, const size_t node_index2) const {
    switch(m_conn_type) {
    case STATIC_STRUCTURE_NONE:
        return DEFAULT_NON_EXISTANCE_CONNECTION_VALUE;

    case STATIC_STRUCTURE_ALL_TO_ALL:
        return DEFAULT_EXISTANCE_CONNECTION_VALUE;

    default:
        break;
    }

    const size_t index_element = node_index2 / (sizeof(size_t) << 3);
    const size_t bit_number = node_index2 - (index_element * (sizeof(size_t) << 3));

    return (m_adjacency[node_index1][index_element] >> bit_number) & (size_t) DEFAULT_EXISTANCE_CONNECTION_VALUE;
}

void adjacency_bit_matrix::get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const {
    node_neighbors.clear();
    
    for (size_t neighbor_index = 0; neighbor_index != m_adjacency.size(); neighbor_index++) {
        if (get_connection(node_index, neighbor_index) > 0) {
            node_neighbors.push_back(neighbor_index);
        }
    }    
}