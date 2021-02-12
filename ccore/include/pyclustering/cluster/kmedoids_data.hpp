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

    std::size_t         m_iterations = 0;

    double              m_total_deviation = 0.0;

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
    * @brief    Returns reference to medoids that correspond to allocated clusters.
    *
    */
    medoid_sequence & medoids() { return m_medoids; }

    /**
    *
    * @brief    Returns constant reference to medoids that correspond to allocated clusters.
    *
    */
    const medoid_sequence & medoids() const { return m_medoids; }

    /*
    
    @brief      Returns reference to the amount of iterations that were performed during the clustering process.

    */
    std::size_t & iterations() { return m_iterations; }

    /*

    @brief      Returns the amount of iterations that were performed during the clustering process.

    */
    std::size_t iterations() const { return m_iterations; }

    /*

    @brief      Returns reference to the final loss (total deviation).

    */
    double & total_deviation() { return m_total_deviation; }

    /*

    @brief      Returns the final loss (total deviation).

    */
    double total_deviation() const { return m_total_deviation; }
};


}

}