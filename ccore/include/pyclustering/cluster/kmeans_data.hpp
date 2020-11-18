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

@class    kmeans_data kmeans_data.hpp pyclustering/cluster/kmeans_data.hpp

@brief    Clustering results of K-Means algorithm that consists of information about allocated
           clusters and centers of each cluster.

*/
class kmeans_data : public cluster_data {
private:
    dataset       m_centers   = { };

    bool          m_observed  = false;

    double        m_wce       = 0.0;

    std::vector<dataset> m_evolution_centers            = { };
    std::vector<cluster_sequence> m_evolution_clusters  = { };

public:
    /*!
    
    @brief    Default constructor that creates empty clustering data.
    @details  In case of default constructor clusters and centers are not stored on each clustering iteration.
    
    */
    kmeans_data() = default;

    /*!
    
    @brief    Constructor that provides flag to specify that clusters and centers changes are stored on each step.
    
    @param[in] p_iteration_observe: if 'true' then cluster and centers changes on each iteration are collected.
    
    */
    explicit kmeans_data(const bool p_iteration_observe);

    /*!
    
    @brief    Copy constructor that creates clustering data that is the same to specified.
    
    @param[in] p_other: another clustering data.
    
    */
    kmeans_data(const kmeans_data & p_other) = default;

    /*!
    
    @brief    Move constructor that creates clustering data from another by moving data.
    
    @param[in] p_other: another clustering data.
    
    */
    kmeans_data(kmeans_data && p_other) = default;

    /*!
    
    @brief    Default destructor that destroys clustering data.
    
    */
    virtual ~kmeans_data() = default;

public:
    /*!
    
    @brief    Returns reference to centers that correspond to allocated clusters.
    
    */
    dataset & centers() { return m_centers; }

    /*!
    
    @brief    Returns constant reference to centers that correspond to allocated clusters.
    
    */
    const dataset & centers() const { return m_centers; };

    /*!
    
    @brief    Returns 'true' if clusters and centers are collected during process of clustering.
    
    */
    bool is_observed() const { return m_observed; }

    /*!
    
    @brief    Returns total within-cluster errors.
    
    */
    double & wce() { return m_wce; }

    /*!
    
    @brief    Returns constant total within-cluster errors.
    
    */
    const double & wce() const { return m_wce; }

    /*!
    
    @brief    Returns reference to evolution of centers.
    @details  The evolution does not contain initial centers.
    
    */
    std::vector<dataset> & evolution_centers() { return m_evolution_centers; }

    /*!
    
    @brief    Returns constant reference to evolution of centers.
    @details  The evolution does not contain initial centers.
    
    */
    const std::vector<dataset> & evolution_centers() const { return m_evolution_centers; }

    /*!
    
    @brief    Returns reference to evolution of clusters.
    
    */
    std::vector<cluster_sequence> & evolution_clusters() { return m_evolution_clusters; }

    /*!
    
    @brief    Returns constant reference to evolution of clusters.
    
    */
    const std::vector<cluster_sequence> & evolution_clusters() const { return m_evolution_clusters; }
};


}

}