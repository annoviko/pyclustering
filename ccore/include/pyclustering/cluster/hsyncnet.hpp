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


#include <vector>

#include <pyclustering/cluster/syncnet.hpp>


namespace pyclustering {

namespace clst {


typedef std::vector<std::size_t>            hsyncnet_cluster;
typedef ensemble_data<hsyncnet_cluster>     hsyncnet_cluster_data;
typedef syncnet_analyser                    hsyncnet_analyser;


class hsyncnet: public syncnet {
private:
    std::size_t m_number_clusters;
    std::size_t m_initial_neighbors;
    double m_increase_persent;
    double m_time;

private:
    const static double         DEFAULT_TIME_STEP;
    const static std::size_t    DEFAULT_INCREASE_STEP;

public:
    hsyncnet(std::vector<std::vector<double> > * input_data, 
        const std::size_t cluster_number, 
        const initial_type initial_phases);

    hsyncnet(std::vector<std::vector<double> > * input_data,
        const std::size_t cluster_number,
        const initial_type initial_phases,
        const std::size_t initial_neighbors,
        const double increase_persent);

    virtual ~hsyncnet() = default;

public:
    virtual void process(const double order, const solve_type solver, const bool collect_dynamic, hsyncnet_analyser & analyser) override;

private:
    void store_state(sync_network_state & state, hsyncnet_analyser & analyser);

    double calculate_radius(const double radius, const std::size_t amount_neighbors) const;
};


}

}