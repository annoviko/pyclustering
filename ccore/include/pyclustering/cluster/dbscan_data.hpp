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


namespace pyclustering {

namespace clst {


/**
*
* @brief    Clustering results of DBSCAM algorithm that consists of information about allocated
*           clusters and noise (points that are not related to any cluster).
*
*/
class dbscan_data : public cluster_data {
private:
    clst::noise       m_noise;

public:
    /**
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    */
    dbscan_data() = default;

    /**
    *
    * @brief    Copy constructor that creates clustering data that is the same to specified.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    dbscan_data(const dbscan_data & p_other) = default;

    /**
    *
    * @brief    Move constructor that creates clustering data from another by moving data.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    dbscan_data(dbscan_data && p_other) = default;

    /**
    *
    * @brief    Default destructor that destroys clustering data.
    *
    */
    virtual ~dbscan_data() = default;

public:
    /**
    *
    * @brief    Returns reference to noise.
    *
    */
    clst::noise & noise() { return m_noise; }

    /**
    *
    * @brief    Returns constant reference to noise.
    *
    */
    const clst::noise & noise() const { return m_noise; }
};


}

}