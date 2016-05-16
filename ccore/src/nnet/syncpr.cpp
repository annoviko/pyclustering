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

#include "nnet/syncpr.hpp"

#include <complex>
#include <cmath>

#include "utils.hpp"


syncpr_invalid_pattern::syncpr_invalid_pattern(void) :
runtime_error("invalid pattern is used") { }


syncpr_invalid_pattern::syncpr_invalid_pattern(const std::string & description) :
runtime_error(description) { }


syncpr::syncpr(const unsigned int num_osc,
    const double increase_strength1,
    const double increase_strength2) :

    sync_network(num_osc, 1, 0, connection_t::CONNECTION_ALL_TO_ALL, initial_type::RANDOM_GAUSSIAN),
    m_increase_strength1(increase_strength1),
    m_increase_strength2(increase_strength2),
    m_coupling(num_osc, std::vector<double>(num_osc, 0.0))
{
    set_callback_solver(&syncpr::adapter_phase_kuramoto);
}


syncpr::syncpr(const unsigned int num_osc,
    const size_t height,
    const size_t width,
    const double increase_strength1,
    const double increase_strength2) :

    sync_network(num_osc, 1, 0, connection_t::CONNECTION_ALL_TO_ALL, height, width, initial_type::RANDOM_GAUSSIAN),
    m_increase_strength1(increase_strength1),
    m_increase_strength2(increase_strength2),
    m_coupling(num_osc, std::vector<double>(num_osc, 0.0))
{
    set_callback_solver(&syncpr::adapter_phase_kuramoto);
}


syncpr::~syncpr() { }


void syncpr::train(const std::vector<syncpr_pattern> & patterns) {
    for (std::vector<syncpr_pattern>::const_iterator iter = patterns.begin(); iter != patterns.end(); iter++) {
        validate_pattern( (*iter) );
    }

    for (size_t i = 0; i < size(); i++) {
        for (size_t j = i + 1; j < size(); j++) {

            /* go through via all patterns */
            for (size_t p = 0; p < patterns.size(); p++) {
                double value1 = patterns[p][i];
                double value2 = patterns[p][j];

                m_coupling[i][j] += value1 * value2;
            }

            m_coupling[i][j] /= (double) size();
            m_coupling[j][i] = m_coupling[i][j];
        }
    }
}


void syncpr::simulate_static(const unsigned int steps,
    const double time,
    const syncpr_pattern & input_pattern,
    const solve_type solver,
    const bool collect_dynamic,
    syncpr_dynamic & output_dynamic) 
{
    validate_pattern(input_pattern);
    initialize_phases(input_pattern);

    for (size_t i = 0; i < input_pattern.size(); i++) {
        if (input_pattern[i] > 0.0) {
            m_oscillators[i].phase = 0.0;
        }
        else {
            m_oscillators[i].phase = pi() / 2.0;
        }
    }

    output_dynamic.clear();

    const double step = time / (double) steps;
    const double int_step = step / 10.0;

    store_dynamic(0.0, collect_dynamic, output_dynamic);    /* store initial state */
    for (double cur_time = step; cur_time < (time + step); cur_time += step) {
        calculate_phases(solver, cur_time, step, int_step);

        store_dynamic(cur_time, collect_dynamic, output_dynamic);   /* store initial state */
    }
}


void syncpr::simulate_dynamic(const syncpr_pattern & input_pattern,
    const double order,
    const double step,
    const solve_type solver,
    const bool collect_dynamic,
    syncpr_dynamic & output_dynamic) 
{
    validate_pattern(input_pattern);
    initialize_phases(input_pattern);

    output_dynamic.clear();

    double previous_order = 0.0;
    double current_order = calculate_memory_order(input_pattern);

    double integration_step = step / 10;

    store_dynamic(0, collect_dynamic, output_dynamic);     /* store initial state */

    for (double time_counter = step; current_order < order; time_counter += step) {
        calculate_phases(solver, time_counter, step, integration_step);

        store_dynamic(time_counter, collect_dynamic, output_dynamic);

        previous_order = current_order;
        current_order = calculate_memory_order(input_pattern);

        if (std::abs(current_order - previous_order) < 0.000001) {
            // std::cout << "Warning: sync_network::simulate_dynamic - simulation is aborted due to low level of convergence rate (order = " << current_order << ")." << std::endl;
            break;
        }
    }
}


void syncpr::initialize_phases(const syncpr_pattern & sample) {
    for (size_t i = 0; i < sample.size(); i++) {
        if (sample[i] > 0.0) {
            m_oscillators[i].phase = 0.0;
        }
        else {
            m_oscillators[i].phase = pi() / 2.0;
        }
    }
}


double syncpr::memory_order(const syncpr_pattern & input_pattern) const {
    validate_pattern(input_pattern);

    return calculate_memory_order(input_pattern);
}


double syncpr::calculate_memory_order(const syncpr_pattern & input_pattern) const {
    std::complex<double> order(0, 0);

    for (size_t i = 0; i < size(); i++) {
        order += std::complex<double>(input_pattern[i], 0) * std::exp(std::complex<double>(0, 1) * m_oscillators[i].phase);
    }

    order /= std::complex<double>(size(), 0);
    return std::abs(order);
}


double syncpr::phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv) {
    size_t oscillator_index = *(unsigned int *)argv[1];

    double phase = 0.0;
    double term = 0.0;

    for (size_t neighbor_index = 0; neighbor_index < size(); neighbor_index++) {
        if (oscillator_index != neighbor_index) {
            double phase_delta = m_oscillators[neighbor_index].phase - m_oscillators[oscillator_index].phase;

            phase += m_coupling[oscillator_index][neighbor_index] * std::sin(phase_delta);

            double term1 = m_increase_strength1 * std::sin(2.0 * phase_delta);
            double term2 = m_increase_strength2 * std::sin(3.0 * phase_delta);

            term += (term1 - term2);
        }
    }

    return ( phase + term / ((double) size()) );
}


void syncpr::validate_pattern(const syncpr_pattern & sample) const {
    if (sample.size() != size()) {
        throw syncpr_invalid_pattern("invalid size of the pattern, it should be the same as network size");
    }

    for (size_t i = 0; i < sample.size(); i++) {
        if ((sample[i] != 1) && (sample[i] != -1)) {
            throw syncpr_invalid_pattern("invalid value in the pattern, pattern value should be +1 or -1");
        }
    }
}


void syncpr::adapter_phase_kuramoto(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
    outputs.resize(1);
    outputs[0] = ((syncpr *) argv[0])->phase_kuramoto(t, inputs[0], argv);
}
