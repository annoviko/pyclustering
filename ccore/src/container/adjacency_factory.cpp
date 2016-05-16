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

#include "container/adjacency_factory.hpp"

#include "container/adjacency_bit_matrix.hpp"
#include "container/adjacency_list.hpp"
#include "container/adjacency_matrix.hpp"
#include "container/adjacency_weight_list.hpp"


namespace container {

std::shared_ptr<adjacency_collection> adjacency_unweight_factory::create_collection(const size_t amount_nodes, const adjacency_unweight_t storing_type, const connection_t structure_type) {
    adjacency_collection * collection = nullptr;

    switch(storing_type) {
    case adjacency_unweight_t::ADJACENCY_BIT_MATRIX:
        collection = new adjacency_bit_matrix(amount_nodes);
        break;

    case adjacency_unweight_t::ADJACENCY_LIST:
        collection = new adjacency_list(amount_nodes);
        break;

    case adjacency_unweight_t::ADJACENCY_MATRIX:
        collection = new adjacency_matrix(amount_nodes);
        break;

    default:
        throw new std::runtime_error("Unknown type of adjacency collection without weights is required from the factory.");
    }

    /* establish structures between nodes */
    adjacency_connector<adjacency_collection> connector;
    connector.create_structure(structure_type, *collection);

    return std::shared_ptr<adjacency_collection>(collection);
}


std::shared_ptr<adjacency_weight_collection> adjacency_weight_factory::create_collection(const size_t amount_nodes, const adjacency_weight_t storing_type, const connection_t structure_type, const std::function<double(void)> & weight_value_generator) {
    adjacency_weight_collection * collection = nullptr;

    switch(storing_type) {
    case adjacency_weight_t::ADJACENCY_LIST:
        collection = new adjacency_weight_list(amount_nodes);
        break;

    case adjacency_weight_t::ADJACENCY_MATRIX:
        collection = new adjacency_matrix(amount_nodes);
        break;

    default:
        throw new std::runtime_error("Unknown type of adjacency collection without weights is required from the factory.");
    }

    /* establish structures between nodes */
    adjacency_weight_connector<adjacency_weight_collection> connector(weight_value_generator);
    connector.create_structure(structure_type, *collection);

    return std::shared_ptr<adjacency_weight_collection>(collection);
}

}
