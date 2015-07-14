/**************************************************************************************************************

Cluster analysis algorithm: Hierarchical Sync (HSyncNet)

Based on article description:
 - J.Shao, X.He, C.Bohm, Q.Yang, C.Plant. Synchronization-Inspired Partitioning and Hierarchical Clustering. 2013.

Copyright (C) 2015    Andrei Novikov (pyclustering@yandex.ru)

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


hsyncnet::hsyncnet(std::vector<std::vector<double> > * input_data, const unsigned int cluster_number, const initial_type initial_phases) :
syncnet(input_data, 0, false, initial_phases) { 
	number_clusters = cluster_number;
}


hsyncnet::~hsyncnet() { }


void hsyncnet::process(const double order, const solve_type solver, const bool collect_dynamic, hsyncnet_analyser & analyser) {
	unsigned int number_neighbors = 0;
	unsigned int current_number_clusters = std::numeric_limits<unsigned int>::max();

	double radius = 0.0;
	double current_time = 0.0;

	while(current_number_clusters > number_clusters) {
		create_connections(radius, false);

		sync_dynamic current_dynamic;
		simulate_dynamic(order, 0.1, solver, collect_dynamic, current_dynamic);

		sync_dynamic::const_iterator last_state_dynamic = current_dynamic.cend() - 1;
		analyser.push_back(*(last_state_dynamic));

		hsyncnet_cluster_data clusters;
		analyser.allocate_sync_ensembles(0.05, clusters);

		current_number_clusters = clusters.size();

		number_neighbors++;

		if (number_neighbors >= oscillator_locations->size()) {
			radius = radius * 0.1 + radius;
		}
		else {
			radius = average_neighbor_distance(oscillator_locations, number_neighbors);
		}
	}
}
