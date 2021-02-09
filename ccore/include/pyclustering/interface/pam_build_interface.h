/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/definitions.hpp>


/*

@brief   PAM BUILD result is returned by pyclustering_package that consist sub-packages and this enumerator provides
          named indexes for sub-packages.

*/
enum pam_build_package_indexer {
    PAM_BUILD_PACKAGE_INDEX_MEDOIDS = 0,
    PAM_BUILD_PACKAGE_SIZE
};


/*

@brief   Initialize initial medoids using PAM BUILD algorithm.
@details Caller should destroy returned result that is in 'pyclustering_package'.

@param[in] p_sample: input data for clustering.
@param[in] p_amount: the amount of medoids to initialize.
@param[in] p_metric: pointer to distance metric 'distance_metric' that is used for distance calculation between two points.
@param[in] p_data_type: representation of data type ('0' - points, '1' - distance matrix).

@return  Returns result of initialization - array of allocated clusters in pyclustering package.

*/
extern "C" DECLARATION pyclustering_package * pam_build_algorithm(const pyclustering_package * const p_sample,
                                                                  const std::size_t p_amount,
                                                                  const void * const p_metric,
                                                                  const std::size_t p_data_type);
