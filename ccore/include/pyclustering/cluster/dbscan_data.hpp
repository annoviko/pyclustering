/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <memory>
#include <vector>

#include <pyclustering/cluster/cluster_data.hpp>


namespace pyclustering {

namespace clst {


/*!

@class    dbscan_data dbscan_data.hpp pyclustering/cluster/dbscan_data.hpp

@brief    Clustering results of DBSCAM algorithm that consists of information about allocated
           clusters and noise (points that are not related to any cluster).

*/
class dbscan_data : public cluster_data {
private:
    clst::noise       m_noise;

public:
    /*!
    
    @brief    Default constructor that creates empty clustering data.
    
    */
    dbscan_data() = default;

    /*!
    
    @brief    Copy constructor of DBSCAN clustering data.
    
    @param[in] p_other: another DBSCAN clustering data.
    
    */
    dbscan_data(const dbscan_data & p_other) = default;

    /*!
    
    @brief    Move constructor of DBSCAN clustering data.
    
    @param[in] p_other: another clustering data.
    
    */
    dbscan_data(dbscan_data && p_other) = default;

    /*!
    
    @brief    Default destructor that destroys DBSCAN clustering data.
    
    */
    virtual ~dbscan_data() = default;

public:
    /*!
    
    @brief    Returns reference to outliers represented by indexes.
    
    */
    clst::noise & noise() { return m_noise; }

    /*!
    
    @brief    Returns constant reference to outliers represented by indexes.
    
    */
    const clst::noise & noise() const { return m_noise; }
};


}

}