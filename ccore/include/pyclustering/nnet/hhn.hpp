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


#pragma once


#include <fstream>
#include <memory>
#include <ostream>
#include <set>
#include <sstream>
#include <tuple>
#include <vector>
#include <unordered_map>

#include <pyclustering/utils/metric.hpp>
#include <pyclustering/utils/random.hpp>

#include <pyclustering/differential/differ_state.hpp>


using namespace pyclustering::differential;
using namespace pyclustering::utils::random;


namespace pyclustering {

namespace nnet {


struct hnn_parameters {
public:
    double m_nu       = generate_uniform_random(-1.0, 1.0);     /* Intrinsic noise      */

    double m_gNa      = 120.0 * (1.0 + 0.02 * m_nu);    /* Maximal conductivity for sodium current     */
    double m_gK       = 36.0 * (1.0 + 0.02 * m_nu);     /* Maximal conductivity for potassium current  */
    double m_gL       = 0.3 * (1.0 + 0.02 * m_nu);      /* Maximal conductivity for leakage current    */

    double m_vNa      = 50.0;                         /* Reverse potential of sodium current [mV]    */
    double m_vK       = -77.0;                        /* Reverse potential of potassium current [mV] */
    double m_vL       = -54.4;                        /* Reverse potantial of leakage current [mV]   */
    double m_vRest    = -65.0;                        /* Rest potential [mV].                        */

    double m_Icn1     = 5.0;            /* External current [mV] for central element 1   */
    double m_Icn2     = 30.0;           /* External current [mV] for central element 2   */

    double m_Vsyninh          = -80.0;  /* Synaptic reversal potential [mV] for inhibitory effects   */
    double m_Vsynexc          = 0.0;    /* Synaptic reversal potential [mV] for exciting effects     */

    double m_alfa_inhibitory  = 6.0;    /* Alfa-parameter for alfa-function for inhibitory effect    */
    double m_betta_inhibitory = 0.3;    /* Betta-parameter for alfa-function for inhibitory effect   */

    double m_alfa_excitatory  = 40.0;   /* Alfa-parameter for alfa-function for excitatoty effect    */
    double m_betta_excitatory = 2.0;    /* Betta-parameter for alfa-function for excitatoty effect   */

    double m_w1 = 0.1;                  /* Strength of the synaptic connection from PN to CN1 */
    double m_w2 = 9.0;                  /* Strength of the synaptic connection from CN1 to PN */
    double m_w3 = 5.0;                  /* Strength of the synaptic connection from CN2 to PN */

    double m_deltah     = 650.0;        /* Period of time [ms] when high strength value of synaptic connection exists from CN2 to PN */
    double m_threshold  = -10;          /* Threshold of the membrane potential that should exceeded by oscillator to be considered as an active */
    double m_eps        = 0.16;         /* Affects pulse counter */
};



struct basic_neuron_state {
public:
    double m_membrane_potential      = 0.0;     /* Membrane potential of cenral neuron (V)                */
    double m_active_cond_sodium      = 0.0;     /* Activation conductance of the sodium channel (m)       */
    double m_inactive_cond_sodium    = 0.0;     /* Inactivaton conductance of the sodium channel (h)      */
    double m_active_cond_potassium   = 0.0;     /* Activaton conductance of the sodium channel (h)        */

    bool m_pulse_generation         = false;            /* Spike generation of central neuron   */
    std::vector<double> m_pulse_generation_time = { };  /* Timestamps of generated pulses       */

    double m_Iext   = 0.0;
};


struct central_element : public basic_neuron_state { };



struct hhn_oscillator : public basic_neuron_state {
    double m_link_activation_time     = 0.0;
    double m_link_pulse_counter       = 0.0;
    double m_link_deactivation_time   = 0.0;
    double m_link_weight3             = 0.0;
};



class hhn_dynamic {
public:
    enum class collect {
        MEMBRANE_POTENTIAL,
        ACTIVE_COND_SODIUM,
        INACTIVE_COND_SODIUM,
        ACTIVE_COND_POTASSIUM,
    };

    struct collect_hash {
        std::size_t operator()(hhn_dynamic::collect t) const
        {
            return static_cast<std::size_t>(t);
        }
    };


public:
    using ptr                 = std::shared_ptr<hhn_dynamic>;

