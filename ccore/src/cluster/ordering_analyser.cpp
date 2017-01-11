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


#include "ordering_analyser.hpp"


#include <algorithm>
#include <limits>


namespace cluster_analysis {


ordering_analyser::ordering_analyser(const ordering_ptr & p_ordering) : m_ordering(p_ordering) { }


double ordering_analyser::calculate_connvectivity_radius(const std::size_t p_amount_clusters) const {
	const double maximum_distance = *std::max_element(m_ordering->cbegin(), m_ordering->cend());

	double upper_distance = maximum_distance;
	double lower_distance = 0.0;

	double radius = -1.0;
	
	if (extract_cluster_amount(maximum_distance) <= p_amount_clusters) {
		while(true) {
			radius = (lower_distance + upper_distance) / 2.0;

			std::size_t amount = extract_cluster_amount(radius);
			if (amount == p_amount_clusters) {
				break;
			}
			else if (amount > p_amount_clusters) {
				lower_distance = radius;
			}
			else if (amount < p_amount_clusters) {
				upper_distance = radius;
			}
		}
	}

	return radius;
}


std::size_t ordering_analyser::extract_cluster_amount(const double p_radius) const {
	std::size_t amount_clusters = 1;

	bool cluster_start = false;
	bool cluster_pick = false;

	double previous_distance = 0.0;

	for (auto & distance : *m_ordering) {
		if (distance >= p_radius) {
			if (!cluster_start) {
				cluster_start = true;
				amount_clusters++;
			}
			else {
				if ( (distance < previous_distance) && (!cluster_pick) ) {
					cluster_pick = true;
				}
				else if ( (distance > previous_distance) && (cluster_pick) ) {
					cluster_pick = false;
					amount_clusters += 1;
				}
			}

			previous_distance = distance;
		}
		else {
			cluster_start = false;
			cluster_pick = false;
		}
	}

	return amount_clusters;
}


}
