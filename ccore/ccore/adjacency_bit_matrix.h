#ifndef _ADJACENCY_BIT_MATRIX_
#define _ADJACENCY_BIT_MATRIX_

#include "adjacency.h"


template <class TypeNode> using adjacency_bit_matrix_container = std::vector<std::vector<TypeNode>>;


/***********************************************************************************************
*
* @brief   Implementation of classical bit adjacency matrix where each node has bit map where 
*          each bit stores state of connection to correspoding node.
*
* @details Bit matrix implementation helps to significantly reduce usage of memory than list matrix
*          and classic matrix representations. But operations of getting and setting are slower than
*          mentioned implementations.
*          
* @see     adjacency_list_matrix
* @see     adjacency_matrix
*
***********************************************************************************************/
class adjacency_bit_matrix : public adjacency_collection<size_t, adjacency_bit_matrix_container> {
private:
    static const size_t DEFAULT_EXISTANCE_CONNECTION_VALUE;
    static const size_t DEFAULT_NON_EXISTANCE_CONNECTION_VALUE;

public:
    /***********************************************************************************************
    *
    * @brief   Establishes one-way connection from the first node to the second in adjacency collection.
    *
    * @details Requies math-logical operations to set connection.
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
    *          in case of zero state of connection and resets connection (remove it) in case of zero state.
    *
    * @param[in]  node_index1: index of node in the collection whose connection should be updated with another.
    * @param[in]  node_index2: index of another node in the collection.
    * @param[in]  state_connection: connection state from the first node to the second.
    *
    ***********************************************************************************************/
    virtual void update_connection(const size_t node_index1, const size_t node_index2, const size_t state_connection);

    /***********************************************************************************************
    *
    * @brief   Returns value of connection that denotes weight of connection, if there is no connection
    *          from the first node to the second then null value is returned.
    *
    * @details Requies math-logical operations to set connection.
    *
    * @param[in]  node_index1: index of node in the collection.
    * @param[in]  node_index2: index of another node in the collection.
    *
    ***********************************************************************************************/
    virtual size_t get_connection(const size_t node_index1, const size_t node_index2) const;

    /***********************************************************************************************
    *
    * @brief   Returns vector of indexes of neighbors of specified node in line with adjacency collection.
    *
    * @details Requies math-logical operations to set connection.
    *
    * @param[in]  node_index: index of node in the collection.
    * @param[out] node_neighbors: vector of indexes of neighbors of specified node.
    *
    ***********************************************************************************************/
    virtual void get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const;
};

#endif

