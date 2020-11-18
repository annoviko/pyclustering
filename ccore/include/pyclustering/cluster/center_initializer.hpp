/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <pyclustering/definitions.hpp>

#include <pyclustering/cluster/cluster_data.hpp>


namespace pyclustering {

namespace clst {


/*!

@brief Center initializer interface that provides general services to initialize centers.

*/
class center_initializer {
public:
    /*!
    
    @brief    Performs center initialization process in line algorithm configuration.
    
    @param[in]  p_data: data for that centers are calculated.
    @param[out] p_centers: initialized centers for the specified data.
    
    */
    virtual void initialize(const dataset & p_data, dataset & p_centers) const = 0;

    /*!
    
    @brief    Performs center initialization process in line algorithm configuration for
              specific range of points.
    
    @param[in]  p_data: data for that centers are calculated.
    @param[in]  p_indexes: point indexes from data that are defines which points should be considered
                 during calculation process. If empty then all data points are considered.
    @param[out] p_centers: initialized centers for the specified data.
    
    */
    virtual void initialize(const dataset & p_data, const index_sequence & p_indexes, dataset & p_centers) const = 0;
};


}

}