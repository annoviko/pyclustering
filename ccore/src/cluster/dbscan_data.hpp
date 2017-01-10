/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#ifndef SRC_CLUSTER_DBSCAN_DATA_HPP_
#define SRC_CLUSTER_DBSCAN_DATA_HPP_


#include <memory>
#include <vector>

#include "cluster/cluster_data.hpp"


namespace cluster_analysis {


/**
*
* @brief    Clustering results of DBSCAM algorithm that consists of information about allocated
*           clusters and noise (points that are not related to any cluster).
*
*/
class dbscan_data : public cluster_data {
private:
    noise_ptr       m_noise = std::make_shared<cluster_analysis::noise>();

public:
    /**
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    */
    dbscan_data(void) = default;

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
    virtual ~dbscan_data(void) = default;

public:
    /**
    *
    * @brief    Returns shared pointer to noise.
    *
    */
    inline noise_ptr noise(void) { return m_noise; }
};


}


#endif
