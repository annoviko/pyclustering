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

#include "nnet/legion.hpp"

#include "container/adjacency_bit_matrix.hpp"
#include "container/adjacency_connector.hpp"
#include "container/adjacency_matrix.hpp"

#include "utils.hpp"


const size_t legion_network::MAXIMUM_MATRIX_REPRESENTATION_SIZE = 4096;


legion_network::legion_network(void) : m_stimulus(nullptr) { }


legion_network::legion_network(const size_t num_osc, const connection_t connection_type, const legion_parameters & params) {
    initialize(num_osc, connection_type, 0, 0, params);
}


legion_network::legion_network(const size_t num_osc, const connection_t connection_type, const size_t height, const size_t width, const legion_parameters & params) {
    initialize(num_osc, connection_type, height, width, params);
}


legion_network::~legion_network() {
	m_stimulus = nullptr;
}


void legion_network::simulate(const unsigned int steps, 
                              const double time, 
                              const solve_type solver, 
                              const bool collect_dynamic, 
                              const legion_stimulus & stimulus, 
                              legion_dynamic & output_dynamic) {

	output_dynamic.clear();

	m_stimulus = (legion_stimulus *) &stimulus;
	create_dynamic_connections(stimulus);

	const double step = time / (double) steps;
	const double int_step = step / 10.0;

	store_dynamic(0.0, collect_dynamic, output_dynamic);	/* store initial state */

	for (double cur_time = step; cur_time < time; cur_time += step) {
		calculate_states(stimulus, solver, cur_time, step, int_step);
		
		store_dynamic(cur_time, collect_dynamic, output_dynamic);	/* store initial state */
	}
}

void legion_network::create_dynamic_connections(const legion_stimulus & stimulus) {
	for (size_t i = 0; i < size(); i++) {
		/* re-initialization by 0.0 */
		std::fill(m_dynamic_connections[i].begin(), m_dynamic_connections[i].end(), 0.0);

		std::vector<size_t> neighbors;
		m_static_connections->get_neighbors(i, neighbors);

		if (neighbors.size() > 0 && stimulus[i] > 0) {
			int number_stimulated_neighbors = 0;

			for (std::vector<size_t>::iterator index_iterator = neighbors.begin(); index_iterator != neighbors.end(); index_iterator++) {
				if (stimulus[*index_iterator] > 0) {
					number_stimulated_neighbors++;
				}
			}

			if (number_stimulated_neighbors > 0) {
				double dynamic_weight = m_params.Wt / (double) number_stimulated_neighbors;

				for (std::vector<size_t>::iterator index_iterator = neighbors.begin(); index_iterator != neighbors.end(); index_iterator++) {
					m_dynamic_connections[i][*index_iterator] = dynamic_weight;
				}
			}
		}
	}
}

void legion_network::store_dynamic(const double time, const bool collect_dynamic, legion_dynamic & dynamic) {
	legion_network_state state(size());

	for (unsigned int index = 0; index < size(); index++) {
		state.m_output[index] = m_oscillators[index].m_excitatory;
	}

	state.m_inhibitor = m_global_inhibitor;
	state.m_time = time;
	
	if ( (collect_dynamic == false) && (!dynamic.empty()) ) {
		dynamic[0] = state;
	}
	else {
		dynamic.push_back(state);
	}
}

void legion_network::calculate_states(const legion_stimulus & stimulus, const solve_type solver, const double t, const double step, const double int_step) {
	std::vector<void *> argv(2, NULL);
	std::vector<differ_result<double> > next_states(size());

	argv[0] = (void *) this;

	unsigned int number_int_steps = (unsigned int) (step / int_step);

	for (unsigned int index = 0; index < size(); index++) {
		argv[1] = (void *) &index;

		differ_state<double> inputs { m_oscillators[index].m_excitatory, m_oscillators[index].m_inhibitory };
		if (m_params.ENABLE_POTENTIAL) {
			inputs.push_back(m_oscillators[index].m_potential);
		}

		switch(solver) {
			case solve_type::FAST: {
				throw std::runtime_error("Forward Euler first-order method is not supported due to low accuracy.");
			}

			case solve_type::RK4: {
				if (m_params.ENABLE_POTENTIAL) {
					runge_kutta_4(&legion_network::adapter_neuron_states, inputs, t, t + step, number_int_steps, false /* only last states */, argv, next_states[index]);
				}
				else {
					runge_kutta_4(&legion_network::adapter_neuron_simplify_states, inputs, t, t + step, number_int_steps, false /* only last states */, argv, next_states[index]);
				}

				break;
			}

			case solve_type::RKF45: {
				if (m_params.ENABLE_POTENTIAL) {
					runge_kutta_fehlberg_45(&legion_network::adapter_neuron_states, inputs, t, t + step, 0.00001, false /* only last states */, argv, next_states[index]);
				}
				else {
					runge_kutta_fehlberg_45(&legion_network::adapter_neuron_simplify_states, inputs, t, t + step, 0.00001, false /* only last states */, argv, next_states[index]);
				}
				
				break;
			}

			default: {
				throw std::runtime_error("Unknown type of solver");
			}
		}

        std::vector<size_t> neighbors;
        m_static_connections->get_neighbors(index, neighbors);

		double coupling = 0.0;

        for (std::vector<size_t>::const_iterator index_neighbor_iterator = neighbors.begin(); index_neighbor_iterator != neighbors.end(); index_neighbor_iterator++) {
			coupling += m_dynamic_connections[index][*index_neighbor_iterator] * heaviside(m_oscillators[*index_neighbor_iterator].m_excitatory - m_params.teta_x);
		}

		m_oscillators[index].m_buffer_coupling_term = coupling - m_params.Wz * heaviside(m_global_inhibitor - m_params.teta_xz);
	}

	differ_result<double> inhibitor_next_state;
	differ_state<double> inhibitor_input { m_global_inhibitor };

	switch (solver) {
		case solve_type::RK4: {
			runge_kutta_4(&legion_network::adapter_inhibitor_state, inhibitor_input, t, t + step, number_int_steps, false /* only last states */, argv, inhibitor_next_state);
			break;
		}
		case solve_type::RKF45: {
			runge_kutta_fehlberg_45(&legion_network::adapter_inhibitor_state, inhibitor_input, t, t + step, 0.00001, false /* only last states */, argv, inhibitor_next_state);
			break;
		}
	}

	m_global_inhibitor = inhibitor_next_state[0].state[0];

	for (unsigned int i = 0; i < size(); i++) {
		m_oscillators[i].m_excitatory = next_states[i][0].state[0];
		m_oscillators[i].m_inhibitory = next_states[i][0].state[1];

		if (m_params.ENABLE_POTENTIAL) {
			m_oscillators[i].m_potential = next_states[i][0].state[2];
		}

		m_oscillators[i].m_coupling_term = m_oscillators[i].m_buffer_coupling_term;
		m_oscillators[i].m_noise = m_noise_distribution(m_generator);
	}
}


