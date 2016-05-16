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

#ifndef _ADJACENCY_FACTORY_H_
#define _ADJACENCY_FACTORY_H_


#include <memory>

#include "container/adjacency.hpp"
#include "container/adjacency_connector.hpp"


namespace container {

/**
*
* @brief   Enumeration of pre-defined types of ajacency collections where weight of connections
*          is not used.
*
*/
enum class adjacency_unweight_t {
	ADJACENCY_BIT_MATRIX,
    ADJACENCY_MATRIX,
	ADJACENCY_LIST
};


/**
*
* @brief   Enumeration of pre-defined types of ajacency collections where weight of connections
*          is supported.
*
*/
enum class adjacency_weight_t {
    ADJACENCY_MATRIX,
    ADJACENCY_LIST
};


/**
*
* @brief   Factory of adjacency collections without weights.
*
*/
class adjacency_unweight_factory {
public:
    /**
    *
    * @brief   Creates adjacency collection with specified size without connections between nodes.
    *
    * @param[in] amount_nodes: size of adjacency collection that is defined by amount of nodes in it.
    * @param[in] storing_type: type of collection that should be used for representation of adjacency
    *                          collection, for example, bit-matrix, list or classical matrix.
    * @param[in] structure_type: type of connections that should be formed in the collection.
    *
    */
    static std::shared_ptr<adjacency_collection> create_collection(const size_t amount_nodes, 
                                                                   const adjacency_unweight_t storing_type = adjacency_unweight_t::ADJACENCY_MATRIX, 
                                                                   const connection_t structure_type = connection_t::CONNECTION_NONE);
};


/**
*
* @brief   Factory of adjacency collections that supports weights when each connection between
*          nodes has weight.
*
*/
class adjacency_weight_factory {
public:
    /**
    *
    * @brief   Creates adjacency collection with specified size without connections between nodes
    *          and initial value for weight of each connection.
    *
    * @param[in] amount_nodes: size of adjacency collection that is defined by amount of nodes in it.
    * @param[in] storing_type: type of collection that should be used for representation of adjacency
    *                          collection, for example, bit-matrix, list or classical matrix.
    * @param[in] structure_type: type of connections that should be formed in the collection.
    * @param[in] default_weight_value: value that is assign to each connection weight.
    * @param[in] weight_value_generator: generator of values that are assigned to connection weights.
    *
    */
    static std::shared_ptr<adjacency_weight_collection> create_collection(const size_t amount_nodes, 
                                                                          const adjacency_weight_t storing_type = adjacency_weight_t::ADJACENCY_MATRIX, 
                                                                          const connection_t structure_type = connection_t::CONNECTION_NONE, 
                                                                          const std::function<double(void)> & weight_value_generator = nullptr);
};

}

#endif
