/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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


#include "nnet/hhn.hpp"

#include "differential/differ_state.hpp"
#include "differential/runge_kutta_4.hpp"
#include "differential/runge_kutta_fehlberg_45.hpp"


using namespace std::placeholders;

using namespace ccore::utils::random;


namespace ccore {

namespace nnet {


hhn_dynamic::hhn_dynamic(void) {
    initialize_collection(*m_peripheral_dynamic);
    initialize_collection(*m_central_dynamic);
}


void hhn_dynamic::enable(const hhn_dynamic::collect p_state) {
    if (m_enable[p_state] != true) {
        m_enable[p_state] = true;
        m_amount_collections++;
    }
}


void hhn_dynamic::enable_all(void) {
    for (auto & collection : m_enable) {
        collection.second = true;
    }

    m_amount_collections = m_enable.size();
}


void hhn_dynamic::disable(const hhn_dynamic::collect p_state) {
    if (m_enable[p_state] != false) {
        m_enable[p_state] = false;
        m_amount_collections--;
    }
}


void hhn_dynamic::disable_all(void) {
    for (auto & collection : m_enable) {
        collection.second = false;
    }

    m_amount_collections = 0;
}


void hhn_dynamic::get_enabled(std::set<hhn_dynamic::collect> & p_enabled) const {
    get_collected_types(true, p_enabled);
}


void hhn_dynamic::get_disabled(std::set<hhn_dynamic::collect> & p_disabled) const {
    get_collected_types(false, p_disabled);
}


void hhn_dynamic::store(const double p_time, const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central) {
    if (!m_amount_collections) {
        return;
    }

    if (m_enable[collect::MEMBRANE_POTENTIAL]) {
        store_membrane_potential(p_peripheral, p_central);
    }

    if (m_enable[collect::ACTIVE_COND_POTASSIUM]) {
        store_active_cond_potassium(p_peripheral, p_central);
    }

    if (m_enable[collect::ACTIVE_COND_SODIUM]) {
        store_active_cond_sodium(p_peripheral, p_central);
    }

    if (m_enable[collect::INACTIVE_COND_SODIUM]) {
        store_inactive_cond_sodium(p_peripheral, p_central);
    }

    m_time->push_back(p_time);
}


void hhn_dynamic::reserve(const std::size_t p_dynamic_size) {
    if (m_enable[collect::MEMBRANE_POTENTIAL]) {
        reserve_collection(collect::MEMBRANE_POTENTIAL, p_dynamic_size);
    }

    if (m_enable[collect::ACTIVE_COND_POTASSIUM]) {
        reserve_collection(collect::ACTIVE_COND_POTASSIUM, p_dynamic_size);
    }

    if (m_enable[collect::ACTIVE_COND_SODIUM]) {
        reserve_collection(collect::ACTIVE_COND_SODIUM, p_dynamic_size);
    }

    if (m_enable[collect::INACTIVE_COND_SODIUM]) {
        reserve_collection(collect::INACTIVE_COND_SODIUM, p_dynamic_size);
    }
}


hhn_dynamic::evolution_dynamic & hhn_dynamic::get_peripheral_dynamic(const hhn_dynamic::collect & p_type) {
    return (*m_peripheral_dynamic)[p_type];
}


hhn_dynamic::network_dynamic_ptr hhn_dynamic::get_peripheral_dynamic(void) const {
    return m_peripheral_dynamic;
}


hhn_dynamic::evolution_dynamic & hhn_dynamic::get_central_dynamic(const hhn_dynamic::collect & p_type) {
    return (*m_central_dynamic)[p_type];
}


hhn_dynamic::network_dynamic_ptr hhn_dynamic::get_central_dynamic(void) const {
    return m_central_dynamic;
}


void hhn_dynamic::initialize_collection(network_dynamic & p_dynamic) {
    p_dynamic[hhn_dynamic::collect::MEMBRANE_POTENTIAL]     = evolution_dynamic();
    p_dynamic[hhn_dynamic::collect::ACTIVE_COND_SODIUM]     = evolution_dynamic();
    p_dynamic[hhn_dynamic::collect::INACTIVE_COND_SODIUM]   = evolution_dynamic();
    p_dynamic[hhn_dynamic::collect::ACTIVE_COND_POTASSIUM]  = evolution_dynamic();
}


void hhn_dynamic::get_collected_types(const bool p_enabled, std::set<hhn_dynamic::collect> & p_types) const {
    for (const auto & p_collect_element : m_enable) {
        if (p_collect_element.second == p_enabled) {
            p_types.insert(p_collect_element.first);
        }
    }
}


void hhn_dynamic::reserve_collection(const hhn_dynamic::collect p_state, const std::size_t p_size) {
    reserve_dynamic_collection(p_state, p_size, *m_peripheral_dynamic);
    reserve_dynamic_collection(p_state, p_size, *m_central_dynamic);

    m_time->reserve(p_size);
}


void hhn_dynamic::reserve_dynamic_collection(const hhn_dynamic::collect p_state, const std::size_t p_size, network_dynamic & p_dynamic) {
    if (p_dynamic.find(p_state) != p_dynamic.end()) {
        p_dynamic.at(p_state).reserve(p_size);
    }
    else {
        evolution_dynamic dynamic;
        dynamic.reserve(p_size);

        p_dynamic[p_state] = std::move(dynamic);
    }
}


void hhn_dynamic::store_membrane_potential(const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central) {
    std::vector<double> peripheral_membrane_values(p_peripheral.size(), 0.0);
    for (std::size_t index = 0; index < p_peripheral.size(); index++) {
        peripheral_membrane_values[index] = p_peripheral[index].m_membrane_potential;
    }

    m_peripheral_dynamic->at(collect::MEMBRANE_POTENTIAL).emplace_back(std::move(peripheral_membrane_values));

    std::vector<double> central_membrane_values(p_central.size(), 0.0);
    for (std::size_t index = 0; index < p_central.size(); index++) {
        central_membrane_values[index] = p_central[index].m_membrane_potential;
    }

    m_central_dynamic->at(collect::MEMBRANE_POTENTIAL).emplace_back(std::move(central_membrane_values));
}


void hhn_dynamic::store_active_cond_sodium(const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central) {
    std::vector<double> peripheral_active_sodium(p_peripheral.size(), 0.0);
    for (std::size_t index = 0; index < p_peripheral.size(); index++) {
        peripheral_active_sodium[index] = p_peripheral[index].m_active_cond_sodium;
    }

    m_peripheral_dynamic->at(collect::ACTIVE_COND_SODIUM).emplace_back(std::move(peripheral_active_sodium));

    std::vector<double> central_active_sodium(p_central.size(), 0.0);
    for (std::size_t index = 0; index < p_central.size(); index++) {
        central_active_sodium[index] = p_central[index].m_active_cond_sodium;
    }

    m_central_dynamic->at(collect::ACTIVE_COND_SODIUM).emplace_back(std::move(central_active_sodium));
}


void hhn_dynamic::store_inactive_cond_sodium(const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central) {
    std::vector<double> peripheral_inactive_sodium(p_peripheral.size(), 0.0);
    for (std::size_t index = 0; index < p_peripheral.size(); index++) {
        peripheral_inactive_sodium[index] = p_peripheral[index].m_inactive_cond_sodium;
    }

    m_peripheral_dynamic->at(collect::INACTIVE_COND_SODIUM).emplace_back(std::move(peripheral_inactive_sodium));

    std::vector<double> central_inactive_sodium(p_central.size(), 0.0);
    for (std::size_t index = 0; index < p_central.size(); index++) {
        central_inactive_sodium[index] = p_central[index].m_inactive_cond_sodium;
    }

    m_central_dynamic->at(collect::INACTIVE_COND_SODIUM).emplace_back(std::move(central_inactive_sodium));
}


void hhn_dynamic::store_active_cond_potassium(const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central) {
    std::vector<double> peripheral_active_potassium(p_peripheral.size(), 0.0);
    for (std::size_t index = 0; index < p_peripheral.size(); index++) {
        peripheral_active_potassium[index] = p_peripheral[index].m_active_cond_potassium;
    }

    m_peripheral_dynamic->at(collect::ACTIVE_COND_POTASSIUM).emplace_back(std::move(peripheral_active_potassium));

    std::vector<double> central_active_potassium(p_central.size(), 0.0);
    for (std::size_t index = 0; index < p_central.size(); index++) {
        central_active_potassium[index] = p_central[index].m_active_cond_potassium;
    }

    m_central_dynamic->at(collect::ACTIVE_COND_POTASSIUM).emplace_back(std::move(central_active_potassium));
}




const std::size_t hhn_network::POSITION_MEMBRAN_POTENTIAL       = 0;

const std::size_t hhn_network::POSITION_ACTIVE_COND_SODIUM      = 1;

const std::size_t hhn_network::POSITION_INACTIVE_COND_SODIUM    = 2;

const std::size_t hhn_network::POSITION_ACTIVE_COND_POTASSIUM   = 3;


hhn_network::hhn_network(const std::size_t p_size, const hnn_parameters p_parameters) :
    m_peripheral(p_size),
    m_central(2),
    m_stimulus(nullptr),
    m_params(p_parameters)
{ }


void hhn_network::simulate(const std::size_t p_steps, const double p_time, const solve_type p_solver, const hhn_stimulus & p_stimulus, hhn_dynamic & p_output_dynamic) {
    p_output_dynamic.reserve(p_steps + 1);

    m_stimulus = (hhn_stimulus *) &p_stimulus;

    const double step = p_time / (double) p_steps;
    const double int_step = step / 10.0;

    initialize_current();

    store_dynamic(0.0, p_output_dynamic);

    double cur_time = step;
    for (std::size_t cur_step = 0; cur_step < p_steps; cur_step++) {
        calculate_states(p_solver, cur_time, step, int_step);

        store_dynamic(cur_time, p_output_dynamic);

        cur_time += step;
    }
}


std::size_t hhn_network::size(void) const {
    return m_peripheral.size();
}


void hhn_network::store_dynamic(const double p_time, hhn_dynamic & p_dynamic) {
    p_dynamic.store(p_time, m_peripheral, m_central);
}


void hhn_network::calculate_states(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step) {
    hhn_states next_peripheral_states(m_peripheral.size());
    calculate_peripheral_states(p_solver, p_time, p_step, p_int_step, next_peripheral_states);

    hhn_states next_central_states(m_central.size());
    calculate_central_states(p_solver, p_time, p_step, p_int_step, next_central_states);

    assign_neuron_states(p_time, p_step, next_peripheral_states, next_central_states);
}


void hhn_network::assign_neuron_states(const double p_time, const double p_step, const hhn_states & p_next_peripheral, const hhn_states & p_next_central) {
    for (std::size_t index = 0; index < m_peripheral.size(); index++) {
        m_peripheral[index].m_membrane_potential      = p_next_peripheral[index][0].state[POSITION_MEMBRAN_POTENTIAL];
        m_peripheral[index].m_active_cond_sodium      = p_next_peripheral[index][0].state[POSITION_ACTIVE_COND_SODIUM];
        m_peripheral[index].m_inactive_cond_sodium    = p_next_peripheral[index][0].state[POSITION_INACTIVE_COND_SODIUM];
        m_peripheral[index].m_active_cond_potassium   = p_next_peripheral[index][0].state[POSITION_ACTIVE_COND_POTASSIUM];

        hhn_oscillator & oscillator = m_peripheral[index];
        if ( (!oscillator.m_pulse_generation) && (oscillator.m_membrane_potential >= 0.0)) {
            oscillator.m_pulse_generation = true;
            oscillator.m_pulse_generation_time.push_back(p_time);
        }
        else if (oscillator.m_membrane_potential < 0.0) {
            oscillator.m_pulse_generation = false;
        }

        if ( (oscillator.m_link_weight3 == 0.0) && (oscillator.m_membrane_potential > m_params.m_threshold) ) {
            oscillator.m_link_pulse_counter += p_step;

            if (oscillator.m_link_pulse_counter >= (1.0 / m_params.m_eps)) {
                oscillator.m_link_weight3 = m_params.m_w3;
                oscillator.m_link_activation_time = p_time;
            }
        }
        else if ( !((oscillator.m_link_activation_time < p_time) && (p_time < oscillator.m_link_activation_time + m_params.m_deltah)) ) {
            oscillator.m_link_weight3 = 0.0;
            oscillator.m_link_pulse_counter = 0.0;
        }
    }


    for (std::size_t index = 0; index < m_central.size(); index++) {
        m_central[index].m_membrane_potential      = p_next_central[index][0].state[POSITION_MEMBRAN_POTENTIAL];
        m_central[index].m_active_cond_sodium      = p_next_central[index][0].state[POSITION_ACTIVE_COND_SODIUM];
        m_central[index].m_inactive_cond_sodium    = p_next_central[index][0].state[POSITION_INACTIVE_COND_SODIUM];
        m_central[index].m_active_cond_potassium   = p_next_central[index][0].state[POSITION_ACTIVE_COND_POTASSIUM];

        central_element & elem = m_central[index];
        if ( (!elem.m_pulse_generation) && (elem.m_membrane_potential >= 0.0) ) {
            elem.m_pulse_generation = true;
            elem.m_pulse_generation_time.push_back(p_time);
        }
        else if (elem.m_membrane_potential < 0.0) {
            elem.m_pulse_generation = false;
        }
    }
}


void hhn_network::calculate_peripheral_states(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step, hhn_states & p_next_states) {
    std::vector<void *> argv(1, nullptr);

    for (std::size_t index = 0; index < m_peripheral.size(); index++) {
        argv[0] = (void *) &index;

        differ_state<double> inputs { 
            m_peripheral[index].m_membrane_potential,
            m_peripheral[index].m_active_cond_sodium,
            m_peripheral[index].m_inactive_cond_sodium,
            m_peripheral[index].m_active_cond_potassium
        };

        perform_calculation(p_solver, p_time, p_step, p_int_step, inputs, argv, p_next_states[index]);
    }
}


void hhn_network::calculate_central_states(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step, hhn_states & p_next_states) {
    std::vector<void *> argv(1, nullptr);

    for (std::size_t index = 0; index < m_central.size(); index++) {
        std::size_t index_central = index + m_peripheral.size();
        argv[0] = (void *) &index_central;

        differ_state<double> inputs { 
            m_central[index].m_membrane_potential,
            m_central[index].m_active_cond_sodium,
            m_central[index].m_inactive_cond_sodium,
            m_central[index].m_active_cond_potassium
        };

        perform_calculation(p_solver, p_time, p_step, p_int_step, inputs, argv, p_next_states[index]);
    }
}


void hhn_network::perform_calculation(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step, const differ_state<double> & p_inputs, const differ_extra<> & p_extra, hhn_state & p_next_states) {
    equation<double> peripheral_equation = std::bind(&hhn_network::neuron_states, this, _1, _2, _3, _4);

    switch(p_solver) {
        case solve_type::FORWARD_EULER: {
            throw std::invalid_argument("Forward Euler first-order method is not supported due to low accuracy.");
        }

        case solve_type::RUNGE_KUTTA_4: {
            std::size_t number_int_steps = (std::size_t) (p_step / p_int_step);
            runge_kutta_4(peripheral_equation, p_inputs, p_time, p_time + p_step, number_int_steps, false, p_extra, p_next_states);
            break;
        }

        case solve_type::RUNGE_KUTTA_FEHLBERG_45: {
            runge_kutta_fehlberg_45(peripheral_equation, p_inputs, p_time, p_time + p_step, 0.00001, false, p_extra, p_next_states);
            break;
        }

        default: {
            throw std::invalid_argument("Specified differential solver is not supported.");
        }
    }
}


void hhn_network::neuron_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) {
    std::size_t index = *(std::size_t *) argv[0];

    double v = inputs[POSITION_MEMBRAN_POTENTIAL];       /* membrane potential (v)                               */
    double m = inputs[POSITION_ACTIVE_COND_SODIUM];      /* activation conductance of the sodium channel (m)     */
    double h = inputs[POSITION_INACTIVE_COND_SODIUM];    /* inactivaton conductance of the sodium channel (h)    */
    double n = inputs[POSITION_ACTIVE_COND_POTASSIUM];   /* activation conductance of the potassium channel (n)  */

    /* Calculate ion current */
    double active_sodium_part = m_params.m_gNa * std::pow(m, 3) * h * (v - m_params.m_vNa);
    double inactive_sodium_part = m_params.m_gK * std::pow(n, 4) * (v - m_params.m_vK);
    double active_potassium_part = m_params.m_gL * (v - m_params.m_vL);

    double Iion = active_sodium_part + inactive_sodium_part + active_potassium_part;

    double Iext = 0.0;
    double Isyn = 0.0;

    /* External and internal currents */
    if (index < size()) {
        Iext = m_peripheral[index].m_Iext;
        Isyn = peripheral_synaptic_current(index, t, v);
    }
    else {
        std::size_t central_index = index - size();
        Iext = m_central[central_index].m_Iext;
        if (central_index == 0) {
            Isyn = central_first_synaptic_current(t, v);
        }
    }

    /* Membrane potential */
    double dv = -Iion + Iext - Isyn;

    /* Calculate variables */
    double potential = v - m_params.m_vRest;
    double am = (2.5 - 0.1 * potential) / (std::exp(2.5 - 0.1 * potential) - 1.0);
    double ah = 0.07 * std::exp(-potential / 20.0);
    double an = (0.1 - 0.01 * potential) / (std::exp(1.0 - 0.1 * potential) - 1.0);

    double bm = 4.0 * std::exp(-potential / 18.0);
    double bh = 1.0 / (std::exp(3.0 - 0.1 * potential) + 1.0);
    double bn = 0.125 * std::exp(-potential / 80.0);

    double dm = am * (1.0 - m) - bm * m;
    double dh = ah * (1.0 - h) - bh * h;
    double dn = an * (1.0 - n) - bn * n;

    outputs = { dv, dm, dh, dn };
}


double hhn_network::peripheral_external_current(const std::size_t p_index) const {
    return (*m_stimulus)[p_index] * (1.0 + 0.01 * generate_uniform_random(-1.0, 1.0));
}


double hhn_network::peripheral_synaptic_current(const std::size_t p_index, const double p_time, const double p_membrane) const {
    double memory_impact1 = 0.0;
    for (auto & pulse_time : m_central[0].m_pulse_generation_time) {
        memory_impact1 += alpha_function(p_time - pulse_time, m_params.m_alfa_inhibitory, m_params.m_betta_inhibitory);
    }

    double memory_impact2 = 0.0;
    for (auto & pulse_time : m_central[1].m_pulse_generation_time) {
        memory_impact2 += alpha_function(p_time - pulse_time, m_params.m_alfa_inhibitory, m_params.m_betta_inhibitory);
    }

    return m_params.m_w2 * (p_membrane - m_params.m_Vsyninh) * memory_impact1 + m_peripheral[p_index].m_link_weight3 * (p_membrane - m_params.m_Vsyninh) * memory_impact2;
}


double hhn_network::central_first_synaptic_current(const double p_time, const double p_membrane) const {
    double memory_impact = 0.0;
    for (std::size_t index_oscillator = 0; index_oscillator < size(); index_oscillator++) {
        for (auto & pulse_time : m_peripheral[index_oscillator].m_pulse_generation_time) {
            memory_impact += alpha_function(p_time - pulse_time, m_params.m_alfa_excitatory, m_params.m_betta_excitatory);
        }
    }

    return m_params.m_w1 * (p_membrane - m_params.m_Vsynexc) * memory_impact;
}


double hhn_network::alpha_function(const double p_time, const double p_alfa, const double p_betta) const {
    return p_alfa * p_time * std::exp(-p_betta * p_time);
}


void hhn_network::initialize_current(void) {
    update_peripheral_current();

    m_central[0].m_Iext = m_params.m_Icn1;
    m_central[1].m_Iext = m_params.m_Icn2;
}


void hhn_network::update_peripheral_current(void) {
    for (std::size_t index = 0; index < m_peripheral.size(); index++) {
        m_peripheral[index].m_Iext = peripheral_external_current(index);
    }
}


}

}