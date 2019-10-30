/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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

#include <pyclustering/nnet/legion.hpp>

#include <chrono>
#include <stdexcept>

#include <pyclustering/container/adjacency_bit_matrix.hpp>
#include <pyclustering/container/adjacency_connector.hpp>
#include <pyclustering/container/adjacency_matrix.hpp>

#include <pyclustering/utils/math.hpp>
#include <pyclustering/utils/metric.hpp>


using namespace std::placeholders;

using namespace pyclustering::utils::math;


namespace pyclustering {

namespace nnet {


const size_t legion_network::MAXIMUM_MATRIX_REPRESENTATION_SIZE = 4096;


std::size_t legion_network_state::size() const {
    return m_output.size();
}


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

    store_dynamic(0.0, collect_dynamic, output_dynamic);  /* store initial state */

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

            for (auto & index_neighbor : neighbors) {
                if (stimulus[index_neighbor] > 0) {
                    number_stimulated_neighbors++;
                }
            }

            if (number_stimulated_neighbors > 0) {
                double dynamic_weight = m_params.Wt / (double) number_stimulated_neighbors;

                for (auto & index_neighbor : neighbors) {
                    m_dynamic_connections[i][index_neighbor] = dynamic_weight;
                }
            }
        }
    }
}

void legion_network::store_dynamic(const double time, const bool collect_dynamic, legion_dynamic & dynamic) const {
    legion_network_state state(size());

    for (std::size_t index = 0; index < size(); index++) {
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
    std::vector< differ_result<double> > next_states(size());
    std::vector<void *> argv(1, nullptr);

    std::size_t number_int_steps = static_cast<std::size_t>(step / int_step);

    for (std::size_t index = 0; index < size(); index++) {
        argv[0] = (void *) index;

        differ_state<double> inputs { m_oscillators[index].m_excitatory, m_oscillators[index].m_inhibitory };
        if (m_params.ENABLE_POTENTIAL) {
            inputs.push_back(m_oscillators[index].m_potential);
        }

        switch(solver) {
            case solve_type::FORWARD_EULER: {
                throw std::invalid_argument("Forward Euler first-order method is not supported due to low accuracy.");
            }

            case solve_type::RUNGE_KUTTA_4: {
                if (m_params.ENABLE_POTENTIAL) {
                    equation<double> neuron_equation = std::bind(&legion_network::neuron_states, this, _1, _2, _3, _4);
                    runge_kutta_4(neuron_equation, inputs, t, t + step, number_int_steps, false /* only last states */, argv, next_states[index]);
                }
                else {
                    equation<double> neuron_simplify_equation = std::bind(&legion_network::neuron_simplify_states, this, _1, _2, _3, _4);
                    runge_kutta_4(neuron_simplify_equation, inputs, t, t + step, number_int_steps, false /* only last states */, argv, next_states[index]);
                }

                break;
            }

            case solve_type::RUNGE_KUTTA_FEHLBERG_45: {
                if (m_params.ENABLE_POTENTIAL) {
                    equation<double> neuron_equation = std::bind(&legion_network::neuron_states, this, _1, _2, _3, _4);
                    runge_kutta_fehlberg_45(neuron_equation, inputs, t, t + step, 0.00001, false /* only last states */, argv, next_states[index]);
                }
                else {
                    equation<double> neuron_simplify_equation = std::bind(&legion_network::neuron_simplify_states, this, _1, _2, _3, _4);
                    runge_kutta_fehlberg_45(neuron_simplify_equation, inputs, t, t + step, 0.00001, false /* only last states */, argv, next_states[index]);
                }

                break;
            }

            default: {
                throw std::invalid_argument("Not supported solver is used.");
            }
        }

        std::vector<size_t> neighbors;
        m_static_connections->get_neighbors(index, neighbors);

        double coupling = 0.0;

        for (auto & index_neighbor : neighbors) {
            coupling += m_dynamic_connections[index][index_neighbor] * heaviside(m_oscillators[index_neighbor].m_excitatory - m_params.teta_x);
        }

        m_oscillators[index].m_buffer_coupling_term = coupling - m_params.Wz * heaviside(m_global_inhibitor - m_params.teta_xz);
    }

    differ_result<double> inhibitor_next_state;
    differ_state<double> inhibitor_input { m_global_inhibitor };

    equation<double> inhibitor_equation = std::bind(&legion_network::inhibitor_state, this, _1, _2, _3, _4);

    switch (solver) {
        case solve_type::RUNGE_KUTTA_4: {
            runge_kutta_4(inhibitor_equation, inhibitor_input, t, t + step, number_int_steps, false /* only last states */, argv, inhibitor_next_state);
            break;
        }
        case solve_type::RUNGE_KUTTA_FEHLBERG_45: {
            runge_kutta_fehlberg_45(inhibitor_equation, inhibitor_input, t, t + step, 0.00001, false /* only last states */, argv, inhibitor_next_state);
            break;
        }
        default:
            throw std::invalid_argument("Not supported solver is used.");
    }

    m_global_inhibitor = inhibitor_next_state[0].state[0];

    for (std::size_t i = 0; i < size(); i++) {
        m_oscillators[i].m_excitatory = next_states[i][0].state[0];
        m_oscillators[i].m_inhibitory = next_states[i][0].state[1];

        if (m_params.ENABLE_POTENTIAL) {
            m_oscillators[i].m_potential = next_states[i][0].state[2];
        }

        m_oscillators[i].m_coupling_term = m_oscillators[i].m_buffer_coupling_term;
        m_oscillators[i].m_noise = m_noise_distribution(m_generator);
    }
}


void legion_network::neuron_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
    std::size_t index = (std::size_t) argv[0];

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

    std::vector<std::size_t> neighbors;
    m_static_connections->get_neighbors(index, neighbors);

    double potential = 0.0;

    for (auto index_neighbor : neighbors) {
        potential += m_params.T * heaviside(m_oscillators[index_neighbor].m_excitatory - m_params.teta_x);
    }

    double dp = m_params.lamda * (1 - p) * heaviside(potential - m_params.teta_p) - m_params.mu * p;

    outputs.clear();
    outputs.push_back(dx);
    outputs.push_back(dy);
    outputs.push_back(dp);
}


void legion_network::neuron_simplify_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
    unsigned int index = *(unsigned int *) argv[0];

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


void legion_network::inhibitor_state(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) const {
    const double z = inputs[0];

    double sigma = 0.0;
    for (std::size_t index = 0; index < size(); index++) {
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
    m_generator.seed(static_cast<unsigned int>(std::chrono::system_clock::now().time_since_epoch().count()));
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


}

}