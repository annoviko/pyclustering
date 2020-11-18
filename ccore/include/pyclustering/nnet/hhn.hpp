/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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


/*!

@class  hnn_parameters hhn.hpp pyclustering/nnet/hhn.hpp

@brief  Defines parameters of Hodgkin-Hixley Oscillatory Network.

*/
struct hnn_parameters {
public:
    double m_nu       = generate_uniform_random(-1.0, 1.0);     /**< Intrinsic noise.      */

    double m_gNa      = 120.0 * (1.0 + 0.02 * m_nu);    /**< Maximal conductivity for sodium current.     */
    double m_gK       = 36.0 * (1.0 + 0.02 * m_nu);     /**< Maximal conductivity for potassium current.  */
    double m_gL       = 0.3 * (1.0 + 0.02 * m_nu);      /**< Maximal conductivity for leakage current.    */

    double m_vNa      = 50.0;                         /**< Reverse potential of sodium current [mV].    */
    double m_vK       = -77.0;                        /**< Reverse potential of potassium current [mV]. */
    double m_vL       = -54.4;                        /**< Reverse potantial of leakage current [mV].   */
    double m_vRest    = -65.0;                        /**< Rest potential [mV].                        */

    double m_Icn1     = 5.0;            /**< External current [mV] for central element 1.   */
    double m_Icn2     = 30.0;           /**< External current [mV] for central element 2.   */

    double m_Vsyninh          = -80.0;  /**< Synaptic reversal potential [mV] for inhibitory effects.   */
    double m_Vsynexc          = 0.0;    /**< Synaptic reversal potential [mV] for exciting effects.     */

    double m_alfa_inhibitory  = 6.0;    /**< Alfa-parameter for alfa-function for inhibitory effect.    */
    double m_betta_inhibitory = 0.3;    /**< Betta-parameter for alfa-function for inhibitory effect.   */

    double m_alfa_excitatory  = 40.0;   /**< Alfa-parameter for alfa-function for excitatoty effect.    */
    double m_betta_excitatory = 2.0;    /**< Betta-parameter for alfa-function for excitatoty effect.   */

    double m_w1 = 0.1;                  /**< Strength of the synaptic connection from PN to CN1. */
    double m_w2 = 9.0;                  /**< Strength of the synaptic connection from CN1 to PN. */
    double m_w3 = 5.0;                  /**< Strength of the synaptic connection from CN2 to PN. */

    double m_deltah     = 650.0;        /**< Period of time [ms] when high strength value of synaptic connection exists from CN2 to PN. */
    double m_threshold  = -10;          /**< Threshold of the membrane potential that should exceeded by oscillator to be considered as an active. */
    double m_eps        = 0.16;         /**< Devider of pulse threshold counter `1.0 / eps`. */
};


/*!

@class  basic_neuron_state hhn.hpp pyclustering/nnet/hhn.hpp

@brief  Basic state (applicable for central and peripheral oscillators) of a neuron in Hodgkin-Hixley Oscillatory Network.

*/
struct basic_neuron_state {
public:
    double m_membrane_potential      = 0.0;     /**< Membrane potential of cenral neuron (V).                */
    double m_active_cond_sodium      = 0.0;     /**< Activation conductance of the sodium channel (m).       */
    double m_inactive_cond_sodium    = 0.0;     /**< Inactivaton conductance of the sodium channel (h).      */
    double m_active_cond_potassium   = 0.0;     /**< Activaton conductance of the sodium channel (h).        */

    bool m_pulse_generation         = false;            /**< Spike generation of central neuron.   */
    std::vector<double> m_pulse_generation_time = { };  /**< Timestamps of generated pulses.       */

    double m_Iext   = 0.0;      /**< External current [mV] for neuron.       */
};


/*!

@class      central_element hhn.hpp pyclustering/nnet/hhn.hpp

@brief      Defines a state of the central neuron that is based on Hodgkin-Huxley model.

*/
struct central_element : public basic_neuron_state { };


/*!

@class      hhn_oscillator hhn.hpp pyclustering/nnet/hhn.hpp

@brief      Defines a state of the peripheral neuron that is based on Hodgkin-Huxley model.

*/
struct hhn_oscillator : public basic_neuron_state {
    double m_link_activation_time     = 0.0;    /**< The onset time of plasticity. */
    double m_link_pulse_counter       = 0.0;    /**< The iteration counter of the spike duration. */
    double m_link_weight3             = 0.0;    /**< The modifiable GABAergic connection strength from Central Neuron 2 to the i-th peripheral neuron, representing the short-term plasticity. */
};



