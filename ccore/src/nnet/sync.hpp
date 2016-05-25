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

#ifndef _SYNC_NETWORK_H_
#define _SYNC_NETWORK_H_

#include "ccore.h"

#include <vector>
#include <memory>

#include "container/adjacency.hpp"
#include "container/adjacency_connector.hpp"
#include "container/dynamic_data.hpp"
#include "container/ensemble_data.hpp"

#include "differential/runge_kutta_4.hpp"
#include "differential/runge_kutta_fehlberg_45.hpp"

#include "nnet/network.hpp"


using namespace container;
using namespace differential;


typedef struct sync_oscillator {
	double phase;
	double frequency;

	sync_oscillator() :
		phase(0.0),
		frequency(0.0) { }
} sync_oscillator;


typedef std::vector<unsigned int>   sync_ensemble;


typedef void (*sync_callback_solver)(const double, const differ_state<double> &, const differ_extra<void *> &, differ_state<double> &);


typedef std::vector<double>           sync_corr_row;
typedef std::vector<sync_corr_row>    sync_corr_matrix;


typedef struct sync_network_state {
public:
	std::vector<double> m_phase;
	double m_time;

public:
	sync_network_state(void) : m_time(0.0) { }

	sync_network_state(const unsigned int size) : m_phase(size, 0.0), m_time(0.0) { }

    sync_network_state(double time, std::vector<double> phases) : m_phase(phases), m_time(time) { }

	inline size_t size(void) const { return m_phase.size(); }

	inline sync_network_state & operator=(const sync_network_state & other) {
		if (this != &other) {
			m_phase.resize(other.size());
			std::copy(other.m_phase.cbegin(), other.m_phase.cend(), m_phase.begin());

			m_time = other.m_time;
		}

		return *this;
	}
} sync_network_state;


/***********************************************************************************************
 *
 * @brief   Output dynamic of the oscillatory network 'sync' based on Kuramoto model.
 *
 ***********************************************************************************************/
class sync_dynamic : public dynamic_data<sync_network_state> {
public:
    /***********************************************************************************************
     *
     * @brief   Default destructor.
     *
     ***********************************************************************************************/
	virtual ~sync_dynamic(void);

public:
    /***********************************************************************************************
     *
     * @brief Allocate clusters in line with ensembles of synchronous oscillators.
     * @details  Each synchronous ensemble corresponds to only one cluster.
     *
     * @param[in]  tolerance: maximum error for allocation of synchronous ensemble oscillators.
     * @param[out] ensembles: synchronous ensembles of oscillators where each ensemble consists of
     *              indexes of oscillators that are synchronous to each other.
     *
     ***********************************************************************************************/
    void allocate_sync_ensembles(const double tolerance, ensemble_data<sync_ensemble> & ensembles) const;

    /***********************************************************************************************
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
    ***********************************************************************************************/
    void allocate_sync_ensembles(const double tolerance, const size_t iteration, ensemble_data<sync_ensemble> & ensembles) const;

    /***********************************************************************************************
     *
     * @brief Allocate correlation matrix between oscillators at the last step of simulation.
     *
     * @param[out] p_matrix: correlation matrix between oscillators on specified iteration.
     *
     ***********************************************************************************************/
    void allocate_correlation_matrix(sync_corr_matrix & p_matrix) const;

    /***********************************************************************************************
     *
     * @brief Allocate correlation matrix between oscillators at the specified step of simulation.
     *
     * @param[in]  p_iteration: Number of iteration of simulation for which correlation matrix should
     *              be allocated.
     * @param[out] p_matrix: correlation matrix between oscillators on specified iteration.
     *
     ***********************************************************************************************/
    void allocate_correlation_matrix(const size_t p_iteration, sync_corr_matrix & p_matrix) const;
};


/***********************************************************************************************
 *
 * @brief   Oscillatory neural network based on Kuramoto model with phase oscillator.
 *
 ***********************************************************************************************/
class sync_network {
protected:
    std::vector<sync_oscillator> m_oscillators;

    std::shared_ptr<adjacency_collection> m_connections;

    double weight;


private:
    sync_callback_solver m_callback_solver;


private:
    const static size_t MAXIMUM_MATRIX_REPRESENTATION_SIZE;

public:
    /***********************************************************************************************
     *
     * @brief   Contructor of the oscillatory network SYNC based on Kuramoto model.
     *
     * @param[in] size: number of oscillators in the network.
     * @param[in] weight_factor: coupling strength of the links between oscillators.
     * @param[in] frequency_factor: multiplier of internal frequency of the oscillators.
     * @param[in] connection_type: type of connection between oscillators in the network.
     * @param[in] initial_phases: type of initialization of initial phases of oscillators.
     *
     ***********************************************************************************************/
    sync_network(const size_t size, 
        const double weight_factor, 
        const double frequency_factor, 
        const connection_t connection_type,
        const initial_type initial_phases);

