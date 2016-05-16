#ifndef SRC_INTERFACE_PCNN_INTERFACE_H_
#define SRC_INTERFACE_PCNN_INTERFACE_H_


#include "interface/pyclustering_package.hpp"

#include "definitions.hpp"
#include "utils.hpp"


/***********************************************************************************************
 *
 * @brief   Clustering algorithm K-Medians returns allocated clusters.
 * @details Caller should destroy returned result in 'pyclustering_package'.
 *
 * @param[in] p_sample: input data for clustering.
 * @param[in] p_medians: initial medians of clusters.
 * @param[in] p_tolerance: stop condition - when changes of medians are less then tolerance value.
 *
 * @return  Returns result of clustering - array of allocated clusters.
 *
 ***********************************************************************************************/
extern "C" DECLARATION pyclustering_package * kmedians_algorithm(const data_representation * const p_sample, const data_representation * const p_medians, const double p_tolerance);


#endif
