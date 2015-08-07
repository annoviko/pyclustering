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

#include "network.h"

#include <cmath>
#include <exception>
#include <stdexcept>
#include <algorithm>


network::network(const unsigned int number_oscillators, const conn_type connection_type) {
	num_osc = number_oscillators;
	m_conn_type = connection_type;

	if ( (m_conn_type != conn_type::ALL_TO_ALL) && (m_conn_type != conn_type::NONE) ) {
	    m_osc_conn.resize(number_oscillators, std::vector<unsigned int>());

		if (m_conn_type == conn_type::DYNAMIC) {
			unsigned int number_elements = 0;
			if (number_oscillators > MAXIMUM_OSCILLATORS_MATRIX_REPRESENTATION) {
				conn_representation = BITMAP_CONN_REPRESENTATION;
				number_elements = std::ceil( number_oscillators / sizeof(unsigned int) );
			}
			else {
				conn_representation = MATRIX_CONN_REPRESENTATION;
				number_elements = number_oscillators;
			}
	
			for (unsigned int index = 0; index < number_oscillators; index++) {
			    m_osc_conn[index].resize(number_elements, 0);
			}
		}
		else if ( (m_conn_type == conn_type::GRID_FOUR) || 
			      (m_conn_type == conn_type::GRID_EIGHT) ||
				  (m_conn_type == conn_type::LIST_BIDIR) ) {
			       conn_representation = LIST_CONN_REPRESENTATION;

			       /* No predefined size for list representation */
		}

		create_structure(connection_type);
	}
}

network::~network() { }

void network::get_neighbors(const unsigned int index, std::vector<unsigned int> & result) const {
	result.clear();

	switch (m_conn_type) {
		case conn_type::ALL_TO_ALL: {
			for (unsigned int index_neighbour = 0; index_neighbour < num_osc; index_neighbour++) {
				if (index_neighbour != index) {
					result.push_back(index_neighbour);
				}
			}
			break;
		}

		case conn_type::GRID_EIGHT:
		case conn_type::GRID_FOUR:
		case conn_type::LIST_BIDIR: {
			result.resize(m_osc_conn[index].size());
			std::copy(m_osc_conn[index].begin(), m_osc_conn[index].end(), result.begin());
			break;
		}

		case conn_type::DYNAMIC: {
			for (unsigned int index_neighbour = 0; index_neighbour < num_osc; index_neighbour++) {
				if (get_connection(index, index_neighbour) > 0) {
					result.push_back(index_neighbour);
				}
			}
			break;
		}

		case conn_type::NONE:
		default:
			break;
	}
}

unsigned int network::get_connection(const unsigned int index1, const unsigned int index2) const { 
	if (m_conn_type == conn_type::ALL_TO_ALL) {
		if (index1 == index2) {
			return (unsigned int) 0;
		}
        else {
            return (unsigned int) 1;
        }
	}
	else if (m_conn_type == conn_type::NONE) {
		return (unsigned int) 0;
	}

	switch(conn_representation) {
		case MATRIX_CONN_REPRESENTATION: {
			return m_osc_conn[index1][index2];
		}
		case BITMAP_CONN_REPRESENTATION: {
			const unsigned int index_element = index2 / ( sizeof(unsigned int) << 3 );
			const unsigned int bit_number = index2 - ( index_element * (sizeof(unsigned int) << 3) );

			return ( m_osc_conn[index1][index_element] >> bit_number ) & (unsigned int) 0x01;
		}
		case LIST_CONN_REPRESENTATION: {
			unsigned int output_value = (unsigned int) 0;
			const std::vector<unsigned int> & neighbors = m_osc_conn[index1];
			std::vector<unsigned int>::const_iterator existance = std::find(neighbors.begin(), neighbors.end(), index2);
			if (existance != neighbors.end()) {
				output_value = (unsigned int) 1;
			}

			return output_value;
		}
		default: {
			throw std::runtime_error("Unknown type of representation of connections");
		}
	}
}

