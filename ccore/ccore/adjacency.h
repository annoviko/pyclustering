#ifndef _ADJACENCY_H_
#define _ADJACENCY_H_

#include <vector>

/***********************************************************************************************
*
* @brief   Interface of the adjacency collection that provides ability to control adjacancy objects.
*
***********************************************************************************************/
class adjacency {
public:
    /***********************************************************************************************
    *
    * @brief   Returns size of adjacency collection that is defined by number of nodes.
    *
    ***********************************************************************************************/
    virtual size_t size(void) const = 0;

    /***********************************************************************************************
    *
    * @brief   Returns width of adjacency collection that defines number of nodes in row.
    *
    ***********************************************************************************************/
    virtual size_t width(void) const = 0;

    /***********************************************************************************************
    *
    * @brief   Returns height of adjacency collection that defines number of nodes in column.
    *
    ***********************************************************************************************/
    virtual size_t height(void) const = 0;

    /***********************************************************************************************
    *
    * @brief   Establishes connection between two nodes in adjacency collection.
    *
    * @param[in] node_index1: index of node in the collection that should be connected with another.
    * @param[in] node_index2: index of another node in the collection that should be connected with
    *                         the node defined by the first argument 'node_index1'.
    *
    ***********************************************************************************************/
    virtual void set_connection(const size_t node_index1, const size_t node_index2) = 0;

    /***********************************************************************************************
    *
    * @brief   Returns value of connection that denotes weight of connection.
    *
    * @param[in] node_index1: index of node in the collection.
    * @param[in] node_index2: index of another node in the collection.
    *
    ***********************************************************************************************/
    virtual double get_connection(const size_t node_index1, const size_t node_index2) const = 0;

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


template<typename T>
using matrix = std::vector<std::vector<T>>;


class adjacency_bit_matrix : public adjacency {
public:
    matrix<size_t>      m_adjacency;            
};

class adjacency_list_matrix : public adjacency {
public:
    matrix<size_t>      m_adjacency;
};

class adjacency_matrix : public adjacency {
public:
    matrix<double>      m_adjacency;
};

#endif