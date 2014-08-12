#include "syncnet.h"
#include "support.h"

syncnet::syncnet(std::vector<std::vector<double> > * input_data, const double connectivity_radius, const initial_type initial_phases) :
sync_network(input_data->size(), 1, 0, 1, conn_type::NONE, initial_type::RANDOM_GAUSSIAN) {
	oscillator_locations = input_data;
	create_connections(connectivity_radius);
}

syncnet::~syncnet() {
	if (oscillator_locations != NULL) {
		delete oscillator_locations;
		oscillator_locations = NULL;
	}
}

void syncnet::create_connections(const double connectivity_radius) {
	double sqrt_connectivity_radius = connectivity_radius * connectivity_radius;

	for (unsigned int i = 0; i < num_osc; i++) {
		for (unsigned int j = 0; j < num_osc; j++) {
			double distance = euclidean_distance_sqrt( &(*oscillator_locations)[i], &(*oscillator_locations)[j] );

			if (distance <= connectivity_radius) {
				(*(*osc_conn)[i])[j] = 1;
				(*(*osc_conn)[j])[i] = 1;
			}
		}
	}
}

double syncnet::phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) {
	unsigned int index = *(unsigned int *) argv[1];
	unsigned int num_neighbors = 0;
	double phase = 0;

	for (unsigned int k = 0; k < num_osc; k++) {
		if (get_connection(index, k) > 0) {
			phase += std::sin( (*oscillators)[k].phase - teta );
			num_neighbors++;
		}
	}

	if (num_neighbors == 0) {
		num_neighbors = 1;
	}

	phase = phase * weight / num_neighbors;
	return phase;
}

dynamic_result * syncnet::process(const double order, const solve_type solver, const bool collect_dynamic) {
	return simulate_dynamic(order, solver, collect_dynamic);
}