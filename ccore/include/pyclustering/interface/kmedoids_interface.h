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


#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/definitions.hpp>


/**
 *
 * @brief   K-Medians result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum kmedoids_package_indexer {
    KMEDOIDS_PACKAGE_INDEX_CLUSTERS = 0,
    KMEDOIDS_PACKAGE_INDEX_MEDOIDS,
    KMEDOIDS_PACKAGE_SIZE
};


/**
 *
 * @brief   Clustering algorithm K-Medoids returns allocated clusters.
 * @details Caller should destroy returned result that is in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_medoids: initial medoids of clusters.
 * @param[in] p_tolerance: stop condition - when changes of medians are less then tolerance value.
 * @param[in] p_itermax: maximum number of iterations for cluster analysis.
 * @param[in] p_metric: pointer to distance metric 'distance_metric' that is used for distance calculation between two points.
 * @param[in] p_type: representation of data type ('0' - points, '1' - distance matrix).
 *
 * @return  Returns result of clustering - array of allocated clusters in pyclustering package.
 *
 */
extern "C" DECLARATION pyclustering_package * kmedoids_algorithm(const pyclustering_package * const p_sample,
                                                                 const pyclustering_package * const p_medoids,
                                                                 const double p_tolerance,
                                                                 const std::size_t p_itermax,
                                                                 const void * const p_metric,
                                                                 const std::size_t p_type);
