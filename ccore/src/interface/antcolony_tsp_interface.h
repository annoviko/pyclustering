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
#include "utils.hpp"


/**
 *
 * @brief   Creates and runs ant colony algorithm for TSP.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] objects_coord: pointer to array with objects.
 * @param[in] ant_colony_parameters: pointer to parameters of the ant colony algorithm.
 *
 * @return Pointer to allocated TSP result where shortest length is stored with sequence of visited
 *         objects.
 *
 */
extern "C" DECLARATION pyclustering_package * antcolony_tsp_process(const pyclustering_package * objects_coord, const void * ant_colony_parameters);

/**
 *
 * @brief   Creates and runs ant colony algorithm for TSP.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] objects_coord: pointer to array with objects.
 * @param[in] ant_colony_parameters: pointer to parameters of the ant colony algorithm.
 *
 * @return Pointer to allocated TSP result where shortest length is stored with sequence of visited
 *         objects.
 *
 */
extern "C" DECLARATION pyclustering_package * antcolony_tsp_process_by_matrix(const pyclustering_package * objects_coord, const void * ant_colony_parameters);
