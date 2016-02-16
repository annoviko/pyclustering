#ifndef _ADJACENCY_WEIGHT_CONNECTOR_H_
#define _ADJACENCY_WEIGHT_CONNECTOR_H_

#include "adjacency_connector.h"

#include <memory>
#include <functional>



/***********************************************************************************************
*
* @brief   Class for creating pre-defined most popular structures by establishing connections
*          between nodes in weight adjacency collections.
*
***********************************************************************************************/
class adjacency_weight_connector {
protected:
    std::function<double(void)> m_initializer;

    std::function<void(const size_t, const size_t, adjacency_weight_collection &)> m_connector;

public:
    /***********************************************************************************************
    *
    * @brief   Default constructor of connector where weight initializer is not specified.
    * @details In this case adjacency collection defines default value of weight by itself in
    *          method 'set_connection()'.
    *
    ***********************************************************************************************/
    adjacency_weight_connector(void);

    /***********************************************************************************************
    *
    * @brief   Constructor of connector with weight initializer.
    *
    * @param[in] initializer: initializer that is used for setting value of each weight connection.
    *
    ***********************************************************************************************/
    adjacency_weight_connector(std::function<double(void)> initializer);

public:
    /***********************************************************************************************
    *
    * @brief   Creates connections between nodes in adjacency collection in line with specified
    *          structure.
    * @details In case of grid structures it creates only square grids only, otherwise special
    *          methods should be used such as 'create_grid_four_connections(...)' or 
    *          'create_grid_eight_connections(...)'.
    *
    * @param[in] structure_type: structure of connections in adjacency collection that should be created.
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_structure(const connection_t structure_type, adjacency_weight_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Removes all connections in adjacency collection.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_none_connections(adjacency_weight_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections between all nodes where each node has connection with others.
    * @details This method does not connect node with itself.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_all_to_all_connections(adjacency_weight_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections where each node is connected with two node-neighbors (except the 
    *          first and the last node): left and right in line with following scheme: 1 <-> 2 <-> 3 <- ... -> 
    *          (N - 2) <-> (N - 1) <-> N.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_list_bidir_connections(adjacency_weight_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections where each node is connected with four node-neighbors: left, right, 
    *          upper and lower.
    * @details This method does not receive arguments that specify grid description: width and height.
    *          Every adjacency collection is considered as a square and if root cannot be extracted
    *          from amount of nodes then exception will be generated. 
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_grid_four_connections(adjacency_weight_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections where each node is connected with four node-neighbors: left, right, 
    *          upper and lower.
    *
    * @param[in] width: width of created grid structure that is defined by amount of nodes in a column.
    * @param[in] height: height of created grid structure that is defined by amount of nodes in a row.
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_grid_four_connections(const size_t width, const size_t height, adjacency_weight_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections where each node is connected with eight node-neighbors: left,
    *          left-upper, upper, upper-right, right, right-lower, lower, lower-left.
    * @details This method does not receive arguments that specify grid description: width and height.
    *          Every adjacency collection is considered as a square and if root cannot be extracted
    *          from amount of nodes then exception will be generated.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_grid_eight_connections(adjacency_weight_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections where each node is connected with eight node-neighbors: left,
    *          left-upper, upper, upper-right, right, right-lower, lower, lower-left.
    *
    * @param[in] width: width of created grid structure that is defined by amount of nodes in a column.
    * @param[in] height: height of created grid structure that is defined by amount of nodes in a row.
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_grid_eight_connections(const size_t width, const size_t height, adjacency_weight_collection & output_adjacency_collection);

protected:
    virtual void create_default_connection(const size_t index1, const size_t index2, adjacency_weight_collection & collection);

    virtual void create_specify_connection(const size_t index1, const size_t index2, adjacency_weight_collection & collection);
};

#endif