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
 * @brief   Clustering algorithm ROCK returns allocated clusters.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_radius: connectivity radius (similarity threshold).
 * @param[in] p_number_clusters: defines number of clusters that should be allocated from the input data set.
 * @param[in] p_threshold: value that defines degree of normalization that influences
 *             on choice of clusters for merging during processing.
 *
 * @return  Returns result of clustering - array of allocated clusters in the pyclustering package.
 *
 */
extern "C" DECLARATION pyclustering_package * rock_algorithm(const pyclustering_package * const p_sample, const double p_radius, const size_t p_number_clusters, const double p_threshold);
