/**
*
* Copyright (C) 2014-2016    Andrei Novikov (pyclustering@yandex.ru)
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

#include "cluster/hsyncnet.hpp"

#include <limits>
#include <cmath>

#include "utils.hpp"


hsyncnet::hsyncnet(std::vector<std::vector<double> > * input_data, const unsigned int cluster_number, const initial_type initial_phases) :
    syncnet(input_data, 0, false, initial_phases),
    m_number_clusters(cluster_number),
    m_initial_neighbors(3),
    m_increase_persent(0.15) { }

hsyncnet::hsyncnet(std::vector<std::vector<double> > * input_data, 
    const unsigned int cluster_number, 
    const initial_type initial_phases, 
    const unsigned int initial_neighbors, 
    const double increase_persent) :

    syncnet(input_data, 0, false, initial_phases),
    m_number_clusters(cluster_number),
    m_initial_neighbors(initial_neighbors),
    m_increase_persent(increase_persent) { }


hsyncnet::~hsyncnet() { }


void hsyncnet::process(const double order, const solve_type solver, const bool collect_dynamic, hsyncnet_analyser & analyser) {
	unsigned int number_neighbors = m_initial_neighbors;
	unsigned int current_number_clusters = std::numeric_limits<unsigned int>::max();

	double radius = average_neighbor_distance(oscillator_locations, number_neighbors);
    
    unsigned int increase_step = (unsigned int) round(oscillator_locations->size() * m_increase_persent);
    if (increase_step < 1) {
        increase_step = 1;
    }

    double current_time = 0.0;
    while(current_number_clusters > m_number_clusters) {
        create_connections(radius, false);

        sync_dynamic current_dynamic;
        simulate_dynamic(order, 0.1, solver, collect_dynamic, current_dynamic);

        sync_dynamic::iterator last_state_dynamic = current_dynamic.end() - 1;
        (*last_state_dynamic).m_time = current_time;
        analyser.push_back(*(last_state_dynamic));

        hsyncnet_cluster_data clusters;
        analyser.allocate_sync_ensembles(0.05, clusters);

        current_number_clusters = clusters.size();

        number_neighbors += increase_step;

        if (number_neighbors >= oscillator_locations->size()) {
            radius = radius * m_increase_persent + radius;
        }
        else {
            radius = average_neighbor_distance(oscillator_locations, number_neighbors);
        }

        current_time += 1.0;
    }
}
