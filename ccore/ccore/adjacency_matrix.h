#ifndef _ADJACENCY_MATRIX_H_
#define _ADJACENCY_MATRIX_H_

#include "adjacency.h"


template <class TypeNode> using adjacency_matrix_container = std::vector<std::vector<double>>;


/***********************************************************************************************
*
* @brief   Implementation of classical adjacency matrix where each node stores weight of connection
*          to each node.
*
* @details This collection requires much more memory O(n^2) than others adjacency collections, but
*          setting and getting connection operations are faster O(1). Classic adjacency matrix 
*          collection allows to specify weight of each connection between nodes.
*
* @see     adjacency_bit_matrix
* @see     adjacency_list_matrix
*
***********************************************************************************************/
class adjacency_matrix : public adjacency_collection<double, adjacency_matrix_container> {
private:
    static const double DEFAULT_EXISTANCE_CONNECTION_VALUE;
    static const double DEFAULT_NON_EXISTANCE_CONNECTION_VALUE;

public:
    /***********************************************************************************************
    *
    * @brief   Establishes one-way connection from the first node to the second in adjacency collection.
    *
    * @details Complexity of setting weight of connection is O(1).
    *
    * @param[in]  node_index1: index of node in the collection that should be connected with another.
    * @param[in]  node_index2: index of another node in the collection that should be connected with
    *                          the node defined by the first argument 'node_index1'.
    *
    ***********************************************************************************************/
    virtual void set_connection(const size_t node_index1, const size_t node_index2);

    /***********************************************************************************************
    *
    * @brief   Establishes one-way connection from the first node to the second in adjacency collection
    *          in case of zero value of weight of connection and resets connection (remove it) in case of 
    *          zero value.
    *
    * @details Complexity of updating weight of connection is O(1).
    *
    * @param[in]  node_index1: index of node in the collection whose connection should be updated with another.
    * @param[in]  node_index2: index of another node in the collection.
    * @param[in]  weight_connection: weight of connection from the first node to the second.
    *
    ***********************************************************************************************/
    virtual void update_connection(const size_t node_index1, const size_t node_index2, const double weight_connection);

    /***********************************************************************************************
    *
    * @brief   Returns value of connection that denotes weight of connection, if there is no connection
    *          from the first node to the second then null value is returned.
    *
    * @details Complexity of getting weight of connection is O(1).
    *
    * @param[in]  node_index1: index of node in the collection.
    * @param[in]  node_index2: index of another node in the collection.
    *
    ***********************************************************************************************/
    virtual double get_connection(const size_t node_index1, const size_t node_index2) const;

    /***********************************************************************************************
    *
    * @brief   Returns vector of indexes of neighbors of specified node in line with adjacency collection.
    *
    * @details Complexity of getting neighbors is O(n).
    *
    * @param[in]  node_index: index of node in the collection whose neighbors are required.
    * @param[out] node_neighbors: vector of indexes of neighbors of specified node.
    *
    ***********************************************************************************************/
    virtual void get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const;
};

#endif