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


#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/definitions.hpp>


/**
 *
 * @brief   Create oscillatory network Sync that is based on Kuramoto model.
 * @details Caller should destroy returned instance using 'sync_destroy_network' when
 *           it is not required anymore.
 *
 * @param[in] size: number of oscillators in the network.
 * @param[in] weight_factor: coupling strength of the links between oscillators.
 * @param[in] frequency_factor: multiplier of internal frequency of the oscillators.
 * @param[in] connection_type: type of connection between oscillators in the network.
 * @param[in] initial_phases: type of initialization of initial phases of oscillators.
 *
 * @return  Returns pointer to sync oscillatory network.
 *
 */
extern "C" DECLARATION void * sync_create_network(const unsigned int size, const double weight_factor, const double frequency_factor, const unsigned int connection_type, const unsigned int initial_phases);

/**
 *
 * @brief   Returns size of the Sync oscillatory network that is defined by amount of oscillators.
 *
 * @param[in] pointer_network: pointer to the Sync network.
 *
 */
extern "C" DECLARATION std::size_t sync_get_size(const void * pointer_network);

/**
 *
 * @brief   Destroy sync_network (calls destructor).
 *
 * @param[in] pointer_network: pointer to the Sync network.
 *
 */
extern "C" DECLARATION void sync_destroy_network(const void * pointer_network);

/**
 *
 * @brief   Simulate dynamic of the oscillatory Sync network.
 * @details Caller should destroy returned instance using 'sync_dynamic_destroy' when
 *           it is not required anymore.
 *
 * @param[in] pointer_network: pointer to the Sync network.
 * @param[in] steps: number steps of simulations during simulation.
 * @param[in] time: time of simulation.
 * @param[in] solver: type of solution (solving).
 * @param[in] collect_dynamic: if 'true' then returns whole dynamic of oscillatory network, 
 *             otherwise returns only last values of dynamics.
 *
 * @return  Returns dynamic of simulation of the network.
 *
 */
extern "C" DECLARATION void * sync_simulate_static(const void * pointer_network, unsigned int steps, const double time, const unsigned int solver, const bool collect_dynamic);

/**
 *
 * @brief   Simulate dynamic of the oscillatory Sync network until stop condition is not reached.
 *
 * @param[in] pointer_network: pointer to the Sync network.
 * @param[in] order: order of process synchronization, destributed in (0..1).
 * @param[in] solver: type of solution (solving).
 * @param[in] collect_dynamic: if true - returns whole dynamic of oscillatory network, 
 *             otherwise returns only last values of dynamics.
 * @param[in] step: time step of one iteration of simulation.
 * @param[in] step_int: integration step, should be less than step.
 * @param[in] threshold_changes: additional stop condition that helps prevent infinite 
 *             simulation, defines limit of changes of oscillators between  current and previous steps.
 *
 * @return  Returns pointer to output dynamic of the network.
 *
 */
extern "C" DECLARATION void * sync_simulate_dynamic(const void * pointer_network, const double order, const unsigned int solver, const bool collect_dynamic, const double step, const double step_int, const double threshold_changes);

/**
 *
 * @brief   Returns level of global synchorization in the network.
 *
 * @param[in] pointer_network: pointer to the Sync network.
 *
 */
extern "C" DECLARATION double sync_order(const void * pointer_network);

/**
 *
 * @brief   Returns level of local (partial) synchronization in the network.
 *
 * @param[in] pointer_network: pointer to the Sync network.
 *
 */
extern "C" DECLARATION double sync_local_order(const void * pointer_network);

/**
 *
 * @brief   Returns connectivity matrix that defines connections between oscillators in the network.
 *
 * @param[in] pointer_network: pointer to the Sync network.
 *
 * @return  Package where connectivity matrix is stored.
 *
 */
extern "C" DECLARATION pyclustering_package * sync_connectivity_matrix(const void * pointer_network);

/**
 *
 * @brief   Returns length of dynamic that is defined by amount of time-points of simulation process.
 *
 * @param[in] pointer_dynamic: pointer to the output dynamic.
 *
 */
extern "C" DECLARATION std::size_t sync_dynamic_get_size(const void * pointer_dynamic);

/**
 *
 * @brief   Destroy output dynamic of Sync algorithm.
 *
 * @param[in] pointer_dynamic: pointer to the output dynamic.
 *
 */
extern "C" DECLARATION void sync_dynamic_destroy(const void * pointer_dynamic);

/**
 *
 * @brief   Allocates ensembles (groups) of synchronous oscillators where each group consists of oscillator indexes.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] pointer_network: pointer to the output dynamic.
 *
 * @return  Package where synchronous ensembles are stored.
 *
 */
extern "C" DECLARATION pyclustering_package * sync_dynamic_allocate_sync_ensembles(const void * pointer_dynamic, const double tolerance, const std::size_t iteration);

/**
 *
 * @brief   Allocate correlation matrix between oscillators at the specified step of simulation.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] pointer_network: pointer to the output dynamic.
 * @param[in] tolerance: maximum error for allocation of synchronous ensemble oscillators.
 * @param[in] iteration: iteration number of simulation that should be used for allocation.
 *
 * @return  Package where matrix is stored.
 *
 */
extern "C" DECLARATION pyclustering_package * sync_dynamic_allocate_correlation_matrix(const void * pointer_dynamic, const std::size_t iteration);

/**
 *
 * @brief   Returns time points of simulation process that corresponds to phases.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] pointer_dynamic: Pointer to output dynamic.
 *
 */
extern "C" DECLARATION pyclustering_package * sync_dynamic_get_time(const void * pointer_dynamic);

/**
 *
 * @brief   Returns phases of each oscillator during simulation process that corresponds to time points.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] pointer_dynamic: Pointer to output dynamic.
 *
 */
extern "C" DECLARATION pyclustering_package * sync_dynamic_get_output(const void * pointer_dynamic);


/**
 *
 * @brief   Returns order parameter evolution for output dynamic in specified range.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] p_pointer: Pointer to output dynamic.
 * @param[in] p_start: Iteration from which evolution should be calculated.
 * @param[in] p_stop: Iteration where evolution calculation should be stopped.
 *
 * @return Package where evolution order parameter (estimation of global synchronization) is stored.
 *
 */
extern "C" DECLARATION pyclustering_package * sync_dynamic_calculate_order(const void * p_pointer, const std::size_t p_start, const std::size_t p_stop);


/**
 *
 * @brief   Returns local order parameter evolution for output dynamic in specified range.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] p_pointer_pointer: Pointer to output dynamic of the Sync network.
 * @param[in] p_network_pointer: Sync network connections that are used for calculation.
 * @param[in] p_start: Iteration from which evolution should be calculated.
 * @param[in] p_stop: Iteration where evolution calculation should be stopped.
 *
 * @return Package where evolution local order parameter (estimation of partial synchronization) is stored.
 *
 */
extern "C" DECLARATION pyclustering_package * sync_dynamic_calculate_local_order(const void * p_dynamic_pointer, const void * p_network_pointer, const std::size_t p_start, const std::size_t p_stop);