    using value_dynamic       = std::vector<double>;
    using value_dynamic_ptr   = std::shared_ptr<value_dynamic>;

    using evolution_dynamic   = std::vector<value_dynamic>;

    using network_collector   = std::unordered_map<hhn_dynamic::collect, bool, hhn_dynamic::collect_hash>;

    using network_dynamic     = std::unordered_map<hhn_dynamic::collect, evolution_dynamic, hhn_dynamic::collect_hash>;
    using network_dynamic_ptr = std::shared_ptr<network_dynamic>;


private:
    network_collector   m_enable =
        { { collect::MEMBRANE_POTENTIAL,    true  },
          { collect::ACTIVE_COND_SODIUM,    false },
          { collect::INACTIVE_COND_SODIUM,  false },
          { collect::ACTIVE_COND_POTASSIUM, false } };

    std::size_t         m_amount_collections  = 1;
    std::size_t         m_size_dynamic        = 0;
    std::size_t         m_size_network        = 0;

    network_dynamic_ptr m_peripheral_dynamic  = std::make_shared<network_dynamic>();
    network_dynamic_ptr m_central_dynamic     = std::make_shared<network_dynamic>();

    value_dynamic_ptr   m_time                = std::make_shared<value_dynamic>();


public:
    hhn_dynamic();

    ~hhn_dynamic() = default;

public:
    std::size_t size_dynamic() const;

    std::size_t size_network() const;

    void enable(const hhn_dynamic::collect p_state);

    template <class ContainerType>
    void enable(const ContainerType & p_types);

    void enable_all();

    void disable(const hhn_dynamic::collect p_state);

    template <class ContainerType>
    void disable(const ContainerType & p_types);

    void disable_all();

    void get_enabled(std::set<hhn_dynamic::collect> & p_enabled) const;

    void get_disabled(std::set<hhn_dynamic::collect> & p_disabled) const;

    void store(const double p_time, const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central);

    void reserve(const std::size_t p_dynamic_size);

    evolution_dynamic & get_peripheral_dynamic(const hhn_dynamic::collect & p_type);

    network_dynamic_ptr get_peripheral_dynamic() const;

    network_dynamic_ptr get_central_dynamic() const;

    value_dynamic_ptr get_time() const;

    evolution_dynamic & get_central_dynamic(const hhn_dynamic::collect & p_type);

    double get_peripheral_value(const std::size_t p_iteration, const std::size_t p_index, const hhn_dynamic::collect p_type) const;

    double get_central_value(const std::size_t p_iteration, const std::size_t p_index, const hhn_dynamic::collect p_type) const;


private:
    void get_collected_types(const bool p_enabled, std::set<hhn_dynamic::collect> & p_types) const;

    void reserve_collection(const hhn_dynamic::collect p_state, const std::size_t p_size);

    void store_membrane_potential(const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central);

    void store_active_cond_sodium(const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central);

    void store_inactive_cond_sodium(const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central);

    void store_active_cond_potassium(const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central);

    static void reserve_dynamic_collection(const hhn_dynamic::collect p_state, const std::size_t p_size, network_dynamic & p_dynamic);

    static void initialize_collection(network_dynamic & p_dynamic);

public:
    bool operator==(const hhn_dynamic & p_other) const;

    friend std::ostream& operator<<(std::ostream & p_stream, const hhn_dynamic & p_dynamic);
};


template <class ContainerType>
void hhn_dynamic::enable(const ContainerType & p_types) {
    for (auto & type : p_types) {
        enable(type);
    }
}


template <class ContainerType>
void hhn_dynamic::disable(const ContainerType & p_types) {
    for (auto & type : p_types) {
        disable(type);
    }
}



class hhn_dynamic_reader {
private:
    std::string     m_filename;

    hhn_dynamic *                       m_dynamic       = nullptr;
    std::ifstream                       m_file_stream;
    std::vector<hhn_dynamic::collect>   m_order         = { };
    std::size_t                         m_size_network  = 0;

public:
    hhn_dynamic_reader() = default;

    explicit hhn_dynamic_reader(const std::string & p_filename);

    ~hhn_dynamic_reader();

public:
    void read(hhn_dynamic & p_dynamic);

private:
    void parse_size_header();

    void parse_enable_header();

    void parse_dynamic();

