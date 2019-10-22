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
 * @brief   Create oscillatory network HSyncNet (hierarchical Sync) for cluster analysis.
 *
 * @param[in] p_sample: Input data for clustering.
 * @param[in] p_number_clusters: Number of clusters that should be allocated.
 * @param[in] p_initial_phases: Type of initialization of initial phases of oscillators.
 * @param[in] p_initial_neighbors: Defines initial radius connectivity by calculation average distance 
 *             to connect specify number of oscillators.
 * @param[in] p_increase_persent:  Percent of increasing of radius connectivity on each step (input 
 *             values in range (0.0; 1.0) correspond to (0%; 100%)).
 *
 * @return Pointer of hsyncnet network. Caller should free it by 'hsyncnet_destroy_network'.
 *
 */
extern "C" DECLARATION void * hsyncnet_create_network(const pyclustering_package * const p_sample, 
                                                      const unsigned int p_number_clusters, 
                                                      const unsigned int p_initial_phases,
                                                      const unsigned int p_initial_neighbors,
                                                      const double p_increase_persent);

/**
 *
 * @brief   Destroy oscillatory network HSyncNet (calls destructor).
 *
 * @param[in] pointer_network: Pointer to HSyncNet oscillatory network.
 *
 */
extern "C" DECLARATION void hsyncnet_destroy_network(const void * p_pointer_network);

/**
 *
 * @brief   Simulate oscillatory network hierarchical SYNC until clustering problem is not resolved.
 * @details Caller should destroy instance of hsyncnet analyser of output dynamic using 'hsyncnet_analyser_destroy'.
 *
 * @param[in] p_pointer_network: Pointer to instance of hsyncnet.
 * @param[in] p_order: Order of synchronization that is used as indication for stopping processing.
 * @param[in] p_solver: Specified type of solving diff. equation. 
 * @param[in] p_collect_dynamic: Specified requirement to collect whole dynamic of the network.
 *
 * @return  Return pointer to hsyncnet analyser of output dynamic.
 *
 */
extern "C" DECLARATION void * hsyncnet_process(const void * p_pointer_network, 
                                               const double p_order, 
                                               const unsigned int p_solver, 
                                               const bool p_collect_dynamic);

/**
 *
 * @brief   Destroy instance of analyser of hsyncnet (hierarchical sync oscillatory network).
 *
 * @param[in] p_pointer_analyser: Pointer to hsyncnet output dynamic analyser.
 *
 */
extern "C" DECLARATION void hsyncnet_analyser_destroy(const void * p_pointer_analyser);