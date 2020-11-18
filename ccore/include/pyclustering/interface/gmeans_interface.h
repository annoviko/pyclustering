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
 * @brief   G-Means result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum gmeans_package_indexer {
    GMEANS_PACKAGE_INDEX_CLUSTERS = 0,
    GMEANS_PACKAGE_INDEX_CENTERS,
    GMEANS_PACKAGE_INDEX_WCE,
    GMEANS_PACKAGE_SIZE
};


/*!

@brief   Clustering algorithm G-Means returns allocated clusters.
@details Caller should destroy returned result in `pyclustering_package`.

@param[in] p_sample: input data for clustering.
@param[in] p_amount: initial amount of centers.
@param[in] p_tolerance: stop condition that stops the algorithm's processing when changes of medians are less than tolerance value.
@param[in] p_repeat: how many times K-Means should be run to improve parameters, with larger `repeat` 
            values suggesting higher probability of finding global optimum.
@param[in] p_kmax: maximum amount of clusters that might be allocated. The argument is considered as a stop
            condition. When the maximum amount is reached then algorithm stops processing. By default the maximum
            amount of clusters is not restricted (`k_max` is -1).
@param[in] p_random_state: seed for random state (by default is `RANDOM_STATE_CURRENT_TIME`, current system time is used).

@return  Returns result of clustering - array of allocated clusters.

*/
extern "C" DECLARATION pyclustering_package * gmeans_algorithm(const pyclustering_package * const p_sample, 
                                                               const std::size_t p_amount, 
                                                               const double p_tolerance,
                                                               const std::size_t p_repeat,
                                                               const long long p_kmax,
                                                               const long long p_random_state);
