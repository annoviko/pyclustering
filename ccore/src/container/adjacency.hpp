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

#ifndef _ADJACENCY_H_
#define _ADJACENCY_H_


#include <vector>
#include <cstdlib>


namespace container {

/**
*
* @brief   Abstract class of the adjacency collection that provides interface to control collection.
*
*/
class adjacency_collection {
public:
    /**
    *
    * @brief   Default destructor.
    *
    */
    virtual ~adjacency_collection(void) { }

public:
    /**
    *
    * @brief   Returns amount of nodes in the adjacency collection.
    *
    */
    virtual size_t size(void) const = 0;

    /**
    *
    * @brief   Establishes one-way connection from the first node to the second in adjacency collection.
    *
    * @param[in]  node_index1: index of node in the collection that should be connected with another.
    * @param[in]  node_index2: index of another node in the collection that should be connected with
    *              the node defined by the first argument 'node_index1'.
    *
    */
    virtual void set_connection(const size_t node_index1, const size_t node_index2) = 0;

    /**
    *
    * @brief   Removes one-way connection from the first node to the second in adjacency collection.
    *
    * @param[in]  node_index1: index of node in the collection that should be disconnected from another.
    * @param[in]  node_index2: index of another node in the collection that should be diconnected from
    *              the node defined by the first argument 'node_index1'.
    *
    */
    virtual void erase_connection(const size_t node_index1, const size_t node_index2) = 0;

    /**
    *
    * @brief   Checks existance of connection between specified nodes.
    *
    * @param[in]  node_index1: index of node in the collection.
    * @param[in]  node_index2: index of another node in the collection.
    *
    * @return  'true' - connection between the nodes exists, 'false' - connection does not exist.
    *
    */
    virtual bool has_connection(const size_t node_index1, const size_t node_index2) const = 0;

    /**
    *
    * @brief   Returns vector of indexes of neighbors of specified node in line with adjacency collection.
    *
    * @param[in]  node_index: index of node in the collection.
    * @param[out] node_neighbors: vector of indexes of neighbors of specified node.
    *
    */
    virtual void get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const = 0;

    /**
    *
    * @brief   Clear content of adjacency matrix.
    *
    */
    virtual void clear(void) = 0;
};



/**
*
* @brief   Abstract class of the adjacency collection that provides interface to control collection.
*
*/
class adjacency_weight_collection : public adjacency_collection {
public:
    /**
    *
    * @brief   Set weight of connection between nodes where zero value means lack of connection and
    *          non-zero means connection with specified weight.
    *
    * @param[in]  node_index1: index of node in the collection whose connection weight should be updated 
    *              with another node.
    * @param[in]  node_index2: index of another node in the collection.
    * @param[in]  weight: new value of weight of connection between the nodes.
    *
    */
    virtual void set_connection_weight(const size_t node_index1, const size_t node_index2, const double weight) = 0;

    /**
    *
    * @brief   Returns weight of one-way connection between specified nodes.
    *
    * @param[in]  node_index1: index of node in the collection whose connection weight should be 
    *              updated with another node.
    * @param[in]  node_index2: index of another node in the collection that is connected to the 
    *              first node.
    *
    * @return  Weight of one-way connection between specified nodes.
    *
    */
    virtual double get_connection_weight(const size_t node_index1, const size_t node_index2) const = 0;
};

}

#endif
