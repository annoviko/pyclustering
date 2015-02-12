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
	epouchs = num_epochs;
	conn_type = type_conn;
	init_learn_rate = 0.1;

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
	awards = new std::vector<unsigned int>(size, 0);

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
			(*(*sqrt_distances)[j])[i] = distance;
		}
	}

	/* captured objects */
	capture_objects = new std::vector<std::vector<unsigned int> * >(size, NULL);
	for (unsigned int i = 0; i < size; i++) {
		(*capture_objects)[i] = new std::vector<unsigned int>();
	}

	/* connections */
	if (type_conn != som_conn_type::SOM_FUNC_NEIGHBOR) {
		create_connections(type_conn);
	}

	/* weights */
	create_initial_weights(type_init);
}

som::~som() {
	for (unsigned int i = 0; i < size; i++) {
		if (location != NULL)			{ delete (*location)[i];			}
		if (capture_objects != NULL)	{ delete (*capture_objects)[i];		}
		if (sqrt_distances != NULL)		{ delete (*sqrt_distances)[i];		}
		if (weights != NULL)			{ delete (*weights)[i];				}
		if (previous_weights != NULL)	{ delete (*previous_weights)[i];	}
		if (neighbors != NULL)			{ delete (*neighbors)[i];			}
	}

	if (location != NULL)				{ delete location;			location = NULL;			}
	if (capture_objects != NULL)		{ delete capture_objects;	capture_objects = NULL;		}
	if (awards != NULL)					{ delete awards;			awards = NULL;				}
	if (sqrt_distances != NULL)			{ delete sqrt_distances;	sqrt_distances = NULL;		}
	if (weights != NULL)				{ delete weights;			weights = NULL;				}
	if (previous_weights != NULL)		{ delete previous_weights;	previous_weights = NULL;	}
	if (neighbors != NULL)				{ delete neighbors;			neighbors = NULL;			}
}

void som::create_connections(const som_conn_type type) {
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

		if ( (type == som_conn_type::SOM_GRID_EIGHT) || (type == som_conn_type::SOM_GRID_FOUR) ) {
			if (upper_index >= 0) { 
				neuron_neighbors->push_back(upper_index); 
			}

			if (lower_index < (int) size) { 
				neuron_neighbors->push_back(lower_index); 
			}
		}

		if ( (type == som_conn_type::SOM_GRID_EIGHT) || (type == som_conn_type::SOM_GRID_FOUR) || (type == som_conn_type::SOM_HONEYCOMB) ) {
			if ( (left_index >= 0) && ( (int) std::floor((double) left_index / (double) cols) == node_row_index) ) {
				neuron_neighbors->push_back(left_index);
			}

			if ( (right_index >= 0) && ( (int) std::floor((double) right_index / (double) cols) == node_row_index) ) {
				neuron_neighbors->push_back(right_index);
			}
		}

		if (type == som_conn_type::SOM_GRID_EIGHT) {
			if ( (upper_left_index >= 0) && ( (int) std::floor((double) upper_left_index / (double) cols) == upper_row_index) ) {
				neuron_neighbors->push_back(upper_left_index);
			}

			if ( (upper_right_index >= 0) && ( (int) std::floor((double) upper_right_index / (double) cols) == upper_row_index) ) {
				neuron_neighbors->push_back(upper_right_index);
			}

			if ( (lower_left_index < (int) size) && ( (int) std::floor((double) lower_left_index / (double) cols) == lower_row_index) ) {
				neuron_neighbors->push_back(lower_left_index);
			}

			if ( (lower_right_index < (int) size) && ( (int) std::floor((double) lower_right_index / (double) cols) == lower_row_index) ) {
				neuron_neighbors->push_back(lower_right_index);
			}
		}

		if (type == som_conn_type::SOM_HONEYCOMB) {
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
				neuron_neighbors->push_back(upper_right_index);
			}

			if ( (lower_left_index < (int) size) && ( (int) std::floor(std::floor((double) lower_left_index / (double) cols)) == lower_row_index) ) {
				neuron_neighbors->push_back(lower_left_index);
			}

			if ( (lower_right_index < (int) size) && ( (int) std::floor(std::floor((double) lower_right_index / (double) cols)) == lower_row_index) ) {
				neuron_neighbors->push_back(lower_right_index);
			}
		}
	}
}

