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

#include <pyclustering/cluster/silhouette_ksearch.hpp>

#include <pyclustering/definitions.hpp>


/**
 *
 * @brief   Silhouette K-Search result is returned using pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum silhouette_ksearch_package_indexer {
    SILHOUETTE_KSEARCH_PACKAGE_AMOUNT = 0,
    SILHOUETTE_KSEARCH_PACKAGE_SCORE,
    SILHOUETTE_KSEARCH_PACKAGE_SCORES,
    SILHOUETTE_KSEARCH_PACKAGE_SIZE
};


/**
 *
 * @brief   Silhouette K-Search cluster allocators.
 *
 */
enum silhouette_ksearch_type {
    KMEANS = 0,
    KMEDIANS,
    KMEDOIDS
};


/**
 *
 * @brief   Returns cluster allocator for Silhouette K-Search algorithm.
 *
 * @param[in] p_algorithm: cluster allocator type that should be created.
 *
 * @return  Returns cluster allocator.
 *
 */
pyclustering::clst::silhouette_ksearch_allocator::ptr get_silhouette_ksearch_allocator(
    const silhouette_ksearch_type p_algorithm);


/**
 *
 * @brief   Performs data analysis using Silhouette method using center initializer that is specified by template.
 * @details Caller should destroy returned result by 'free_pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_clusters: clusters that have been allocated for that data.
 * @param[in] p_metric: pointer to distance metric 'distance_metric' that is used for distance calculation between two points.
 * @param[in] p_data_type: defines data type that is used for clustering process ('0' - points, '1' - distance matrix).
 *
 * @return  Returns Silhouette's analysis results as a pyclustering package [ scores ].
 *
 */
extern "C" DECLARATION pyclustering_package * silhouette_algorithm(
    const pyclustering_package * const p_sample,
    const pyclustering_package * const p_clusters,
    const void * const p_metric,
    const std::size_t p_data_type);


/**
 *
 * @brief   Performs data analysis using Silhouette K-Search algorithm using center initializer that is specified by template.
 * @details Caller should destroy returned result by 'free_pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_kmin: minimum amount of clusters that should be considered.
 * @param[in] p_kmax: maximum amount of clusters that should be considered.
 * @param[in] p_metric: cluster allocator that is used by Silhouette K-Search method.
 *
 * @return  Returns Silhouette K-Search results as a pyclustering package [ [ amount of clusters], [ optimal score ], [ score for each K ] ].
 *
 */
extern "C" DECLARATION pyclustering_package * silhouette_ksearch_algorithm(
    const pyclustering_package * const p_sample,
    const std::size_t p_kmin,
    const std::size_t p_kmax,
    const std::size_t p_algorithm);