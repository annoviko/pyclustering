/**************************************************************************************************************

Cluster analysis algorithm: Hierarchical Sync (HSyncNet)

Based on article description:
 - J.Shao, X.He, C.Bohm, Q.Yang, C.Plant. Synchronization-Inspired Partitioning and Hierarchical Clustering. 2013.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

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

**************************************************************************************************************/

#include "hsyncnet.h"
#include "support.h"

#include <limits>

/***********************************************************************************************
 *
 * @brief   Contructor of the oscillatory network heirarchical SYNC for cluster analysis.
 *
 * @param   (in) input_data            - input data for clustering.
 * @param   (in) initial_phases        - type of initialization of initial phases of oscillators.
 *
 ***********************************************************************************************/
hsyncnet::hsyncnet(std::vector<std::vector<double> > * input_data, const unsigned int cluster_number, const initial_type initial_phases) :
syncnet(input_data, 0, false, initial_phases) { 
	number_clusters = cluster_number;
}

/***********************************************************************************************
 *
 * @brief   Default destructor.
 *
 ***********************************************************************************************/
hsyncnet::~hsyncnet() { }

std::vector< std::vector<sync_dynamic> * > * hsyncnet::process(const double order, const solve_type solver, const bool collect_dynamic) {
	unsigned int number_neighbors = 3;
	unsigned int current_number_clusters = std::numeric_limits<unsigned int>::max();

	double radius = average_neighbor_distance(oscillator_locations, number_neighbors);
	double current_time = 0.0;

	std::vector< std::vector<sync_dynamic> * > * dynamic = new std::vector< std::vector<sync_dynamic> * >();

	while(current_number_clusters > number_clusters) {
		create_connections(radius, false);

		std::vector< std::vector<sync_dynamic> * > * current_dynamic = simulate_dynamic(order, solver, collect_dynamic);

		double counter_timer = 0.0;
		for (std::vector< std::vector<sync_dynamic> * >::iterator iter = current_dynamic->begin(); iter != current_dynamic->end(); iter++) {
			for (std::vector<sync_dynamic>::iterator osc_dyn = (*iter)->begin(); osc_dyn != (*iter)->end(); osc_dyn++) {
				(*osc_dyn).time += current_time;
				counter_timer = (*osc_dyn).time;	
			}
			dynamic->push_back(*iter);
		}

		current_time = counter_timer;

		delete current_dynamic;

		std::vector< std::vector<unsigned int> * > * clusters = allocate_sync_ensembles(0.05);
		current_number_clusters = clusters->size();

		number_neighbors++;

		if (number_neighbors >= oscillator_locations->size()) {
			radius = radius * 0.1 + radius;
		}
		else {
			radius = average_neighbor_distance(oscillator_locations, number_neighbors);
		}
	}

	return dynamic;
}
