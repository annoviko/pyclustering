/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
*/

#include "nnet/sync.hpp"

#include <iostream>
#include <cmath>
#include <random>
#include <complex>
#include <stdexcept>
#include <chrono>

#include "container/adjacency_bit_matrix.hpp"
#include "container/adjacency_connector.hpp"
#include "container/adjacency_matrix.hpp"

#include "differential/runge_kutta_4.hpp"
#include "differential/runge_kutta_fehlberg_45.hpp"

#include "utils.hpp"


using namespace container;
using namespace differential;


const size_t sync_network::MAXIMUM_MATRIX_REPRESENTATION_SIZE = 4096;


sync_network::sync_network(const size_t size, const double weight_factor, const double frequency_factor, const connection_t connection_type, const initial_type initial_phases) {
    initialize(size, weight_factor, frequency_factor, connection_type, 0, 0, initial_phases);
}


sync_network::sync_network(const size_t size, const double weight_factor,  const double frequency_factor, const connection_t connection_type, const size_t height, const size_t width, const initial_type initial_phases) {
    initialize(size, weight_factor, frequency_factor, connection_type, height, width, initial_phases);
}


sync_network::~sync_network(void) { }


void sync_network::initialize(const size_t size, const double weight_factor, const double frequency_factor, const connection_t connection_type, const size_t height, const size_t width, const initial_type initial_phases) {
    m_oscillators = std::vector<sync_oscillator>(size, sync_oscillator());
    
    if (size > MAXIMUM_MATRIX_REPRESENTATION_SIZE) {
        m_connections = std::shared_ptr<adjacency_collection>(new adjacency_bit_matrix(size));
    }
    else {
        m_connections = std::shared_ptr<adjacency_matrix>(new adjacency_matrix(size));
    }

    adjacency_connector<adjacency_collection> connector;

    if ((height != 0) && (width != 0)) {
        connector.create_grid_structure(connection_type, width, height, *m_connections);
    }
    else {
        connector.create_structure(connection_type, *m_connections);
    }

    weight = weight_factor;

    m_callback_solver = &sync_network::adapter_phase_kuramoto;

    std::random_device                      device;
    std::default_random_engine              generator(device());
    std::uniform_real_distribution<double>	phase_distribution(0.0, 2.0 * pi());
    std::uniform_real_distribution<double>	frequency_distribution(0.0, 1.0);

    for (unsigned int index = 0; index < size; index++) {
        sync_oscillator & oscillator_context = m_oscillators[index];

        switch (initial_phases) {
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
    }
}


double sync_network::sync_order() const {
	double exp_amount = 0;
	double average_phase = 0;

	for (unsigned int index = 0; index < size(); index++) {
		exp_amount += std::exp( std::abs( std::complex<double>(0, 1) * m_oscillators[index].phase ) );
		average_phase += m_oscillators[index].phase;
	}

	exp_amount /= size();
	average_phase = std::exp( std::abs( std::complex<double>(0, 1) * (average_phase / size()) ) );

	return std::abs(average_phase) / std::abs(exp_amount);
}


double sync_network::sync_local_order() const {
	double			exp_amount = 0.0;
	double			number_neighbors = 0;

	for (unsigned int i = 0; i < size(); i++) {
        std::vector<size_t> neighbors;
        m_connections->get_neighbors(i, neighbors);

        for (std::vector<size_t>::const_iterator iter_index = neighbors.begin(); iter_index != neighbors.cend(); iter_index++) {
			unsigned int index_neighbor = *(iter_index);
			exp_amount += std::exp( -std::abs( m_oscillators[index_neighbor].phase - m_oscillators[i].phase ) );	
		}

		number_neighbors += neighbors.size();
	}

	if (number_neighbors == 0.0) {
		number_neighbors = 1.0;
	}
	
	return exp_amount / number_neighbors;
}


void sync_network::set_callback_solver(sync_callback_solver solver) {
    m_callback_solver = solver;
}


void sync_network::adapter_phase_kuramoto(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
	outputs.resize(1);
	outputs[0] = ((sync_network *) argv[0])->phase_kuramoto(t, inputs[0], argv);
}


double sync_network::phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) const {
    unsigned int index = *(unsigned int *) argv[1];
	double phase = 0.0;

    std::vector<size_t> neighbors;
    m_connections->get_neighbors(index, neighbors);

    for (std::vector<size_t>::const_iterator index_iterator = neighbors.cbegin(); index_iterator != neighbors.cend(); index_iterator++) {
		unsigned int index_neighbor = (*index_iterator);
		phase += std::sin(m_oscillators[index_neighbor].phase - teta);
	}

	phase = m_oscillators[index].frequency + (phase * weight / size());
	return phase;
}


void sync_network::simulate_static(const unsigned int steps, const double time,  const solve_type solver, const bool collect_dynamic, sync_dynamic & output_dynamic) {
    output_dynamic.clear();

    const double step = time / (double) steps;
    const double int_step = step / 10.0;

    store_dynamic(0.0, collect_dynamic, output_dynamic);	/* store initial state */

    for (double cur_time = step; cur_time < (time + step); cur_time += step) {
        calculate_phases(solver, cur_time, step, int_step);

        store_dynamic(cur_time, collect_dynamic, output_dynamic);	/* store initial state */
    }
}


