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

#ifndef _INTERFACE_CCORE_H_
#define _INTERFACE_CCORE_H_


#include "definitions.hpp"

#include "interface/pyclustering_package.hpp"


typedef struct cluster_representation {
    unsigned int            size;
    unsigned int        * objects;
} cluster_representation;


typedef struct tsp_result {
	unsigned int			size;
	double					path_length;
	unsigned int			* objects_sequence;
} tsp_result;


typedef struct tsp_objects {
    unsigned int            size;
    unsigned int            dimention;
    double                  * data;
} tsp_objects;

typedef struct tsp_matrix {
    unsigned int            size;
    double                  ** data;
} tsp_matrix;


/***********************************************************************************************
 *
 * @brief   Creates and runs ant colony algorithm for TSP.
 *
 * @param[in] objects_coord			 - pointer to array with objects.
 * @param[in] ant_colony_parameters  - pointer to parameters of the ant colony algorithm.
 *
 * @return Pointer to allocated TSP result where shortest length is stored with sequence of visited
 *         objects. This pointer should deallocated by client using 'ant_colony_tsp_destroy'.
 *
 * @see ant_colony_tsp_destroy();
 *
 ***********************************************************************************************/
extern "C" DECLARATION tsp_result * ant_colony_tsp_process(const tsp_objects * objects_coord, const void * ant_colony_parameters);

extern "C" DECLARATION tsp_result * ant_colony_tsp_process_by_matrix(const tsp_matrix * objects_coord, const void * ant_colony_parameters);

/***********************************************************************************************
 *
 * @brief   Frees TSP results that is allocated by ant colony algorithm.
 *
 ***********************************************************************************************/
extern "C" DECLARATION void ant_colony_tsp_destroy(const void * pointer);


/**********************
 *
 * Ant clustering algorithm
 *
 * @brief  Run ant clustering algorithm
 *
 *
 */

#endif
