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
 * @brief   Clustering algorithm TTSAS returns allocated clusters.
 * @details Caller should destroy returned result that is in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_threshold1: dissimilarity level (distance) between point and its closest cluster, if the distance is
               less than 'threshold1' value then point is assigned to the cluster.
 * @param[in] p_threshold2: dissimilarity level (distance) between point and its closest cluster, if the distance is
               greater than 'threshold2' value then point is considered as a new cluster.
 * @param[in] p_metric: pointer to distance metric 'distance_metric' that is used for distance calculation between two points.
 *
 * @return  Returns result of clustering - array of allocated clusters in pyclustering package.
 *
 */
extern "C" DECLARATION pyclustering_package * ttsas_algorithm(const pyclustering_package * const p_sample,
                                                              const double p_threshold1,
                                                              const double p_threshold2,
                                                              const void * const p_metric);
