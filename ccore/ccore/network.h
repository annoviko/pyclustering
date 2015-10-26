/**************************************************************************************************************

Abstract network representation that is used as a basic class.

Based on book description:
 - J.B.MacQueen. Some Methods for Classification and Analysis of Multivariate Observations. 1967.

Copyright (C) 2015    Andrei Novikov (pyclustering@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

**************************************************************************************************************/

#ifndef _INTERFACE_NETWORK_H_
#define _INTERFACE_NETWORK_H_

#include <cmath>
#include <vector>
#include <stdexcept>
#include <memory>

#include "dynamic_data.h"
#include "ensemble_data.h"

#define MAXIMUM_OSCILLATORS_MATRIX_REPRESENTATION	(unsigned int) 4096

typedef enum initial_type {
	RANDOM_GAUSSIAN,
	EQUIPARTITION,
	TOTAL_NUMBER_INITIAL_TYPES
} initial_type;


typedef enum solve_type {
	FAST,
	RK4,
	RKF45,
	TOTAL_NUMBER_SOLVE_TYPES
} solve_type;


typedef enum conn_type {
	NONE,
	ALL_TO_ALL,
	GRID_FOUR,
	GRID_EIGHT,
	LIST_BIDIR,
	DYNAMIC,
	TOTAL_NUMBER_CONN_TYPES
} conn_type;


typedef enum conn_repr_type {
	MATRIX_CONN_REPRESENTATION,
	BITMAP_CONN_REPRESENTATION,
	LIST_CONN_REPRESENTATION,
	TOTAL_NUMBER_CONN_REPR_TYPES
} conn_repr_type;



class network {
private:
	size_t			    m_num_osc;
	conn_repr_type		m_conn_representation;
	conn_type			m_conn_type;

    size_t              m_height;
    size_t              m_width;

	std::vector<std::vector<size_t> >		m_osc_conn;

public:
    /***********************************************************************************************
    *
    * @brief   Creates network of coupled oscillators.
    * @details In case of networks with grid structures (GRID_FOUR, GRID_EIGHT) square grid is
    *          considered and it means that value of number of oscillators should be square root 
    *          extractable for these types of connection.
    *
    * @param[in] number_oscillators: number of oscillators that should be in the network.
    * @param[in] connection_type: structure of connections between oscillators.
    *
    ***********************************************************************************************/
    network(const size_t number_oscillators, const conn_type connection_type);

    /***********************************************************************************************
    *
    * @brief   Creates network of coupled oscillators.
    * @details Provides ability to specify number of oscillators in rows and columns in case of
    *          networks with grid structure (GRID_FOUR, GRID_EIGHT). In network with other types
    *          of network connections height and width are ignored.
    *
    * @param[in] number_oscillators: number of oscillators that should be in the network.
    * @param[in] connection_type: structure of connections between oscillators.
    * @param[in] height: number of oscillators in column of the network, this argument is 
    *            used only for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types
    *            this argument is ignored.
    * @param[in] width: number of oscillotors in row of the network, this argument is used 
    *            only for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types this 
    *            argument is ignored.
    *
    ***********************************************************************************************/
    network(const size_t number_oscillators,
            const conn_type connection_type,
            const size_t height,
            const size_t width);

    /***********************************************************************************************
    *
    * @brief   Default destructor of the network.
    *
    ***********************************************************************************************/
	virtual ~network();

    /***********************************************************************************************
    *
    * @brief   Returns size of the network that is defined by number of oscillators.
    *
    ***********************************************************************************************/
    inline size_t size(void) const { return m_num_osc; }

    /***********************************************************************************************
    *
    * @brief   Returns number of oscillators that are located in each column of the network.
    * @details This value is used by networks that have grid structure. Number of oscillators in
    *          the column defines height of the network. In case of structures differ from grid this 
    *          method returns 0.
    *
    ***********************************************************************************************/
    inline size_t height(void) const { return m_height; }

    /***********************************************************************************************
    *
    * @brief   Returns number of oscillators that are located in each row of the network.
    * @details This value is used by networks that have grid structure. Number of oscillators in
    *          the row defines width of the network. In case of structures differ from grid this
    *          method returns 0.
    *
    ***********************************************************************************************/
    inline size_t width(void) const { return m_width; }

    virtual size_t get_connection(const size_t index1, const size_t index2) const;

    virtual void set_connection(const size_t index1, const size_t index2);

    virtual void get_neighbors(const size_t index, std::vector<size_t> & result) const;
	
private:
	void create_grid_four_connections(void);
	void create_grid_eight_connections(void);
	void create_list_bidir_connections(void);

    /***********************************************************************************************
    *
    * @brief   Defines optimal representation for connections and create network structure.
    *
    ***********************************************************************************************/
    void create_structure(void);

    /***********************************************************************************************
    *
    * @brief   Defines optimal representation for connections and prepare storage for them in line
    *          required type connections and number of oscillators in the network.
    *
    ***********************************************************************************************/
    void create_structure_representation(void);
};

#endif
