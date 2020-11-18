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
 * @brief   K-Medians result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum kmedians_package_indexer {
    KMEDIANS_PACKAGE_INDEX_CLUSTERS = 0,
    KMEDIANS_PACKAGE_INDEX_MEDIANS,
    KMEDIANS_PACKAGE_SIZE
};


/**
 *
 * @brief   Clustering algorithm K-Medians returns allocated clusters.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_initial_medians: initial medians of clusters.
 * @param[in] p_tolerance: stop condition - when changes of medians are less then tolerance value.
 * @param[in] p_itermax: maximum amount of iterations for cluster analysis.
 * @param[in] p_metric: distance metric for distance calculation between objects.
 *
 * @return  Returns result of clustering - array of allocated clusters.
 *
 */
extern "C" DECLARATION pyclustering_package * kmedians_algorithm(const pyclustering_package * const p_sample, 
                                                                 const pyclustering_package * const p_initial_medians,
                                                                 const double p_tolerance,
                                                                 const std::size_t p_itermax,
                                                                 const void * const p_metric);
