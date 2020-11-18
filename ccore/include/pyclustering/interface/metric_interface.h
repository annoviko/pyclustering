/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <pyclustering/interface/pyclustering_package.hpp>

#include <pyclustering/definitions.hpp>


enum metric_t {
    EUCLIDEAN = 0,
    EUCLIDEAN_SQUARE,
    MANHATTAN,
    CHEBYSHEV,
    MINKOWSKI,
    CANBERRA,
    CHI_SQUARE,
    GOWER,
    USER_DEFINED = 1000
};


/**
 *
 * @brief   Create distance metric for calculation distance between two points.
 *
 * @param[in] p_type: metric type that is require to create.
 * @param[in] p_arguments: additional arguments, for example, degree in case of minkowski distance.
 * @param[in] p_solver: pointer to user-defined function that should be used for calculation, used only
 *             in case of 'USER_DEFINED' metric type.
 *
 * @return  Returns pointer to metric object, returned object should be destroyed by 'metric_destroy'.
 *
 */
extern "C" DECLARATION void * metric_create(const std::size_t p_type,
                                            const pyclustering_package * const p_arguments,
                                            double (*p_solver)(const void *, const void *));


/**
 *
 * @brief   Destroy distance metric object.
 *
 * @param[in] p_pointer_metric: pointer to distance metric object.
 *
 */
extern "C" DECLARATION void metric_destroy(const void * p_pointer_metric);


/**
 *
 * @brief   Calculate metric between two points.
 *
 * @param[in] p_pointer_metric: pointer to distance metric object.
 * @param[in] p_point1: pointer to package with the first point.
 * @param[in] p_point2: pointer to package with the second point.
 *
 * @return  Distance metric between two points.
 *
 */
extern "C" DECLARATION double metric_calculate(const void * p_pointer_metric,
                                               const pyclustering_package * const p_point1,
                                               const pyclustering_package * const p_point2);