void sync_network::simulate_dynamic(const double order, const double step, const solve_type solver, const bool collect_dynamic, sync_dynamic & output_dynamic) {
	output_dynamic.clear();

	double previous_order = 0.0;
	double current_order = sync_local_order();

	double integration_step = step / 10;

	store_dynamic(0, collect_dynamic, output_dynamic);     /* store initial state */

	for (double time_counter = step; current_order < order; time_counter += step) {
		calculate_phases(solver, time_counter, step, integration_step);

		store_dynamic(time_counter, collect_dynamic, output_dynamic);

		previous_order = current_order;
		current_order = sync_local_order();

		if (std::abs(current_order - previous_order) < 0.000001) {
			// std::cout << "Warning: sync_network::simulate_dynamic - simulation is aborted due to low level of convergence rate (order = " << current_order << ")." << std::endl;
			break;
		}
	}
}


void sync_network::store_dynamic(const double time, const bool collect_dynamic, sync_dynamic & output_dynamic) const {
	sync_network_state state(size());

	for (unsigned int index = 0; index < size(); index++) {
		state.m_phase[index] = m_oscillators[index].phase;
	}

	state.m_time = time;
	
	if ( (collect_dynamic == false) && (!output_dynamic.empty()) ) {
		output_dynamic[0] = state;
	}
	else {
		output_dynamic.push_back(state);
	}
}


void sync_network::calculate_phases(const solve_type solver, const double t, const double step, const double int_step) {
	std::vector<double> next_phases(size(), 0);
	std::vector<void *> argv(2, NULL);

	argv[0] = (void *) this;

	unsigned int number_int_steps = (unsigned int) (step / int_step);

	for (unsigned int index = 0; index < size(); index++) {
		argv[1] = (void *) &index;

		switch(solver) {
			case solve_type::FAST: {
				double result = m_oscillators[index].phase + phase_kuramoto(t, m_oscillators[index].phase, argv);
				next_phases[index] = phase_normalization(result);
				break;
			}
			case solve_type::RK4: {
				differ_state<double> inputs(1, m_oscillators[index].phase);
				differ_result<double> outputs;

				runge_kutta_4(m_callback_solver, inputs, t, t + step, number_int_steps, false, argv, outputs);
				next_phases[index] = phase_normalization( outputs[0].state[0] );

				break;
			}
			case solve_type::RKF45: {
				differ_state<double> inputs(1, m_oscillators[index].phase);
				differ_result<double> outputs;

				runge_kutta_fehlberg_45(m_callback_solver, inputs, t, t + step, 0.00001, false, argv, outputs);
				next_phases[index] = phase_normalization( outputs[0].state[0] );

				break;
			}
			default: {
				throw std::runtime_error("Unknown type of solver");
			}
		}
	}

	/* store result */
	for (unsigned int index = 0; index < size(); index++) {
		m_oscillators[index].phase = next_phases[index];
	}
}


double sync_network::phase_normalization(const double teta) const {
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


sync_dynamic::~sync_dynamic(void) { }


void sync_dynamic::allocate_sync_ensembles(const double tolerance, const size_t iteration, ensemble_data<sync_ensemble> & ensembles) const {
    ensembles.clear();

    if (size() == 0) {
        return;
    }

    /* push back the first object to the first cluster */
    ensembles.push_back(sync_ensemble());
    ensembles[0].push_back(0);

    sync_dynamic::const_iterator last_state_dynamic = cbegin() + iteration;

    for (unsigned int i = 1; i < number_oscillators(); i++) {
        bool cluster_allocated = false;
        ensemble_data<sync_ensemble>::iterator last_sync_ensemble_element = ensembles.end();

        for (ensemble_data<sync_ensemble>::iterator cluster = ensembles.begin(); cluster != last_sync_ensemble_element; cluster++) {
            sync_ensemble::const_iterator last_cluster_element = (*cluster).cend();

            for (sync_ensemble::const_iterator iter_neuron_index = (*cluster).cbegin(); iter_neuron_index != last_cluster_element; iter_neuron_index++) {
                unsigned int index = (*iter_neuron_index);

                double phase_first = (*last_state_dynamic).m_phase[i];
                double phase_second = (*last_state_dynamic).m_phase[index];

                double phase_shifted = std::abs((*last_state_dynamic).m_phase[i] - 2 * pi());

                if (((phase_first < (phase_second + tolerance)) && (phase_first >(phase_second - tolerance))) ||
                    ((phase_shifted < (phase_second + tolerance)) && (phase_shifted >(phase_second - tolerance)))) {

                    cluster_allocated = true;
                    (*cluster).push_back(i);

                    break;
                }
            }

            if (cluster_allocated == true) {
                break;
            }
        }

        if (cluster_allocated == false) {
            sync_ensemble allocated_cluster;
            allocated_cluster.push_back(i);
            ensembles.push_back(allocated_cluster);
        }
    }
}


void sync_dynamic::allocate_sync_ensembles(const double tolerance, ensemble_data<sync_ensemble> & ensembles) const {
    allocate_sync_ensembles(tolerance, size() - 1, ensembles);
}


void sync_dynamic::allocate_correlation_matrix(sync_corr_matrix & p_matrix) const {
    allocate_correlation_matrix(size() - 1, p_matrix);
}


void sync_dynamic::allocate_correlation_matrix(const size_t p_iteration, sync_corr_matrix & p_matrix) const {
    if ( (size() == 0) || (p_iteration >= size()) ) {
        return;
    }

    p_matrix.resize(number_oscillators(), sync_corr_row(number_oscillators(), 0.0));

    for (size_t i = 0; i < number_oscillators(); i++) {
        for (size_t j = i + 1; j < number_oscillators(); j++) {
            const double phase1 = dynamic_at(p_iteration).m_phase[i];
            const double phase2 = dynamic_at(p_iteration).m_phase[j];

            p_matrix[i][j] = std::abs(std::sin(phase1 - phase2));
            p_matrix[j][i] = p_matrix[i][j];
        }
    }
}
