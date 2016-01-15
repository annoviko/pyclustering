#ifndef _ADJACENCY_H_
#define _ADJACENCY_H_

#include <vector>


template<typename T>
using matrix = std::vector<std::vector<T>>;


/***********************************************************************************************
*
* @brief   Abstract class of the adjacency collection that provides ability to control objects.
*
***********************************************************************************************/
template<typename TypeNode>
class adjacency_collection {
public:
    matrix<TypeNode>      m_adjacency; 
    
public:
    /***********************************************************************************************
    *
    * @brief   Returns size of adjacency collection that is defined by number of nodes.
    *
    ***********************************************************************************************/
    virtual size_t size(void) const = 0;

    /***********************************************************************************************
    *
    * @brief   Establishes connection between two nodes in adjacency collection.
    *
    * @param[in] node_index1: index of node in the collection that should be connected with another.
    * @param[in] node_index2: index of another node in the collection that should be connected with
    *                         the node defined by the first argument 'node_index1'.
    * @param[in] conn_weight: value of connection that defines
    *
    ***********************************************************************************************/
    virtual void set_connection(const size_t node_index1, const size_t node_index2, const TypeNode conn_weight) = 0;

    /***********************************************************************************************
    *
    * @brief   Returns value of connection that denotes weight of connection.
    *
    * @param[in] node_index1: index of node in the collection.
    * @param[in] node_index2: index of another node in the collection.
    *
    ***********************************************************************************************/
    virtual TypeNode get_connection(const size_t node_index1, const size_t node_index2) const = 0;

    /***********************************************************************************************
    *
    * @brief   Returns value of connection that denotes weight of connection.
    *
    * @param[in] node_index1: index of node in the collection.
    * @param[in] node_index2: index of another node in the collection.
    *
    ***********************************************************************************************/
    virtual void get_neighbors(const size_t node_index, std::vector<size_t> & node_neighbors) const = 0;
};


class adjacency_bit_matrix : public adjacency_collection<size_t> {
public:

};

class adjacency_list_matrix : public adjacency_collection<size_t> {
public:

};

class adjacency_matrix : public adjacency_collection<double> {
public:

};

#endif