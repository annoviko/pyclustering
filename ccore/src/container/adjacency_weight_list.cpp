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

#include "container/adjacency_weight_list.hpp"


namespace container {


const double adjacency_weight_list::DEFAULT_EXISTANCE_CONNECTION_VALUE = 1.0;
const double adjacency_weight_list::DEFAULT_NON_EXISTANCE_CONNECTION_VALUE = 0.0;


adjacency_weight_list::adjacency_weight_list(const adjacency_weight_list & another_matrix) {
    m_adjacency = another_matrix.m_adjacency;
}


adjacency_weight_list::adjacency_weight_list(adjacency_weight_list && another_matrix) {
    m_adjacency = std::move(another_matrix.m_adjacency);
}


adjacency_weight_list::adjacency_weight_list(const size_t node_amount) : m_adjacency(node_amount) { }


adjacency_weight_list::~adjacency_weight_list(void) { }


size_t adjacency_weight_list::size(void) const { return m_adjacency.size(); }


void adjacency_weight_list::set_connection(const size_t node_index1, const size_t node_index2) {
    m_adjacency[node_index1].insert( { node_index2, DEFAULT_EXISTANCE_CONNECTION_VALUE } );
}


void adjacency_weight_list::erase_connection(const size_t node_index1, const size_t node_index2) {
    m_adjacency[node_index1].erase(node_index2);
}


bool adjacency_weight_list::has_connection(const size_t node_index1, const size_t node_index2) const {
    const std::unordered_map<size_t, double> & node_neighbors = m_adjacency[node_index1];

    if (node_neighbors.find(node_index2) != node_neighbors.end()) {
        return true;
    }

    return false;
}


void adjacency_weight_list::get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const {
    node_neighbors.clear();
    node_neighbors.reserve(m_adjacency[node_index].size());

    for (auto index_neighbor : m_adjacency[node_index]) {
        node_neighbors.push_back(index_neighbor.first);
    }
}


void adjacency_weight_list::set_connection_weight(const size_t node_index1, const size_t node_index2, const double weight) {
    std::unordered_map<size_t, double> & node_neighbors = m_adjacency[node_index1];

    if (weight != 0.0) {
        node_neighbors[node_index2] = weight;
    }
    else {
        node_neighbors.erase(node_index2);
    }
}


double adjacency_weight_list::get_connection_weight(const size_t node_index1, const size_t node_index2) const {
    const std::unordered_map<size_t, double> & node_neighbors = m_adjacency[node_index1];
    const std::unordered_map<size_t, double>::const_iterator connection_iterator = node_neighbors.find(node_index2);

    if (connection_iterator != node_neighbors.end()) {
        return connection_iterator->second;
    }

    return DEFAULT_NON_EXISTANCE_CONNECTION_VALUE;
}


void adjacency_weight_list::clear(void) {
    m_adjacency.clear();
}


adjacency_weight_list & adjacency_weight_list::operator=(const adjacency_weight_list & another_collection) {
    if (this != &another_collection) {
        m_adjacency = another_collection.m_adjacency;
    }

    return *this;
}


adjacency_weight_list & adjacency_weight_list::operator=(adjacency_weight_list && another_collection) {
    if (this != &another_collection) {
        m_adjacency = std::move(another_collection.m_adjacency);
    }

    return *this;
}


}