    void extract_dynamic(const std::string & p_line, double & p_time, std::vector<hhn_oscillator> & p_peripheral, std::vector<central_element> & p_central);

    void extract_state(std::istringstream & p_stream, basic_neuron_state & p_state) const;

    static void extract_size_header(const std::string & p_line, std::size_t & p_size_dynamic, std::size_t & p_size_network);

    static void extract_enable_header(const std::string & p_line, std::vector<hhn_dynamic::collect> & p_collect);
};



using hhn_stimulus        = std::vector<double>;



class hhn_network {
private:
    enum: std::size_t {
        POSITION_MEMBRAN_POTENTIAL = 0,
        POSITION_ACTIVE_COND_SODIUM,
        POSITION_INACTIVE_COND_SODIUM,
        POSITION_ACTIVE_COND_POTASSIUM,
        POSITION_AMOUNT
    };

private:
    using hhn_state           = differ_result<double>;
    using hhn_states          = std::vector< hhn_state >;

private:
    std::vector<hhn_oscillator>   m_peripheral  = { };

    std::vector<central_element>  m_central     = { };

    hhn_stimulus *                m_stimulus    = nullptr;

    hnn_parameters                m_params;

public:
    hhn_network() = default;

    hhn_network(const std::size_t      p_size,
                const hnn_parameters & p_parameters);

    ~hhn_network() = default;

public:
    void simulate(const std::size_t         p_steps,
                  const double              p_time,
                  const solve_type          p_solver,
                  const hhn_stimulus &      p_stimulus,
                  hhn_dynamic &             p_output_dynamic);

    std::size_t size() const;

private:
    void store_dynamic(const double p_time, hhn_dynamic & p_dynamic);

    void calculate_states(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step);

    void calculate_peripheral_states(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step, hhn_states & p_next_states);

    void calculate_central_states(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step, hhn_states & p_next_states);

    void perform_calculation(const solve_type p_solver, const double p_time, const double p_step, const double p_int_step, const differ_state<double> & p_inputs, const differ_extra<> & p_extra, hhn_state & p_next_states);

    void neuron_states(const double t, const differ_state<double> & inputs, const differ_extra<void *> & argv, differ_state<double> & outputs) const;

    double peripheral_external_current(const std::size_t p_index) const;

    double peripheral_synaptic_current(const std::size_t p_index, const double p_time, const double p_membrane) const;

    double central_first_synaptic_current(const double p_time, const double p_membrane) const;

    void initialize_current();

    void update_peripheral_current();

    void assign_neuron_states(const double p_time, const double p_step, const hhn_states & p_next_peripheral, const hhn_states & p_next_central);

    static double alpha_function(const double p_time, const double p_alfa, const double p_betta);

    template <class NeuronType>
    static void pack_equation_input(const NeuronType & p_neuron, differ_state<double> & p_inputs);

    template <class NeuronType>
    static void unpack_equation_output(const hhn_state & p_outputs, NeuronType & p_neuron);
};


template <class NeuronType>
void hhn_network::pack_equation_input(const NeuronType & p_neuron, differ_state<double> & p_inputs) {
    p_inputs.resize(POSITION_AMOUNT);
    p_inputs[POSITION_MEMBRAN_POTENTIAL]      = p_neuron.m_membrane_potential;
    p_inputs[POSITION_ACTIVE_COND_SODIUM]     = p_neuron.m_active_cond_sodium;
    p_inputs[POSITION_INACTIVE_COND_SODIUM]   = p_neuron.m_inactive_cond_sodium;
    p_inputs[POSITION_ACTIVE_COND_POTASSIUM]  = p_neuron.m_active_cond_potassium;
}


template <class NeuronType>
void hhn_network::unpack_equation_output(const hhn_state & p_outputs, NeuronType & p_neuron) {
    p_neuron.m_membrane_potential      = p_outputs[0].state[POSITION_MEMBRAN_POTENTIAL];
    p_neuron.m_active_cond_sodium      = p_outputs[0].state[POSITION_ACTIVE_COND_SODIUM];
    p_neuron.m_inactive_cond_sodium    = p_outputs[0].state[POSITION_INACTIVE_COND_SODIUM];
    p_neuron.m_active_cond_potassium   = p_outputs[0].state[POSITION_ACTIVE_COND_POTASSIUM];
}


}

}
