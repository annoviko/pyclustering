/**************************************************************************************************************

Neural Network: Oscillatory Neural Network based on Kuramoto model

Based on article description:
 - A.Arenas, Y.Moreno, C.Zhou. Synchronization in complex networks. 2008.
 - X.B.Lu. Adaptive Cluster Synchronization in Coupled Phase Oscillators. 2009.
 - X.Lou. Adaptive Synchronizability of Coupled Oscillators With Switching. 2012.
 - A.Novikov, E.Benderskaya. Oscillatory Neural Networks Based on the Kuramoto Model. 2014.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

**************************************************************************************************************/

#ifndef _SYNC_NETWORK_H_
#define _SYNC_NETWORK_H_

#include "network.h"
#include "interface_ccore.h"

#include <vector>


typedef struct sync_oscillator {
	double phase;
	double frequency;
} sync_oscillator;


typedef struct sync_dynamic {
	double time;
	double phase;
} sync_dynamic;


/***********************************************************************************************
 *
 * @brief   Oscillatory neural network based on Kuramoto model.
 *
 ***********************************************************************************************/
class sync_network : public network {
protected:
	std::vector<sync_oscillator> * oscillators;	                    /* oscillators                  */
	std::vector< std::vector<unsigned int> * > * sync_ensembles;    /* pointer to sync ensembles    */

	double weight;                                                  /* multiplier for connections   */

public:
	/***********************************************************************************************
	 *
	 * @brief   Contructor of the oscillatory network SYNC based on Kuramoto model.
	 *
	 * @param   (in) size                - number of oscillators in the network.
	 * @param   (in) weight_factor       - coupling strength of the links between oscillators.
	 * @param   (in) frequency_factor    - multiplier of internal frequency of the oscillators.
	 * @param   (in) connection_type     - type of connection between oscillators in the network.
	 * @param   (in) initial_phases      - type of initialization of initial phases of oscillators.
	 *
	 ***********************************************************************************************/
	sync_network(const unsigned int size, const double weight_factor, const double frequency_factor, const conn_type connection_type, const initial_type initial_phases);
	
	/***********************************************************************************************
	 *
	 * @brief   Default destructor.
	 *
	 ***********************************************************************************************/
	virtual ~sync_network(void);

	/***********************************************************************************************
	 *
	 * @brief   Calculates level of global synchorization in the network.
	 *
	 * @return  Return level of global synchorization in the network.
	 *
	 ***********************************************************************************************/
	double sync_order(void) const;

	/***********************************************************************************************
	 *
	 * @brief   Calculates level of local (partial) synchorization in the network.
	 *
	 * @return  Return level of local (partial) synchorization in the network.
	 *
	 ***********************************************************************************************/
	double sync_local_order(void) const;

	/***********************************************************************************************
	 *
	 * @brief   Allocate clusters in line with ensembles of synchronous oscillators where each
	 *          synchronous ensemble corresponds to only one cluster.
	 *
	 * @param   (in) tolerance   - maximum error for allocation of synchronous ensemble oscillators.
	 *
	 * @return  Return vectors synchronous oscillators.
	 *
	 ***********************************************************************************************/
	std::vector< std::vector<unsigned int> * > * allocate_sync_ensembles(const double tolerance = 0.01);
	
	/***********************************************************************************************
	 *
	 * @brief   Performs static simulation of oscillatory network.
	 *
	 * @param   (in) steps             - number steps of simulations during simulation.
	 * @param   (in) time              - time of simulation.
	 * @param   (in) solver            - type of solver for simulation.
	 * @param   (in) collect_dynamic   - if true - returns whole dynamic of oscillatory network, 
	 *                                   otherwise returns only last values of dynamics.
	 *
	 * @return  Returns dynamic of oscillatory network. If argument 'collect_dynamic' = true, than it 
	 *          returns dynamic for the whole simulation time, otherwise returns only last values 
	 *          (last step of simulation) of dynamic.
	 *
	 ***********************************************************************************************/
	std::vector< std::vector<sync_dynamic> * > * simulate_static(const unsigned int steps, const double time, const solve_type solver, const bool collect_dynamic);