    /***********************************************************************************************
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
    ***********************************************************************************************/
    sync_network(const size_t size,
        const double weight_factor,
        const double frequency_factor,
        const connection_t connection_type,
        const size_t height,
        const size_t width,
        const initial_type initial_phases);

    /***********************************************************************************************
     *
     * @brief   Default destructor.
     *
     ***********************************************************************************************/
    virtual ~sync_network(void);


public:

    /***********************************************************************************************
     *
     * @brief   Calculates level of global synchorization in the network.
     *
     * @return  Return level of global synchorization in the network.
     *
     ***********************************************************************************************/
    virtual double sync_order(void) const;

    /***********************************************************************************************
     *
     * @brief   Calculates level of local (partial) synchorization in the network.
     *
     * @return  Return level of local (partial) synchorization in the network.
     *
     ***********************************************************************************************/
    virtual double sync_local_order(void) const;

    /***********************************************************************************************
     *
     * @brief   Performs static simulation of oscillatory network.
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
     ***********************************************************************************************/
    virtual void simulate_static(
        const unsigned int steps,
        const double time,
        const solve_type solver,
        const bool collect_dynamic,
        sync_dynamic & output_dynamic);

    /***********************************************************************************************
     *
     * @brief   Performs dynamic simulation of oscillatory network until stop condition is not
     *          reached. Stop condition is defined by input argument 'order'.
     *
     * @param[in]  order: order of process synchronization, destributed 0..1.
     * @param[in]  step: time step of one iteration of simulation.
     * @param[in]  solver: type of solver for simulation.
     * @param[in]  collect_dynamic: if true - returns whole dynamic of oscillatory network,
     *              otherwise returns only last values of dynamics.
     * @param[out] output_dynamic: output dynamic of the network, if argument 'collect_dynamic' = true,
     *              than it will be dynamic for the whole simulation time, otherwise returns only last
     *              values  (last step of simulation) of dynamic.
     *
     ***********************************************************************************************/
    virtual void simulate_dynamic(
        const double order,
        const double step,
        const solve_type solver,
        const bool collect_dynamic,
        sync_dynamic & output_dynamic);

    /***********************************************************************************************
    *
    * @brief   Returns size of the oscillatory network that is defined by amout of oscillators.
    *
    ***********************************************************************************************/
    inline size_t size(void) const { return m_oscillators.size(); }

protected:

    /***********************************************************************************************
     *
     * @brief   Normalization of phase of oscillator that should be placed between [0; 2 * pi].
     *
     * @param[in] teta: phase of oscillator.
     *
     * @return  Normalized phase.
     *
     ***********************************************************************************************/
    virtual double phase_normalization(const double teta) const;

    /***********************************************************************************************
     *
     * @brief   Calculation of oscillator phase using Kuramoto model.
     *
     * @param[in] t: current value of phase.
     * @param[in] teta: time (can be ignored).
     * @param[in] argv: index of oscillator whose phase represented by argument teta.
     *
     * @return  Return new value of phase of oscillator with index 'argv[1]'.
     *
     ***********************************************************************************************/
    virtual double phase_kuramoto(
        const double t, 
        const double teta, 
        const std::vector<void *> & argv) const;

    /***********************************************************************************************
     *
     * @brief   Calculates new phases for oscillators in the network in line with current step.
     *
     * @param[in] solver: type solver of the differential equation.
     * @param[in] t: time of simulation.
     * @param[in] step: step of solution at the end of which states of oscillators should be calculated.
     * @param[in] int_step: step differentiation that is used for solving differential equation (can 
     *             be ignored in case of solvers when integration step is defined by solver itself).
     *
     ***********************************************************************************************/
    virtual void calculate_phases(
        const solve_type solver, 
        const double t, 
        const double step, 
        const double int_step);

    /***********************************************************************************************
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
    ***********************************************************************************************/
    virtual void store_dynamic(
        const double step, 
        const bool collect_dynamic, 
        sync_dynamic & dynamic) const;

    virtual void set_callback_solver(sync_callback_solver solver);

private:
    /***********************************************************************************************
     *
     * @brief   Adapter for solving differential equation for calculation of oscillator phase.
     *
     * @param[in] t: current time.
     * @param[in] inputs: phase of oscillator whose new state should be calculated.
     * @param[in] argv: pointer to the network 'argv[0]' and index of oscillator whose phase represented 
     *             by argument teta 'argv[1]'.
     * @param[out] outputs: new value of phase of oscillator that is specified in index 'argv[1]'.
     *
     ***********************************************************************************************/
    static void adapter_phase_kuramoto(
        const double t, 
        const differ_state<double> & inputs, 
        const differ_extra<void *> & argv, 
        differ_state<double> & outputs);

    /***********************************************************************************************
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
    ***********************************************************************************************/
    void initialize(
        const size_t size,
        const double weight_factor,
        const double frequency_factor,
        const connection_t connection_type,
        const size_t height,
        const size_t width,
        const initial_type initial_phases);
};

#endif
