/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/interface/pyclustering_package.hpp>


/*!

@brief   X-Means result is returned using pyclustering_package that consist sub-packages and this enumerator provides
          named indexes for sub-packages.

*/
enum xmeans_package_indexer {
    XMEANS_PACKAGE_INDEX_CLUSTERS = 0,
    XMEANS_PACKAGE_INDEX_CENTERS,
    XMEANS_PACKAGE_INDEX_WCE,
    XMEANS_PACKAGE_SIZE
};


/*!

@brief   Clustering algorithm X-Means returns allocated clusters.
@details Caller should destroy returned result in 'pyclustering_package'.

@param[in] p_sample: input data for clustering.
@param[in] p_centers: initial coordinates of centers of clusters.
@param[in] p_kmax: maximum number of clusters that can be allocated.
@param[in] p_tolerance: stop condition for local parameter improvement.
@param[in] p_criterion: cluster splitting criterion.
@param[in] p_alpha: alpha based probabilistic bound \f$\Q\left(\alpha\right)\f$ that is distributed from [0, 1] and that is used only in case MNDL splitting criteria.
@param[in] p_beta: beta based probabilistic bound \f$\Q\left(\beta\right)\f$ that is distributed from [0, 1] and that is used only in case MNDL splitting criteria.
@param[in] p_repeat: how many times K-Means should be run to improve parameters (by default is `1`), 
            with larger 'repeat' values suggesting higher probability of finding global optimum.
@param[in] p_random_state: seed for random state (by default is `RANDOM_STATE_CURRENT_TIME`, current system time is used).
@param[in] p_metric: pointer to distance metric 'distance_metric' that is used for distance calculation between two points.

@return  Returns result of clustering - array of allocated clusters in the pyclustering package.

*/
extern "C" DECLARATION pyclustering_package * xmeans_algorithm(const pyclustering_package * const p_sample,
                                                               const pyclustering_package * const p_centers,
                                                               const std::size_t p_kmax,
                                                               const double p_tolerance,
                                                               const unsigned int p_criterion,
                                                               const double p_alpha,
                                                               const double p_beta,
                                                               const std::size_t p_repeat,
                                                               const long long p_random_state,
                                                               const void * const p_metric);
