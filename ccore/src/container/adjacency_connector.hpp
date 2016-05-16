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

#ifndef _ADJACENCY_CONNECTOR_H_
#define _ADJACENCY_CONNECTOR_H_


#include <memory>
#include <functional>
#include <cmath>
#include <ostream>

#include "container/adjacency.hpp"


namespace container {

/**
*
* @brief   Enumeration of pre-defined structures of connections between nodes in collection.
*
*/
enum class connection_t {
	/*!< Connections does not exists. */
	CONNECTION_NONE = 0,

	/*!< Each node is connected with all nodes except itself. */
	CONNECTION_ALL_TO_ALL = 1,

    /*!< Each node is connected with four neighbors: left, upper, right and lower. */
    CONNECTION_GRID_FOUR = 2,

    /*!< Each node is connected with eight neighbors: left, left-upper, upper, upper-right, right, right-lower, lower and lower-left. */
    CONNECTION_GRID_EIGHT = 3,

    /*!< Each node is connected with two neighbors: left and right. */
    CONNECTION_LIST_BIDIRECTIONAL = 4,
};


/**
*
* @brief   Generates a sequence of characters with the representation of structure of connections.
*
*/
std::ostream & operator<<(std::ostream & p_stream, const connection_t & p_structure);


/**
*
* @brief   Class for creating pre-defined most popular structures by establishing connections
*          between nodes in unweight adjacency collections.
*
*/
template <typename TypeCollection = adjacency_collection>
class adjacency_connector {
protected:
    typedef std::function<void(const size_t, const size_t, TypeCollection &)>  connector_controller;


protected:
    connector_controller    m_connector;


public:
    /**
    *
    * @brief   Default constructor of connector.
    *
    */
    adjacency_connector(void) {
        m_connector = [this](const size_t index1, const size_t index2, TypeCollection & collection) { 
            collection.set_connection(index1, index2); 
        };
    }

public:
    /**
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
    */
    virtual void create_structure(const connection_t structure_type, TypeCollection & output_adjacency_collection) {
        switch(structure_type) {
        case connection_t::CONNECTION_NONE:
            create_none_connections(output_adjacency_collection);
            break;

        case connection_t::CONNECTION_ALL_TO_ALL:
            create_all_to_all_connections(output_adjacency_collection);
            break;

        case connection_t::CONNECTION_GRID_FOUR:
            create_grid_four_connections(output_adjacency_collection);
            break;

        case connection_t::CONNECTION_GRID_EIGHT:
            create_grid_eight_connections(output_adjacency_collection);
            break;

        case connection_t::CONNECTION_LIST_BIDIRECTIONAL:
            create_list_bidir_connections(output_adjacency_collection);
            break;

        default:
            throw std::runtime_error("Type of connection is not supported.");
        }
    }

    /**
    *
    * @brief   Removes all connections in adjacency collection.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    */
    virtual void create_none_connections(TypeCollection & output_adjacency_collection) {
        for (size_t i = 0; i < output_adjacency_collection.size(); i++) {
            output_adjacency_collection.erase_connection(i, i);

            for (size_t j = i + 1; j < output_adjacency_collection.size(); j++) {
                output_adjacency_collection.erase_connection(i, j);
                output_adjacency_collection.erase_connection(j, i);
            }
        }
    }

    /**
    *
    * @brief   Creates connections between all nodes where each node has connection with others.
    * @details This method does not connect node with itself.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    */
    virtual void create_all_to_all_connections(TypeCollection & output_adjacency_collection) {
        for (size_t i = 0; i < output_adjacency_collection.size(); i++) {
            output_adjacency_collection.erase_connection(i, i);

            for (size_t j = i + 1; j < output_adjacency_collection.size(); j++) {
                m_connector(i, j, output_adjacency_collection);
                m_connector(j, i, output_adjacency_collection);
            }
        }
    }

