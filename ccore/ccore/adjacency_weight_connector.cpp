#include "adjacency_weight_connector.h"


adjacency_weight_connector::adjacency_weight_connector(void) : 
//m_connector(std::bind(&adjacency_weight_connector::create_default_connection, this)), 
m_initializer(nullptr) 
{
    m_connector = std::bind(&adjacency_weight_connector::create_default_connection, this);
}


adjacency_weight_connector::adjacency_weight_connector(std::function<double(void)> initializer) : 
//m_connector(std::bind(&adjacency_weight_connector::create_specify_connection, this)),
m_initializer(initializer)
{
    m_connector = std::bind(&adjacency_weight_connector::create_specify_connection, this);
}


void adjacency_weight_connector::create_structure(const connection_t structure_type, adjacency_weight_collection & output_adjacency_collection) {
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


void adjacency_weight_connector::create_none_connections(adjacency_weight_collection & output_adjacency_collection) {
    for (size_t i = 0; i < output_adjacency_collection.size(); i++) {
        output_adjacency_collection.erase_connection(i, i);

        for (size_t j = i + 1; j < output_adjacency_collection.size(); j++) {
            output_adjacency_collection.erase_connection(i, j);
            output_adjacency_collection.erase_connection(j, i);
        }
    }
}


void adjacency_weight_connector::create_all_to_all_connections(adjacency_weight_collection & output_adjacency_collection) {
    for (size_t i = 0; i < output_adjacency_collection.size(); i++) {
        output_adjacency_collection.erase_connection(i, i);

        for (size_t j = i + 1; j < output_adjacency_collection.size(); j++) {
            m_connector(i, j, output_adjacency_collection);
            m_connector(j, i, output_adjacency_collection);
        }
    }
}


void adjacency_weight_connector::create_list_bidir_connections(adjacency_weight_collection & output_adjacency_collection) {
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


void adjacency_weight_connector::create_grid_four_connections(adjacency_weight_collection & output_adjacency_collection) {
    const double conv_side_size = std::sqrt((double)output_adjacency_collection.size());
    if (conv_side_size - std::floor(conv_side_size) > 0) {
        throw std::runtime_error("Invalid number of nodes in the adjacency for the square grid structure.");
    }

    const size_t edge = (size_t) conv_side_size;
    create_grid_four_connections(edge, edge, output_adjacency_collection);
}


void adjacency_weight_connector::create_grid_four_connections(const size_t width, const size_t height, adjacency_weight_collection & output_adjacency_collection) {
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


void adjacency_weight_connector::create_grid_eight_connections(adjacency_weight_collection & output_adjacency_collection) {
    const double conv_side_size = std::sqrt((double)output_adjacency_collection.size());
    if (conv_side_size - std::floor(conv_side_size) > 0) {
        throw std::runtime_error("Invalid number of nodes in the adjacency for the square grid structure.");
    }

    const size_t edge = (size_t) conv_side_size;
    create_grid_four_connections(edge, edge, output_adjacency_collection);
}


void adjacency_weight_connector::create_grid_eight_connections(const size_t width, const size_t height, adjacency_weight_collection & output_adjacency_collection) {
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


void adjacency_weight_connector::create_default_connection(const size_t index1, const size_t index2, adjacency_weight_collection & output_adjacency_collection) {
    output_adjacency_collection.set_connection(index1, index2);
}


void adjacency_weight_connector::create_specify_connection(const size_t index1, const size_t index2, adjacency_weight_collection & output_adjacency_collection) {
    output_adjacency_collection.set_connection_weight(index1, index2, m_initializer());
}