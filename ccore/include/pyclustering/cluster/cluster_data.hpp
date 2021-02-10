/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

*/

#pragma once


#include <vector>
#include <memory>


namespace pyclustering {

namespace clst {


using noise = std::vector<size_t>;
using noise_ptr = std::shared_ptr<noise>;

using index_sequence = std::vector<std::size_t>;

using cluster = std::vector<std::size_t>;
using cluster_sequence = std::vector<cluster>;
using cluster_sequence_ptr = std::shared_ptr<cluster_sequence>;


/*!

@class    cluster_data cluster_data.hpp pyclustering/cluster/cluster_data.hpp

@brief    Represents result of cluster analysis.

*/
class cluster_data {
protected:
    cluster_sequence      m_clusters = { };     /**< Allocated clusters during clustering process. */

public:
    /*!
    
    @brief    Default constructor that creates empty clustering data.
    
    */
    cluster_data() = default;

    /*!
    
    @brief    Copy constructor that creates clustering data that is the same to specified.
    
    @param[in] p_other: another clustering data.
    
    */
    cluster_data(const cluster_data & p_other) = default;

    /*!
    
    @brief    Move constructor that creates clustering data from another by moving data.
    
    @param[in] p_other: another clustering data.
    
    */
    cluster_data(cluster_data && p_other) = default;

    /*!
    
    @brief    Default destructor that destroy clustering data.
    
    */
    virtual ~cluster_data() = default;

public:
    /*!
    
    @brief    Returns reference to clusters.
    
    */
    cluster_sequence & clusters();

    /*!
    
    @brief    Returns constant reference to clusters.
    
    */
    const cluster_sequence & clusters() const;

    /*!
    
    @brief    Returns amount of clusters.
    
    */
    std::size_t size() const;

public:
    /*!
    
    @brief    Provides access to specified cluster.
    
    @param[in] p_index: index of specified cluster.
    
    */
    cluster & operator[](const size_t p_index);

    /*!
    
    @brief    Provides access to specified cluster.
    
    @param[in] p_index: index of specified cluster.
    
    */
    const cluster & operator[](const size_t p_index) const;

    /*!
    
    @brief    Compares clustering data.
    
    @param[in] p_other: another clustering data that is used for comparison.
    
    @return  Returns true if both objects have the same amount of clusters with the same elements.
    
    */
    bool operator==(const cluster_data & p_other) const;

    /*!
    
    @brief    Compares clustering data.
    
    @param[in] p_other: another clustering data that is used for comparison.
    
    @return  Returns true if both objects have are not the same.
    
    */
    bool operator!=(const cluster_data & p_other) const;
};


}

}