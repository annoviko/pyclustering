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
 * @brief   Create instance of LEGION (local excitatory global inhibitory oscillatory network).
 * @details Caller should destroy returned instance using 'legion_destroy' when it is not required anymore.
 *
 * @param[in] p_size: Number of oscillators in the network.
 * @param[in] p_connection_type: Type of connection between oscillators in the network.
 * @param[in] p_parameters: Parameters of the network that are defined by structure 'legion_parameters'.
 *
 * @return  Returns pointer to LEGION instance.
 *
 */
extern "C" DECLARATION void * legion_create(const unsigned int p_size, const unsigned int p_connection_type, const void * const p_parameters);

/**
 *
 * @brief   Destroy 'legion_network'.
 *
 * @param[in] p_network_pointer: Pointer to instance of LEGION.
 *
 */
extern "C" DECLARATION void legion_destroy(const void * p_network_pointer);

/**
 *
 * @brief   Performs static simulation of LEGION oscillatory network.
 * @details Returned output dynamic of the network should be destoyed by 'legion_dynamic_destroy'.
 *
 * @param[in] p_network_pointer: Pointer to instance of LEGION.
 * @param[in] p_steps: Number steps of simulations during simulation.
 * @param[in] p_time: Time of simulation.
 * @param[in] p_solver: Method that is used for differential equation.
 * @param[in] p_collect_dynamic: If true - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
 * @param[in] p_stimulus: Stimulus for oscillators, number of stimulus should be equal to number of oscillators,
 *             example of stimulus for 5 oscillators [0, 0, 1, 1, 0], value of stimulus is defined by parameter 'I'.
 *
 * @return Pointer to dynamic of oscillatory network.
 *
 */
extern "C" DECLARATION void * legion_simulate(const void * p_network_pointer, 
                                              const unsigned int p_steps, 
                                              const double p_time, 
                                              const unsigned int p_solver, 
                                              const bool p_collect_dynamic, 
                                              const pyclustering_package * const p_stimulus);

/**
 *
 * @brief   Returns size of the oscillatory network (LEGION) that is defined by amount of oscillators.
 *
 * @param[in] p_network_pointer: Pointer to instance of LEGION.
 *
 */
extern "C" DECLARATION std::size_t legion_get_size(const void * p_network_pointer);

/**
 *
 * @brief   Destroy instance of output dynamic of LEGION.
 *
 * @param[in] p_dynamic_pointer: Pointer to instance of LEGION.
 *
 */
extern "C" DECLARATION void legion_dynamic_destroy(const void * p_dynamic_pointer);

/**
 *
 * @brief   Returns output dynamic (amplitude of the excitatory component) of each oscillator during simulation process that corresponds to time points.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] p_dynamic_pointer: Pointer to output dynamic.
 *
 */
extern "C" DECLARATION pyclustering_package * legion_dynamic_get_output(const void * p_dynamic_pointer);

/**
 *
 * @brief   Returns output dynamic (amplitude of the inhibitory component) of each oscillator during simulation process that corresponds to time points.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] p_dynamic_pointer: Pointer to output dynamic.
 *
 */
extern "C" DECLARATION pyclustering_package * legion_dynamic_get_inhibitory_output(const void * p_dynamic_pointer);

/**
 *
 * @brief   Returns time points of simulation process that corresponds to amplitude.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] p_dynamic_pointer: Pointer to output dynamic.
 *
 */
extern "C" DECLARATION pyclustering_package * legion_dynamic_get_time(const void * p_dynamic_pointer);

/**
 *
 * @brief   Returns length of dynamic that is defined by amount of time-points of simulation process.
 *
 * @param[in] p_dynamic_pointer: Pointer to output dynamic.
 *
 */
extern "C" DECLARATION std::size_t legion_dynamic_get_size(const void * p_dynamic_pointer);