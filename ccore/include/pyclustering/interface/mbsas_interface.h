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
 * @brief   Clustering algorithm MBSAS returns allocated clusters.
 * @details Caller should destroy returned result that is in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_amount: maximum allowable number of clusters that can be allocated during processing.
 * @param[in] p_threshold: threshold of dissimilarity (maximum distance) between points.
 * @param[in] p_metric: pointer to distance metric 'distance_metric' that is used for distance calculation between two points.
 *
 * @return  Returns result of clustering - array of allocated clusters in pyclustering package.
 *
 */
extern "C" DECLARATION pyclustering_package * mbsas_algorithm(const pyclustering_package * const p_sample,
                                                              const std::size_t p_amount,
                                                              const double p_threshold,
                                                              const void * const p_metric);