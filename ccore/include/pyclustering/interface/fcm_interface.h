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
 * @brief   Fuzzy C-Means result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum fcm_package_indexer {
    FCM_PACKAGE_INDEX_CLUSTERS = 0,
    FCM_PACKAGE_INDEX_CENTERS,
    FCM_PACKAGE_INDEX_MEMBERSHIP,
    FCM_PACKAGE_SIZE
};


/**
 *
 * @brief   Clustering algorithm Fuzzy C-Medians returns allocated clusters.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_centers: initial cluster centers.
 * @param[in] p_m: hyper parameter that controls how fuzzy the cluster will be.
 * @param[in] p_tolerance: stop condition - when changes of medians are less then tolerance value.
 * @param[in] p_itermax: maximum amount of iterations for cluster analysis.
 *
 * @return  Returns result of clustering - array of allocated clusters.
 *
 */
extern "C" DECLARATION pyclustering_package * fcm_algorithm(const pyclustering_package * const p_sample, 
                                                            const pyclustering_package * const p_centers, 
                                                            const double p_m,
                                                            const double p_tolerance,
                                                            const std::size_t p_itermax);