void legion_network::adapter_neuron_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
	((legion_network *) argv[0])->neuron_states(t, inputs, argv, outputs);
}


void legion_network::adapter_neuron_simplify_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
	((legion_network *) argv[0])->neuron_simplify_states(t, inputs, argv, outputs);
}


void legion_network::adapter_inhibitor_state(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
	((legion_network *) argv[0])->inhibitor_state(t, inputs, argv, outputs);
}


void legion_network::neuron_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
	unsigned int index = *(unsigned int *) argv[1];

	const double x = inputs[0];
	const double y = inputs[1];
	const double p = inputs[2];

	double potential_influence = heaviside(p + std::exp(-m_params.alpha * t) - m_params.teta);

	double stumulus = 0.0;
	if ((*m_stimulus)[index] > 0) {
		stumulus = m_params.I;
	}

	double dx = 3.0 * x - std::pow(x, 3) + 2.0 - y + stumulus * potential_influence + m_oscillators[index].m_coupling_term + m_oscillators[index].m_noise;
	double dy = m_params.eps * (m_params.gamma * (1.0 + std::tanh(x / m_params.betta)) - y);

    std::vector<size_t> neighbors;
    m_static_connections->get_neighbors(index, neighbors);

	double potential = 0.0;

    for (std::vector<size_t>::const_iterator index_iterator = neighbors.begin(); index_iterator != neighbors.end(); index_iterator++) {
		unsigned int index_neighbor = *index_iterator;
		potential += m_params.T * heaviside(m_oscillators[index_neighbor].m_excitatory - m_params.teta_x);
	}

	double dp = m_params.lamda * (1 - p) * heaviside(potential - m_params.teta_p) - m_params.mu * p;

	outputs.clear();
	outputs.push_back(dx);
	outputs.push_back(dy);
	outputs.push_back(dp);
}

void legion_network::neuron_simplify_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
	unsigned int index = *(unsigned int *) argv[1];

	const double x = inputs[0];
	const double y = inputs[1];

	double stumulus = 0.0;
	if ((*m_stimulus)[index] > 0) {
		stumulus = m_params.I;
	}

	double dx = 3.0 * x - std::pow(x, 3) + 2.0 - y + stumulus + m_oscillators[index].m_coupling_term + m_oscillators[index].m_noise;
	double dy = m_params.eps * (m_params.gamma * (1.0 + std::tanh(x / m_params.betta)) - y);

	outputs.clear();
	outputs.push_back(dx);
	outputs.push_back(dy);
}


void legion_network::inhibitor_state(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
	const double z = inputs[0];

	double sigma = 0.0;
	for (unsigned int index = 0; index < size(); index++) {
		if (m_oscillators[index].m_excitatory > m_params.teta_zx) {
			sigma = 1.0;
			break;
		}
	}

	double dz = m_params.fi * (sigma - z);

	outputs.clear();
	outputs.push_back(dz);
}


void legion_network::initialize(const size_t num_osc, const connection_t connection_type, const size_t height, const size_t width, const legion_parameters & params) {
    m_oscillators = std::vector<legion_oscillator>(num_osc, legion_oscillator());
    m_dynamic_connections = std::vector<std::vector<double> >(num_osc, std::vector<double>(num_osc, 0.0)),
    m_stimulus = nullptr;
    m_generator = std::default_random_engine(m_device());
    m_noise_distribution = std::uniform_real_distribution<double>(0.0, params.ro);
    m_global_inhibitor = 0;

    m_params = params;

    for (size_t index = 0; index < m_oscillators.size(); index++) {
        m_oscillators[index].m_noise = m_noise_distribution(m_generator);
    }

    if (num_osc > MAXIMUM_MATRIX_REPRESENTATION_SIZE) {
        m_static_connections = std::shared_ptr<adjacency_collection>(new adjacency_bit_matrix(num_osc));
    }
    else {
        m_static_connections = std::shared_ptr<adjacency_matrix>(new adjacency_matrix(num_osc));
    }

    adjacency_connector<adjacency_collection> connector;

    if ((height != 0) && (width != 0)) {
        connector.create_grid_structure(connection_type, width, height, *m_static_connections);
    }
    else {
        connector.create_structure(connection_type, *m_static_connections);
    }
}