	/***********************************************************************************************
	 *
	 * @brief   Performs dynamic simulation of oscillatory network until stop condition is not 
	 *          reached. Stop condition is defined by input argument 'order'.
	 *
	 * @param   (in) order               - order of process synchronization, destributed 0..1.
	 * @param   (in) solver              - type of solver for simulation.
	 * @param   (in) collect_dynamic     - if true - returns whole dynamic of oscillatory network, 
	 *                                     otherwise returns only last values of dynamics.
	 * @param   (in) step                - time step of one iteration of simulation (can be ignored).
	 * @param   (in) step_int            - integration step, should be less than step (can be ignored).
	 * @param   (in) threshold_changes   - additional stop condition that helps prevent infinite 
	 *                                     simulation, defines limit of changes of oscillators between 
	 *                                     current and previous steps.
	 *
	 * @return  Returns dynamic of oscillatory network. If argument 'collect_dynamic' = true, than it 
	 *          returns dynamic for the whole simulation time, otherwise returns only last values 
	 *          (last step of simulation) of dynamic.
	 *
	 ***********************************************************************************************/
	std::vector< std::vector<sync_dynamic> * > * simulate_dynamic(const double order, const solve_type solver, const bool collect_dynamic, const double step = 0.1, const double step_int = 0.01, const double threshold_changes = 0.0000001);

	/***********************************************************************************************
	 *
	 * @brief   Normalization of phase of oscillator that should be placed between [0; 2 * pi].
	 *
	 * @param   (in) teta    - phase of oscillator.
	 *
	 * @return  Returns normalized phase.
	 *
	 ***********************************************************************************************/
	static double phase_normalization(const double teta);

	/***********************************************************************************************
	 *
	 * @brief   Convert dynamic of the network to CCORE interface representation of dynamic. It
	 *          creates new data block and it should deleted by user.
	 *
	 * @param   (in) dynamic    - dynamic of the network.
	 *
	 * @return  Returns dynamic in line with CCORE interface representation.
	 *
	 ***********************************************************************************************/
	static dynamic_result * convert_dynamic_representation(std::vector< std::vector<sync_dynamic> * > * dynamic);

protected:
	/***********************************************************************************************
	 *
	 * @brief   Calculation of oscillator phase using Kuramoto model.
	 *
	 * @param   (in) t      - current value of phase.
	 * @param   (in) teta   - time (can be ignored). 
	 * @param   (in) argv   - index of oscillator whose phase represented by argument teta.
	 *
	 * @return  Return new value of phase of oscillator with index 'argv[1]'.
	 *
	 ***********************************************************************************************/
	virtual double phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv);

	/***********************************************************************************************
	 *
	 * @brief   Calculates new phases for oscillators in the network in line with current step.
	 *
	 * @param   (in) solver             - type solver of the differential equation.
	 * @param   (in) t                  - time of simulation.
	 * @param   (in) step               - step of solution at the end of which states of oscillators 
	 *                                    should be calculated.
	 * @param   (in) int_step           - step differentiation that is used for solving differential 
	 *                                    equation (can be ignored in case of solvers when integration
	 *                                    step is defined by solver itself).
	 *
	 ***********************************************************************************************/
	virtual void calculate_phases(const solve_type solver, const double t, const double step, const double int_step);

private:
	/***********************************************************************************************
	 *
	 * @brief   Adapter for solving differential equation for calculation of oscillator phase.
	 *
	 * @param   (in) t      - current value of phase.
	 * @param   (in) teta   - time (can be ignored). 
	 * @param   (in) argv   - pointer to the network 'argv[0]' and index of oscillator whose phase 
	 *                        represented by argument teta 'argv[1]'.
	 *
	 * @return  Return new value of phase of oscillator that is specified in index 'argv[1]'.
	 *
	 ***********************************************************************************************/
	static double adapter_phase_kuramoto(const double t, const double teta, const std::vector<void *> & argv);

	/***********************************************************************************************
	 *
	 * @brief   Remove allocated clusters. Should be used when dynamic is changed (phases of
	 *          oscillators are changed). Required for fast providing results of clustering.
	 *
	 ***********************************************************************************************/
	void free_sync_ensembles(void);

	/***********************************************************************************************
	 *
	 * @brief   Stores dynamic of oscillators. Type of saving depends on argument 'collect_dynamic', 
	 *          if it's true - than new values are added to previous, otherwise new values rewrite 
	 *          previous.
	 *
	 * @param   (in) dynamic             - dynamic of oscillators.
	 * @param   (in) time                - type of solver for simulation.
	 * @param   (in) collect_dynamic     - if true - added new values to previous, otherwise rewrites 
	 *                                     previous values by new values of dynamics.
	 *
	 ***********************************************************************************************/
	void store_dynamic(std::vector< std::vector<sync_dynamic> * > * dynamic, const double time, const bool collect_dynamic) const;
};

#endif
