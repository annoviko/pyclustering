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


#include "hhn.hpp"


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


hhn_dynamic::network_dynamic_ptr hhn_dynamic::get_peripheral_dynamic(void) const {
    return m_peripheral_dynamic;
}


hhn_dynamic::network_dynamic_ptr hhn_dynamic::get_central_dynamic(void) const {
    return m_central_dynamic;
}


void hhn_dynamic::reserve_collection(const hhn_dynamic::collect p_state, const std::size_t p_size) {
    m_peripheral_dynamic->at(p_state).reserve(p_size);
    m_peripheral_dynamic->at(p_state).reserve(p_size);
    m_time->reserve(p_size);
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



hhn_network::hhn_network(const std::size_t p_size, const hnn_parameters p_parameters) :
    m_peripheral(p_size),
    m_central(p_size),
    m_stimulus(nullptr),
    m_parameters(p_parameters)
{ }


void hhn_network::simulate(const std::size_t p_steps, const double p_time, const solve_type p_solver, const hhn_stimulus_ptr & p_stimulus, hhn_dynamic & p_output_dynamic) {
    p_output_dynamic.reserve(p_steps + 1);  /* initial state is not taken into account */

    m_stimulus = p_stimulus;

    const double step = p_time / (double) p_steps;
    const double int_step = step / 10.0;

    store_dynamic(0.0, p_output_dynamic);

    for (double cur_time = step; cur_time < p_time; cur_time += step) {
        calculate_states(p_solver, cur_time, step, int_step);
    }
}


size_t hhn_network::size(void) const {
    return m_peripheral.size();
}


void hhn_network::store_dynamic(const double p_time, hhn_dynamic & p_dynamic) {
    p_dynamic.store(p_time, m_peripheral, m_central);
}


void hhn_network::calculate_states(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step) {
    (void) p_solver;
    (void) p_time;
    (void) p_step;
    (void) p_int_step;

    /* Wait for refactoring of differential part */
}