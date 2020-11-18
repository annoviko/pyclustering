/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <memory>
#include <vector>

#include <pyclustering/cluster/cluster_data.hpp>

#include <pyclustering/definitions.hpp>


namespace pyclustering {

namespace clst {


/*!

@class    gmeans_data gmeans_data.hpp pyclustering/cluster/gmeans_data.hpp

@brief    Clustering results of G-Means algorithm that consists of information about allocated
           clusters and centers of each cluster.

*/
class gmeans_data : public cluster_data {
private:
    dataset       m_centers   = { };

    double        m_wce       = 0.0;

public:
    /*!
    
    @brief    Default constructor that creates empty clustering data.
    @details  In case of default constructor clusters and centers are not stored on each clustering iteration.
    
    */
    gmeans_data() = default;

    /*!
    
    @brief    Copy constructor that creates clustering data that is the same to specified.
    
    @param[in] p_other: another clustering data.
    
    */
    gmeans_data(const gmeans_data & p_other) = default;

    /*!
    
    @brief    Move constructor that creates clustering data from another by moving data.
    
    @param[in] p_other: another clustering data.
    
    */
    gmeans_data(gmeans_data && p_other) = default;

    /*!
    
    @brief    Default destructor that destroys clustering data.
    
    */
    virtual ~gmeans_data() = default;

public:
    /*!
    
    @brief    Returns reference to centers that correspond to allocated clusters.

    @return   Reference to centers that correspond to allocated clusters.
    
    */
    dataset & centers() { return m_centers; }

    /*!
    
    @brief    Returns constant reference to centers that correspond to allocated clusters.
    
    @return   Constant reference to centers that correspond to allocated clusters.

    */
    const dataset & centers() const { return m_centers; };

    /*!
    
    @brief    Returns total within-cluster errors.
    
    @return   Total within-cluster errors.

    */
    double & wce() { return m_wce; }

    /*!
    
    @brief    Returns constant total within-cluster errors.

    @return   Constant total within-cluster errors.
    
    */
    const double & wce() const { return m_wce; }
};


}

}