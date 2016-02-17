#ifndef _ADJACENCY_CONNECTOR_H_
#define _ADJACENCY_CONNECTOR_H_

#include "adjacency.h"

#include <memory>
#include <functional>


/***********************************************************************************************
*
* @brief   Enumeration of pre-defined structures of connections between nodes in collection.
*
***********************************************************************************************/
enum class connection_t {
    /*!< Connections does not exists. */
    CONNECTION_NONE,

    /*!< Each node is connected with four neighbors: left, upper, right and lower. */
    CONNECTION_GRID_FOUR,

    /*!< Each node is connected with eight neighbors: left, left-upper, upper, upper-right, right, right-lower, lower and lower-left. */
    CONNECTION_GRID_EIGHT,

    /*!< Each node is connected with all nodes except itself. */
    CONNECTION_ALL_TO_ALL,

    /*!< Each node is connected with two neighbors: left and right. */
    CONNECTION_LIST_BIDIRECTIONAL,
};


/***********************************************************************************************
*
* @brief   Class for creating pre-defined most popular structures by establishing connections
*          between nodes in unweight adjacency collections.
*
***********************************************************************************************/
class adjacency_connector {
protected:
    typedef std::function<void(const size_t, const size_t, adjacency_collection &)>  connector_controller;


protected:
    connector_controller    m_connector;


public:
    /***********************************************************************************************
    *
    * @brief   Default constructor of connector.
    *
    ***********************************************************************************************/
    adjacency_connector(void);

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
    virtual void create_structure(const connection_t structure_type, adjacency_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Removes all connections in adjacency collection.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_none_connections(adjacency_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections between all nodes where each node has connection with others.
    * @details This method does not connect node with itself.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_all_to_all_connections(adjacency_collection & output_adjacency_collection);

    /***********************************************************************************************
    *
    * @brief   Creates connections where each node is connected with two node-neighbors (except the 
    *          first and the last node): left and right in line with following scheme: 1 <-> 2 <-> 3 <- ... -> 
    *          (N - 2) <-> (N - 1) <-> N.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    ***********************************************************************************************/
    virtual void create_list_bidir_connections(adjacency_collection & output_adjacency_collection);

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
    virtual void create_grid_four_connections(adjacency_collection & output_adjacency_collection);

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
    virtual void create_grid_four_connections(const size_t width, const size_t height, adjacency_collection & output_adjacency_collection);

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
    virtual void create_grid_eight_connections(adjacency_collection & output_adjacency_collection);

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
    virtual void create_grid_eight_connections(const size_t width, const size_t height, adjacency_collection & output_adjacency_collection);
};


/***********************************************************************************************
*
* @brief   Class for creating pre-defined most popular structures by establishing connections
*          between nodes in weight adjacency collections.
*
***********************************************************************************************/
class adjacency_weight_connector : public adjacency_connector {
public:
    typedef std::function<double(void)>     adjacency_weight_initializer;


protected:
    adjacency_weight_initializer    m_initializer;


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
    adjacency_weight_connector(adjacency_weight_initializer & initializer);
};


#endif