void network::set_connection(const unsigned int index1, const unsigned int index2) {
	switch(conn_representation) {
		case MATRIX_CONN_REPRESENTATION: {
			m_osc_conn[index1][index2] = 1;
			break;
		}
		case BITMAP_CONN_REPRESENTATION: {
			unsigned int index_element = index2 / ( sizeof(unsigned int) << 3 );
			unsigned int bit_number = index2 % ( sizeof(unsigned int) << 3 );

			m_osc_conn[index1][index_element] = m_osc_conn[index1][index_element] | ( (unsigned int) 0x01 << bit_number );
			break;
		}
		case LIST_CONN_REPRESENTATION: {
			m_osc_conn[index1].push_back(index2);
			break;
		}
		default: {
			throw std::runtime_error("Unknown type of representation of connections");
		}
	}
}

void network::create_structure(const conn_type connection_structure) {
	switch(connection_structure) {
		case conn_type::NONE:
		case conn_type::DYNAMIC:
		case conn_type::ALL_TO_ALL:
			break;
		case conn_type::GRID_FOUR:
			create_grid_four_connections();
			break;
		case conn_type::GRID_EIGHT:
			create_grid_eight_connections();
			break;
		case conn_type::LIST_BIDIR:
			create_list_bidir_connections();
			break;
		default:
			throw std::runtime_error("Unknown type of connection");
	}
}


void network::create_list_bidir_connections() {
	for (unsigned int index = 0; index < num_osc; index++) {
		if (index > 0) {
			set_connection(index, index - 1);
		}

		if (index < (num_osc - 1)) {
			set_connection(index, index + 1);
		}
	}
}

void network::create_grid_four_connections() {
	const double conv_side_size = std::sqrt((double) num_osc);
	if (conv_side_size - std::floor(conv_side_size) > 0) {
		throw std::runtime_error("Invalid number of oscillators in the network for the grid structure");
	}

	const unsigned int side_size = (unsigned int) conv_side_size;

	for (unsigned int index = 0; index < num_osc; index++) {


		const int upper_index = index - side_size;
		const int lower_index = index + side_size;
		const int left_index = index - 1;
		const int right_index = index + 1;

		unsigned int node_row_index = std::ceil(index / side_size);
		if (upper_index >= 0) {
			set_connection(index, upper_index);
		}

		if (lower_index < num_osc) {
			set_connection(index, lower_index);
		}

		if ( (left_index >= 0) && (std::ceil(left_index / side_size) == node_row_index) ) {
			set_connection(index, left_index);
		}

		if ( (right_index < num_osc) && (std::ceil(right_index / side_size) == node_row_index) ) {
			set_connection(index, right_index);
		}
	}
}

void network::create_grid_eight_connections() {
	create_grid_four_connections();	/* create connection with right, upper, left, lower neighbor */
	
	const int side_size = (unsigned int) std::sqrt((double) num_osc);

	for (unsigned int index = 0; index < num_osc; index++) {
        const int upper_index = index - side_size;
        const int upper_left_index = index - side_size - 1;
        const int upper_right_index = index - side_size + 1;
            
        const int lower_index = index + side_size;
        const int lower_left_index = index + side_size - 1;
        const int lower_right_index = index + side_size + 1;
            
        const int left_index = index - 1;
        const int right_index = index + 1;
            
        const int node_row_index = std::floor(index / side_size);
        const int upper_row_index = node_row_index - 1;
        const int lower_row_index = node_row_index + 1;

		if ( (upper_left_index >= 0) && (std::floor(upper_left_index / side_size) == upper_row_index) ) {
			set_connection(index, upper_left_index);
		}

		if ( (upper_right_index >= 0) && (std::floor(upper_right_index / side_size) == upper_row_index) ) {
			set_connection(index, upper_right_index);
		}

		if ( (lower_left_index < num_osc) && (std::floor(lower_left_index / side_size) == lower_row_index) ) {
			set_connection(index, lower_left_index);
		}

		if ( (lower_right_index < num_osc) && (std::floor(lower_right_index / side_size) == lower_row_index) ) {
			set_connection(index, lower_right_index);
		}
	}
}
