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

#ifndef _ADJACENCY_WEIGHT_LIST_H_
#define _ADJACENCY_WEIGHT_LIST_H_


#include <unordered_map>

#include "container/adjacency.hpp"


namespace container {

/**
*
* @brief   Implementation of adjacency matrix where each node stores its neighbors in unordered
*          set with corresponding weight of connection to corresponding neighbor.
*
* @details Unordered ensures maximum performance in case of getting elements by index because only 
*          indexes are used as keys that ensures uniform distribution. It takes less memory
*          than classical matrix representation. And it is faster in case of getting neighbors than
*          bit matrix and classical matrix representation. Unlike adjacency_list this implementation
*          requires twice as much memory because of storing weight of each connection.
*
* @see     adjacency_bit_matrix
* @see     adjacency_matrix
*
*/
class adjacency_weight_list : public adjacency_weight_collection {
private:
    typedef std::vector<std::unordered_map<size_t, double>>     adjacency_list_container;


protected:
    adjacency_list_container     m_adjacency;


public:
    /**
    *
    * @brief   Default destructor without arguments is forbiden.
    *
    */
    adjacency_weight_list(void) = delete;

    /**
    *
    * @brief   Default copy constructor.
    *
    * @param[in]  another_matrix: adjacency matrix that should be copied.
    *
    */
    adjacency_weight_list(const adjacency_weight_list & another_matrix);

    /**
    *
    * @brief   Default move constructor.
    *
    * @param[in]  another_matrix: adjacency matrix that should be moved.
    *
    */
    adjacency_weight_list(adjacency_weight_list && another_matrix);

    /**
    *
    * @brief   Adjacency list constructor.
    *
    * @param[in]  node_amount: number of nodes whose connections are described in matrix.
    *
    */
    adjacency_weight_list(const size_t node_amount);

    /**
    *
    * @brief   Default destructor.
    *
    */
    virtual ~adjacency_weight_list(void);


private:
    /**
    *
    * @brief   Default value that denotes existance of connection (non-zero weight of connection).
    *
    */
    static const double DEFAULT_EXISTANCE_CONNECTION_VALUE;

    /**
    *
    * @brief   Default value that denotes lack of connection (zero weight of connection).
    *
    */
    static const double DEFAULT_NON_EXISTANCE_CONNECTION_VALUE;


public:
    /**
    *
    * @brief   Returns amount of nodes in the adjacency collection.
    *
    */
    virtual size_t size(void) const;

    /**
    *
    * @brief   Establishes one-way connection from the first node to the second in adjacency collection.
    *
    * @details Complexity equals to complexity of insertion of std::unrodered_map.
    *
    * @param[in]  node_index1: index of node in the collection that should be connected with another.
    * @param[in]  node_index2: index of another node in the collection that should be connected with
    *                          the node defined by the first argument 'node_index1'.
    *
    */
    virtual void set_connection(const size_t node_index1, const size_t node_index2);

    /**
    *
    * @brief   Removes one-way connection from the first node to the second in adjacency collection.
    *
    * @details Complexity equals to complexity of erasing of std::unrodered_map.
    *
    * @param[in]  node_index1: index of node in the collection that should be disconnected from another.
    * @param[in]  node_index2: index of another node in the collection that should be diconnected from
    *              the node defined by the first argument 'node_index1'.
    *
    */
    virtual void erase_connection(const size_t node_index1, const size_t node_index2);

    /**
    *
    * @brief   Checks existance of connection between specified nodes.
    *
    * @details Complexity equal to searching element in std::unrodered_map.
    *
    * @param[in]  node_index1: index of node in the collection.
    * @param[in]  node_index2: index of another node in the collection.
    *
    * @return  'true' - connection between the nodes exists, 'false' - connection does not exist.
    *
    */
    virtual bool has_connection(const size_t node_index1, const size_t node_index2) const;

    /**
    *
    * @brief   Returns vector of indexes of neighbors of specified node in line with adjacency collection.
    *
    * @details Complexity equals to complexity of traversing of unrodered_map.
    *
    * @param[in]  node_index: index of node in the collection whose neighbors are required.
    * @param[out] node_neighbors: vector of indexes of neighbors of specified node.
    *
    */
    virtual void get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const;

    /**
    *
    * @brief   Set weight of connection between nodes where zero value means lack of connection and
    *          non-zero means connection with specified weight.
    *
    * @details Complexity equal to searching element in std::unrodered_map.
    *
    * @param[in]  node_index1: index of node in the collection whose connection weight should be updated 
    *              with another node.
    * @param[in]  node_index2: index of another node in the collection.
    * @param[in]  weight: new value of weight of connection between the nodes.
    *
    */
    virtual void set_connection_weight(const size_t node_index1, const size_t node_index2, const double weight);

    /**
    *
    * @brief   Returns weight of one-way connection between specified nodes.
    *
    * @details Complexity equal to searching element in std::unrodered_map.
    *
    * @param[in]  node_index1: index of node in the collection whose connection weight should be 
    *              updated with another node.
    * @param[in]  node_index2: index of another node in the collection that is connected to the 
    *              first node.
    *
    * @return  Weight of one-way connection between specified nodes.
    *
    */
    virtual double get_connection_weight(const size_t node_index1, const size_t node_index2) const;

    /**
    *
    * @brief   Clear content of adjacency matrix.
    *
    */
    virtual void clear(void);

public:
	adjacency_weight_list & operator=(const adjacency_weight_list & another_collection);

	adjacency_weight_list & operator=(adjacency_weight_list && another_collection);
};

}

#endif
