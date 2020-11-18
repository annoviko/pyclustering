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


/**
*
* @brief    Clustering results of K-Medians algorithm that consists of information about allocated
*           clusters and medians of each cluster.
*
*/
class kmedians_data : public cluster_data {
private:
    dataset       m_medians = { };

public:
    /**
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    */
    kmedians_data() = default;

    /**
    *
    * @brief    Copy constructor that creates clustering data that is the same to specified.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    kmedians_data(const kmedians_data & p_other) = default;

    /**
    *
    * @brief    Move constructor that creates clustering data from another by moving data.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    kmedians_data(kmedians_data && p_other) = default;

    /**
    *
    * @brief    Default destructor that destroys clustering data.
    *
    */
    virtual ~kmedians_data() = default;

public:
    /**
    *
    * @brief    Returns reference to medians that correspond to allocated clusters.
    *
    */
    dataset & medians() { return m_medians; }

    /**
    *
    * @brief    Returns constant reference to medians that correspond to allocated clusters.
    *
    */
    const dataset & medians() const { return m_medians; }
};


}

}