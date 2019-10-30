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

#include <pyclustering/cluster/hsyncnet.hpp>

#include <limits>
#include <cmath>

#include <pyclustering/utils/metric.hpp>


using namespace pyclustering::utils::metric;
using namespace pyclustering::nnet;


namespace pyclustering {

namespace clst {


const double        hsyncnet::DEFAULT_TIME_STEP         = 1.0;
const std::size_t   hsyncnet::DEFAULT_INCREASE_STEP     = 1;


hsyncnet::hsyncnet(std::vector<std::vector<double> > * input_data, const std::size_t cluster_number, const initial_type initial_phases) :
    syncnet(input_data, 0, false, initial_phases),
    m_number_clusters(cluster_number),
    m_initial_neighbors(3),
    m_increase_persent(0.15),
    m_time(0.0)
{ }

hsyncnet::hsyncnet(std::vector<std::vector<double> > * input_data, 
    const std::size_t cluster_number, 
    const initial_type initial_phases, 
    const std::size_t initial_neighbors, 
    const double increase_persent) :

    syncnet(input_data, 0, false, initial_phases),
    m_number_clusters(cluster_number),
    m_initial_neighbors(initial_neighbors),
    m_increase_persent(increase_persent),
    m_time(0.0)
{ }


void hsyncnet::process(const double order, const solve_type solver, const bool collect_dynamic, hsyncnet_analyser & analyser) {
    std::size_t number_neighbors = m_initial_neighbors;
    std::size_t current_number_clusters = m_oscillators.size();

    if (current_number_clusters <= m_number_clusters) {
        return;   /* Nothing to process, amount of objects is less than required amount of clusters. */
    }

    double radius = average_neighbor_distance(oscillator_locations, number_neighbors);
    
    std::size_t increase_step = static_cast<std::size_t>(round(oscillator_locations->size() * static_cast<std::size_t>(m_increase_persent)));
    if (increase_step < 1) {
        increase_step = DEFAULT_INCREASE_STEP;
    }

    sync_dynamic current_dynamic;
    do {
        create_connections(radius, false);

        simulate_dynamic(order, 0.1, solver, collect_dynamic, current_dynamic);

        if (collect_dynamic) {
            if (analyser.empty()) {
                store_state(*(current_dynamic.begin()), analyser);
            }

            store_state(*(current_dynamic.end() - 1), analyser);
        }
        else {
            m_time += DEFAULT_TIME_STEP;
        }

        hsyncnet_cluster_data clusters;
        current_dynamic.allocate_sync_ensembles(0.05, clusters);

        current_number_clusters = clusters.size();

        number_neighbors += increase_step;
        radius = calculate_radius(radius, number_neighbors);
    }
    while(current_number_clusters > m_number_clusters);

    if (!collect_dynamic) {
        store_state(*(current_dynamic.end() - 1), analyser);
    }
}


void hsyncnet::store_state(sync_network_state & state, hsyncnet_analyser & analyser) {
    state.m_time = m_time;
    analyser.push_back(state);

    m_time += DEFAULT_TIME_STEP;
}


double hsyncnet::calculate_radius(const double radius, const std::size_t amount_neighbors) const {
    double next_radius = 0.0;
    if (amount_neighbors >= oscillator_locations->size()) {
        next_radius = radius * m_increase_persent + radius;
    }
    else {
        next_radius = average_neighbor_distance(oscillator_locations, amount_neighbors);
    }

    return next_radius;
}


}

}