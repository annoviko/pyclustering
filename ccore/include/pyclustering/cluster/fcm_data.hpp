/*!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    pyclustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyclustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

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