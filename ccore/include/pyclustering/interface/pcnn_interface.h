/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/nnet/pcnn.hpp>

#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/definitions.hpp>


/**
*
* @brief    Creates Pulse Coupled Neural Network (PCNN).
* @details  Caller should destroy created instance by 'pcnn_destroy' when it is not required.
*
* @param[in] p_size: network size that is defined by amount of oscillator (neurons).
* @param[in] p_connection_type: type of connections that is used in the network (all-to-all, grid, etc.).
* @param[in] p_height: height of grid network structure (used only in case of grid structure types).
* @param[in] p_width: width of grid network structure (used only in case of grid structure types).
* @param[in] p_parameters: pointer to parameters of the network.
*
* @return   Pointer to instance of created oscillatory network.
*
* @see  pcnn_destroy
*
*/
extern "C" DECLARATION void * pcnn_create(const unsigned int p_size, const unsigned int p_connection_type, const unsigned int p_height, const unsigned int p_width, const void * const p_parameters);

/**
*
* @brief    Destroy instance of Pulse Coupled Neural Network.
*
* @param[in] p_pointer: pointer to instance of destroying network.
*
*/
extern "C" DECLARATION void pcnn_destroy(const void * p_pointer);

/**
*
* @brief    Simulates Pulse Coupled Neural Network during specify simulation time.
* @details  Caller should destroy output dynamic of the network when it is not required.
*
* @param[in] p_pointer: pointer to instance of the network that is simulated.
* @param[in] p_steps: simulation time that is measured in steps (iterations).
* @param[in] p_stimulus: stimulus for oscillators (neurons).
*
* @return   Pointer to instance of output dynamic of the network.
*
* @see  pcnn_dynamic_destroy
*
*/
extern "C" DECLARATION void * pcnn_simulate(const void * p_pointer, const unsigned int p_steps, const void * const p_stimulus);

/**
*
* @brief    Returns size of the oscillatory network that is defined by amount of oscillators.
*
* @param[in] p_pointer: pointer to instance of the network.
*
* @return   Size of the oscillatory network.
*
*/
extern "C" DECLARATION std::size_t pcnn_get_size(const void * p_pointer);

/**
*
* @brief    Destroys instance of the output dynamic of Pulse Coupled Neural Network (PCNN).
*
* @param[in] p_pointer: pointer to instance of the network.
*
*/
extern "C" DECLARATION void pcnn_dynamic_destroy(const void * pointer);

/**
*
* @brief    Allocates synchronous ensembles of oscillators.
* @details  Allocated puclustering package should be freed by caller using 'free_pyclustering_package'.
*
* @param[in] p_pointer: pointer to instance of output dynamic of the oscillatory network (PCNN).
*
* @return   Pointer to pyclustering package where allocated synchronous are located.
*
*/
extern "C" DECLARATION pyclustering_package * pcnn_dynamic_allocate_sync_ensembles(const void * pointer);

/**
*
* @brief    Allocates spike ensembles of the network (PCNN).
* @details  Allocated puclustering package should be freed by caller using 'free_pyclustering_package'.
*
* @param[in] p_pointer: pointer to instance of output dynamic of the oscillatory network (PCNN).
*
* @return   Pointer to pyclustering package where allocated spikes ensembles are located.
*
*/
extern "C" DECLARATION pyclustering_package * pcnn_dynamic_allocate_spike_ensembles(const void * pointer);

/**
*
* @brief    Allocates time signal of output dynamic of the network (PCNN).
* @details  Allocated puclustering package should be freed by caller using 'free_pyclustering_package'.
*
* @param[in] p_pointer: pointer to instance of output dynamic of the oscillatory network (PCNN).
*
* @return   Pointer to pyclustering package where time signal is located.
*
*/
extern "C" DECLARATION pyclustering_package * pcnn_dynamic_allocate_time_signal(const void * pointer);

/**
*
* @brief    Returns output of each oscillator on each step of simulation.
* @details  Allocated puclustering package should be freed by caller using 'free_pyclustering_package'.
*
* @param[in] p_pointer: pointer to instance of output dynamic of the oscillatory network (PCNN).
*
* @return   Pointer to pyclustering package where output of each oscillator is located.
*
*/
extern "C" DECLARATION pyclustering_package * pcnn_dynamic_get_output(const void * pointer);

/**
*
* @brief    Returns steps of simulation of the network (PCNN).
* @details  Allocated puclustering package should be freed by caller using 'free_pyclustering_package'.
*
* @param[in] p_pointer: pointer to instance of output dynamic of the oscillatory network (PCNN).
*
* @return   Pointer to pyclustering package where time steps are located.
*
*/
extern "C" DECLARATION pyclustering_package * pcnn_dynamic_get_time(const void * pointer);

/**
*
* @brief    Returns size of the output dynamic that is defined by amount of simulation steps
*           stored in the output dynamic of the network (PCNN).
*
* @param[in] p_pointer: pointer to instance of output dynamic of the oscillatory network (PCNN).
*
* @return   Size of the output dynamic of the network (PCNN).
*
*/
extern "C" DECLARATION size_t pcnn_dynamic_get_size(const void * pointer);
