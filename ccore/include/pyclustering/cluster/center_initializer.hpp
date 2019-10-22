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


#include <pyclustering/definitions.hpp>

#include <pyclustering/cluster/cluster_data.hpp>


namespace pyclustering {

namespace clst {


class center_initializer {
public:
    /**
    *
    * @brief    Performs center initialization process in line algorithm configuration.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[out] p_centers: initialized centers for the specified data.
    *
    */
    virtual void initialize(const dataset & p_data, dataset & p_centers) const = 0;

    /**
    *
    * @brief    Performs center initialization process in line algorithm configuration for
    *           specific range of points.
    *
    * @param[in]  p_data: data for that centers are calculated.
    * @param[in]  p_indexes: point indexes from data that are defines which points should be considered
    *              during calculation process. If empty then all data points are considered.
    * @param[out] p_centers: initialized centers for the specified data.
    *
    */
    virtual void initialize(const dataset & p_data, const index_sequence & p_indexes, dataset & p_centers) const = 0;
};


}

}