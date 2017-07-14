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
 * @brief   Create oscillatory network SYNC for cluster analysis.
 *
 * @param   (in) sample                - input data for clustering.
 * @param   (in) connectivity_radius   - connectivity radius between points.
 * @param   (in) enable_conn_weight    - if True - enable mode when strength between oscillators 
 *                                       depends on distance between two oscillators. Otherwise
 *                                       all connection between oscillators have the same strength.
 * @param   (in) initial_phases        - type of initialization of initial phases of oscillators.
 *
 ***********************************************************************************************/
extern "C" DECLARATION void * syncnet_create_network(const data_representation * const sample, 
                                                     const double connectivity_radius, 
                                                     const bool enable_conn_weight, 
                                                     const unsigned int initial_phases);

/***********************************************************************************************
 *
 * @brief   Destroy SyncNet (calls destructor).
 *
 * @param   (in) pointer_network       - pointer to the SyncNet network.
 *
 ***********************************************************************************************/
extern "C" DECLARATION void syncnet_destroy_network(const void * pointer_network);

/***********************************************************************************************
 *
 * @brief   Simulate oscillatory network SYNC until clustering problem is not resolved.
 *
 * @param   (in) order             - order of synchronization that is used as indication for 
 *                                   stopping processing.
 * @param   (in) solver            - specified type of solving diff. equation. 
 * @param   (in) collect_dynamic   - specified requirement to collect whole dynamic of the network.
 *
 * @return  Returns analyser of output dynamic.
 *
 ***********************************************************************************************/
extern "C" DECLARATION void * syncnet_process(const void * pointer_network, 
                                              const double order, 
                                              const unsigned int solver, 
                                              const bool collect_dynamic);

extern "C" DECLARATION void syncnet_analyser_destroy(const void * pointer_analyser);


/***********************************************************************************************
 *
 * @brief   Create oscillatory network HSyncNet (hierarchical Sync) for cluster analysis.
 *
 * @param[in] sample:            Input data for clustering.
 * @param[in] number_clusters:   Number of clusters that should be allocated.
 * @param[in] initial_phases:    Type of initialization of initial phases of oscillators.
 * @param[in] initial_neighbors: Defines initial radius connectivity by calculation average distance 
 *                               to connect specify number of oscillators.
 * @param[in] increase_persent:  Percent of increasing of radius connectivity on each step (input 
 *                               values in range (0.0; 1.0) correspond to (0%; 100%)).
 *
 * @return Pointer of hsyncnet network. Caller should free it by 'hsyncnet_destroy_network'.
 *
 ***********************************************************************************************/
extern "C" DECLARATION void * hsyncnet_create_network(const data_representation * const sample, 
                                                      const unsigned int number_clusters, 
                                                      const unsigned int initial_phases,
                                                      const unsigned int initial_neighbors,
                                                      const double increase_persent);

/***********************************************************************************************
 *
 * @brief   Destroy oscillatory network HSyncNet (calls destructor).
 *
 * @param   (in) pointer_network      - pointer to HSyncNet oscillatory network.
 *
 ***********************************************************************************************/
extern "C" DECLARATION void hsyncnet_destroy_network(const void * pointer_network);

/***********************************************************************************************
 *
 * @brief   Simulate oscillatory network hierarchical SYNC until clustering problem is not resolved.
 *
 * @param   (in) order             - order of synchronization that is used as indication for 
 *                                   stopping processing.
 * @param   (in) solver            - specified type of solving diff. equation. 
 * @param   (in) collect_dynamic   - specified requirement to collect whole dynamic of the network.
 *
 * @return  Return pointer to hsyncnet analyser of output dynamic
 *
 ***********************************************************************************************/
extern "C" DECLARATION void * hsyncnet_process(const void * pointer_network, const double order, const unsigned int solver, const bool collect_dynamic);

extern "C" DECLARATION void hsyncnet_analyser_destroy(const void * pointer_analyser);


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
