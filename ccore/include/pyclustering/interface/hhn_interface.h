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
 * @brief   Create HHN oscillatory network.
 * @details HHN oscillatory network should be freed by 'hhn_destroy'.
 *
 * @param[in] p_size: Defines amount peripheral neurons in the network.
 * @param[in] p_params: Parameters of the HHN network.
 *
 * @return Pointer to HHN network.
 *
 */
extern "C" DECLARATION void * hhn_create(const std::size_t p_size, const void * const p_params);

/**
 *
 * @brief   Destroy HHN network 'hhn_network'.
 *
 * @param[in] p_network_pointer: Pointer to HHN network.
 *
 */
extern "C" DECLARATION void hhn_destroy(const void * p_network_pointer);

/**
 *
 * @brief   Create HHN dynamic where collect parameters are specified.
 * @details HHN dynamic should be freed by 'hhn_destroy_dynamic'.
 *
 * @param[in] p_collect_membrane: If 'true' then membrane potential will be collected during simulation.
 * @param[in] p_collect_active_cond_sodium: If 'true' then active cond sodium current will be collected during simulation.
 * @param[in] p_collect_inactive_cond_sodium: If 'true' then inactive cond sodium current will be collected during simulation.
 * @param[in] p_collect_active_cond_potassium: If 'true' then active cond potassium current will be collected during simulation.
 *
 * @return Pointer to HHN dynamic.
 *
 */
extern "C" DECLARATION void * hhn_dynamic_create(bool p_collect_membrane,
                                                 bool p_collect_active_cond_sodium,
                                                 bool p_collect_inactive_cond_sodium,
                                                 bool p_collect_active_cond_potassium);

/**
 *
 * @brief   Destroy HHN dynamic.
 *
 * @param[in] p_dynamic: Pointer to HHN dynamic.
 *
 */
extern "C" DECLARATION void hhn_dynamic_destroy(const void * p_dynamic);

/**
 *
 * @brief   Performs simulation of HHN network.
 *
 * @param[in] p_network_pointer: Pointer to HHN network.
 * @param[in] p_steps: Number steps of simulations during simulation.
 * @param[in] p_time: Time of simulation.
 * @param[in] p_solver: Method that is used for differential equation.
 * @param[in] p_stimulus: Stimulus for oscillators, number of stimulus should be equal to number of oscillators.
 * @param[in,out] p_output_dynamic: Pointer to HHN dynamic where collected results are stored.
 *
 */
extern "C" DECLARATION void hhn_simulate(const void * p_network_pointer,
                                         const std::size_t p_steps,
                                         const double p_time,
                                         const std::size_t p_solver,
                                         const pyclustering_package * const p_stimulus,
                                         const void * p_output_dynamic);

/**
 *
 * @brief   Get specific dynamic evolution of peripheral neurons that is defined by collection index.
 * @details Collection indexes: 
 *            0 - membrane potential;
 *            1 - active cond sodium;
 *            2 - inactive cond sodium;
 *            3 - active cond potassium;
 *
 * Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] p_output_dynamic: Pointer to HHN dynamic.
 * @param[in] p_collection_index: Index of collection that should be returned.
 *
 * @return Pointer to pyclustering package where dynamic evolution of peripheral neurons is stored.
 *
 */
extern "C" DECLARATION pyclustering_package * hhn_dynamic_get_peripheral_evolution(const void * p_output_dynamic, const std::size_t p_collection_index);

/**
 *
 * @brief   Get specific dynamic evolution of central elements that is defined by collection index.
 * @details Collection indexes: 
 *            0 - membrane potential;
 *            1 - active cond sodium;
 *            2 - inactive cond sodium;
 *            3 - active cond potassium;
 *
 * Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] p_output_dynamic: Pointer to HHN dynamic.
 * @param[in] p_collection_index: Index of collection that should be returned.
 *
 */
extern "C" DECLARATION pyclustering_package * hhn_dynamic_get_central_evolution(const void * p_output_dynamic, const std::size_t p_collection_index);

/**
 *
 * @brief   Returns time points of simulation process that corresponds to amplitude.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] p_output_dynamic: Pointer to HHN dynamic.
 *
 * @return Pyclustering package where simulation time points are stored.
 *
 */
extern "C" DECLARATION pyclustering_package * hhn_dynamic_get_time(const void * p_output_dynamic);

/**
 *
 * @brief   Write out output dynamic to specified file in human-readable text format.
 *
 * @param[in] p_output_dynamic: Pointer to HHN dynamic.
 * @param[in] p_file: Output text file where output dynamic should be stored.
 *
 */
extern "C" DECLARATION void hhn_dynamic_write(const void * p_output_dynamic, const char * p_filename);

/**
 *
 * @brief   Read and construct HHN output dynamic from specified file.
 * @details Returned HHN output dynamic should be freed by 'hhn_dynamic_destroy'.
 *
 * @param[in] p_file: File where output dynamic is stored.
 *
 * @return  HHN output dynamic with values from file.
 *
 */
extern "C" DECLARATION void * hhn_dynamic_read(const char * p_filename);
