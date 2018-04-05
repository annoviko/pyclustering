/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


#include "cluster/dbscan_data.hpp"


namespace ccore {

namespace clst {


using ordering = std::vector<double>;
using ordering_ptr = std::shared_ptr<ordering>;


/**
*
* @brief    Clustering results of OPTICS algorithm that consists of information about allocated
*           clusters and noise (points that are not related to any cluster), ordering (that represents
*           density-based clustering structure) and proper radius.
*
*/
class optics_data : public dbscan_data {
private:
    ordering         m_ordering = { };
    double           m_radius   = 0;

public:
    /**
    *
    * @brief    Default constructor that creates empty clustering data.
    *
    */
    optics_data(void) = default;

    /**
    *
    * @brief    Default copy constructor.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    optics_data(const optics_data & p_other) = default;

    /**
    *
    * @brief    Default move constructor.
    *
    * @param[in] p_other: another clustering data.
    *
    */
    optics_data(optics_data && p_other) = default;

    /**
    *
    * @brief    Default destructor that destroys clustering data..
    *
    */
    virtual ~optics_data(void) = default;

public:
    /**
    *
    * @brief    Returns reference to cluster-ordering that represents density-based clustering structure.
    *
    */
    ordering & cluster_ordering(void) { return m_ordering; }

    /**
    *
    * @brief    Returns const reference to cluster-ordering that represents density-based clustering structure.
    *
    */
    const ordering & cluster_ordering(void) const { return m_ordering; }

    /**
    *
    * @brief    Returns connectivity radius that can be differ from input parameter.
    * @details  It may be changed by OPTICS ('optics') algorithm if there is requirement to
    *           allocate specified amount of clusters.
    *
    */
    double get_radius(void) const { return m_radius; }

    /**
    *
    * @brief    Set new value for connectivity radius.
    *
    */
    void set_radius(const double p_radius) { m_radius = p_radius; }
};


}

}