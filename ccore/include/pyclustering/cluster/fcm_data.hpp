/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
*
* GNU_PUBLIC_LICENSE
*   pyclustering is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyclustering is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*
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
* @brief    Clustering results of Fuzzy C-Means algorithm that consists of information about allocated
*           clusters and centers of each cluster.
*
*/
class fcm_data : public cluster_data {
private:
    dataset       m_centers     = { };
    dataset       m_membership  = { };

public:
    dataset & centers() { return m_centers; }

    const dataset & centers() const { return m_centers; };

    dataset & membership() { return m_membership; }

    const dataset & membership() const { return m_membership; };
};


}

}