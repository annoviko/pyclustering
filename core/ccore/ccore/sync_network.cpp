#include "sync_network.h"
#include "support.h"

#include <cmath>
#include <random>
#include <complex>

sync_network::sync_network(const unsigned int size, const double weight_factor, const double frequency_factor, const conn_type connection_type, const initial_type initial_phases) :
	network(size, connection_type) 
{
	num_osc = size;
	weight = weight_factor;

	cluster = 1;

	std::default_random_engine				generator;
	std::uniform_real_distribution<double>	phase_distribution(0.0, 2.0 * pi());
	std::uniform_real_distribution<double>	frequency_distribution(0.0, 1.0);
	
	oscillators = new std::vector<sync_oscillator>();
	for (unsigned int index = 0; index < size; index++) {
		sync_oscillator oscillator_context;

		switch(initial_phases) {
		case initial_type::RANDOM_GAUSSIAN:
			oscillator_context.phase = phase_distribution(generator);
			break;
		case initial_type::EQUIPARTITION:
			oscillator_context.phase = (2 * pi() / (size - 1) * index);
			break;
		default:
			throw std::runtime_error("Unknown type of initialization");
		}

		oscillator_context.frequency = frequency_distribution(generator) * frequency_factor;
		oscillators->push_back(oscillator_context);
	}
}

sync_network::~sync_network() {
	if (oscillators != NULL) {
		delete oscillators;
		oscillators = NULL;
	}
}

double sync_network::sync_order() const {
	double exp_amount = 0;
	double average_phase = 0;

	for (unsigned int index = 0; index < num_osc; index++) {
		exp_amount += std::exp( std::abs( std::complex<double>(0, 1) * (*oscillators)[index].phase ) );
		average_phase += (*oscillators)[index].phase;
	}

	exp_amount /= num_osc;
	average_phase = std::exp( std::abs( std::complex<double>(0, 1) * (average_phase / num_osc) ) );

	return std::abs(average_phase) / std::abs(exp_amount);
}

double sync_network::sync_local_order() const {
	double			exp_amount = 0;
	unsigned int	number_neighbors = 0;

	for (unsigned int i = 0; i < num_osc; i++) {
		for (unsigned int j = 0; j < num_osc; j++) {
			if (get_connection(i, j) > 0) {
				exp_amount += std::exp( -std::abs( (*oscillators)[j].phase - (*oscillators)[i].phase ) );
				number_neighbors++;
			}
		}
	}

	if (number_neighbors == 0) {
		number_neighbors = 1;
	}

	return exp_amount / (double) number_neighbors;
}

double sync_network::phase_kuramoto(const double teta, const double t, const std::vector<double> & argv) {
	unsigned int index = (unsigned int) argv[0];
	double phase = 0;

	for (unsigned int k = 0; k < num_osc; k++) {
		if (get_connection(index, k) > 0) {
			phase += std::sin(cluster * ( (*oscillators)[k].phase - teta ) );
		}
	}

	phase = (*oscillators)[index].frequency + (phase * weight / num_osc);
	return phase;
}

std::vector< std::vector<unsigned int> * > * sync_network::allocate_sync_ensembles(const double tolerance) const {	
	std::vector< std::vector<unsigned int> * > * clusters = new std::vector< std::vector<unsigned int> * >();
	clusters->push_back(new std::vector<unsigned int> ());
	
	if (num_osc > 0) {
		(*clusters)[0]->push_back(0);
	}

	for (unsigned int i = 1; i < num_osc; i++) {
		bool cluster_allocated = false;
		for (std::vector< std::vector<unsigned int> * >::const_iterator cluster = clusters->begin(); cluster != clusters->end(); cluster++) {
			for (std::vector<unsigned int>::const_iterator neuron_index = (*cluster)->begin(); neuron_index != (*cluster)->end(); neuron_index++) {
				if ( ( (*oscillators)[i].phase < ((*oscillators)[*neuron_index].phase + tolerance) ) && ( (*oscillators)[i].phase > ((*oscillators)[*neuron_index].phase - tolerance) ) ) {
					cluster_allocated = true;
					(*cluster)->push_back(i);
					break;
				}
			}

			if (cluster_allocated == true) {
				break;
			}
		}

		if (cluster_allocated == false) {
			std::vector<unsigned int> * allocated_cluster = new std::vector<unsigned int>();
			allocated_cluster->push_back(i);
		}
	}

	return clusters;
}

std::vector< std::vector<sync_dynamic> * > * sync_network::simulate(const unsigned int steps, const double time, const solve_type solver, const bool collect_dynamic) {
	return simulate_static(steps, time, solver, collect_dynamic);
}

std::vector< std::vector<sync_dynamic> * > * sync_network::simulate_static(const unsigned int steps, const double time, const solve_type solver, const bool collect_dynamic) {
	std::vector< std::vector<sync_dynamic> * > * dynamic = new std::vector< std::vector<sync_dynamic> * >;

	const double step = time / (double) steps;
	const double int_step = step / 10.0;

	for (double cur_time = 0; cur_time < time; cur_time += step) {
		calculate_phases(solver, cur_time, step, int_step);

		if (collect_dynamic == true) {
			std::vector<sync_dynamic> * network_dynamic = new std::vector<sync_dynamic>();

			for (unsigned int index = 0; index < num_osc; index++) {
				sync_dynamic oscillator_dynamic;
				oscillator_dynamic.phase = (*oscillators)[index].phase;
				oscillator_dynamic.time = cur_time;

				network_dynamic->push_back(oscillator_dynamic);
			}

			dynamic->push_back(network_dynamic);
		}
	}

	return dynamic;
}

void sync_network::calculate_phases(const solve_type solver, const double t, const double step, const double int_step) {
	std::vector<double> * next_phases = new std::vector<double> (num_osc, 0);
	std::vector<double> argv(1, 0);

	for (unsigned int index = 0; index < num_osc; index++) {
		argv[0] = index;

		switch(solver) {
			case solve_type::FAST: {
				double result = (*oscillators)[index].phase + phase_kuramoto((*oscillators)[index].phase, t, argv);
				(*next_phases)[index] = phase_normalization(result);
				break;
			}
			case solve_type::RK4: {
				throw std::runtime_error("RK4 is not supported");
			}
			default: {
				throw std::runtime_error("Unknown type of solver");
			}
		}
	}

	/* store result */
	for (unsigned int index = 0; index < num_osc; index++) {
		(*oscillators)[index].phase = (*next_phases)[index];
	}

	delete next_phases;
}

double sync_network::phase_normalization(const double teta) {
	double norm_teta = teta;

	while ( (norm_teta > 2.0 * pi()) || (norm_teta < 0) ) {
		if (norm_teta > 2.0 * pi()) {
			norm_teta -= 2.0 * pi();
		}
		else {
			norm_teta += 2.0 * pi();
		}
	}

	return norm_teta;
}