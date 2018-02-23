/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


#include <vector>
#include <memory>

#include "container/adjacency.hpp"
#include "container/adjacency_connector.hpp"
#include "container/dynamic_data.hpp"
#include "container/ensemble_data.hpp"

#include "differential/runge_kutta_4.hpp"
#include "differential/runge_kutta_fehlberg_45.hpp"

#include "nnet/network.hpp"

#include "parallel/thread_pool.hpp"


using namespace ccore::container;
using namespace ccore::differential;
using namespace ccore::parallel;


namespace ccore {

namespace nnet {


typedef struct sync_oscillator {
    double phase;
    double frequency;

    sync_oscillator() :
        phase(0.0),
        frequency(0.0)
    { }
} sync_oscillator;


typedef std::vector<unsigned int>     sync_ensemble;


typedef std::vector<double>           sync_corr_row;
typedef std::vector<sync_corr_row>    sync_corr_matrix;


/**
 *
 * @brief   Oscillatory network state where oscillator phases and corresponding time-point are stored.
 *
 */
typedef struct sync_network_state {
public:
    std::vector<double>     m_phase = { };
    double                  m_time = 0.0;

public:
    sync_network_state(void) = default;

    sync_network_state(const sync_network_state & p_other) = default;

    sync_network_state(sync_network_state && p_other) = default;

    sync_network_state(const std::size_t size) :
        m_phase(size, 0.0), m_time(0.0) { }

    sync_network_state(const double time, const std::vector<double> & phases) :
        m_phase(phases), m_time(time) { }

    sync_network_state(const double time, const std::initializer_list<double> & initializer) :
        m_phase(initializer), m_time(time) { }

public:
    inline std::size_t size(void) const { return m_phase.size(); }

public:
    sync_network_state & operator=(const sync_network_state & other) = default;

    sync_network_state & operator=(sync_network_state && other) = default;
} sync_network_state;


/**
 *
 * @brief   Provides methods related to calculation of ordering parameters.
 *
 */
class sync_ordering {
private:
    using phase_getter = std::function<double(std::size_t)>;

public:
    /**
     *
     * @brief   Default constructor is forbidden.
     *
     */
    sync_ordering(void) = delete;

    /**
     *
     * @brief   Default destructor is forbidden.
     *
     */
    ~sync_ordering(void) = delete;

public:
    /**
     *
     * @brief    Calculates level of global synchronization (order parameter) for input phases.
     * @details  This parameter is tend 1.0 when the oscillatory network close to global synchronization and it
     *            tend to 0.0 when desynchronization is observed in the network.
     *
     * @param[in]  p_phases: Oscillator phases that are used for calculation.
     *
     * @return  Order parameter for the specified state.
     *
     */
    static double calculate_sync_order(const std::vector<double> & p_phases);

    /**
     *
     * @brief    Calculates level of global synchronization (order parameter) for input phases.
     * @details  This parameter is tend 1.0 when the oscillatory network close to global synchronization and it
     *            tend to 0.0 when desynchronization is observed in the network.
     *
     * @param[in]  p_oscillators: Network oscillators that are used for calculation.
     *
     * @return  Order parameter for the specified state.
     *
     */
    static double calculate_sync_order(const std::vector<sync_oscillator> & p_oscillators);

    /**
     *
     * @brief    Calculates level of local synchronization (order parameter) for input phases.
     * @details  This parameter is tend 1.0 when the oscillatory network close to global synchronization and it
     *            tend to 0.0 when desynchronization is observed in the network.
     *
     * @param[in]  p_connections: Connections between oscillators in the network for which calculation is performed.
     * @param[in]  p_phases: Oscillator phases that are used for calculation.
     *
     * @return  Order parameter for the specified state.
     *
     */
    static double calculate_local_sync_order(
            const std::shared_ptr<adjacency_collection> p_connections,
            const std::vector<double> & p_phases);

    /**
     *
     * @brief    Calculates level of local synchronization (order parameter) for input phases.
     * @details  This parameter is tend 1.0 when the oscillatory network close to global synchronization and it
     *            tend to 0.0 when desynchronization is observed in the network.
     *
     * @param[in]  p_connections: Connections between oscillators in the network for which calculation is performed.
     * @param[in]  p_oscillators: Network oscillators that are used for calculation.
     *
     * @return  Order parameter for the specified state.
     *
     */
    static double calculate_local_sync_order(
            const std::shared_ptr<adjacency_collection> p_connections,
            const std::vector<sync_oscillator> & p_oscillators);

private:
    template <class TypeContainer>
    static double calculate_sync_order_parameter(
            const TypeContainer & p_container,
            const phase_getter & p_getter);

