#ifndef _ADJACENCY_BIT_MATRIX_
#define _ADJACENCY_BIT_MATRIX_

#include "adjacency.h"


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
class adjacency_bit_matrix : public adjacency_collection {
private:
    typedef std::vector<std::vector<size_t>>      adjacency_bit_matrix_container;


protected:
    adjacency_bit_matrix_container  m_adjacency;

public:
    /***********************************************************************************************
    *
    * @brief   Default destructor without arguments is forbiden.
    *
    ***********************************************************************************************/
    adjacency_bit_matrix(void) = delete;

    /***********************************************************************************************
    *
    * @brief   Default copy constructor.
    *
    * @param[in]  another_matrix: adjacency matrix that should be copied.
    *
    ***********************************************************************************************/
    adjacency_bit_matrix(const adjacency_bit_matrix & another_matrix);

    /***********************************************************************************************
    *
    * @brief   Default move constructor.
    *
    * @param[in]  another_matrix: adjacency matrix that should be moved.
    *
    ***********************************************************************************************/
    adjacency_bit_matrix(adjacency_bit_matrix && another_matrix);

    /***********************************************************************************************
    *
    * @brief   Adjacency bit matrix constructor.
    *
    * @param[in]  node_amount: number of nodes whose connections are described in matrix.
    *
    ***********************************************************************************************/
    adjacency_bit_matrix(const size_t node_amount);

    /***********************************************************************************************
    *
    * @brief   Default destructor.
    *
    ***********************************************************************************************/
    virtual ~adjacency_bit_matrix(void);


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
    * @brief   Removes one-way connection from the first node to the second in adjacency collection.
    *
    * @param[in]  node_index1: index of node in the collection that should be disconnected from another.
    * @param[in]  node_index2: index of another node in the collection that should be diconnected from
    *              the node defined by the first argument 'node_index1'.
    *
    ***********************************************************************************************/
    virtual void erase_connection(const size_t node_index1, const size_t node_index2);

    /***********************************************************************************************
    *
    * @brief   Checks existance of connection between specified nodes.
    *
    * @param[in]  node_index1: index of node in the collection.
    * @param[in]  node_index2: index of another node in the collection.
    *
    * @return  'true' - connection between the nodes exists, 'false' - connection does not exist.
    *
    ***********************************************************************************************/
    virtual bool has_connection(const size_t node_index1, const size_t node_index2) const;

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


private:
    /***********************************************************************************************
    *
    * @brief   Sets or erases connection in line with specified state of connection.
    *
    * @details Requies math-logical operations to set connection.
    *
    * @param[in]  node_index1: index of node whose state of connection should be updated.
    * @param[in]  node_index2: index of another node in the collection.
    *
    ***********************************************************************************************/
    void update_connection(const size_t node_index1, const size_t node_index2, const size_t state_connection);
};

#endif

