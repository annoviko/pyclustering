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

#include <pyclustering/nnet/sync.hpp>

#include <cmath>
#include <random>
#include <complex>
#include <stdexcept>
#include <chrono>

#include <pyclustering/container/adjacency_bit_matrix.hpp>
#include <pyclustering/container/adjacency_connector.hpp>
#include <pyclustering/container/adjacency_matrix.hpp>

#include <pyclustering/differential/runge_kutta_4.hpp>
#include <pyclustering/differential/runge_kutta_fehlberg_45.hpp>

#include <pyclustering/parallel/parallel.hpp>

#include <pyclustering/utils/math.hpp>
#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::container;
using namespace pyclustering::differential;
using namespace pyclustering::parallel;
using namespace pyclustering::utils::math;
using namespace pyclustering::utils::metric;

using namespace std::placeholders;


namespace pyclustering {

namespace nnet {



const std::size_t sync_network::MAXIMUM_MATRIX_REPRESENTATION_SIZE      = 4096;



double sync_ordering::calculate_sync_order(const std::vector<double> & p_phases) {
    phase_getter getter = [&p_phases](std::size_t index){ return p_phases[index]; };
    return calculate_sync_order_parameter(p_phases, getter);
}


double sync_ordering::calculate_sync_order(const std::vector<sync_oscillator> & p_oscillators) {
    phase_getter getter = [&p_oscillators](std::size_t index){ return p_oscillators[index].phase; };
    return calculate_sync_order_parameter(p_oscillators, getter);
}


template <class TypeContainer>
double sync_ordering::calculate_sync_order_parameter(const TypeContainer & p_container, const phase_getter & p_getter) {
    double exp_amount = 0.0;
    double average_phase = 0.0;

    for (std::size_t index = 0; index < p_container.size(); index++) {
        const double phase = p_getter(index);

        exp_amount += std::exp( std::abs( std::complex<double>(0, 1) * phase ) );
        average_phase += phase;
    }

    exp_amount /= p_container.size();
    average_phase = std::exp( std::abs( std::complex<double>(0, 1) * (average_phase / p_container.size()) ) );

    return std::abs(average_phase) / std::abs(exp_amount);
}


double sync_ordering::calculate_local_sync_order(const std::shared_ptr<adjacency_collection> & p_connections, const std::vector<double> & p_phases) {
    phase_getter getter = [&p_phases](std::size_t index){ return p_phases[index]; };
    return calculate_local_sync_order_parameter(p_connections, p_phases, getter);
}


double sync_ordering::calculate_local_sync_order(const std::shared_ptr<adjacency_collection> & p_connections, const std::vector<sync_oscillator> & p_oscillators) {
    phase_getter getter = [&p_oscillators](std::size_t index){ return p_oscillators[index].phase; };
    return calculate_local_sync_order_parameter(p_connections, p_oscillators, getter);
}


template <class TypeContainer>
double sync_ordering::calculate_local_sync_order_parameter(const std::shared_ptr<adjacency_collection> & p_connections, const TypeContainer & p_container, const phase_getter & p_getter) {
    double exp_amount = 0.0;
    double number_neighbors = 0.0;

    for (std::size_t i = 0; i < p_container.size(); i++) {
        double phase = p_getter(i);

        std::vector<std::size_t> neighbors;
        p_connections->get_neighbors(i, neighbors);

        for (auto & index_neighbor : neighbors) {
            double phase_neighbor = p_getter(index_neighbor);
            exp_amount += std::exp( -std::abs( phase_neighbor - phase ) );
        }

        number_neighbors += static_cast<double>(neighbors.size());
    }

    if (number_neighbors == 0.0) {
        number_neighbors = 1.0;
    }

    return exp_amount / number_neighbors;
}



sync_network::sync_network(const size_t size, const double weight_factor, const double frequency_factor, const connection_t connection_type, const initial_type initial_phases) {
    initialize(size, weight_factor, frequency_factor, connection_type, 0, 0, initial_phases);
}


sync_network::sync_network(const size_t size, const double weight_factor,  const double frequency_factor, const connection_t connection_type, const size_t height, const size_t width, const initial_type initial_phases) {
    initialize(size, weight_factor, frequency_factor, connection_type, height, width, initial_phases);
}


sync_network::~sync_network() { }


void sync_network::initialize(const std::size_t size, const double weight_factor, const double frequency_factor, const connection_t connection_type, const std::size_t height, const std::size_t width, const initial_type initial_phases) {
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

    m_equation = std::bind(&sync_network::phase_kuramoto_equation, this, _1, _2, _3, _4);

    std::random_device                      device;
    std::default_random_engine              generator(device());

    generator.seed(static_cast<unsigned int>(std::chrono::system_clock::now().time_since_epoch().count()));

    std::uniform_real_distribution<double>  phase_distribution(0.0, 2.0 * pi);
    std::uniform_real_distribution<double>  frequency_distribution(0.0, 1.0);

    for (std::size_t index = 0; index < size; index++) {
        sync_oscillator & oscillator_context = m_oscillators[index];

        switch (initial_phases) {
        case initial_type::RANDOM_GAUSSIAN:
            oscillator_context.phase = phase_distribution(generator);
            break;
        case initial_type::EQUIPARTITION:
            oscillator_context.phase = pi / static_cast<double>(size) * static_cast<double>(index);
            break;
        default:
            throw std::runtime_error("Unknown type of initialization");
        }

        oscillator_context.frequency = frequency_distribution(generator) * frequency_factor;
    }
}


double sync_network::sync_order() const {
    return sync_ordering::calculate_sync_order(m_oscillators);
}


double sync_network::sync_local_order() const {
    return sync_ordering::calculate_local_sync_order(m_connections, m_oscillators);
}


void sync_network::set_equation(equation<double> & solver) {
    m_equation = solver;
}


void sync_network::phase_kuramoto_equation(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) const {
    outputs.resize(1);
    outputs[0] = phase_kuramoto(t, inputs[0], argv);
}


double sync_network::phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) const {
    std::size_t index = *(std::size_t *) argv[0];
    double phase = 0.0;

    std::vector<size_t> neighbors;
    m_connections->get_neighbors(index, neighbors);

    for (auto & index_neighbor : neighbors) {
        phase += std::sin(m_oscillators[index_neighbor].phase - teta);
    }

    phase = m_oscillators[index].frequency + (phase * weight / static_cast<double>(size()));
    return phase;
}


void sync_network::simulate_static(const std::size_t steps, const double time, const solve_type solver, const bool collect_dynamic, sync_dynamic & output_dynamic) {
    output_dynamic.clear();

    const double step = time / (double) steps;
    const double int_step = step / 10.0;

    store_dynamic(0.0, collect_dynamic, output_dynamic);    /* store initial state */

    double cur_time = step;
    for (std::size_t cur_step = 0; cur_step < steps; cur_step++) {
        calculate_phases(solver, cur_time, step, int_step);

        store_dynamic(cur_time, collect_dynamic, output_dynamic);

        cur_time += step;
    }
}


void sync_network::simulate_dynamic(const double order, const double step, const solve_type solver, const bool collect_dynamic, sync_dynamic & output_dynamic) {
    output_dynamic.clear();

    store_dynamic(0, collect_dynamic, output_dynamic);     /* store initial state */

    double current_order = sync_local_order();

    double integration_step = step / 10.0;

    for (double time_counter = step; current_order < order; time_counter += step) {
        calculate_phases(solver, time_counter, step, integration_step);

        store_dynamic(time_counter, collect_dynamic, output_dynamic);

        double previous_order = current_order;
        current_order = sync_local_order();

        if (std::abs(current_order - previous_order) < 0.000001) {
            // std::cout << "Warning: sync_network::simulate_dynamic - simulation is aborted due to low level of convergence rate (order = " << current_order << ")." << std::endl;
            break;
        }
    }
}


void sync_network::store_dynamic(const double time, const bool collect_dynamic, sync_dynamic & output_dynamic) const {
    sync_network_state state(size());

    for (std::size_t index = 0; index < size(); index++) {
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
    std::vector<double> next_phases(size(), 0.0);

    parallel_for(std::size_t(0), size(), [this, solver, t, step, int_step, &next_phases](const std::size_t p_index) {
        calculate_phase(solver, t, step, int_step, p_index, next_phases);
    });

    /* store result */
    for (std::size_t index = 0; index < size(); index++) {
        m_oscillators[index].phase = next_phases[index];
    }
}


void sync_network::calculate_phase(const solve_type solver,
                                   const double t,
                                   const double step,
                                   const double int_step,
                                   const std::size_t index,
                                   std::vector<double> & p_next_phases)
{
    std::size_t number_int_steps = (std::size_t) (step / int_step);

    std::vector<void *> argv(1, nullptr);
    argv[0] = (void *) &index;

    switch(solver) {
        case solve_type::FORWARD_EULER: {
            double result = m_oscillators[index].phase + phase_kuramoto(t, m_oscillators[index].phase, argv);
            p_next_phases[index] = phase_normalization(result);

            break;
        }
        case solve_type::RUNGE_KUTTA_4: {
            differ_state<double> inputs(1, m_oscillators[index].phase);
            differ_result<double> outputs;

            runge_kutta_4(m_equation, inputs, t, t + step, number_int_steps, false, argv, outputs);
            p_next_phases[index] = phase_normalization( outputs[0].state[0] );

            break;
        }
        case solve_type::RUNGE_KUTTA_FEHLBERG_45: {
            differ_state<double> inputs(1, m_oscillators[index].phase);
            differ_result<double> outputs;

            runge_kutta_fehlberg_45(m_equation, inputs, t, t + step, 0.00001, false, argv, outputs);
            p_next_phases[index] = phase_normalization( outputs[0].state[0] );

            break;
        }
        default: {
            throw std::runtime_error("Unknown type of solver");
        }
    }
}


double sync_network::phase_normalization(const double teta) const {
    double norm_teta = teta;

    while ( (norm_teta > 2.0 * pi) || (norm_teta < 0.0) ) {
        if (norm_teta > 2.0 * pi) {
            norm_teta -= 2.0 * pi;
        }
        else {
            norm_teta += 2.0 * pi;
        }
    }

    return norm_teta;
}



void sync_dynamic::allocate_sync_ensembles(const double tolerance, const size_t iteration, ensemble_data<sync_ensemble> & ensembles) const {
    ensembles.clear();

    if (size() == 0) {
        return;
    }

    /* push back the first object to the first cluster */
    ensembles.push_back(sync_ensemble());
    ensembles[0].push_back(0);

    sync_dynamic::const_iterator last_state_dynamic = cbegin() + iteration;

    for (std::size_t i = 1; i < oscillators(); i++) {
        bool cluster_allocated = false;

        for (auto & cluster : ensembles) {
            for (auto & index : cluster) {
                double phase_first = (*last_state_dynamic).m_phase[i];
                double phase_second = (*last_state_dynamic).m_phase[index];

                double phase_shifted = std::abs((*last_state_dynamic).m_phase[i] - 2 * pi);

                if (((phase_first < (phase_second + tolerance)) && (phase_first >(phase_second - tolerance))) ||
                    ((phase_shifted < (phase_second + tolerance)) && (phase_shifted >(phase_second - tolerance)))) {

                    cluster_allocated = true;
                    cluster.push_back(i);

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
    if ( (empty()) || (p_iteration >= size()) ) {
        return;
    }

    p_matrix.resize(oscillators(), sync_corr_row(oscillators(), 0.0));

    for (size_t i = 0; i < oscillators(); i++) {
        for (size_t j = i + 1; j < oscillators(); j++) {
            const double phase1 = at(p_iteration).m_phase[i];
            const double phase2 = at(p_iteration).m_phase[j];

            p_matrix[i][j] = std::abs(std::sin(phase1 - phase2));
            p_matrix[j][i] = p_matrix[i][j];
        }
    }
}


void sync_dynamic::calculate_order_parameter(const std::size_t start_iteration, const std::size_t stop_iteration, std::vector<double> & sequence_order) const {
    sequence_order.resize(stop_iteration - start_iteration, 0.0);

    for (std::size_t i = start_iteration; i < stop_iteration; i++) {
        const double order_value =  sync_ordering::calculate_sync_order(at(i).m_phase);
        sequence_order[i - start_iteration] = order_value;
    }
}


void sync_dynamic::calculate_local_order_parameter(const std::shared_ptr<adjacency_collection> & connections, const std::size_t start_iteration, const std::size_t stop_iteration, std::vector<double> & sequence_local_order) const {
    sequence_local_order.resize(stop_iteration - start_iteration, 0.0);

    for (std::size_t i = start_iteration; i < stop_iteration; i++) {
        const double order_value =  sync_ordering::calculate_local_sync_order(connections, at(i).m_phase);
        sequence_local_order[i - start_iteration] = order_value;
    }
}


}

}