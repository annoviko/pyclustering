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
 * @brief   OPTICS result is returned by pyclustering_package that consist sub-packages and this enumerator provides
 *           named indexes for sub-packages.
 *
 */
enum optics_package_indexer {
    OPTICS_PACKAGE_INDEX_CLUSTERS = 0,
    OPTICS_PACKAGE_INDEX_NOISE,
    OPTICS_PACKAGE_INDEX_ORDERING,
    OPTICS_PACKAGE_INDEX_RADIUS,
    OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_INDEX,
    OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_CORE_DISTANCE,
    OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_REACHABILITY_DISTANCE,
    OPTICS_PACKAGE_SIZE
};


/**
 *
 * @brief   Clustering algorithm OPTICS returns allocated clusters, noise, ordering and proper connectivity radius.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering that is represented by points or distance matrix (see p_data_type argument).
 * @param[in] p_radius: connectivity radius between points, points may be connected if distance
 *             between them less then the radius.
 * @param[in] p_minumum_neighbors: minimum number of shared neighbors that is required for
 *             establish links between points.
 * @param[in] p_amount_clusters: amount of clusters that should be allocated.
 * @param[in] p_data_type: defines data type that is used for clustering process ('0' - points, '1' - distance matrix).
 *
 * @return  Returns result of clustering - array that consists of four general clustering results that are represented by arrays too:
 *          [ [allocated clusters], [noise], [ordering], [connectivity radius], [optics objects indexes], [ optics objects core distances ], 
 *          [ optics objects reachability distances ] ]. It is important to note that connectivity radius is also placed into array.
 *
 */
extern "C" DECLARATION pyclustering_package * optics_algorithm(const pyclustering_package * const p_sample, 
                                                               const double p_radius, 
                                                               const size_t p_minumum_neighbors, 
                                                               const size_t p_amount_clusters,
                                                               const size_t p_data_type);
