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

#include "cluster/dbscan.hpp"

#include "utils.hpp"


namespace cluster_analysis {


dbscan::dbscan(void) :
    m_data_ptr(nullptr),
    m_result_ptr(nullptr),
    m_radius(0.0),
    m_neighbors(0),
    m_visited(std::vector<bool>()),
    m_belong(std::vector<bool>())
{ }


dbscan::dbscan(const double p_radius_connectivity, const size_t p_minimum_neighbors) :
    m_data_ptr(nullptr),
    m_result_ptr(nullptr),
    m_radius(p_radius_connectivity * p_radius_connectivity),
    m_neighbors(p_minimum_neighbors),
    m_visited(std::vector<bool>()),
    m_belong(std::vector<bool>())
{ }


dbscan::~dbscan(void) { }


void dbscan::process(const dataset & p_data, cluster_data & p_result) {
    m_data_ptr = &p_data;

    m_visited = std::vector<bool>(m_data_ptr->size(), false);
    m_belong = std::vector<bool>(m_data_ptr->size(), false);

    m_result_ptr = (dbscan_data *) &p_result;

    for (size_t i = 0; i < m_data_ptr->size(); i++) {
        if (m_visited[i] == true) {
            continue;
        }

        m_visited[i] = true;

        /* expand cluster */
        cluster allocated_cluster;

        std::vector<size_t> index_matrix_neighbors;
        get_neighbors(i, index_matrix_neighbors);

        if (index_matrix_neighbors.size() >= m_neighbors) {
            allocated_cluster.push_back(i);
            m_belong[i] = true;

            for (size_t k = 0; k < index_matrix_neighbors.size(); k++) {
                size_t index_neighbor = index_matrix_neighbors[k];

                if (m_visited[index_neighbor] != true) {
                    m_visited[index_neighbor] = true;

                    /* check for neighbors of the current neighbor - maybe it's noise */
                    std::vector<size_t> neighbor_neighbor_indexes;
                    get_neighbors(index_neighbor, neighbor_neighbor_indexes);
                    if (neighbor_neighbor_indexes.size() >= m_neighbors) {

                        /* Add neighbors of the neighbor for checking */
                        for (auto neighbor_index : neighbor_neighbor_indexes) {
                            /* Check if some of neighbors already in check list */
                            std::vector<size_t>::const_iterator position = std::find(index_matrix_neighbors.begin(), index_matrix_neighbors.end(), neighbor_index);
                            if (position == index_matrix_neighbors.end()) {
                                /* Add neighbor if it does not exist in the list */
                                index_matrix_neighbors.push_back(neighbor_index);
                            }
                        }
                    }
                }

                if (m_belong[index_neighbor] != true) {
                    allocated_cluster.push_back(index_neighbor);
                    m_belong[index_neighbor] = true;
                }
            }

            index_matrix_neighbors.clear();
        }

        if (allocated_cluster.empty() != true) {
            m_result_ptr->clusters()->push_back(allocated_cluster);
        }
        else {
            m_result_ptr->noise()->push_back(i);
            m_belong[i] = true;
        }
    }

    m_data_ptr = nullptr;
    m_result_ptr = nullptr;
}


void dbscan::get_neighbors(const size_t p_index, std::vector<size_t> & p_neighbors) {
    for (size_t index = 0; index < m_data_ptr->size(); index++) {
        if ( ( p_index != index ) && ( euclidean_distance_sqrt(&((*m_data_ptr)[index]), &((*m_data_ptr)[p_index])) <= m_radius ) ) {
            p_neighbors.push_back(index);
        }
    }
}


}
