/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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


#include "interface/pyclustering_package.hpp"

#include "definitions.hpp"


/**
 *
 * @brief
 *
 */
extern "C" DECLARATION void * hhn_create(const std::size_t p_size, const void * const p_params);

/**
 *
 * @brief
 *
 */
extern "C" DECLARATION void hhn_destroy(const void * p_network_pointer);

/**
 *
 * @brief
 *
 */
extern "C" DECLARATION void * hhn_create_dynamic(bool p_collect_membrane,
                                                 bool p_collect_active_cond_sodium,
                                                 bool p_collect_inactive_cond_sodium,
                                                 bool p_collect_active_cond_potassium);

/**
 *
 * @brief
 *
 */
extern "C" DECLARATION void * hhn_destroy_dynamic(const void * p_dynamic);

/**
 *
 * @brief
 *
 */
extern "C" DECLARATION void * hhn_simulate(const void * p_network_pointer,
                                           const std::size_t p_steps,
                                           const double p_time,
                                           const std::size_t p_solver,
                                           const pyclustering_package * const p_stimulus,
                                           const void * p_output_dynamic);


/**
 *
 * @brief
 *
 */
extern "C" DECLARATION void * hhn_get_dynamic_evolution(const std::size_t p_collection_index);