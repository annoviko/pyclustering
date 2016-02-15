#include "adjacency_connector.h"

void adjacency_connector::create_structure(const connection_t structure_type, adjacency_collection & output_adjacency_collection) {

}

void adjacency_connector::create_none_connections(adjacency_collection & output_adjacency_collection) {
    for (size_t i = 0; i < output_adjacency_collection.size(); i++) {
        output_adjacency_collection.erase_connection(i, i);

        for (size_t j = i + 1; j < output_adjacency_collection.size(); j++) {
            output_adjacency_collection.erase_connection(i, j);
            output_adjacency_collection.erase_connection(j, i);
        }
    }
}


void adjacency_connector::create_all_to_all_connections(adjacency_collection & output_adjacency_collection) {
    for (size_t i = 0; i < output_adjacency_collection.size(); i++) {
        output_adjacency_collection.erase_connection(i, i);

        for (size_t j = i + 1; j < output_adjacency_collection.size(); j++) {
            output_adjacency_collection.set_connection(i, j);
            output_adjacency_collection.set_connection(j, i);
        }
    }
}


void adjacency_connector::create_list_bidir_connections(adjacency_collection & output_adjacency_collection) {
    create_none_connections(output_adjacency_collection);

    for (size_t i = 0; i < output_adjacency_collection.size(); i++) {
		if (i > 0) {
			output_adjacency_collection.set_connection(i, i - 1);
		}

		if (i < (output_adjacency_collection.size() - 1)) {
			output_adjacency_collection.set_connection(i, i + 1);
		}
	}
}


void adjacency_connector::create_grid_four_connections(adjacency_collection & output_adjacency_collection) {

}


void adjacency_connector::create_grid_eight_connections(adjacency_collection & output_adjacency_collection) {

}