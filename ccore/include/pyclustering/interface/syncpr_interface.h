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
 * @brief   Creates Sync-PR (Sync Pattern Recognition) oscillatory network.
 * @details Caller should destroy returned pointer to instance of the oscillatory network using function 'syncpr_destroy'.
 *
 * @param[in] num_osc: Number of oscillators in the network.
 * @param[in] increase_strength1: Parameter for increasing strength of the second term of the Fourier component.
 * @param[in] increase_strength2: Parameter for increasing strength of the third term of the Fourier component.
 *
 * @return  Returns pointer to instance of created oscillatory network.
 *
 */
extern "C" DECLARATION void * syncpr_create(const unsigned int num_osc, 
                                            const double increase_strength1, 
                                            const double increase_strength2);

/**
 *
 * @brief   Deallocate oscillatory network.
 *
 * @param[in] pointer_network: Pointer to the instance of the Sync-PR oscillatory network.
 *
 */
extern "C" DECLARATION void syncpr_destroy(const void * pointer_network);

/**
 *
 * @brief   Returns size of oscillatory network that is defined by amount of oscillators.
 *
 * @param[in] pointer_network: Pointer to the instance of the Sync-PR oscillatory network.
 *
 */
extern "C" DECLARATION std::size_t syncpr_get_size(const void * pointer_network);

/**
 *
 * @brief   Trans oscillatory network using specified patterns.
 *
 * @param[in] pointer_network: Pointer to the instance of the Sync-PR oscillatory network.
 * @param[in] patterns: Pyclustering package pointer to patterns.
 *
 */
extern "C" DECLARATION void syncpr_train(const void * pointer_network, 
                                         const void * const patterns);

/**
 *
 * @brief   Simulates oscillatory network during specified amount of steps - so-called static simulation.
 *
 * @param[in] pointer_network: Pointer to the instance of the Sync-PR oscillatory network.
 * @param[in] steps: Number steps of simulations during simulation.
 * @param[in] time: Time of simulation.
 * @param[in] pattern: Pyclustering package of pattern for recognition represented by list of features that are equal to [-1; 1].
 * @param[in] solution: Type of solver that should be used for simulation.
 * @param[in] collect_dynamic: If true - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
 *
 * @return  Pointer to output dynamic.
 *
 */
extern "C" DECLARATION void * syncpr_simulate_static(const void * pointer_network, 
                                                     unsigned int steps, 
                                                     const double time, 
                                                     const void * const pattern,
                                                     const unsigned int solver, 
                                                     const bool collect_dynamic);

/**
 *
 * @brief   Simulates oscillatory network until partial synchronization is reached that is defined by 'order'.
 *
 * @param[in] pointer_network: pointer to the instance of the Sync-PR oscillatory network.
 * @param[in] pattern: Pointer to pattern for recognition represented by list of features that are equal to [-1; 1].
 * @param[in] order: Order of process synchronization, distributed 0..1.
 * @param[in] solver: Type of solution.
 * @param[in] collect_dynamic: If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
 * @param[in] step: Time step of one iteration of simulation.
 *
 * @return  Pointer to output dynamic.
 *
 */
extern "C" DECLARATION void * syncpr_simulate_dynamic(const void * pointer_network, 
                                                      const void * const pattern, 
                                                      const double order, 
                                                      const unsigned int solver, 
                                                      const bool collect_dynamic, 
                                                      const double step);

/**
 *
 * @brief   Calculates function of the memorized pattern.
 *
 * @param[in] pointer_network: Pointer to the instance of the Sync-PR oscillatory network.
 * @param[in] pattern: Pattern for recognition represented by list of features that are equal to [-1; 1].
 *
 * @return Order of memory for the specified pattern.
 *
 */
extern "C" DECLARATION double syncpr_memory_order(const void * pointer_network, 
                                                  const void * const pattern);

/**
 *
 * @brief   Returns size of output SyncPR dynamic.
 *
 * @param[in] pointer_network: Pointer to the instance of the Sync-PR oscillatory network.
 *
 */
extern "C" DECLARATION std::size_t syncpr_dynamic_get_size(const void * pointer_network);

/**
 *
 * @brief   Deallocate output dynamic.
 *
 * @param[in] pointer_network: Pointer to output dynamic.
 *
 */
extern "C" DECLARATION void syncpr_dynamic_destroy(const void * pointer_dynamic);

/**
 *
 * @brief   Allocates synchronous ensembles of oscillators (groups).
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] pointer_network: Pointer to output dynamic.
 * @param[in] tolerance: Maximum error for allocation of synchronous ensemble oscillators.
 *
 */
extern "C" DECLARATION pyclustering_package * syncpr_dynamic_allocate_sync_ensembles(const void * pointer_dynamic, 
                                                                                     const double tolerance);

/**
 *
 * @brief   Returns time points of simulation process that corresponds to phases.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] pointer_network: Pointer to output dynamic.
 *
 */
extern "C" DECLARATION pyclustering_package * syncpr_dynamic_get_time(const void * pointer_dynamic);

/**
 *
 * @brief   Returns phases of each oscillator during simulation process that corresponds to time points.
 * @details Returned package should deallocated by 'free_pyclustering_package'.
 *
 * @param[in] pointer_network: Pointer to output dynamic.
 *
 */
extern "C" DECLARATION pyclustering_package * syncpr_dynamic_get_output(const void * pointer_dynamic);