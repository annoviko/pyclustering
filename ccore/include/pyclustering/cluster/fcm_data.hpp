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

@brief  Container for membership (probability) of each point from data.

*/
using membership_sequence = dataset;


/*!

@class    fcm_data fcm_data.hpp pyclustering/cluster/fcm_data.hpp

@brief    Clustering results of Fuzzy C-Means algorithm that consists of information about allocated
           clusters and centers of each cluster.

*/
class fcm_data : public cluster_data {
private:
    dataset       m_centers     = { };
    dataset       m_membership  = { };

public:
    /*!
    
    @brief  Returns reference to centers of allocated clusters.

    @return Reference to centers of allocated clusters.
    
    */
    dataset & centers() { return m_centers; }

    /*!

    @brief  Returns const reference to centers of allocated clusters.

    @return Const reference to centers of allocated clusters.

    */
    const dataset & centers() const { return m_centers; };

    /*!

    @brief  Returns reference to cluster membership (probability) for each point in data.

    @return Reference to cluster membership (probability) for each point in data.

    */
    membership_sequence & membership() { return m_membership; }

    /*!

    @brief  Returns constant reference to cluster membership (probability) for each point in data.

    @return Constant reference to cluster membership (probability) for each point in data.

    */
    const membership_sequence & membership() const { return m_membership; };
};


}

}