    /**
    *
    * @brief   Creates connections where each node is connected with two node-neighbors (except the 
    *          first and the last node): left and right in line with following scheme: 1 <-> 2 <-> 3 <- ... -> 
    *          (N - 2) <-> (N - 1) <-> N.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    */
    virtual void create_list_bidir_connections(TypeCollection & output_adjacency_collection) {
        create_none_connections(output_adjacency_collection);

        for (size_t i = 0; i < output_adjacency_collection.size(); i++) {
		    if (i > 0) {
			    m_connector(i, i - 1, output_adjacency_collection);
		    }

		    if (i < (output_adjacency_collection.size() - 1)) {
			    m_connector(i, i + 1, output_adjacency_collection);
		    }
	    }
    }

    /**
    *
    * @brief   Creates connections where each node is connected with four node-neighbors: left, right, 
    *          upper and lower.
    * @details This method does not receive arguments that specify grid description: width and height.
    *          Every adjacency collection is considered as a square and if root cannot be extracted
    *          from amount of nodes then exception will be generated. 
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    */
    virtual void create_grid_four_connections(TypeCollection & output_adjacency_collection) {
        const double conv_side_size = std::sqrt((double)output_adjacency_collection.size());
        if (conv_side_size - std::floor(conv_side_size) > 0) {
            throw std::runtime_error("Invalid number of nodes in the adjacency for the square grid structure.");
        }

        const size_t edge = (size_t) conv_side_size;
        create_grid_four_connections(edge, edge, output_adjacency_collection);
    }

    /**
    *
    * @brief   Creates connections where each node is connected with four node-neighbors: left, right, 
    *          upper and lower.
    *
    * @param[in] width: width of created grid structure that is defined by amount of nodes in a column.
    * @param[in] height: height of created grid structure that is defined by amount of nodes in a row.
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    */
    virtual void create_grid_four_connections(const size_t width, const size_t height, TypeCollection & output_adjacency_collection) {
        if (width * height != output_adjacency_collection.size()) {
            throw std::runtime_error("Invalid number of nodes in the adjacency for the grid structure.");
        }

        create_none_connections(output_adjacency_collection);

	    for (int index = 0; index < (int) output_adjacency_collection.size(); index++) {
            const int upper_index = index - width;
            const int lower_index = index + width;
		    const int left_index = index - 1;
		    const int right_index = index + 1;

            const int node_row_index = (size_t) std::ceil(index / width);
		    if (upper_index >= 0) {
			    m_connector(index, upper_index, output_adjacency_collection);
		    }

		    if (lower_index < output_adjacency_collection.size()) {
			    m_connector(index, lower_index, output_adjacency_collection);
		    }

            if ((left_index >= 0) && (std::ceil(left_index / width) == node_row_index)) {
			    m_connector(index, left_index, output_adjacency_collection);
		    }

            if ((right_index < output_adjacency_collection.size()) && (std::ceil(right_index / width) == node_row_index)) {
			    m_connector(index, right_index, output_adjacency_collection);
		    }
	    }
    }

    /**
    *
    * @brief   Creates connections where each node is connected with eight node-neighbors: left,
    *          left-upper, upper, upper-right, right, right-lower, lower, lower-left.
    * @details This method does not receive arguments that specify grid description: width and height.
    *          Every adjacency collection is considered as a square and if root cannot be extracted
    *          from amount of nodes then exception will be generated.
    *
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    */
    virtual void create_grid_eight_connections(TypeCollection & output_adjacency_collection) {
        const double conv_side_size = std::sqrt((double)output_adjacency_collection.size());
        if (conv_side_size - std::floor(conv_side_size) > 0) {
            throw std::runtime_error("Invalid number of nodes in the adjacency for the square grid structure.");
        }

        const size_t edge = (size_t) conv_side_size;
		create_grid_eight_connections(edge, edge, output_adjacency_collection);
    }

