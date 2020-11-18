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


using representor_sequence = std::vector<dataset>;
using representor_sequence_ptr = std::shared_ptr<representor_sequence>;


/*!

@brief    Clustering results of CURE algorithm that consists of information about allocated
           clusters and their representative points and mean value.

*/
class cure_data : public cluster_data {
private:
    representor_sequence       m_representative_sequence = { };

    dataset                    m_mean_sequence = { };

public:
    /*!
    
    @brief    Default constructor that creates empty clustering data.
    
    */
    cure_data() = default;

    /*!
    
    @brief    Copy constructor that creates clustering data that is the same to specified.
    
    @param[in] p_other: another clustering data.
    
    */
    cure_data(const cure_data & p_other) = default;

    /*!
    
    @brief    Move constructor that creates clustering data from another by moving data.
    
    @param[in] p_other: another clustering data.
    
    */
    cure_data(cure_data && p_other) = default;

    /*!
    
    @brief    Default destructor that destroys clustering data.
    
    */
    virtual ~cure_data() = default;

public:
    /*!
    
    @brief    Returns reference to representative points of each cluster.
    @details  Cluster index should be used to navigate in collections of representative points.
               An example of representative points of two clusters:
               { {{ 1.0, 2.0 }, { 3.4, 4.0 }}, {{ 7.5, 6.3 }, { -1.4, -4.7 }} }
               where points { {{ 1.0, 2.0 }, { 3.4, 4.0 }} are related to the first cluster
               and {{ 7.5, 6.3 }, { -1.4, -4.7 }} to the second.
    
    @return   Shared pointer to representative points of each cluster.
    
    */
    representor_sequence & representors() { return m_representative_sequence; }

    /*!
    
    @brief    Returns constant reference to representative points of each cluster.
    
    */
    const representor_sequence & representors() const { return m_representative_sequence; }

    /*!
    
    @brief    Returns reference to mean point of each cluster.
    @details  Cluster index should be used to navigate in collections of mean points.
               An example of mean points of three clusters: { { 1.0, 2.0 }, { 3.4, 4.0 }, { 7.0, 9.1 } }
               where { 1.0, 2.0 } is mean of the first cluster, { 3.4, 4.0 } - mean of the second and
               { 7.0, 9.1 } of the third.
    
    @return   Shared pointer to mean point of each cluster.
    
    */
    dataset & means() { return m_mean_sequence; }

    /*!
    
    @brief    Returns constant reference to mean point of each cluster.
    
    */
    const dataset & means() const { return m_mean_sequence; }
};


}

}