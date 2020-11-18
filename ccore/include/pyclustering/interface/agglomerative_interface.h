/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/definitions.hpp>


/*!

@brief   Clustering algorithm Agglomerative returns allocated clusters.
@details Caller should destroy returned result in 'pyclustering_package'.

@param[in] p_sample: input data for clustering.
@param[in] p_number_clusters: amount of clusters that should be allocated.
@param[in] p_link: type of links for merging clusters.

@return  Returns result of clustering - array of allocated clusters. The last cluster in the
          array is noise.

*/
extern "C" DECLARATION pyclustering_package * agglomerative_algorithm(const pyclustering_package * const p_sample, const std::size_t p_number_clusters, const std::size_t p_link);
