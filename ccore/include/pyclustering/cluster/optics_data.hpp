/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/


#pragma once


#include <pyclustering/cluster/dbscan_data.hpp>
#include <pyclustering/cluster/optics_descriptor.hpp>


namespace pyclustering {

namespace clst {


/*!

@brief  Sequence container where ordering diagram is stored.

*/
using ordering                = std::vector<double>;

/*!

@brief  Sequence container where OPTICS descriptors are stored.

*/
using optics_object_sequence  = std::vector<optics_descriptor>;


/*!

@class    optics_data optics_data.hpp pyclustering/cluster/optics_data.hpp

@brief    Clustering results of OPTICS algorithm that consists of information about allocated
           clusters and noise (points that are not related to any cluster), ordering (that represents
           density-based clustering structure) and proper radius.

*/
class optics_data : public dbscan_data {
private:
    ordering                m_ordering = { };
    double                  m_radius   = 0;
    optics_object_sequence  m_optics_objects = { };

public:
    /*!
    
    @brief    Default constructor that creates empty clustering data.
    
    */
    optics_data() = default;

    /*!
    
    @brief    Default copy constructor.
    
    @param[in] p_other: another clustering data.
    
    */
    optics_data(const optics_data & p_other) = default;

    /*!
    
    @brief    Default move constructor.
    
    @param[in] p_other: another clustering data.
    
    */
    optics_data(optics_data && p_other) = default;

    /*!
    
    @brief    Default destructor that destroys clustering data.
    
    */
    virtual ~optics_data() = default;

public:
    /*!
    
    @brief    Returns reference to cluster-ordering that represents density-based clustering structure.
    
    @return   Reference to cluster-ordering that represents density-based clustering structure.

    */
    ordering & cluster_ordering() { return m_ordering; }

    /*!
    
    @brief    Returns const reference to cluster-ordering that represents density-based clustering structure.
    
    @return   Const reference to cluster-ordering that represents density-based clustering structure.

    */
    const ordering & cluster_ordering() const { return m_ordering; }

    /*!
    
    @brief    Returns reference to optics objects that corresponds to points from input dataspace.
    
    @return   Reference to optics objects that corresponds to points from input dataspace.

    */
    optics_object_sequence & optics_objects() { return m_optics_objects; }

    /*!
    
    @brief    Returns const reference to optics objects that corresponds to points from input dataspace.
    
    @return   Const reference to optics objects that corresponds to points from input dataspace.

    */
    const optics_object_sequence & optics_objects() const { return m_optics_objects; }

    /*!
    
    @brief    Returns connectivity radius that can be differ from input parameter.
    @details  It may be changed by OPTICS ('optics') algorithm if there is requirement to
               allocate specified amount of clusters.
    
    @return   Connectivity radius.

    */
    double get_radius() const { return m_radius; }

    /*!
    
    @brief    Set new value for connectivity radius.
    
    @param[in] p_radius: new value of the connectivity radius.

    */
    void set_radius(const double p_radius) { m_radius = p_radius; }
};


}

}