/*!

@class      hhn_dynamic hhn.hpp pyclustering/nnet/hhn.hpp

@brief      Output dynamic of the oscillatory network based on HHN.
@details    The output dynamic is a container that stores state of each neuron in the network on each simulation step.

*/
class hhn_dynamic {
public:
    /*!
    
    @brief  Defines what kind of information can be collected and stored by the dynamic.

    */
    enum class collect {
        MEMBRANE_POTENTIAL,     /**< Neuron's membrane potential.                       */
        ACTIVE_COND_SODIUM,     /**< Activation conductance of the sodium channel.      */
        INACTIVE_COND_SODIUM,   /**< Inactivaton conductance of the sodium channel.     */
        ACTIVE_COND_POTASSIUM,  /**< Activaton conductance of the sodium channel.       */
    };

    /*!

    @brief  Defines hash calculation for `hhn_dynamic::collect` type.

    @see hhn_dynamic::collect

    */
    struct collect_hash {
        /*!

        @brief      Calculates hash of the output dynamic component (membrane potential, conductance of the sodium channel, etc.).

        @param[in] t: output dynamic component value for that hash should be calculated.

        @returns    Hash value of the output dynamic component.

        */
        std::size_t operator()(hhn_dynamic::collect t) const
        {
            return static_cast<std::size_t>(t);
        }
    };


public:
    /*!
    
    @brief  Defines shared pointer to the output dynamic of the HHN.
    
    */
    using ptr                 = std::shared_ptr<hhn_dynamic>;

    /*!

    @brief  Defines container to store specific state of each neuron of the HHN.

    */
    using value_dynamic       = std::vector<double>;

    /*!

    @brief  Defines shared pointer to the container to store state of each neuron of the HHN.

    */
    using value_dynamic_ptr   = std::shared_ptr<value_dynamic>;

    /*!

    @brief  Defines containers to store simulation process where specific state of each neuron on each iteration is stored.

    */
    using evolution_dynamic   = std::vector<value_dynamic>;

    /*!

    @brief  Filter that defines what kind of states should be collected (membrane potential, conductance of the sodium channel, etc.).

    */
    using network_collector   = std::unordered_map<hhn_dynamic::collect, bool, hhn_dynamic::collect_hash>;

    /*!

    @brief  Defines container to store the evolution of neurons per state type.
    @details The container is represented by a associative container where the key is a state that is collected and
              the value is a evolution of neurons that corresponds to the state.

    */
    using network_dynamic     = std::unordered_map<hhn_dynamic::collect, evolution_dynamic, hhn_dynamic::collect_hash>;

    /*!

    @brief  Defines shared pointer to the network dynamic - container to store the evolution of neurons per state type.

    */
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
    /*!

    @brief  Default constructor of the output dynamic of the HHN.

    */
    hhn_dynamic();

    /*!

    @brief  Default destructor of the output dynamic of the HHN.

    */
    ~hhn_dynamic() = default;

public:
    /*!

    @brief  Returns amount of stored simulation steps (iterations).

    @return Amount of stored simulation steps (iterations).

    */
    std::size_t size_dynamic() const;

    /*!

    @brief  Returns amount of neurons in the network whose output dynamic was stored in the current output dynamic object.

    @return Amount of neurons in the HHN network.

    */
    std::size_t size_network() const;

    /*!

    @brief  Enable collecting of the specific output dynamic component for each neuron (membrane potential, conductance of the sodium channel, etc.).

    @param[in] p_state: output dynamic component that should be collected for each neuron.

    */
    void enable(const hhn_dynamic::collect p_state);

    /*!

    @brief  Enable collecting of a set of output dynamic components for each neuron (membrane potential, conductance of the sodium channel, etc.).

    @param[in] p_types: iterable container that contains output dynamic components that should be collected for each neuron.

    */
    template <class ContainerType>
    void enable(const ContainerType & p_types);

    /*!

    @brief  Enable collecting of all possible output dynamic components for each neuron (membrane potential, conductance of the sodium channel, etc.).

    */
    void enable_all();