void som::create_initial_weights(const som_init_type type) {
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
		case som_init_type::SOM_UNIFORM_GRID: {
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

		case som_init_type::SOM_RANDOM_SURFACE: {
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

		case som_init_type::SOM_RANDOM_CENTROID: {
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

		case som_init_type::SOM_RANDOM: {
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

unsigned int som::competition(const std::vector<double> * pattern) const {
	unsigned int index = 0;
	double minimum = euclidean_distance_sqrt((*weights)[0], pattern);

	for (unsigned int i = 1; i < size; i++) {
		double candidate = euclidean_distance_sqrt((*weights)[i], pattern);
		if (candidate < minimum) {
			index = i;
			minimum = candidate;
		}
	}

	return index;
}

unsigned int som::adaptation(const unsigned int index_winner, const std::vector<double> * pattern) {
	unsigned int dimensions = (*weights)[0]->size();
	unsigned int number_adapted_neurons = 0;

	if (conn_type == som_conn_type::SOM_FUNC_NEIGHBOR) {
		for (unsigned int neuron_index = 0; neuron_index < size; neuron_index++) {
			double distance = (*(*sqrt_distances)[index_winner])[neuron_index];

			if (distance < local_radius) {
				double influence = std::exp( -( distance / (2.0 * local_radius) ) );

				std::vector<double> * neuron_weight = (*weights)[neuron_index];
				for (unsigned int dim = 0; dim < dimensions; dim++) {
					(*neuron_weight)[dim] += learn_rate * influence * ( (*pattern)[dim] - (*(*weights)[neuron_index])[dim] );
				}

				number_adapted_neurons++;
			}
		}
	}
	else {
		std::vector<double> * neuron_winner_weight = (*weights)[index_winner];
		for (unsigned int dim = 0; dim < dimensions; dim++) {
			(*neuron_winner_weight)[dim] += learn_rate * ( (*pattern)[dim] - (*neuron_winner_weight)[dim] );
		}

		std::vector<unsigned int> * winner_neighbors = (*neighbors)[index_winner];
		for (std::vector<unsigned int>::iterator neighbor_index = winner_neighbors->begin(); neighbor_index != winner_neighbors->end(); neighbor_index++) {
			double distance = (*(*sqrt_distances)[index_winner])[*neighbor_index];

			if (distance < local_radius) {
				double influence = std::exp( -( distance / (2.0 * local_radius) ) );

				std::vector<double> * neighbor_weight = (*weights)[*neighbor_index];
				for (unsigned int dim = 0; dim < dimensions; dim++) {
					(*neighbor_weight)[dim] += learn_rate * influence * ( (*pattern)[dim] - (*neighbor_weight)[dim] );
				}

				number_adapted_neurons++;
			}
		}
	}

	return number_adapted_neurons;
}

unsigned int som::train(bool autostop) {
	previous_weights = NULL;

	for (unsigned int epouch = 1; epouch < (epouchs + 1); epouch++) {
		/* Depression term of coupling */
		local_radius = std::pow( ( init_radius * std::exp(-( (double) epouch / (double) epouchs)) ), 2);
		learn_rate = init_learn_rate * std::exp(-( (double) epouch / (double) epouchs));

		/* Feature SOM 0003: Clear statistics */
		if (autostop == true) {
			for (unsigned int i = 0; i < size; i++) {
				(*awards)[i] = 0;
				(*capture_objects)[i]->clear();
			}
		}

		for (unsigned int i = 0; i < data->size(); i++) {
			/* Step 1: Competition */
			unsigned int index_winner = competition(&(*data)[i]);

			/* Step 2: Adaptation */
			adaptation(index_winner, &(*data)[i]);

			/* Update statistics */
			if ( (autostop == true) || (epouch == (epouchs - 1)) ) {
				(*awards)[index_winner]++;
				(*capture_objects)[index_winner]->push_back(i);
			}
		}

		/* Feature SOM 0003: Check requirement of stopping */
		if (autostop == true) {
			if (previous_weights == NULL) {
				previous_weights = new std::vector<std::vector<double> * >(size, NULL);

				unsigned int dimensions = (*weights)[0]->size();
				for (unsigned int i = 0; i < weights->size(); i++) {
					(*previous_weights)[i] = new std::vector<double>(dimensions, 0.0);

					std::copy((*weights)[i]->begin(), (*weights)[i]->end(), (*previous_weights)[i]->begin());
				}
			}
			else {
				double maximal_adaptation = calculate_maximal_adaptation();
				if (maximal_adaptation < adaptation_threshold) {
					return epouch;
				}

				for (unsigned int i = 0; i < weights->size(); i++) {
					std::copy((*weights)[i]->begin(), (*weights)[i]->end(), (*previous_weights)[i]->begin());
				}
			}
		}
	}

	return epouchs;
}

unsigned int som::simulate(const std::vector<double> * pattern) const {
	return competition(pattern);
}

double som::calculate_maximal_adaptation() const {
	unsigned int dimensions = (*data)[0].size();
	double maximal_adaptation = 0;

	for (unsigned int neuron_index = 0; neuron_index < size; neuron_index++) {
		std::vector<double> * neuron_weight = (*weights)[neuron_index];
		std::vector<double> * previous_neuron_weight = (*previous_weights)[neuron_index];

		for (unsigned int dim = 0; dim < dimensions; dim++) {
			double current_adaptation = (*previous_neuron_weight)[dim] - (*neuron_weight)[dim];

			if (current_adaptation < 0) { current_adaptation = -current_adaptation; }

			if (maximal_adaptation < current_adaptation) {
				maximal_adaptation = current_adaptation;
			}
		}
	}

	return maximal_adaptation;
}

unsigned int som::get_winner_number(void) const {
	unsigned int winner_number = 0;
	for (unsigned int i = 0; i < size; i++) {
		if ((*awards)[i] > 0) {
			winner_number++;
		}
	}

	return winner_number;
}

