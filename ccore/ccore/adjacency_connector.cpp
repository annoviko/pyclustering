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
    const double conv_side_size = std::sqrt((double)output_adjacency_collection.size());
    if (conv_side_size - std::floor(conv_side_size) > 0) {
        throw std::runtime_error("Invalid number of nodes in the adjacency for the square grid structure.");
    }

    const size_t edge = (size_t) conv_side_size;
    create_grid_four_connections(edge, edge, output_adjacency_collection);
}


void adjacency_connector::create_grid_four_connections(const size_t width, const size_t height, adjacency_collection & output_adjacency_collection) {
    if (width * height != output_adjacency_collection.size()) {
        throw std::runtime_error("Invalid number of nodes in the adjacency for the grid structure.");
    }

    create_none_connections(output_adjacency_collection);

	for (size_t index = 0; index < output_adjacency_collection.size(); index++) {
        const size_t upper_index = index - width;
        const size_t lower_index = index + width;
		const size_t left_index = index - 1;
		const size_t right_index = index + 1;

        const size_t node_row_index = (size_t) std::ceil(index / width);
		if (upper_index >= 0) {
			output_adjacency_collection.set_connection(index, upper_index);
		}

		if (lower_index < output_adjacency_collection.size()) {
			output_adjacency_collection.set_connection(index, lower_index);
		}

        if ((left_index >= 0) && (std::ceil(left_index / width) == node_row_index)) {
			output_adjacency_collection.set_connection(index, left_index);
		}

        if ((right_index < output_adjacency_collection.size()) && (std::ceil(right_index / width) == node_row_index)) {
			output_adjacency_collection.set_connection(index, right_index);
		}
	}
}


void adjacency_connector::create_grid_eight_connections(adjacency_collection & output_adjacency_collection) {
    const double conv_side_size = std::sqrt((double)output_adjacency_collection.size());
    if (conv_side_size - std::floor(conv_side_size) > 0) {
        throw std::runtime_error("Invalid number of nodes in the adjacency for the square grid structure.");
    }

    const size_t edge = (size_t) conv_side_size;
    create_grid_four_connections(edge, edge, output_adjacency_collection);
}


void adjacency_connector::create_grid_eight_connections(const size_t width, const size_t height, adjacency_collection & output_adjacency_collection) {
	create_grid_four_connections(width, height, output_adjacency_collection);	/* create connection with right, upper, left, lower neighbor */

	for (size_t index = 0; index < output_adjacency_collection.size(); index++) {
        const size_t upper_index = index - width;
        const size_t upper_left_index = index - width - 1;
        const size_t upper_right_index = index - width + 1;
            
        const size_t lower_index = index + width;
        const size_t lower_left_index = index + width - 1;
        const size_t lower_right_index = index + width + 1;
            
        const size_t left_index = index - 1;
        const size_t right_index = index + 1;
            
        const size_t node_row_index = (size_t) std::floor(index / width);
        const size_t upper_row_index = node_row_index - 1;
        const size_t lower_row_index = node_row_index + 1;

        if ((upper_left_index >= 0) && (std::floor(upper_left_index / width) == upper_row_index)) {
			output_adjacency_collection.set_connection(index, upper_left_index);
		}

        if ((upper_right_index >= 0) && (std::floor(upper_right_index / width) == upper_row_index)) {
			output_adjacency_collection.set_connection(index, upper_right_index);
		}

        if ((lower_left_index < output_adjacency_collection.size()) && (std::floor(lower_left_index / width) == lower_row_index)) {
			output_adjacency_collection.set_connection(index, lower_left_index);
		}

        if ((lower_right_index < output_adjacency_collection.size()) && (std::floor(lower_right_index / width) == lower_row_index)) {
			output_adjacency_collection.set_connection(index, lower_right_index);
		}
	}
}