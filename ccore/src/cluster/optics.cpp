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

#include "cluster/optics.hpp"

#include "utils.hpp"


namespace cluster_analysis {


optics_descriptor::optics_descriptor(const std::size_t p_index, const double p_core_distance, const double p_reachability_distance) :
    m_index(p_index),
    m_core_distance(p_core_distance),
    m_reachability_distance(p_reachability_distance),
    m_processed(false) 
{ }


const double optics::NONE_DISTANCE = -1.0;


optics::optics(const double p_radius, const std::size_t p_neighbors) : optics() { 
    m_radius = p_radius;
    m_neighbors = p_neighbors;
}


optics::optics(const double p_radius, const std::size_t p_neighbors, const std::size_t p_amount_clusters) : optics() { 
    m_radius = p_radius;
    m_neighbors = p_neighbors;
    m_amount_clusters = p_amount_clusters;
}


void optics::process(const dataset & p_data, cluster_data & p_result) {
    m_data_ptr = &p_data;
    m_result_ptr = (optics_data *) &p_result;

    m_data_ptr = nullptr;
    m_result_ptr = nullptr;
}


void optics::initialize(void) {
    m_optics_objects.reserve(m_data_ptr->size());

    for (std::size_t i = 0; i < m_data_ptr->size(); i++) {
        m_optics_objects.emplace_back(i, 0, 0);
    }
}


void optics::allocate_clusters(void) {
    for (auto & optics_object : m_optics_objects) {
        if (!optics_object.m_processed) {
            expand_cluster_order(optics_object);
        }
    }

    extract_clusters();
}


void optics::expand_cluster_order(optics_descriptor & p_object) {
    p_object.m_processed = true;

    std::vector< std::tuple<std::size_t, double> > neighbors;
    get_neighbors(p_object.m_index, neighbors);

    m_ordered_database.push_back(&p_object);

    if (neighbors.size() >= m_neighbors) {
        std::sort(neighbors.begin(), neighbors.end(), [](const auto & a, const auto & b) { return std::get<1>(a) < std::get<1>(b); });
		p_object.m_core_distance = std::get<1>(neighbors[m_neighbors - 1]);

		std::list<optics_descriptor *> order_seed;
		update_order_seed(p_object, neighbors, order_seed);

		std::size_t order_seed_length = order_seed.size();
		while(order_seed_length > 0) {
			optics_descriptor * descriptor = order_seed.front();
			order_seed.erase(order_seed.begin());

			get_neighbors(descriptor->m_index, neighbors);
			descriptor->m_processed = true;

			m_ordered_database.push_back(descriptor);

			if (neighbors.size() >= m_neighbors) {
				std::sort(neighbors.begin(), neighbors.end(), [](const auto & a, const auto & b) { return std::get<1>(a) < std::get<1>(b); });
				descriptor->m_core_distance = std::get<1>(neighbors[m_neighbors - 1]);

				update_order_seed(*descriptor, neighbors, order_seed);
			}
			else {
				descriptor->m_core_distance = optics::NONE_DISTANCE;
			}

			order_seed_length = order_seed.size();
		}
    }
	else {
		p_object.m_core_distance = optics::NONE_DISTANCE;
	}
}


void optics::update_order_seed(const optics_descriptor & p_object, const std::vector< std::tuple<std::size_t, double> > & neighbors, std::list<optics_descriptor *> & order_seed) {
	for (auto & descriptor : neighbors) {
		std::size_t index_neighbor = std::get<0>(descriptor);
		double current_reachability_distance = std::get<1>(descriptor);

		if (!m_optics_objects[index_neighbor].m_processed) {
			double reachable_distance = std::max({ current_reachability_distance, p_object.m_reachability_distance });

			if (m_optics_objects[index_neighbor].m_reachability_distance == optics::NONE_DISTANCE) {
				m_optics_objects[index_neighbor].m_reachability_distance = reachable_distance;

				auto position_insertion = order_seed.end();
				for (auto position = order_seed.begin(); position != order_seed.end(); position++) {
					if (reachable_distance < (*position)->m_reachability_distance) {
						position_insertion = position;
						break;
					}
				}

				order_seed.insert(position_insertion, &m_optics_objects[index_neighbor]);
			}
			else {
				if (reachable_distance < m_optics_objects[index_neighbor].m_reachability_distance) {
					m_optics_objects[index_neighbor].m_reachability_distance = reachable_distance;
					order_seed.sort([](const auto & a, const auto & b) { return a->m_reachability_distance < b->m_reachability_distance; });
				}
			}
		}
	}
}


void optics::extract_clusters(void) {
	m_result_ptr->clusters()->clear();
	m_result_ptr->noise()->clear();
	m_result_ptr->ordering()->clear();

	cluster_sequence_ptr clusters = m_result_ptr->clusters();
	noise_ptr noise = m_result_ptr->noise();

	std::size_t index_current_cluster = 0;
	clusters->push_back(cluster());

	for (auto optics_object : m_ordered_database) {
		if ( (optics_object->m_reachability_distance == optics::NONE_DISTANCE) || (optics_object->m_reachability_distance > m_radius) ) {
			if ( (optics_object->m_core_distance != optics::NONE_DISTANCE) && (optics_object->m_core_distance <= m_radius) ) {
				if (clusters->at(index_current_cluster).size() > 0) {
					index_current_cluster++;
					clusters->push_back(cluster());
				}

				clusters->at(index_current_cluster).push_back(optics_object->m_index);
			}
			else {
				noise->push_back(optics_object->m_index);
			}
		}
	}
}


void optics::get_neighbors(const size_t p_index, std::vector< std::tuple<std::size_t, double> > & p_neighbors) {
    for (size_t index = 0; index < m_data_ptr->size(); index++) {
        point object1 = (*m_data_ptr)[index];
        point object2 = (*m_data_ptr)[p_index];

        const double distance = euclidean_distance_sqrt(object1, object2);

        if ( ( p_index != index ) && ( distance <= m_radius ) ) {
            p_neighbors.push_back(std::make_tuple(index, distance));
        }
    }
}


}