    template <class TypeContainer>
    static double calculate_local_sync_order_parameter(
            const std::shared_ptr<adjacency_collection> p_connections,
            const TypeContainer & p_container,
            const phase_getter & p_getter);
};


/**
 *
 * @brief   Output dynamic of the oscillatory network 'sync' based on Kuramoto model.
 *
 */
class sync_dynamic : public dynamic_data<sync_network_state> {
public:
    /**
     *
     * @brief   Default destructor.
     *
     */
	virtual ~sync_dynamic(void);

public:
    /**
     *
     * @brief Allocate clusters in line with ensembles of synchronous oscillators.
     * @details  Each synchronous ensemble corresponds to only one cluster.
     *
     * @param[in]  tolerance: maximum error for allocation of synchronous ensemble oscillators.
     * @param[out] ensembles: synchronous ensembles of oscillators where each ensemble consists of
     *              indexes of oscillators that are synchronous to each other.
     *
     */
    void allocate_sync_ensembles(const double tolerance, ensemble_data<sync_ensemble> & ensembles) const;

    /**
     *
     * @brief    Allocate clusters in line with ensembles of synchronous oscillators at the specify iteration
     *           of simulation.
     * @details  Each synchronous ensemble corresponds to only one cluster.
     *
     * @param[in]  tolerance: maximum error for allocation of synchronous ensemble oscillators.
     * @param[in]  iteration: simulation iteration that should be used for allocation.
     * @param[out] ensembles: synchronous ensembles of oscillators where each ensemble consists of
     *              indexes of oscillators that are synchronous to each other.
     *
     */
    void allocate_sync_ensembles(const double tolerance, const std::size_t iteration, ensemble_data<sync_ensemble> & ensembles) const;

    /**
     *
     * @brief Allocate correlation matrix between oscillators at the last step of simulation.
     *
     * @param[out] p_matrix: correlation matrix between oscillators on specified iteration.
     *
     */
    void allocate_correlation_matrix(sync_corr_matrix & p_matrix) const;

    /**
     *
     * @brief Allocate correlation matrix between oscillators at the specified step of simulation.
     *
     * @param[in]  p_iteration: Number of iteration of simulation for which correlation matrix should
     *              be allocated.
     * @param[out] p_matrix: correlation matrix between oscillators on specified iteration.
     *
     */
    void allocate_correlation_matrix(const std::size_t p_iteration, sync_corr_matrix & p_matrix) const;

    /**
     *
     * @brief Calculates evolution of level of global synchronization (order parameter).
     *
     * @param[in] start_iteration: The first iteration that is used for calculation.
     * @param[in] stop_iteration: The last iteration that is used for calculation.
     * @param[out] sequence_order: Evolution of order parameter.
     *
     */
    void calculate_order_parameter(
            const std::size_t start_iteration,
            const std::size_t stop_iteration,
            std::vector<double> & sequence_order) const;

    /**
     *
     * @brief Calculates evolution of level of partial synchronization (local order parameter).
     *
     * @param[in] connections: Connections of Sync oscillatory network.
     * @param[in] start_iteration: The first iteration that is used for calculation.
     * @param[in] stop_iteration: The last iteration that is used for calculation.
     * @param[out] sequence_order: Evolution of local order parameter.
     *
     */
    void calculate_local_order_parameter(
            const std::shared_ptr<adjacency_collection> & connections,
            const std::size_t start_iteration,
            const std::size_t stop_iteration,
            std::vector<double> & sequence_local_order) const;
};


/**
 *
 * @brief   Oscillatory neural network based on Kuramoto model with phase oscillator.
 *
 */
class sync_network {
public:
    const static std::size_t DEFAULT_DATA_SIZE_PARALLEL_PROCESSING;

private:
    const static std::size_t MAXIMUM_MATRIX_REPRESENTATION_SIZE;

private:
    using iterator = std::vector<sync_oscillator>::iterator;

protected:
    std::vector<sync_oscillator> m_oscillators;

    std::shared_ptr<adjacency_collection> m_connections;

    double weight;

    thread_pool::ptr m_pool         = nullptr;

    bool m_parallel_processing      = false;

    std::size_t m_parallel_trigger  = DEFAULT_DATA_SIZE_PARALLEL_PROCESSING;

private:
    equation<double>  m_equation;

public:
    /**
     *
     * @brief   Contructor of the oscillatory network SYNC based on Kuramoto model.
     *
     * @param[in] size: number of oscillators in the network.
     * @param[in] weight_factor: coupling strength of the links between oscillators.
     * @param[in] frequency_factor: multiplier of internal frequency of the oscillators.
     * @param[in] connection_type: type of connection between oscillators in the network.
     * @param[in] initial_phases: type of initialization of initial phases of oscillators.
     *
     */
    sync_network(const size_t size, 
        const double weight_factor, 
        const double frequency_factor, 
        const connection_t connection_type,
        const initial_type initial_phases);

