/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <memory>

#include <pyclustering/container/adjacency.hpp>
#include <pyclustering/container/adjacency_connector.hpp>


namespace pyclustering {

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
                                                                          const std::function<double()> & weight_value_generator = nullptr);
};


}

}