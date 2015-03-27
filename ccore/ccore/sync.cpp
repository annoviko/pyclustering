/**************************************************************************************************************

Neural Network: Oscillatory Neural Network based on Kuramoto model

Based on article description:
 - A.Arenas, Y.Moreno, C.Zhou. Synchronization in complex networks. 2008.
 - X.B.Lu. Adaptive Cluster Synchronization in Coupled Phase Oscillators. 2009.
 - X.Lou. Adaptive Synchronizability of Coupled Oscillators With Switching. 2012.
 - A.Novikov, E.Benderskaya. Oscillatory Neural Networks Based on the Kuramoto Model. 2014.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

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

#include "sync.h"
#include "support.h"

#include <iostream>
#include <cmath>
#include <random>
#include <complex>
#include <stdexcept>
#include <chrono>


sync_network::sync_network(const unsigned int size, const double weight_factor, const double frequency_factor, const conn_type connection_type, const initial_type initial_phases) :
	network(size, connection_type) 
{
	weight = weight_factor;

	std::random_device			device;
	std::default_random_engine		generator(device());
	std::uniform_real_distribution<double>	phase_distribution(0.0, 2.0 * pi());
	std::uniform_real_distribution<double>	frequency_distribution(0.0, 1.0);

	sync_oscillator oscillator_context;
	oscillators = new std::vector<sync_oscillator>(size, oscillator_context);

	for (unsigned int index = 0; index < size; index++) {
		switch(initial_phases) {
		case initial_type::RANDOM_GAUSSIAN:
			oscillator_context.phase = phase_distribution(generator);
			break;
		case initial_type::EQUIPARTITION:
			oscillator_context.phase = (pi() / size * index);
			break;
		default:
			throw std::runtime_error("Unknown type of initialization");
		}

		oscillator_context.frequency = frequency_distribution(generator) * frequency_factor;
		(*oscillators)[index] = oscillator_context;
	}

	sync_ensembles = NULL;
}


sync_network::~sync_network() {
	if (oscillators != NULL) {
		delete oscillators;
		oscillators = NULL;
	}

	free_sync_ensembles();
}


void sync_network::free_sync_ensembles() {
	if (sync_ensembles != NULL) {
		for (std::vector< std::vector<unsigned int> * >::const_iterator iter = sync_ensembles->begin(); iter != sync_ensembles->end(); iter++) {
			if (*iter != NULL) {
				delete *iter;
			}
		}

		delete sync_ensembles;
		sync_ensembles = NULL;
	}
}


double sync_network::sync_order() const {
	double exp_amount = 0;
	double average_phase = 0;

	for (unsigned int index = 0; index < size(); index++) {
		exp_amount += std::exp( std::abs( std::complex<double>(0, 1) * (*oscillators)[index].phase ) );
		average_phase += (*oscillators)[index].phase;
	}

	exp_amount /= size();
	average_phase = std::exp( std::abs( std::complex<double>(0, 1) * (average_phase / size()) ) );

	return std::abs(average_phase) / std::abs(exp_amount);
}


double sync_network::sync_local_order() const {
	double			exp_amount = 0.0;
	unsigned int	number_neighbors = 0;

	for (unsigned int i = 0; i < size(); i++) {
		for (unsigned int j = 0; j < size(); j++) {
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


double sync_network::adapter_phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) {
	return ((sync_network *) argv[0])->phase_kuramoto(t, teta, argv);
}


double sync_network::phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) {
	unsigned int index = *(unsigned int *) argv[1];
	double phase = 0;

	for (unsigned int k = 0; k < size(); k++) {
		if (get_connection(index, k) > 0) {
			phase += std::sin((*oscillators)[k].phase - teta);
		}
	}

	phase = (*oscillators)[index].frequency + (phase * weight / size());
	return phase;
}


std::vector< std::vector<unsigned int> * > * sync_network::allocate_sync_ensembles(const double tolerance) {	
	if (sync_ensembles == NULL) {
		sync_ensembles = new std::vector< std::vector<unsigned int> * >();
	}
	else {
		return sync_ensembles;
	}

	sync_ensembles->push_back(new std::vector<unsigned int> ());
	
	if (size() > 0) {
		(*sync_ensembles)[0]->push_back(0);
	}

	for (unsigned int i = 1; i < size(); i++) {
		bool cluster_allocated = false;

		std::vector< std::vector<unsigned int> * >::iterator last_sync_ensemble_element = sync_ensembles->end();
		for (std::vector< std::vector<unsigned int> * >::const_iterator cluster = sync_ensembles->begin(); cluster != last_sync_ensemble_element; cluster++) {

			std::vector<unsigned int>::iterator last_cluster_element = (*cluster)->end();
			for (std::vector<unsigned int>::const_iterator neuron_index = (*cluster)->begin(); neuron_index != last_cluster_element; neuron_index++) {
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
			sync_ensembles->push_back(allocated_cluster);
		}
	}

	return sync_ensembles;
}


std::vector< std::vector<sync_dynamic> * > * sync_network::simulate_static(const unsigned int steps, const double time, const solve_type solver, const bool collect_dynamic) {
	free_sync_ensembles();

	std::vector< std::vector<sync_dynamic> * > * dynamic = new std::vector< std::vector<sync_dynamic> * >;

	const double step = time / (double) steps;
	const double int_step = step / 10.0;

	for (double cur_time = 0; cur_time < time; cur_time += step) {
		calculate_phases(solver, cur_time, step, int_step);

		store_dynamic(dynamic, cur_time, collect_dynamic);
	}

	return dynamic;
}


std::vector< std::vector<sync_dynamic> * > * sync_network::simulate_dynamic(const double order, const solve_type solver, const bool collect_dynamic, const double step, const double step_int, const double threshold_changes) {
	free_sync_ensembles();

	double previous_order = 0.0;
	double current_order = sync_local_order();

	std::vector< std::vector<sync_dynamic> * > * dynamic = new std::vector< std::vector<sync_dynamic> * >();

	for (double time_counter = 0; current_order < order; time_counter += step) {
		calculate_phases(solver, time_counter, step, step_int);

		store_dynamic(dynamic, time_counter, collect_dynamic);

		previous_order = current_order;
		current_order = sync_local_order();

		if (std::abs(current_order - previous_order) < threshold_changes) {
			std::cout << "Warning: sync_network::simulate_dynamic - simulation is aborted due to low level of convergence rate (order = " << current_order << ")." << std::endl;
			break;
		}
	}

	return dynamic;
}


void sync_network::store_dynamic(std::vector< std::vector<sync_dynamic> * > * dynamic, const double time, const bool collect_dynamic) const {
	std::vector<sync_dynamic> * network_dynamic = new std::vector<sync_dynamic>();

	for (unsigned int index = 0; index < size(); index++) {
		sync_dynamic oscillator_dynamic;
		oscillator_dynamic.phase = (*oscillators)[index].phase;
		oscillator_dynamic.time = time;

		network_dynamic->push_back(oscillator_dynamic);
	}
	
	if (collect_dynamic == false) {
		dynamic->clear();
	}

	dynamic->push_back(network_dynamic);
}


void sync_network::calculate_phases(const solve_type solver, const double t, const double step, const double int_step) {
	std::vector<double> * next_phases = new std::vector<double> (size(), 0);
	std::vector<void *> argv(2, NULL);

	argv[0] = (void *) this;

	unsigned int number_int_steps = (unsigned int) (step / int_step);

	for (unsigned int index = 0; index < size(); index++) {
		argv[1] = (void *) &index;

		switch(solver) {
			case solve_type::FAST: {
				double result = (*oscillators)[index].phase + phase_kuramoto(t, (*oscillators)[index].phase, argv);
				(*next_phases)[index] = phase_normalization(result);
				break;
			}
			case solve_type::RK4: {
				std::vector<differential_result> * result = rk4(&sync_network::adapter_phase_kuramoto, (*oscillators)[index].phase, t, t + step, number_int_steps, false, argv);
				(*next_phases)[index] = phase_normalization( (*result)[0].value );

				delete result;
				break;
			}
			case solve_type::RKF45: {
				std::vector<differential_result> * result = rkf45(&sync_network::adapter_phase_kuramoto, (*oscillators)[index].phase, t, t + step, 0.00001, false, argv);
				(*next_phases)[index] = phase_normalization( (*result)[0].value );

				delete result;
				break;
			}
			default: {
				throw std::runtime_error("Unknown type of solver");
			}
		}
	}

	/* store result */
	for (unsigned int index = 0; index < size(); index++) {
		(*oscillators)[index].phase = (*next_phases)[index];
	}

	delete next_phases;
}


double sync_network::phase_normalization(const double teta) {
	double norm_teta = teta;

	while ( (norm_teta > 2.0 * pi()) || (norm_teta < 0.0) ) {
		if (norm_teta > 2.0 * pi()) {
			norm_teta -= 2.0 * pi();
		}
		else {
			norm_teta += 2.0 * pi();
		}
	}

	return norm_teta;
}


dynamic_result * sync_network::convert_dynamic_representation(std::vector< std::vector<sync_dynamic> * > * dynamic) {
	dynamic_result * result = new dynamic_result();

	result->size_dynamic = dynamic->size();
	result->size_network = ((*dynamic)[0])->size();
	result->times = new double[result->size_dynamic];
	result->dynamic = new double * [result->size_dynamic];

	for (unsigned int index_dynamic = 0; index_dynamic < result->size_dynamic; index_dynamic++) {
		result->times[index_dynamic] = (*(*dynamic)[index_dynamic])[0].time;
		result->dynamic[index_dynamic] = new double[result->size_network];
		for (unsigned int index_neuron = 0; index_neuron < result->size_network; index_neuron++) {
			result->dynamic[index_dynamic][index_neuron] = (*(*dynamic)[index_dynamic])[index_neuron].phase;
		}

	}

	return result;
}
