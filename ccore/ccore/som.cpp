#include "som.h"
#include "support.h"

#include <cmath>
#include <climits>
#include <random>

som::som(std::vector<std::vector<double> > * input_data, const unsigned int num_rows, const unsigned int num_cols, const unsigned int num_epochs, const som_conn_type type_conn, const som_init_type type_init) {
	data = input_data;
	rows = num_rows;
	cols = num_cols;
	size = cols * rows;
	enophs = num_epochs;
	conn_type = type_conn;

	/* Feature SOM 0001: Predefined initial radius that depends on size of the network. */
	if ( (cols + rows) / 4.0 > 1.0 ) {
		init_radius = 2.0;
	}
	else if ( (cols > 1.0) && (rows > 1.0) ) {
		init_radius = 1.5;
	}
	else {
		init_radius = 1.0;
	}

	/* location */
	location = new std::vector<std::vector<double> * >(size, NULL);
	for (unsigned int i = 0; i < rows; i++) {
		for (unsigned int j = 0; j < cols; j++) {
			std::vector<double> * neuron_location = new std::vector<double>(2, 0);
			(*neuron_location)[0] = i;
			(*neuron_location)[1] = j;

			(*location)[i * cols + j] = neuron_location;
		}
	}

	/* awards */
	awards = new std::vector<std::vector<unsigned int> * >(size, NULL);
	for (unsigned int i = 0; i < size; i++) {
		std::vector<unsigned int> * neuron_awards = new std::vector<unsigned int>();
		(*awards)[i] = neuron_awards;
	}

	/* distances */
	sqrt_distances = new std::vector<std::vector<double> * >(size, NULL);
	for (unsigned int i = 0; i < size; i++) {
		std::vector<double> * column_distances = new std::vector<double>(size, 0);
		(*sqrt_distances)[i] = column_distances;
	}

	for (unsigned int i = 0; i < size; i++) {
		for (unsigned int j = i; j < size; j++) {
			double distance = euclidean_distance_sqrt((*location)[i], (*location)[j]);
			(*(*sqrt_distances)[i])[j] = distance;
			(*(*sqrt_distances)[i])[j] = distance;
		}
	}

	/* connections */
	if (type_conn != som_conn_type::FUNC_NEIGHBOR) {
		create_connections(type_conn);
	}

	/* weights */
	create_initial_weights(type_init);
}

som::~som() {
	/* locations */
	if (location != NULL) {
		for (unsigned int i = 0; i < size; i++) { delete (*location)[i]; }
	}
	delete location;
	location = NULL;
	
	/* awards */
	if (awards != NULL) {
		for (unsigned int i = 0; i < size; i++) { delete (*awards)[i]; }
	}
	delete awards;
	awards = NULL;

	/* distances */
	if (sqrt_distances != NULL) {
		for (unsigned int i = 0; i < size; i++) { delete (*sqrt_distances)[i]; }
	}
	delete sqrt_distances;
	sqrt_distances = NULL;
}

void som::create_connections(som_conn_type type) {
	neighbors = new std::vector<std::vector<unsigned int> * >(size, NULL);

	for (int index = 0; index < size; index++) {
		std::vector<unsigned int> * neuron_neighbors = new std::vector<unsigned int>();
		(*neighbors)[index] = neuron_neighbors;

		int upper_index = index - cols;
		int upper_left_index = index - cols - 1;
		int upper_right_index = index - cols + 1;

		int lower_index = index + cols;
		int lower_left_index = index + cols - 1;
		int lower_right_index = index + cols + 1;

		int left_index = index - 1;
		int right_index = index + 1;

		int node_row_index = (int) std::floor( (double) index / (double) cols );
		int upper_row_index = node_row_index - 1;
		int lower_row_index = node_row_index + 1;

		if ( (type == som_conn_type::GRID_EIGHT) || (type == som_conn_type::GRID_FOUR) ) {
			if (upper_index >= 0) { 
				neuron_neighbors->push_back(upper_index); 
			}

			if (lower_index < size) { 
				neuron_neighbors->push_back(lower_index); 
			}
		}

		if ( (type == som_conn_type::GRID_EIGHT) || (type == som_conn_type::GRID_FOUR) || (type == som_conn_type::HONEYCOMB) ) {
			if ( (left_index >= 0) && ( (int) std::floor((double) left_index / (double) cols) == node_row_index) ) {
				neuron_neighbors->push_back(left_index);
			}

			if ( (right_index >= 0) && ( (int) std::floor((double) right_index / (double) cols) == node_row_index) ) {
				neuron_neighbors->push_back(right_index);
			}
		}

		if (type == som_conn_type::GRID_EIGHT) {
			if ( (upper_left_index >= 0) && ( (int) std::floor((double) upper_left_index / (double) cols) == upper_row_index) ) {
				neuron_neighbors->push_back(upper_left_index);
			}

			if ( (upper_right_index >= 0) && ( (int) std::floor((double) upper_right_index / (double) cols) == upper_row_index) ) {
				neuron_neighbors->push_back(upper_right_index);
			}

			if ( (lower_left_index < size) && ( (int) std::floor((double) lower_left_index / (double) cols) == lower_row_index) ) {
				neuron_neighbors->push_back(lower_left_index);
			}

			if ( (lower_right_index < size) && ( (int) std::floor((double) lower_right_index / (double) cols) == lower_row_index) ) {
				neuron_neighbors->push_back(lower_right_index);
			}
		}

		if (type == som_conn_type::HONEYCOMB) {
			if ( (node_row_index % 2) == 0 ) {
				upper_left_index = index - cols;
				upper_right_index = index - cols + 1;

				lower_left_index = index + cols;
				lower_right_index = index + cols + 1;
			}
			else {
				upper_left_index = index - cols - 1;
				upper_right_index = index - cols;

				lower_left_index = index + cols - 1;
				lower_right_index = index + cols;
			}

			if ( (upper_left_index >= 0) && ( (int) std::floor(std::floor((double) upper_left_index / (double) cols)) == upper_row_index) ) {
				neuron_neighbors->push_back(upper_left_index);
			}

			if ( (upper_right_index >= 0) && ( (int) std::floor(std::floor((double) upper_right_index / (double) cols)) == upper_row_index) ) {
				neuron_neighbors->push_back(upper_left_index);
			}

			if ( (lower_left_index < size) && ( (int) std::floor(std::floor((double) lower_left_index / (double) cols)) == lower_row_index) ) {
				neuron_neighbors->push_back(upper_left_index);
			}

			if ( (lower_right_index < size) && ( (int) std::floor(std::floor((double) lower_right_index / (double) cols)) == lower_row_index) ) {
				neuron_neighbors->push_back(upper_left_index);
			}
		}
	}
}