    /**
    *
    * @brief   Contructor of the oscillatory network SYNC based on Kuramoto model.
    *
    * @param[in] size: number of oscillators in the network.
    * @param[in] weight_factor: coupling strength of the links between oscillators.
    * @param[in] frequency_factor: multiplier of internal frequency of the oscillators.
    * @param[in] connection_type: type of connection between oscillators in the network.
    * @param[in] height: number of oscillators in column of the network, this argument is
    *            used only for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types
    *            this argument is ignored.
    * @param[in] width: number of oscillotors in row of the network, this argument is used
    *            only for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types this
    *            argument is ignored.
    * @param[in] initial_phases: type of initialization of initial phases of oscillators.
    *
    */
    sync_network(const std::size_t size,
        const double weight_factor,
        const double frequency_factor,
        const connection_t connection_type,
        const std::size_t height,
        const std::size_t width,
        const initial_type initial_phases);

    /**
     *
     * @brief   Default destructor.
     *
     */
    virtual ~sync_network(void);


public:
    /**
     *
     * @brief   Calculates level of global synchronization in the network.
     *
     * @return  Return level of global synchronization in the network.
     *
     */
    virtual double sync_order(void) const;

    /**
     *
     * @brief   Calculates level of local (partial) synchronization in the network.
     *
     * @return  Return level of local (partial) synchronization in the network.
     *
     */
    virtual double sync_local_order(void) const;

    /**
     *
     * @brief   Performs static simulation of oscillatory network.
     * @details In case 'collect_dynamic = True' output dynamic will consists all steps of simulation
     *           and the initial state of the network, for example, in case of 20 steps, length of
     *           output dynamic will be 21 (20 simulation steps + 1 initial state).
     *
     * @param[in]  steps: number steps of simulations during simulation.
     * @param[in]  time: time of simulation.
     * @param[in]  solver: type of solver for simulation.
     * @param[in]  collect_dynamic: if true - returns whole dynamic of oscillatory network,
     *              otherwise returns only last values of dynamics.
     * @param[out] output_dynamic: output dynamic of the network, if argument 'collect_dynamic' = true,
     *              than it will be dynamic for the whole simulation time, otherwise returns only last
     *              values  (last step of simulation) of dynamic.
     *
     */
    virtual void simulate_static(
        const std::size_t steps,
        const double time,
        const solve_type solver,
        const bool collect_dynamic,
        sync_dynamic & output_dynamic);

    /**
     *
     * @brief   Performs dynamic simulation of oscillatory network until stop condition is not
     *           reached. Stop condition is defined by input argument 'order'.
     * @details In case 'collect_dynamic = True' output dynamic will consists all steps of simulation
     *           and the initial state of the network, for example, in case of 20 steps, length of
     *           output dynamic will be 21 (20 simulation steps + 1 initial state).
     *
     * @param[in]  order: order of process synchronization, distributed 0..1.
     * @param[in]  step: time step of one iteration of simulation.
     * @param[in]  solver: type of solver for simulation.
     * @param[in]  collect_dynamic: if true - returns whole dynamic of oscillatory network,
     *              otherwise returns only last values of dynamics.
     * @param[out] output_dynamic: output dynamic of the network, if argument 'collect_dynamic' = true,
     *              than it will be dynamic for the whole simulation time, otherwise returns only last
     *              values  (last step of simulation) of dynamic.
     *
     */
    virtual void simulate_dynamic(
        const double order,
        const double step,
        const solve_type solver,
        const bool collect_dynamic,
        sync_dynamic & output_dynamic);

    /**
    *
    * @brief    Set custom trigger (that is defined by network size) for parallel processing,
    *            by default this value is defined by static constant DEFAULT_DATA_SIZE_PARALLEL_PROCESSING.
    *
    * @param[in]  p_data_size: network size that triggers parallel processing.
    *
    */
    virtual void set_parallel_processing_trigger(const std::size_t p_network_size);

    /**
     *
     * @brief   Returns size of the oscillatory network that is defined by amount of oscillators.
     *
     */
    inline std::size_t size(void) const { return m_oscillators.size(); }

    /**
     *
     * @brief   Returns connections represented by chosen adjacency collection.
     *
     */
    inline std::shared_ptr<adjacency_collection> connections(void) const { return m_connections; }

protected:
    /**
     *
     * @brief   Normalization of phase of oscillator that should be placed between [0; 2 * pi].
     *
     * @param[in] teta: phase of oscillator.
     *
     * @return  Normalized phase.
     *
     */
    virtual double phase_normalization(const double teta) const;

