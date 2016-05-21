/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#include "container/adjacency_bit_matrix.hpp"

#include <string>
#include <stdexcept>


namespace container {

const size_t adjacency_bit_matrix::DEFAULT_EXISTANCE_CONNECTION_VALUE = 0x01;
const size_t adjacency_bit_matrix::DEFAULT_NON_EXISTANCE_CONNECTION_VALUE = 0x00;


adjacency_bit_matrix::adjacency_bit_matrix(const adjacency_bit_matrix & another_matrix) {
    m_adjacency = another_matrix.m_adjacency;
    m_size = another_matrix.m_size;
}


adjacency_bit_matrix::adjacency_bit_matrix(adjacency_bit_matrix && another_matrix) {
    m_adjacency = std::move(another_matrix.m_adjacency);
    m_size = std::move(another_matrix.m_size);

    another_matrix.m_size = 0;
}


adjacency_bit_matrix::adjacency_bit_matrix(const size_t node_amount) { 
    m_adjacency = adjacency_bit_matrix_container(node_amount, std::vector<size_t>(node_amount, 0));
    m_size = node_amount;
}


adjacency_bit_matrix::~adjacency_bit_matrix(void) { }


size_t adjacency_bit_matrix::size(void) const { return m_size; }


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


void adjacency_bit_matrix::clear(void) {
    m_adjacency.clear();
    m_size = 0;
}


void adjacency_bit_matrix::update_connection(const size_t node_index1, const size_t node_index2, const size_t state_connection) {
    size_t element_byte_length = (sizeof(size_t) << 3);
    size_t index_element = node_index2 / element_byte_length;
    size_t bit_number = node_index2 % element_byte_length;

    if ( (node_index1 > m_adjacency.size()) || (index_element > m_adjacency.size()) ) {
        std::string message("adjacency bit matrix size: " + std::to_string(m_adjacency.size()) + ", index1: " + std::to_string(node_index1) + ", index2: " + std::to_string(node_index2));
        throw std::out_of_range(message);
    }

    if (state_connection > 0) {
        m_adjacency[node_index1][index_element] |= ((size_t) 0x01 << bit_number);
    }
    else {
        m_adjacency[node_index1][index_element] &= ~((size_t) 0x01 << bit_number);
    }
}



adjacency_bit_matrix & adjacency_bit_matrix::operator=(const adjacency_bit_matrix & another_matrix) {
    if (this != &another_matrix) {
        m_adjacency = another_matrix.m_adjacency;
        m_size = another_matrix.m_size;
    }

    return *this;
}


adjacency_bit_matrix & adjacency_bit_matrix::operator=(adjacency_bit_matrix && another_matrix) {
    if (this != &another_matrix) {
        m_adjacency = std::move(another_matrix.m_adjacency);
        m_size = std::move(another_matrix.m_size);

        another_matrix.m_size = 0;    
    }

    return *this;
}

}
