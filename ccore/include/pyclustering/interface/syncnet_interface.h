/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/definitions.hpp>


/**
 *
 * @brief   Create oscillatory network SYNC for cluster analysis.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_connectivity_radius: connectivity radius between points.
 * @param[in] p_enable_conn_weight: if True - enable mode when strength between oscillators depends on distance between two oscillators. Otherwise all connection between 
 *             oscillators have the same strength.
 * @param[in] p_initial_phases: type of initialization of initial phases of oscillators.
 *
 */
extern "C" DECLARATION void * syncnet_create_network(const pyclustering_package * const p_sample, 
                                                     const double p_connectivity_radius, 
                                                     const bool p_enable_conn_weight, 
                                                     const unsigned int p_initial_phases);

/**
 *
 * @brief   Destroy SyncNet (calls destructor).
 *
 * @param[in] p_pointer_network: pointer to the SyncNet network.
 *
 */
extern "C" DECLARATION void syncnet_destroy_network(const void * p_pointer_network);

/**
 *
 * @brief   Simulate oscillatory network SYNC until clustering problem is not resolved.
 * @details Allocated output dynamic analyser should be destroyed by called using 'syncnet_analyser_destroy'.
 *
 * @param[in] p_pointer_network: pointer to syncnet instance.
 * @param[in] p_order: order of synchronization that is used as indication for stopping processing.
 * @param[in] p_solver: specified type of solving diff. equation. 
 * @param[in] p_collect_dynamic: specified requirement to collect whole dynamic of the network.
 *
 * @return  Returns analyser of output dynamic.
 *
 */
extern "C" DECLARATION void * syncnet_process(const void * p_pointer_network, 
                                              const double p_order, 
                                              const unsigned int p_solver, 
                                              const bool p_collect_dynamic);

/**
 *
 * @brief   Destroy syncnet output dynamic analyser instance.
 *
 * @param[in] p_pointer_analyser: pointer to syncnet output dynamic analyser.
 *
 */
extern "C" DECLARATION void syncnet_analyser_destroy(const void * p_pointer_analyser);