    /**
     *
     * @brief   Calculation of oscillator phase using Kuramoto model.
     *
     * @param[in] t: time (can be ignored).
     * @param[in] teta: current value of phase.
     * @param[in] argv: index of oscillator whose phase represented by argument teta.
     *
     * @return  Return new value of phase of oscillator with index 'argv[1]'.
     *
     */
    virtual double phase_kuramoto(
        const double t, 
        const double teta, 
        const std::vector<void *> & argv) const;

    /**
     *
     * @brief   Calculates state of phase oscillator using classic Kuramoto synchonization model.
     *
     * @param[in] t: time (can be ignored).
     * @param[in] inputs: current state of the oscillator (current phase).
     * @param[in] argv: additional parameters that are used by the oscillator's equation (index of oscillator 
                   whose phase represented by argument teta).
     * @param[out] outputs: new states of the oscillator (new phase value).
     *
     */
    virtual void phase_kuramoto_equation(
        const double t, 
        const differ_state<double> & inputs, 
        const differ_extra<void *> & argv, 
        differ_state<double> & outputs) const;

    /**
     *
     * @brief   Calculates new phases for oscillators in the network in line with current step.
     *
     * @param[in] solver: type solver of the differential equation.
     * @param[in] t: time of simulation.
     * @param[in] step: step of solution at the end of which states of oscillators should be calculated.
     * @param[in] int_step: step differentiation that is used for solving differential equation (can 
     *             be ignored in case of solvers when integration step is defined by solver itself).
     *
     */
    virtual void calculate_phases(
        const solve_type solver, 
        const double t, 
        const double step, 
        const double int_step);

    /**
     *
     * @brief   Calculates new phases for specific range of oscillators in the network in line with current step.
     *
     * @param[in] solver: type solver of the differential equation.
     * @param[in] t: time of simulation.
     * @param[in] step: step of solution at the end of which states of oscillators should be calculated.
     * @param[in] int_step: step differentiation that is used for solving differential equation (can 
     *             be ignored in case of solvers when integration step is defined by solver itself).
     * @param[in] p_begin: interator to the first oscillator from the range.
     * @param[in] p_end: iterator to the last oscillator from the range.
     * @param[in|out] p_next_phases: container where new oscillator phases from the range are placed.
     *
     */
    virtual void calculate_phases(
        const solve_type solver, 
        const double t, 
        const double step, 
        const double int_step,
        const iterator p_begin,
        const iterator p_end,
        std::vector<double> & p_next_phases);

    /**
    *
    * @brief   Stores dynamic of oscillators. Type of saving depends on argument 'collect_dynamic',
    *          if it's true - than new values are added to previous, otherwise new values rewrite
    *          previous.
    *
    * @param[in]  step: dynamic of oscillators.
    * @param[in]  collect_dynamic: if true - added new values to previous, otherwise rewrites
    *              previous values by new values of dynamics.
    * @param[out] dynamic: storage of output dynamic.
    *
    */
    virtual void store_dynamic(
        const double step, 
        const bool collect_dynamic, 
        sync_dynamic & dynamic) const;

    /**
    *
    * @brief   Set phase oscillator equation that is used to calculate state of each oscillator in the network.
    *
    * @param[in]  solver: equation of phase oscillator.
    *
    */
    virtual void set_equation(equation<double> & solver);

private:
    /**
    *
    * @brief   Initializer of the oscillatory network SYNC based on Kuramoto model.
    *
    * @param[in] size: number of oscillators in the network.
    * @param[in] weight_factor: coupling strength of the links between oscillators.
    * @param[in] frequency_factor: multiplier of internal frequency of the oscillators.
    * @param[in] connection_type: type of connection between oscillators in the network.
    * @param[in] height: number of oscillators in column of the network, this argument is
    *            used only for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types
    *            this argument is ignored.
    * @param[in] width: number of oscillotors in row of the network, this argument is used
    *            only for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types this
    *            argument is ignored.
    * @param[in] initial_phases: type of initialization of initial phases of oscillators.
    *
    */
    void initialize(
        const size_t size,
        const double weight_factor,
        const double frequency_factor,
        const connection_t connection_type,
        const size_t height,
        const size_t width,
        const initial_type initial_phases);

    /**
    *
    * @brief   Check if parallel processing should be used for network simulation and if it is required then
    *          initialize thread pool for that purpose.
    *
    */
    void check_parallel_condition(void);
};


}

}