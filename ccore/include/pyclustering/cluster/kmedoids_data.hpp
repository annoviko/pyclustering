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


using medoid_sequence = std::vector<size_t>;
using medoid_sequence_ptr = std::shared_ptr<medoid_sequence>;


/**
*
* @brief    Clustering results of K-Medoids algorithm that consists of information about allocated
*           clusters and medoids that correspond to them.
*
*/
class kmedoids_data : public cluster_data {
private:
    medoid_sequence     m_medoids = { };

public:
    /**
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    */
    kmedoids_data() = default;

    /**
    *
    * @brief    Copy constructor that creates clustering data that is the same to specified.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    kmedoids_data(const kmedoids_data & p_other) = default;

    /**
    *
    * @brief    Move constructor that creates clustering data from another by moving data.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    kmedoids_data(kmedoids_data && p_other) = default;

    /**
    *
    * @brief    Default destructor that destroys clustering data.
    *
    */
    virtual ~kmedoids_data() = default;

public:
    /**
    *
    * @brief    Returns medoids that corresponds to allocated clusters.
    *
    */
    medoid_sequence & medoids() { return m_medoids; }

    /**
    *
    * @brief    Returns medoids that corresponds to allocated clusters.
    *
    */
    const medoid_sequence & medoids() const { return m_medoids; }
};


}

}