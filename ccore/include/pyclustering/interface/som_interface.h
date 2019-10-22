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


#include <cstddef>

#include <pyclustering/nnet/som.hpp>

#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/definitions.hpp>


/**
*
* @brief    Creates self-organized feature map (SOM).
* @details  Caller should destroy created instance by 'som_destroy' when it is not required.
*
* @param[in] num_rows: amount of neurons in each row of the map.
* @param[in] num_cols: amount of neurons in each column of the map.
* @param[in] type_conn: type of connections between neurons (grid-four, grid-eight, honeycomb, defined by neighbor function, etc.).
* @param[in] parameters: pointer to parameters of the map.
*
* @return Pointer to instance of self-organized feature map.
*
* @see  som_destroy
*
*/
extern "C" DECLARATION void * som_create(const size_t num_rows, const size_t num_cols, const size_t type_conn, const void * parameters);

/**
*
* @brief Destroy instance of self-organized feature map (SOM).
*
* @param[in] pointer: pointer to instance of self-organized feature map.
*
*/
extern "C" DECLARATION void som_destroy(const void * pointer);

/**
*
* @brief    Load network parameters such weights, amount of won objects by each neuron (optional), captuted objects by each neuron (optional).
*
* @param[in] p_pointer: pointer to instance of self-organized feature map.
* @param[in] p_weights: weights that should be load to the network.
* @param[in] p_awards: amount of captured objects by each neuron (optional parameter and can be 'nullptr').
* @param[in] p_captured_objects: captured objects by each neuron (optional parameter and can be 'nullptr').
*
* @see  som_destroy
*
*/
extern "C" DECLARATION void som_load(const void * p_pointer, const pyclustering_package * p_weights, const pyclustering_package * p_awards, const pyclustering_package * p_captured_objects);

/**
*
* @brief   Trains self-organized feature map (SOM).
*
* @param[in] pointer: pointer to instance of self-organized feature map.
* @param[in] sample: pointer to input dataset for training.
* @param[in] epochs: number of epochs for training.
* @param[in] autostop: stop learining when convergance is too low.
*
* @return  Returns number of learining iterations.
*
*/
extern "C" DECLARATION size_t som_train(const void * pointer, const pyclustering_package * const sample, const size_t epochs, const bool autostop);

/**
*
* @brief   Processes input pattern (no learining) and returns index of neuron-winner.
* @details Using index of neuron winner catched object can be obtained by som_get_capture_objects().
*
* @param[in] pointer: pointer to instance of self-organized feature map.
* @param[in] p_pattern: input pattern for processing.
*
* @return  Returns index of neuron-winner.
*
* @see som_get_capture_objects()
*
*/
extern "C" DECLARATION size_t som_simulate(const void * pointer, const pyclustering_package * const p_pattern);

/**
*
* @brief  Returns number of neuron winners at the last step of learning process.
*
* @param[in] pointer: pointer to instance of self-organized feature map.
*
* @return Returns amout of neurons that are winners.
*
*/
extern "C" DECLARATION size_t som_get_winner_number(const void * pointer);

/**
*
* @brief  Returns size of self-organized map (number of neurons in the map).
*
* @param[in] pointer: pointer to instance of self-organized feature map.
*
*/
extern "C" DECLARATION size_t som_get_size(const void * pointer);

/**
*
* @brief  Returns neuron weights in pyclustering package.
* @details  Allocated puclustering package should be freed by caller using 'free_pyclustering_package'.
*
* @param[in] pointer: pointer to instance of self-organized feature map.
*
* @return Neuron weights in pyclustering package.
*
*/
extern "C" DECLARATION pyclustering_package * som_get_weights(const void * pointer);

/**
*
* @brief  Returns sequence of captured objects by each neuron during training.
* @details  Allocated puclustering package should be freed by caller using 'free_pyclustering_package'.
*
* @param[in] pointer: pointer to instance of self-organized feature map.
*
* @return Captured objects by each neuron in pyclustering package.
*
*/
extern "C" DECLARATION pyclustering_package * som_get_capture_objects(const void * pointer);

/**
*
* @brief  Returns amount of captured objects by each neuron during training.
* @details  Allocated puclustering package should be freed by caller using 'free_pyclustering_package'.
*
* @param[in] pointer: pointer to instance of self-organized feature map.
*
* @return Amount of captured objects by each neuron in pyclustering package.
*
*/
extern "C" DECLARATION pyclustering_package * som_get_awards(const void * pointer);

/**
*
* @brief  Returns neighbor indexes of each neuron.
* @details  Allocated puclustering package should be freed by caller using 'free_pyclustering_package'.
*
* @param[in] pointer: pointer to instance of self-organized feature map.
*
* @return Neighbor indexes of each neuron in pyclustering package.
*
*/
extern "C" DECLARATION pyclustering_package * som_get_neighbors(const void * pointer);
