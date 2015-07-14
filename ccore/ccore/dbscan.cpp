/**************************************************************************************************************

Cluster analysis algorithm: DBSCAN

Based on article description:
 - M.Ester, H.Kriegel, J.Sander, X.Xiaowei. A density-based algorithm for discovering clusters in large spatial 
   databases with noise. 1996.

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

#include "dbscan.h"
#include "support.h"

#if 1
	#define	FAST_SOLUTION
#endif


dbscan::dbscan(std::vector<std::vector<double> > * input_data, const double radius_connectivity, const unsigned int minimum_neighbors) {
	data = (std::vector<std::vector<double> > *) input_data;
#ifdef FAST_SOLUTION
	radius = radius_connectivity * radius_connectivity;
#else
	radius = radius_connectivity;
#endif
	neighbors = minimum_neighbors;

	clusters = new std::vector<std::vector<unsigned int> *>();
	visited = new std::vector<bool>(input_data->size(), false);
	belong = new std::vector<bool>(input_data->size(), false);
	noise = new std::vector<unsigned int>();

	matrix_neighbors = create_neighbor_matrix();
}


dbscan::~dbscan() {
	if (visited != NULL) {
		delete visited;
		visited = NULL;
	}

	if (belong != NULL) {
		delete belong;
		belong = NULL;
	}

	if (clusters != NULL) {
		for (std::vector<cluster *>::const_iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
			delete (*iter);
		}

		delete clusters;
		clusters = NULL;
	}

	if (noise != NULL) {
		delete noise;
		noise = NULL;
	}

	if (matrix_neighbors != NULL) {
		for (unsigned int index = 0; index < matrix_neighbors->size(); index++) {
			if ((*matrix_neighbors)[index] != NULL) {
				delete (*matrix_neighbors)[index];
				(*matrix_neighbors)[index] = NULL;
			}
		}

		delete matrix_neighbors;
		matrix_neighbors = NULL;
	}
}

void dbscan::process(void) {
	for (unsigned int i = 0; i < data->size(); i++) {
		if ((*visited)[i] == true) { continue; }

		(*visited)[i] = true;

		/* expand cluster */
		cluster * allocated_cluster = new cluster();
		if ( ((*matrix_neighbors)[i] != NULL) && ((*matrix_neighbors)[i]->size() >= neighbors) ) {
			allocated_cluster->push_back(i);
			(*belong)[i] = true;
#if 0
			std::cout << "Added to the cluster " << (unsigned int) allocated_cluster << " node [" << i << "]" << std::endl;
#endif

			/* get neighbors of the current node */
			std::vector<unsigned int> index_matrix_neighbors(*(*matrix_neighbors)[i]);

			for (unsigned int k = 0; k < index_matrix_neighbors.size(); k++) {
				unsigned int index_neighbor = index_matrix_neighbors[k];

				if ((*visited)[index_neighbor] != true) {
					(*visited)[index_neighbor] = true;

					/* check for neighbors of the current neighbor - maybe it's noise */
					std::vector<unsigned int> * neighbor_neighbor_indexes = (*matrix_neighbors)[index_neighbor];
					if ( (neighbor_neighbor_indexes != NULL) && (neighbor_neighbor_indexes->size() >= neighbors) ) {

						/* Add neighbors of the neighbor for checking */
						for (std::vector<unsigned int>::const_iterator neighbor_index = neighbor_neighbor_indexes->begin(); neighbor_index != neighbor_neighbor_indexes->end(); neighbor_index++) {
							/* Check if some of neighbors already in check list */
							std::vector<unsigned int>::const_iterator position = std::find(index_matrix_neighbors.begin(), index_matrix_neighbors.end(), *neighbor_index);
							if (position == index_matrix_neighbors.end()) {
								/* Add neighbor if it does not exist in the list */
								index_matrix_neighbors.push_back(*neighbor_index);
							}
						}
					}
				}

				if ((*belong)[index_neighbor] != true) {
					allocated_cluster->push_back(index_neighbor);
					(*belong)[index_neighbor] = true;
				}
			}

			index_matrix_neighbors.clear();
		}

		if (allocated_cluster->empty() != true) {
			clusters->push_back(allocated_cluster);
		}
		else {
			noise->push_back(i);
			(*belong)[i] = true;
		}
	}
}

std::vector<std::vector<unsigned int> * > * dbscan::create_neighbor_matrix(void) {
	std::vector<std::vector<unsigned int> * > * neighbor_matrix = new std::vector<std::vector<unsigned int> * >(data->size(), NULL);
	for (unsigned int point_index1 = 0; point_index1 < data->size(); point_index1++) {
		for (unsigned int point_index2 = (point_index1 + 1); point_index2 < data->size(); point_index2++) {
#ifdef FAST_SOLUTION
			double distance = euclidean_distance_sqrt(&((*data)[point_index1]), &((*data)[point_index2]));
#else
			double distance = euclidean_distance(&((*data)[point_index1]), &((*data)[point_index2]));
#endif
			if (distance < radius) {
				if ((*neighbor_matrix)[point_index1] == NULL) {
					(*neighbor_matrix)[point_index1] = new std::vector<unsigned int>();
				}

				if ((*neighbor_matrix)[point_index2] == NULL) {
					(*neighbor_matrix)[point_index2] = new std::vector<unsigned int>();
				}

				(*neighbor_matrix)[point_index1]->push_back(point_index2);
				(*neighbor_matrix)[point_index2]->push_back(point_index1);
			}
		}
	}

	return neighbor_matrix;
}
