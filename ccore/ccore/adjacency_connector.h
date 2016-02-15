#ifndef _ADJACENCY_CONNECTOR_H_
#define _ADJACENCY_CONNECTOR_H_

#include "adjacency.h"


enum class connection_t {
    CONNECTION_NONE,
    CONNECTION_GRID_FOUR,
    CONNECTION_GRID_EIGHT,
    CONNECTION_ALL_TO_ALL,
    CONNECTION_LIST_BIDIRECTIONAL,
};


class adjacency_connector {
public:
    /***********************************************************************************************
    *
    * @brief   Creates connections between nodes in adjacency collection.
    *
    * @param[in] structure_type: structure of connections in adjacency collection that should be created.
    * @param[in] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    void create_structure(const connection_t structure_type, adjacency_collection & output_adjacency_collection);

private:
    /***********************************************************************************************
    *
    * @brief   Removes all connections in adjacency collection.
    *
    * @param[in] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    void create_none_connections(adjacency_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections between all nodes where each node has connection with others.
    * @details This method does not connect node with itself.
    *
    * @param[in] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    void create_all_to_all_connections(adjacency_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections where each node is connected with two node-neighbors (except the 
    *          first and the last node): left and right in line with following scheme: 1 <-> 2 <-> 3 <- ... -> 
    *          (N - 2) <-> (N - 1) <-> N.
    *
    * @param[in] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    void create_list_bidir_connections(adjacency_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections where each node is connected with four node-neighbors: left, right, 
    *          upper and lower.
    *
    * @param[in] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    void create_grid_four_connections(adjacency_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections where each node is connected with eight node-neighbors: left,
    *          left-upper, upper, upper-right, right, right-lower, lower, lower-left.
    *
    * @param[in] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    void create_grid_eight_connections(adjacency_collection & output_adjacency_collection);
};


#endif