void som::create_initial_weights(som_init_type type) {
	unsigned int dimension = (*data)[0].size();

	weights = new std::vector<std::vector<double> * >(size, NULL);
	for (unsigned int i = 0; i < size; i++) {
		std::vector<double> * neuron_weight = new std::vector<double>(dimension, 0);
		(*weights)[i] = neuron_weight;
	}

	std::vector<double> maximum_value_dimension(dimension, -std::numeric_limits<double>::max());
	std::vector<double> minimum_value_dimension(dimension, std::numeric_limits<double>::max());

	for (unsigned int i = 0; i < data->size(); i++) {
		for (unsigned int dim = 0; dim < dimension; dim++) {
			if (maximum_value_dimension[dim] < (*data)[i][dim]) {
				maximum_value_dimension[dim] = (*data)[i][dim];
			}

			if (minimum_value_dimension[dim] > (*data)[i][dim]) {
				minimum_value_dimension[dim] = (*data)[i][dim];
			}
		}
	}

	std::vector<double> width_value_dimension(dimension, 0);
	std::vector<double> center_value_dimension(dimension, 0);

	for (unsigned int dim = 0; dim < dimension; dim++) {
		width_value_dimension[dim] = maximum_value_dimension[dim] - minimum_value_dimension[dim];
		center_value_dimension[dim] = (maximum_value_dimension[dim] + minimum_value_dimension[dim]) / 2.0;
	}

	double step_x = center_value_dimension[0];
	double step_y = center_value_dimension[1];

	if (rows > 1) { step_x = width_value_dimension[0] / (rows - 1.0); }
	if (cols > 1) { step_y = width_value_dimension[1] / (cols - 1.0); }

	/* generate weights (topological coordinates) */
	std::random_device device;
	std::default_random_engine generator(device());

	switch (type) {
		/* Feature SOM 0002: Uniform grid. */
		case som_init_type::UNIFORM_GRID: {
			for (unsigned int i = 0; i < size; i++) {
				std::vector<double> * neuron_location = (*location)[i];
				std::vector<double> * neuron_weight = (*weights)[i];

				for (unsigned int dim = 0; dim < dimension; dim++) {
					if (dim == 0) {
						if (rows > 1) {
							(*neuron_weight)[dim] = minimum_value_dimension[dim] + step_x * (*neuron_location)[dim];
						}
						else {
							(*neuron_weight)[dim] = center_value_dimension[dim];
						}
					}
					else if (dim == 1) {
						if (cols > 1) {
							(*neuron_weight)[dim] = minimum_value_dimension[dim] + step_y * (*neuron_location)[dim];
						}
						else {
							(*neuron_weight)[dim] = center_value_dimension[dim];
						}
					}
					else {
						(*neuron_weight)[dim] = center_value_dimension[dim];
					}
				}
			}

			break;
		}

		case som_init_type::RANDOM_SURFACE: {
			/* Random weights at the full surface. */
			for (unsigned int i = 0; i < size; i++) {
				std::vector<double> * neuron_weight = (*weights)[i];

				for (unsigned int dim = 0; dim < dimension; dim++) {
					std::uniform_real_distribution<double> position_distribution(minimum_value_dimension[dim], maximum_value_dimension[dim]);
					(*neuron_weight)[dim] = position_distribution(generator);
				}
			}

			break;
		}

		case som_init_type::RANDOM_CENTROID: {
			/* Random weights at the center of input data. */
			std::uniform_real_distribution<double> position_distribution(-0.5, 0.5);

			for (unsigned int i = 0; i < size; i++) {
				std::vector<double> * neuron_weight = (*weights)[i];

				for (unsigned int dim = 0; dim < dimension; dim++) {
					(*neuron_weight)[dim] = position_distribution(generator);
				}
			}

			break;
		}

		case som_init_type::RANDOM: {
			/* Random weights of input data. */
			std::uniform_real_distribution<double> position_distribution(-0.5, 0.5);

			for (unsigned int i = 0; i < size; i++) {
				std::vector<double> * neuron_weight = (*weights)[i];

				for (unsigned int dim = 0; dim < dimension; dim++) {
					(*neuron_weight)[dim] = position_distribution(generator);
				}
			}

			break;
		}
	}
}