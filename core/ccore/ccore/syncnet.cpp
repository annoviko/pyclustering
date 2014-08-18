#include "syncnet.h"
#include "support.h"

#include <limits>

/***********************************************************************************************
 *
 * @brief   Contructor of the adapted oscillatory network SYNC for cluster analysis.
 *
 * @param   (in) input_data            - input data for clustering.
 * @param   (in) connectivity_radius   - connectivity radius between points.
 * @param   (in) enable_conn_weight    - if True - enable mode when strength between oscillators 
 *                                       depends on distance between two oscillators. Otherwise
 *                                       all connection between oscillators have the same strength.
 * @param   (in) initial_phases        - type of initialization of initial phases of oscillators.
 *
 ***********************************************************************************************/
syncnet::syncnet(std::vector<std::vector<double> > * input_data, const double connectivity_radius, const bool enable_conn_weight, const initial_type initial_phases) :
sync_network(input_data->size(), 1, 0, 1, conn_type::NONE, initial_type::RANDOM_GAUSSIAN) {
	oscillator_locations = input_data;
	create_connections(connectivity_radius, enable_conn_weight);
}

/***********************************************************************************************
 *
 * @brief   Default destructor.
 *
 ***********************************************************************************************/
syncnet::~syncnet() {
	if (oscillator_locations != NULL) {
		delete oscillator_locations;
		oscillator_locations = NULL;
	}

	if (distance_conn_weights != NULL) {
		delete distance_conn_weights;
		distance_conn_weights = NULL;
	}
}

/***********************************************************************************************
 *
 * @brief   Create connections between oscillators in line with input radius of connectivity.
 *
 * @param   (in) connectivity_radius  - connectivity radius between oscillators.
 * @param   (in) enable_conn_weight   - if True - enable mode when strength between oscillators 
 *                                      depends on distance between two oscillators. Otherwise
 *                                      all connection between oscillators have the same strength.
 *
 ***********************************************************************************************/
void syncnet::create_connections(const double connectivity_radius, const bool enable_conn_weight) {
	double sqrt_connectivity_radius = connectivity_radius * connectivity_radius;

	if (enable_conn_weight == true) {
		std::vector<double> instance(num_osc, 0);
		distance_conn_weights = new std::vector<std::vector<double> >(num_osc, instance);
	}
	else {
		distance_conn_weights = NULL;
	}

	double maximum_distance = 0;
	double minimum_distance = std::numeric_limits<double>::max();

	for (unsigned int i = 0; i < num_osc; i++) {
		for (unsigned int j = i + 1; j < num_osc; j++) {
			double distance = euclidean_distance_sqrt( &(*oscillator_locations)[i], &(*oscillator_locations)[j] );

			if (distance <= sqrt_connectivity_radius) {
				(*(*osc_conn)[i])[j] = 1;
				(*(*osc_conn)[j])[i] = 1;
			}

			if (enable_conn_weight == true) {
				(*distance_conn_weights)[i][j] = distance;
				(*distance_conn_weights)[j][i] = distance;

				if (distance > maximum_distance) {
					maximum_distance = distance;
				}

				if (distance < maximum_distance) {
					maximum_distance = distance;
				}
			}
		}
	}

	if (enable_conn_weight == true) {
		double multiplier = 1;
		double subtractor = 0;

		if (maximum_distance != minimum_distance) {
			multiplier = maximum_distance - minimum_distance;
			subtractor = minimum_distance;
		}

		for (unsigned int i = 0; i < num_osc; i++) {
			for (unsigned int j = i + 1; j < num_osc; j++) {
				double value_weight = ((*distance_conn_weights)[i][j] - subtractor) / multiplier;

				(*distance_conn_weights)[i][j] = value_weight;
				(*distance_conn_weights)[j][i] = value_weight;
			}
		}
	}
}

/***********************************************************************************************
 *
 * @brief   Adapter for solving differential equation for calculation of oscillator phase.
 *
 * @param   (in) t      - current value of phase.
 * @param   (in) teta   - time (can be ignored). 
 * @param   (in) argv   - pointer to the network 'argv[0]' and index of oscillator whose phase 
 *                        represented by argument teta 'argv[1]'.
 *
 * @return  Return new value of phase of oscillator that is specified in index 'argv[1]'.
 *
 ***********************************************************************************************/
double syncnet::adapter_phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) {
	return ((syncnet *) argv[0])->phase_kuramoto(t, teta, argv);
}

/***********************************************************************************************
 *
 * @brief   Overrided method for calculation of oscillator phase.
 *
 * @param   (in) t      - current value of phase.
 * @param   (in) teta   - time (can be ignored). 
 * @param   (in) argv   - index of oscillator whose phase represented by argument teta.
 *
 * @return  Return new value of phase of oscillator with index 'argv'.
 *
 ***********************************************************************************************/
double syncnet::phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) {
	unsigned int index = *(unsigned int *) argv[1];
	unsigned int num_neighbors = 0;
	double phase = 0;

	/* Avoid a lot of checking of this condition in the loop */
	if (distance_conn_weights != NULL) {
		for (unsigned int k = 0; k < num_osc; k++) {
			if (get_connection(index, k) > 0) {
				phase += (*distance_conn_weights)[index][k] * std::sin( (*oscillators)[k].phase - teta );
				num_neighbors++;
			}
		}
	}
	else {
		for (unsigned int k = 0; k < num_osc; k++) {
			if (get_connection(index, k) > 0) {
				phase += std::sin( (*oscillators)[k].phase - teta );
				num_neighbors++;
			}
		}	
	}

	if (num_neighbors == 0) {
		num_neighbors = 1;
	}

	phase = phase * weight / num_neighbors;
	return phase;
}

/***********************************************************************************************
 *
 * @brief   Network is trained via achievement sync state between the oscillators using the 
 *          radius of coupling.
 *
 * @param   (in) order             - order of synchronization that is used as indication for 
 *                                   stopping processing.
 * @param   (in) solver            - specified type of solving diff. equation. 
 * @param   (in) collect_dynamic   - specified requirement to collect whole dynamic of the network.
 *
 * @return  Return last values of simulation time and phases of oscillators if 
 *          collect_dynamic is False, and whole dynamic if collect_dynamic is True.
 *
 ***********************************************************************************************/
std::vector< std::vector<sync_dynamic> * > * syncnet::process(const double order, const solve_type solver, const bool collect_dynamic) {
	return simulate_dynamic(order, solver, collect_dynamic);
}
