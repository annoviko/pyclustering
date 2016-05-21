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

#ifndef _ADJACENCY_LIST_H_
#define _ADJACENCY_LIST_H_

#include <unordered_set>
#include "container/adjacency.hpp"


namespace container {

/**
*
* @brief   Implementation of adjacency matrix where each node stores its neighbors in unordered
*          set.
*
* @details Unordered ensures maximum performance in case of getting elements by index because only 
*          indexes are used as keys that ensures uniform distribution. It takes less memory
*          than classical matrix representation. And it is faster in case of getting neighbors than
*          bit matrix and classical matrix representation.
*
* @see     adjacency_bit_matrix
* @see     adjacency_matrix
*
*/
class adjacency_list : public adjacency_collection {
private:
    typedef std::vector<std::unordered_set<size_t>>     adjacency_list_container;


protected:
    adjacency_list_container     m_adjacency;


public:
    /**
    *
    * @brief   Default destructor.
    *
    */
    adjacency_list(void);

    /**
    *
    * @brief   Default copy constructor.
    *
    * @param[in]  another_matrix: adjacency matrix that should be copied.
    *
    */
    adjacency_list(const adjacency_list & another_matrix);

    /**
    *
    * @brief   Default move constructor.
    *
    * @param[in]  another_matrix: adjacency matrix that should be moved.
    *
    */
    adjacency_list(adjacency_list && another_matrix);

    /**
    *
    * @brief   Adjacency list matrix constructor.
    *
    * @param[in]  node_amount: number of nodes whose connections are described in matrix.
    *
    */
    adjacency_list(const size_t node_amount);

    /**
    *
    * @brief   Default destructor.
    *
    */
    virtual ~adjacency_list(void);


public:
    /**
    *
    * @brief   Returns amount of nodes in adjacency collection.
    *
    */
    virtual size_t size(void) const;

    /**
    *
    * @brief   Establishes one-way connection from the first node to the second in adjacency collection.
    *
    * @details Complexity equals to complexity of insertion of std::unrodered_set. No bounds checking
    *          is performed.
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
    * @details Complexity equals to complexity of erasing of std::unrodered_set. No bounds checking
    *          is performed.
    *
    * @param[in]  node_index1: index of node in the collection that should be disconnected from another.
    * @param[in]  node_index2: index of another node in the collection that should be diconnected from
    *              the node defined by the first argument 'node_index1'.
    *
    */
    virtual void erase_connection(const size_t node_index1, const size_t node_index2);

    /**
    *
    * @brief   Checks existence of connection between specified nodes.
    *
    * @details Complexity equal to searching of std::unrodered_set. No bounds checking
    *          is performed.
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
    * @details Complexity equals to complexity of copying from unordered_set to vector. No bounds checking
    *          is performed.
    *
    * @param[in]  node_index: index of node in the collection whose neighbors are required.
    * @param[out] node_neighbors: vector of indexes of neighbors of specified node.
    *
    */
    virtual void get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const;

    /**
    *
    * @brief   Clear content of adjacency matrix.
    *
    */
    virtual void clear(void);

public:
    adjacency_list & operator=(const adjacency_list & another_collection);

    adjacency_list & operator=(adjacency_list && another_collection);
};

}

#endif
