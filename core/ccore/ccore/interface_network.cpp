#include "interface_network.h"

network::network(const unsigned int number_oscillators, const conn_type connection_type) {
	num_osc = number_oscillators;

	osc_conn = new std::vector<std::vector<unsigned int> * >(number_oscillators, NULL);
	for (unsigned int index = 0; index < number_oscillators; index++) {
		(*osc_conn)[index] = new std::vector<unsigned int>(number_oscillators, 0);
	}
}

network::~network() {
	if (osc_conn != NULL) {
		for (std::vector<std::vector<unsigned int> *>::iterator iter = osc_conn->begin(); iter != osc_conn->end(); iter++) {
			delete (*iter); 
			(*iter) = NULL;
		}

		delete osc_conn;
		osc_conn = NULL;
	}
}

std::vector<unsigned int> * network::get_neighbors(const unsigned int index) const {
	std::vector<unsigned int> * result = new std::vector<unsigned int>();
	for (std::vector<unsigned int>::const_iterator iter = (*osc_conn)[index]->begin(); iter != (*osc_conn)[index]->end(); iter++) {
		if ((*iter) > 0) {
			result->push_back(*iter);
		}
	}

	return result;
}

void network::create_structure(const conn_type connection_structure) {
	switch(connection_structure) {
		case conn_type::NONE:
			create_none_connections();
			break;
		case conn_type::ALL_TO_ALL:
			create_all_to_all_connections();
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
			break;
	}
}

void network::create_all_to_all_connections() {
	for (unsigned int row = 0; row < num_osc; row++) {
		for (unsigned int col = row + 1; col < num_osc; col++) {
			(*(*osc_conn)[row])[col] = 1;
			(*(*osc_conn)[col])[row] = 1;
		}
	}
}

void network::create_list_bidir_connections() {
	for (unsigned int index = 0; index < num_osc; index++) {
		if (index > 0) {
			
		}
	}
}