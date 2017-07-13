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
 * @brief   Clustering algorithm CURE returns allocated clusters.
 * @details Caller should destroy returned clustering data using 'cure_data_destroy' when
 *           it is not required anymore.
 *
 * @param[in] sample: input data for clustering.
 * @param[in] number_clusters: number of clusters that should be allocated.
 * @param[in] number_repr_points: number of representation points for each cluster.
 * @param[in] compression: coefficient defines level of shrinking of representation
 *             points toward the mean of the new created cluster after merging on each step.
 *
 * @return  Returns pointer to cure data - clustering result that can be used for obtaining
 *           allocated clusters, representative points and means of each cluster.
 *
 */
extern "C" DECLARATION void * cure_algorithm(const pyclustering_package * const sample, const size_t number_clusters, const size_t number_repr_points, const double compression);

/**
 *
 * @brief   Destroys CURE clustering data (clustering results).
 *
 * @param[in] pointer_cure_data: pointer to CURE clustering data.
 *
 */
extern "C" DECLARATION void cure_data_destroy(void * pointer_cure_data);

/**
 *
 * @brief   Returns allocated clusters by CURE algorithm.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] pointer_cure_data: pointer to CURE clustering data.
 *
 * @return  Package where results of clustering are stored.
 *
 */
extern "C" DECLARATION pyclustering_package * cure_get_clusters(void * pointer_cure_data);

/**
 *
 * @brief   Returns CURE representors of each cluster.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] pointer_cure_data: pointer to CURE clustering data.
 *
 * @return  Package where representative points for each cluster are stored.
 *
 */
extern "C" DECLARATION pyclustering_package * cure_get_representors(void * pointer_cure_data);

/**
 *
 * @brief   Returns CURE mean points of each cluster.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] pointer_cure_data: pointer to CURE clustering data.
 *
 * @return  Package where mean point of each cluster is stored.
 *
 */
extern "C" DECLARATION pyclustering_package * cure_get_means(void * pointer_cure_data);
