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


#include <pyclustering/cluster/fcm_data.hpp>


namespace pyclustering {

namespace clst {


class fcm {
public:
    const static double             DEFAULT_TOLERANCE;

    const static std::size_t        DEFAULT_ITERMAX;

    const static double             DEFAULT_HYPER_PARAMETER;

private:
    double          m_tolerance             = DEFAULT_TOLERANCE;

    std::size_t     m_itermax               = DEFAULT_ITERMAX;

    dataset         m_initial_centers       = { };

    double          m_degree                = 0.0;

    fcm_data        * m_ptr_result          = nullptr;      /* temporary pointer to output result */

    const dataset   * m_ptr_data            = nullptr;      /* used only during processing */

public:
    fcm() = default;

    fcm(const dataset & p_initial_centers, 
        const double p_m = DEFAULT_HYPER_PARAMETER,
        const double p_tolerance = DEFAULT_TOLERANCE,
        const std::size_t p_itermax = DEFAULT_ITERMAX);
    
    ~fcm() = default;

public:
    void process(const dataset & p_data, cluster_data & p_result);

private:
    void verify() const;

    double update_centers();

    double update_center(const std::size_t p_index);

    void update_membership();

    void update_point_membership(const std::size_t p_index);

    void extract_clusters(cluster_sequence & p_clusters);
};


}

}