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


#include <pyclustering/nnet/hhn.hpp>

#include <pyclustering/differential/differ_state.hpp>
#include <pyclustering/differential/runge_kutta_4.hpp>
#include <pyclustering/differential/runge_kutta_fehlberg_45.hpp>
#include <pyclustering/parallel/parallel.hpp>


using namespace std::placeholders;



namespace pyclustering {

namespace nnet {


hhn_dynamic::hhn_dynamic() {
    initialize_collection(*m_peripheral_dynamic);
    initialize_collection(*m_central_dynamic);
}


std::size_t hhn_dynamic::size_dynamic() const {
    return m_size_dynamic;
}


std::size_t hhn_dynamic::size_network() const {
    return m_size_network;
}


void hhn_dynamic::enable(const hhn_dynamic::collect p_state) {
    if (m_enable[p_state] != true) {
        m_enable[p_state] = true;
        m_amount_collections++;
    }
}


void hhn_dynamic::enable_all() {
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


void hhn_dynamic::disable_all() {
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

    if (m_size_network != 0) {
        if (m_size_network != p_peripheral.size()) {
            throw std::invalid_argument("Amount of neurons on each iteration should be the same.");
        }
    }
    else {
        m_size_network = p_peripheral.size();
    }

    m_size_dynamic++;
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


hhn_dynamic::network_dynamic_ptr hhn_dynamic::get_peripheral_dynamic() const {
    return m_peripheral_dynamic;
}


hhn_dynamic::evolution_dynamic & hhn_dynamic::get_central_dynamic(const hhn_dynamic::collect & p_type) {
    return (*m_central_dynamic)[p_type];
}


hhn_dynamic::network_dynamic_ptr hhn_dynamic::get_central_dynamic() const {
    return m_central_dynamic;
}


hhn_dynamic::value_dynamic_ptr hhn_dynamic::get_time() const {
    return m_time;
}


double hhn_dynamic::get_peripheral_value(const std::size_t p_iteration, const std::size_t p_index, const hhn_dynamic::collect p_type) const {
    return (*m_peripheral_dynamic)[p_type][p_iteration][p_index];
}


double hhn_dynamic::get_central_value(const std::size_t p_iteration, const std::size_t p_index, const hhn_dynamic::collect p_type) const {
    return (*m_central_dynamic)[p_type][p_iteration][p_index];
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


bool hhn_dynamic::operator==(const hhn_dynamic & p_other) const {
    if ( (m_amount_collections == p_other.m_amount_collections) &&
         (*m_peripheral_dynamic == *(p_other.m_peripheral_dynamic)) &&
         (*m_central_dynamic == *(p_other.m_central_dynamic)) &&
         (*m_time == *(p_other.m_time)) )
    {
        return true;
    }

    return false;
}


std::ostream& operator<<(std::ostream & p_stream, const hhn_dynamic & p_dynamic) {
    const hhn_dynamic::network_dynamic_ptr peripheral = p_dynamic.get_peripheral_dynamic();
    const hhn_dynamic::network_dynamic_ptr central = p_dynamic.get_central_dynamic();

    std::set<hhn_dynamic::collect> enabled;
    p_dynamic.get_enabled(enabled);

    const std::vector<hhn_dynamic::collect> order_types = {
            hhn_dynamic::collect::MEMBRANE_POTENTIAL,
            hhn_dynamic::collect::ACTIVE_COND_SODIUM,
            hhn_dynamic::collect::INACTIVE_COND_SODIUM,
            hhn_dynamic::collect::ACTIVE_COND_POTASSIUM
    };

    p_stream << p_dynamic.size_dynamic() << " " << p_dynamic.size_network() << "\n";
    for (std::size_t index_order = 0; index_order < order_types.size(); index_order++) {
        if (enabled.find(order_types[index_order]) != enabled.cend()) {
            p_stream << index_order << " ";
        }
    }
    p_stream << "\n";

    for (std::size_t iter = 0; iter < p_dynamic.size_dynamic(); iter++) {
        p_stream << p_dynamic.get_time()->at(iter);
        for (std::size_t neuron_index = 0; neuron_index < p_dynamic.size_network() + 2; neuron_index++) {
            p_stream << " [ ";

            for (auto & type : order_types) {
                if (enabled.find(type) == enabled.cend()) {
                    continue;
                }

                if (neuron_index < p_dynamic.size_network()) {
                    p_stream << p_dynamic.get_peripheral_value(iter, neuron_index, type) << " ";
                }
                else {
                    std::size_t central_index = neuron_index - p_dynamic.size_network();
                    p_stream << p_dynamic.get_central_value(iter, central_index, type) << " ";
                }
            }

            p_stream << "]";
        }

        p_stream << "\n";
    }

    return p_stream;
}



hhn_dynamic_reader::hhn_dynamic_reader(const std::string & p_filename) :
        m_filename(p_filename),
        m_dynamic(nullptr),
        m_file_stream()
{ }


hhn_dynamic_reader::~hhn_dynamic_reader() {
    if (m_file_stream.is_open()) {
        m_file_stream.close();
    }
}


void hhn_dynamic_reader::read(hhn_dynamic & p_dynamic) {
    m_file_stream.open(m_filename.c_str(), std::ifstream::in);
    m_dynamic = &p_dynamic;

    parse_size_header();
    parse_enable_header();
    parse_dynamic();

    m_file_stream.close();
}


void hhn_dynamic_reader::parse_size_header() {
    std::string line;
    std::size_t dynamic_size, dynamic_network;

    std::getline(m_file_stream, line);
    extract_size_header(line, dynamic_size, dynamic_network);

    m_size_network = dynamic_network;
    m_dynamic->reserve(dynamic_size);
}


void hhn_dynamic_reader::extract_size_header(const std::string & p_line, std::size_t & p_size_dynamic, std::size_t & p_size_network) {
    std::istringstream string_stream(p_line);
    std::string item;

    if (!std::getline(string_stream, item, ' ')) {
        throw std::invalid_argument("Impossible parse size dynamic from line header: " + p_line);
    }

    p_size_dynamic = (std::size_t) std::stoll(item);

    if (!std::getline(string_stream, item, '\n')) {
        throw std::invalid_argument("Impossible parse size network from line header: " + p_line);
    }

    p_size_network = (std::size_t) std::stoll(item);
}


void hhn_dynamic_reader::parse_enable_header() {
    std::string line;

    std::getline(m_file_stream, line);

    extract_enable_header(line, m_order);

    m_dynamic->disable_all();
    m_dynamic->enable(m_order);
}


void hhn_dynamic_reader::extract_enable_header(const std::string & p_line, std::vector<hhn_dynamic::collect> & p_collect) {
    std::istringstream string_stream(p_line);
    std::string item;
    while (std::getline(string_stream, item, ' ')) {
        /* Each collection type has whitespace after itself */
        p_collect.push_back((hhn_dynamic::collect) std::stoll(item));
    }
}


void hhn_dynamic_reader::parse_dynamic() {
    for (std::string line; std::getline(m_file_stream, line); ) {
        double time = -1;
        std::vector<hhn_oscillator>     peripheral = { };
        std::vector<central_element>    central    = { };

        extract_dynamic(line, time, peripheral, central);

        m_dynamic->store(time, peripheral, central);
    }
}


void hhn_dynamic_reader::extract_dynamic(const std::string & p_line, double & p_time, std::vector<hhn_oscillator> & p_peripheral, std::vector<central_element> & p_central) {
    std::istringstream string_stream(p_line);
    std::string item;

    p_peripheral.resize(m_size_network);
    p_central.resize(2);

    std::size_t counter_filling = p_peripheral.size() + 2;

    std::getline(string_stream, item, ' ');
    p_time = std::stod(item);

    bool extract_status = (bool) std::getline(string_stream, item, ' ');
    for (std::size_t item_index = 0; extract_status; item_index++) {
        if (item == "[") {
            if (item_index < p_peripheral.size()) {
                extract_state(string_stream, p_peripheral[item_index]);
            }
            else {
                std::size_t index_central = item_index - p_peripheral.size();
                extract_state(string_stream, p_central[index_central]);
            }
        }

        counter_filling--;

        extract_status = (bool) std::getline(string_stream, item, ' ');
        if (!extract_status) {
            extract_status = (bool) std::getline(string_stream, item, '\n');
        }
    }

    if (counter_filling != 0) {
        throw std::invalid_argument("Incorrect format of HHN output dynamic: not all neuron states are found.");
    }
}


void hhn_dynamic_reader::extract_state(std::istringstream & p_stream, basic_neuron_state & p_state) const {
    std::string item;
    for (std::size_t item_index = 0; std::getline(p_stream, item, ' '); item_index++) {
        if (item == "]") {
            return;
        }

        hhn_dynamic::collect type_value = m_order[item_index];
        switch(type_value) {
            case hhn_dynamic::collect::MEMBRANE_POTENTIAL:
                p_state.m_membrane_potential = std::stod(item);
                break;
            case hhn_dynamic::collect::ACTIVE_COND_SODIUM:
                p_state.m_active_cond_sodium = std::stod(item);
                break;
            case hhn_dynamic::collect::INACTIVE_COND_SODIUM:
                p_state.m_inactive_cond_sodium = std::stod(item);
                break;
            case hhn_dynamic::collect::ACTIVE_COND_POTASSIUM:
                p_state.m_active_cond_potassium = std::stod(item);
                break;
            default:
                throw std::invalid_argument("Invalid type of value is detected '" + std::to_string((std::size_t) type_value) + "'");
        }
    }
}



hhn_network::hhn_network(const std::size_t p_size, const hnn_parameters & p_parameters) :
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

    double cur_time = 0.0;
    for (std::size_t cur_step = 0; cur_step < p_steps; cur_step++) {
        calculate_states(p_solver, cur_time, step, int_step);

        cur_time += step;

        store_dynamic(cur_time + step, p_output_dynamic);

        update_peripheral_current();
    }
}


std::size_t hhn_network::size() const {
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
        hhn_oscillator & oscillator = m_peripheral[index];

        unpack_equation_output(p_next_peripheral[index], oscillator);

        if (!oscillator.m_pulse_generation) {
            if (oscillator.m_membrane_potential >= 0.0) {
                oscillator.m_pulse_generation = true;
                oscillator.m_pulse_generation_time.push_back(p_time);
            }
        }
        else if (oscillator.m_membrane_potential < 0.0) {
            oscillator.m_pulse_generation = false;
        }

        if (oscillator.m_link_weight3 == 0.0) {
            if (oscillator.m_membrane_potential >= m_params.m_threshold) {
                oscillator.m_link_pulse_counter += p_step;

                if (oscillator.m_link_pulse_counter >= (1.0 / m_params.m_eps)) {
                    oscillator.m_link_weight3 = m_params.m_w3;
                    oscillator.m_link_activation_time = p_time;
                }
            }
        }
        else if ( !((oscillator.m_link_activation_time < p_time) && (p_time < oscillator.m_link_activation_time + m_params.m_deltah)) ) {
            oscillator.m_link_weight3 = 0.0;
            oscillator.m_link_pulse_counter = 0.0;
        }
    }

    for (std::size_t index = 0; index < m_central.size(); index++) {
        unpack_equation_output(p_next_central[index], m_central[index]);

        central_element & elem = m_central[index];
        if (!elem.m_pulse_generation) {
            if (elem.m_membrane_potential >= 0.0) {
                elem.m_pulse_generation = true;
                elem.m_pulse_generation_time.push_back(p_time);
            }
        }
        else if (elem.m_membrane_potential < 0.0) {
            elem.m_pulse_generation = false;
        }
    }
}


void hhn_network::calculate_peripheral_states(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step, hhn_states & p_next_states) {
    parallel::parallel_for(std::size_t(0), m_peripheral.size(), [this, &p_solver, p_time, p_step, p_int_step, &p_next_states](const std::size_t p_index) {
        std::vector<void *> argv(1, nullptr);
        argv[0] = (void *) p_index;

        differ_state<double> inputs;
        pack_equation_input(m_peripheral[p_index], inputs);

        perform_calculation(p_solver, p_time, p_step, p_int_step, inputs, argv, p_next_states[p_index]);
    });
}


void hhn_network::calculate_central_states(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step, hhn_states & p_next_states) {
    parallel::parallel_for(std::size_t(0), m_central.size(), [this, &p_solver, p_time, p_step, p_int_step, &p_next_states](const std::size_t p_index) {
        std::vector<void *> argv(1, nullptr);

        std::size_t index_central = p_index + m_peripheral.size();
        argv[0] = (void *) index_central;

        differ_state<double> inputs;
        pack_equation_input(m_central[p_index], inputs);

        perform_calculation(p_solver, p_time, p_step, p_int_step, inputs, argv, p_next_states[p_index]);
    });
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


void hhn_network::neuron_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) const {
    std::size_t index = (std::size_t) argv[0];

    double v = inputs[POSITION_MEMBRAN_POTENTIAL];       /* membrane potential (v)                               */
    double m = inputs[POSITION_ACTIVE_COND_SODIUM];      /* activation conductance of the sodium channel (m)     */
    double h = inputs[POSITION_INACTIVE_COND_SODIUM];    /* inactivaton conductance of the sodium channel (h)    */
    double n = inputs[POSITION_ACTIVE_COND_POTASSIUM];   /* activation conductance of the potassium channel (n)  */

    /* Calculate ion current */
    double active_sodium_part = m_params.m_gNa * std::pow(m, 3.0) * h * (v - m_params.m_vNa);
    double inactive_sodium_part = m_params.m_gK * std::pow(n, 4.0) * (v - m_params.m_vK);
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
    double am = (2.5 - 0.1 * potential) / (std::expm1(2.5 - 0.1 * potential)); /* 'exp(x) - 1' can be replaced by 'expm1(x)' */
    double ah = 0.07 * std::exp(-potential / 20.0);
    double an = (0.1 - 0.01 * potential) / (std::expm1(1.0 - 0.1 * potential)); /* 'exp(x) - 1' can be replaced by 'expm1(x)' */

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


double hhn_network::alpha_function(const double p_time, const double p_alfa, const double p_betta) {
    return p_alfa * p_time * std::exp(-p_betta * p_time);
}


void hhn_network::initialize_current() {
    update_peripheral_current();

    m_central[0].m_Iext = m_params.m_Icn1;
    m_central[1].m_Iext = m_params.m_Icn2;
}


void hhn_network::update_peripheral_current() {
    for (std::size_t index = 0; index < m_peripheral.size(); index++) {
        m_peripheral[index].m_Iext = peripheral_external_current(index);
    }
}


}

}