    /*!

    @brief  Disable collecting of the specific output dynamic component for each neuron (membrane potential, conductance of the sodium channel, etc.).

    @param[in] p_state: output dynamic component that should not be collected for each neuron.

    */
    void disable(const hhn_dynamic::collect p_state);

    /*!

    @brief  Disable collecting of a set of output dynamic components for each neuron (membrane potential, conductance of the sodium channel, etc.).

    @param[in] p_types: iterable container that contains output dynamic components that should not be collected for each neuron.

    */
    template <class ContainerType>
    void disable(const ContainerType & p_types);

    /*!

    @brief  Disable collecting of all possible output dynamic components for each neuron (membrane potential, conductance of the sodium channel, etc.).

    */
    void disable_all();

    /*!
    
    @brief  Returns collecting neuron states (membrane potential, conductance of the sodium channel, etc.).

    @param[out] p_enabled: a container where collecting states are going to be placed.
    
    */
    void get_enabled(std::set<hhn_dynamic::collect> & p_enabled) const;

    /*!

    @brief  Returns neurons states that are not collected (membrane potential, conductance of the sodium channel, etc.).

    @param[out] p_disabled: a container where non-collecting states are going to be placed.

    */
    void get_disabled(std::set<hhn_dynamic::collect> & p_disabled) const;

    /*!

    @brief  Stores current state of the oscillatory network that is defined by timestamp, peripheral and central neurons.

    @param[in] p_time: current simulation time.
    @param[in] p_peripheral: container with states of peripheral neurons.
    @param[in] p_central: container with states of central neurons.

    */
    void store(const double p_time, const std::vector<hhn_oscillator> & p_peripheral, const std::vector<central_element> & p_central);

    /*!

    @brief  Reserves memory for the evolution that is defined by amount of iterations for simulation.

    @param[in] p_dynamic_size: size of the dynamic evolution.

    */
    void reserve(const std::size_t p_dynamic_size);

    /*!

    @brief  Returns dynamic of peripheral neurons for the specified state (membrane potential, conductance of the sodium channel, etc.).

    @param[in] p_type: state of neuron for which evolution is required.

    @return Dynamic of peripheral neurons for the specified state.

    */
    evolution_dynamic & get_peripheral_dynamic(const hhn_dynamic::collect & p_type);

    /*!

    @brief  Returns full dynamic of peripheral neurons.

    @return Full dynamic of peripheral neurons.

    */
    network_dynamic_ptr get_peripheral_dynamic() const;

    /*!

    @brief  Returns full dynamic of central neurons.

    @returns Full dynamic of central neurons.

    */
    network_dynamic_ptr get_central_dynamic() const;

    /*!

    @brief  Returns all timestamps of simulation process of the oscillatory network.

    @return All timestamps of simulation process of the oscillatory network.

    */
    value_dynamic_ptr get_time() const;

    /*!

    @brief  Returns dynamic of central neurons for the specified state (membrane potential, conductance of the sodium channel, etc.).

    @param[in] p_type: neuron state for which evolution is required.

    @return Dynamic of central neurons for the specified state.

    */
    evolution_dynamic & get_central_dynamic(const hhn_dynamic::collect & p_type);

    /*!

    @brief  Returns state value for specific peripheral neuron on specified iteration.

    @param[in] p_iteration: iteration of simulation process of the oscillatory network.
    @param[in] p_index: neuron index in the oscillatory network.
    @param[in] p_type: neuron state value type (membrane potential, conductance of the sodium channel, etc.).

    @return State value for specific peripheral neuron on specified iteration.

    */
    double get_peripheral_value(const std::size_t p_iteration, const std::size_t p_index, const hhn_dynamic::collect p_type) const;

    /*!

    @brief  Returns state value for specific central neuron on specified iteration.
    @details The oscillatory network always has only two central neurons that forms central unit. Thus there are two possible indexes
              could be: 0 and 1.

    @param[in] p_iteration: iteration of simulation process of the oscillatory network.
    @param[in] p_index: neuron index in the oscillatory network.
    @param[in] p_type: neuron state value type (membrane potential, conductance of the sodium channel, etc.).

    @return State value for specific central neuron on specified iteration.

    */
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
    /*!
    
    @brief Comparison operator `==` to compare output dynamics.

    @param[in] p_other: another output dynamic that should be compared with current.

    @return `true` if output dynamic objects are equal, otherwise `false`.

    */
    bool operator==(const hhn_dynamic & p_other) const;

