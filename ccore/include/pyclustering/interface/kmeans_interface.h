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
 * @brief   K-Means result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum kmeans_package_indexer {
    KMEANS_PACKAGE_INDEX_CLUSTERS = 0,
    KMEANS_PACKAGE_INDEX_CENTERS,
    KMEANS_PACKAGE_INDEX_EVOLUTION_CLUSTERS,
    KMEANS_PACKAGE_INDEX_EVOLUTION_CENTERS,
    KMEANS_PACKAGE_INDEX_WCE,
    KMEANS_PACKAGE_SIZE
};


/**
 *
 * @brief   Clustering algorithm K-Means returns allocated clusters.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_centers: initial cluster centers.
 * @param[in] p_tolerance: stop condition - when changes of medians are less then tolerance value.
 * @param[in] p_itermax: maximum number of iterations for cluster analysis.
 * @param[in] p_observe: if 'true' then evolution of cluster and center changes are collected to result.
 * @param[in] p_metric: pointer to distance metric 'distance_metric' that is used for distance calculation between two points.
 *
 * @return  Returns result of clustering - array of allocated clusters, if 'p_observe' is 'true' then package contains
 *           evolution of cluster and center changes.
 *
 */
extern "C" DECLARATION pyclustering_package * kmeans_algorithm(const pyclustering_package * const p_sample,
                                                               const pyclustering_package * const p_initial_centers,
                                                               const double p_tolerance,
                                                               const std::size_t p_itermax,
                                                               const bool p_observe,
                                                               const void * const p_metric);