    /**
    *
    * @brief   Creates connections where each node is connected with eight node-neighbors: left,
    *          left-upper, upper, upper-right, right, right-lower, lower, lower-left.
    *
    * @param[in] width: width of created grid structure that is defined by amount of nodes in a column.
    * @param[in] height: height of created grid structure that is defined by amount of nodes in a row.
    * @param[out] output_adjacency_collection: adjacency collection whose connections should be updated.
    *
    */
    virtual void create_grid_eight_connections(const size_t width, const size_t height, TypeCollection & output_adjacency_collection) {
	    create_grid_four_connections(width, height, output_adjacency_collection);	/* create connection with right, upper, left, lower neighbor */

	    for (int index = 0; index < output_adjacency_collection.size(); index++) {
            const int upper_left_index = index - width - 1;
            const int upper_right_index = index - width + 1;
            
            const int lower_left_index = index + width - 1;
            const int lower_right_index = index + width + 1;
            
            const int node_row_index = std::floor(index / width);
            const int upper_row_index = node_row_index - 1;
            const int lower_row_index = node_row_index + 1;

            if ((upper_left_index >= 0) && (std::floor(upper_left_index / width) == upper_row_index)) {
			    m_connector(index, upper_left_index, output_adjacency_collection);
		    }

            if ((upper_right_index >= 0) && (std::floor(upper_right_index / width) == upper_row_index)) {
			    m_connector(index, upper_right_index, output_adjacency_collection);
		    }

            if ((lower_left_index < output_adjacency_collection.size()) && (std::floor(lower_left_index / width) == lower_row_index)) {
			    m_connector(index, lower_left_index, output_adjacency_collection);
		    }

            if ((lower_right_index < output_adjacency_collection.size()) && (std::floor(lower_right_index / width) == lower_row_index)) {
			    m_connector(index, lower_right_index, output_adjacency_collection);
		    }
	    }
    }

	/**
	*
	* @brief   Creates rectangle grid structure in line with specify type of connections.
	* @details It throws exception if non-grid structures is specify as a grid type.
	*
	* @param[in] p_grid: type of grid structure (for example, four grid or eight grid).
	* @param[in] p_width: width of created grid structure that is defined by amount of nodes in a column.
	* @param[in] p_height: height of created grid structure that is defined by amount of nodes in a row.
	* @param[out] p_output_adjacency_collection: adjacency collection whose connections should be updated.
	*
	*/
	virtual void create_grid_structure(const connection_t p_grid, const size_t p_width, const size_t p_height, TypeCollection & p_output_adjacency_collection) {
		switch (p_grid) {
		case connection_t::CONNECTION_GRID_FOUR:
			create_grid_four_connections(p_width, p_height, p_output_adjacency_collection);
			break;

		case connection_t::CONNECTION_GRID_EIGHT:
			create_grid_eight_connections(p_width, p_height, p_output_adjacency_collection);
			break;

		default:
			throw std::runtime_error("Grid structure of connection is expected");
		}
	}
};


/**
*
* @brief   Class for creating pre-defined most popular structures by establishing connections
*          between nodes in weight adjacency collections.
*
*/
template <typename TypeCollection>
class adjacency_weight_connector : public adjacency_connector<TypeCollection> {
public:
    typedef std::function<double(void)>     adjacency_weight_initializer;


protected:
    adjacency_weight_initializer    m_initializer;


public:
    /**
    *
    * @brief   Default constructor of connector where weight initializer is not specified.
    * @details In this case adjacency collection defines default value of weight by itself in
    *          method 'set_connection()'.
    *
    */
    adjacency_weight_connector(void) { }

    /**
    *
    * @brief   Constructor of connector with weight initializer.
    * @details Initializer is used during creating connections between nodes for assigning weight
    *          for each connection. Generally the initializer represents pointer to some function
    *          that is used to assign weight, for example, if constant value is required then
    *          the function should return always the same value, otherwise some logic can be
    *          implemented.
    *
    * @param[in] initializer: initializer that is used for setting value of each weight connection.
    *
    */
    adjacency_weight_connector(const adjacency_weight_initializer & initializer) {
        if (initializer != nullptr) {
            m_initializer = initializer; /* [this](const size_t index1, const size_t index2, TypeCollection & collection) {
                collection.set_connection_weight(index1, index2, initializer());
            }; */
        }
    }
};

}


#endif