    /*!

    @brief Writes to an output stream output dynamic of the oscillatory network.

    @param[in] p_stream: output stream for writing.
    @param[in] p_dynamic: output dynamic of the network that should be written.

    */
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


/*!

@class      hhn_dynamic_reader hhn.hpp pyclustering/nnet/hhn.hpp

@brief      Reader of the output dynamic of the oscillatory network based on Hodgkin-Huxley neurons.
@details    The dynamic reader reads the output dynamic from a text file with the specific format.

*/
class hhn_dynamic_reader {
private:
    std::string     m_filename;

    hhn_dynamic *                       m_dynamic       = nullptr;
    std::ifstream                       m_file_stream;
    std::vector<hhn_dynamic::collect>   m_order         = { };
    std::size_t                         m_size_network  = 0;

public:
    /*!
    
    @brief  Default constructor of the dynamic reader of HHN.
    
    */
    hhn_dynamic_reader() = default;

    /*!

    @brief  Constructor of the dynamic reader of HHN where path to a file where output dynamic of the network is stored.

    */
    explicit hhn_dynamic_reader(const std::string & p_filename);

    /*!

    @brief  Default destructor of the dynamic reader of HHN.

    */
    ~hhn_dynamic_reader();

public:
    /*!

    @brief  Reads output dynamic of the network to the specified output dynamic container.

    @param[in] p_dynamic: output dynamic container to which output dynamic from the file should be placed.

    */
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


/*!

@brief      Defines external input (stimulus) to the oscillatory network.
@details    External input type is represented by a container with a random access to its elements.

*/
using hhn_stimulus        = std::vector<double>;


/*!

@class      hhn_network hhn.hpp pyclustering/nnet/hhn.hpp

@brief      The two-layer oscillatory network that is based on Hodgkin-Huxley neurons.
@details    The oscillatory network consists of two types of neurons: peripheral neurons and central neurons.
             Peripheral neurons represent feature detectors in the primary areas of the neocortex that are activated
             by external stimuli. It assumed that the external input to peripheral neurons is sufficiently large
             to cause their firing at some particular frequency. Considering image segmentation problem and visual
             attention modelling, the peripheral neurons are located on another grid of the same size as the an image,
             with each peripheral neuron receiving a signal from the pixel whose location on the grid is identical to the
             location of the peripheral neuron.

             The oscillatory network has two central neurons that forms so-called the central unit. The central unit is an
             extremely simplified version of the central executive. The 1st central neuron enables attention to be focused
             on a selected subset of peripheral neurons. The 2nd central neuron controls the shift of attention from one
             stimulus to another. The architecture of the oscillatory network is presented on figure 1.

             @image html hhn_architecture.png "Fig. 1. The architecture of the oscillatory network based on Hodgkin-Huxley neurons."

             The Implementation is based on paper @cite article::nnet::hnn::1.

*/
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
    /*!
    
    @brief  Default constructor of the oscillatory network based on Hodgkin-Huxley network.
    
    */
    hhn_network() = default;

    /*!

    @brief  Constructor of the oscillatory network based on Hodgkin-Huxley network that creates
             the network with specified size and parameters.

    @param[in] p_size: amount of neurons in the oscillatory network.
    @param[in] p_parameters: parameters of the oscillatory network that defines its behaviour.

    */
    hhn_network(const std::size_t      p_size,
                const hnn_parameters & p_parameters);

    /*!

    @brief  Default destructor of the oscillatory network based on Hodgkin-Huxley network.

    */
    ~hhn_network() = default;

public:
    /*!

    @brief      Runs oscillatory network simulation for the specific time with specified external inputs.

    @param[in] p_steps: number steps of simulations during simulation.
    @param[in] p_time: time of simulation.
    @param[in] p_solver: type of the solver for the simulation.
    @param[in] p_stimulus: external inputs (stimulus) to the network.
    @param[in] p_output_dynamic: output dynamic of the network.

    @return     Amount of neurons that are in the oscillatory network.

    */
    void simulate(const std::size_t         p_steps,
                  const double              p_time,
                  const solve_type          p_solver,
                  const hhn_stimulus &      p_stimulus,
                  hhn_dynamic &             p_output_dynamic);

    /*!

    @brief      Returns size of the oscillatory network.
    @details    Size of the network is defined by amount of neurons (oscillators) in it.

    @return     Amount of neurons that are in the oscillatory network.

    */
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
