#include <stddef.h>

#include <cmath>
#include <vector>
#include <algorithm>

#include <iostream>

using std::vector;

typedef vector<vector<double> >  	matrix;
typedef vector<int>		cluster;

#if 1
	#define	FAST_SOLUTION
#endif

inline double euclidean_distance_sqrt(const vector<double> * const point1, const vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return distance;
}

inline double euclidean_distance(const vector<double> * const point1, const vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return std::sqrt(distance);
}

inline void print_cluster(const vector<int> * const pointer_cluster) {
	std::cout << "[ ";
	for (vector<int>::const_iterator iter = pointer_cluster->begin(); iter != pointer_cluster->end(); iter++) {
		std::cout << (*iter) << " ";
	}
	std::cout << "] " << std::endl;
}



class dbscan {
private:
	matrix *				data;
	vector<bool> * 			visited;
	vector<bool> *			belong;
	vector<cluster *> *		clusters;
	vector<int> *			noise;
	vector<vector<int> *> *	matrix_neighbors;

	double					radius;
	unsigned int			neighbors;

public:
	dbscan(const matrix * const input_data, const double radius_connectivity, const unsigned int minimum_neighbors) {
		data = (matrix *) input_data;
#ifdef FAST_SOLUTION
		radius = radius_connectivity * radius_connectivity;
#else
		radius = radius_connectivity;
#endif
		neighbors = minimum_neighbors;

		clusters = new vector<cluster *>();
		visited = new vector<bool>(input_data->size(), false);
		belong = new vector<bool>(input_data->size(), false);
		noise = new vector<int>();

		matrix_neighbors = create_neighbor_matrix();
	}

	~dbscan() {
		if (visited != NULL) {
			delete visited;
			visited = NULL;
		}

		if (belong != NULL) {
			delete belong;
			belong = NULL;
		}

		if (clusters != NULL) {
			for (vector<cluster *>::const_iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
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

	const vector<cluster *> * const process(void) {
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
				vector<int> index_matrix_neighbors(*((*matrix_neighbors)[i]));

				for (unsigned int k = 0; k < index_matrix_neighbors.size(); k++) {
					unsigned int index_neighbor = index_matrix_neighbors[k];
					if ((*visited)[index_neighbor] != true) {
						(*visited)[index_neighbor] = true;

						/* check for neighbors of the current neighbor - maybe it's noise */
						vector<int> * neighbor_neighbor_indexes = (*matrix_neighbors)[index_neighbor];
						if ( (neighbor_neighbor_indexes != NULL) && (neighbor_neighbor_indexes->size() >= neighbors) ) {

							/* Add neighbors of the neighbor for checking */
							for (vector<int>::const_iterator neighbor_index = neighbor_neighbor_indexes->begin(); neighbor_index != neighbor_neighbor_indexes->end(); neighbor_index++) {
								/* Check if some of neighbors already in check list */
								vector<int>::const_iterator position = std::find(index_matrix_neighbors.begin(), index_matrix_neighbors.end(), *neighbor_index);
								if (position != index_matrix_neighbors.end()) {
									/* Add neighbor if it does not exist in the list */
									index_matrix_neighbors.push_back(*neighbor_index);
								}
							}
						}
					}

					if ((*belong)[index_neighbor] != true) {
						allocated_cluster->push_back(index_neighbor);
						(*belong)[index_neighbor] = true;
#if 0
						std::cout << "Added to the cluster " << (unsigned int) allocated_cluster << " node [" << index_neighbor << "]" << std::endl;
#endif
					}
				}

				index_matrix_neighbors.clear();
			}
			else {
#if 0
				std::cout << "Added to noise node [" << i << "]" << std::endl;
#endif
				noise->push_back(i);
				(*belong)[i] = true;
			}

			if (allocated_cluster->empty() != true) {
				clusters->push_back(allocated_cluster);
			}
		}

		return clusters;
	}

	const vector<cluster *> * const get_clusters(void) const {
		return clusters;
	}

	const vector<int> * const get_noise(void) const {
		return noise;
	}

private:
	vector<vector<int> * > * create_neighbor_matrix(void) {
		vector<vector<int> * > * neighbor_matrix = new vector<vector<int> * >(data->size(), NULL);
		for (unsigned int point_index1 = 0; point_index1 < data->size(); point_index1++) {
			for (unsigned int point_index2 = (point_index1 + 1); point_index2 < data->size(); point_index2++) {
#ifdef FAST_SOLUTION
				double distance = euclidean_distance_sqrt(&((*data)[point_index1]), &((*data)[point_index2]));
#else
				double distance = euclidean_distance(&((*data)[point_index1]), &((*data)[point_index2]));
#endif
				if (distance < radius) {
					if ((*neighbor_matrix)[point_index1] == NULL) {
						(*neighbor_matrix)[point_index1] = new vector<int>();
					}

					if ((*neighbor_matrix)[point_index2] == NULL) {
						(*neighbor_matrix)[point_index2] = new vector<int>();
					}

					(*neighbor_matrix)[point_index1]->push_back(point_index2);
					(*neighbor_matrix)[point_index2]->push_back(point_index1);
				}
			}
		}

#if 0
		for (unsigned int point_index1 = 0; point_index1 < neighbor_matrix->size(); point_index1++) {
			std::cout << (int) point_index1 << ": [ ";
			for (unsigned int point_index2 = 0; point_index2 < (*neighbor_matrix)[point_index1]->size(); point_index2++) {
				std::cout << (int) (*(*neighbor_matrix)[point_index1])[point_index2] << " ";
			}

			std::cout << "]" << std::endl;
		}
#endif

		return neighbor_matrix;
	}
};


#include <string>
#include <fstream>
#include <sstream>
#include <list>

int main(int argc, char * argv[]) {
	std::string filename;
	double radius = 0.0;
	unsigned int minumum_neighbors = 0;

#if 1
	/* General information about running */
	std::cout << argv[0] << " is running..." << std::endl;
#endif

	for (unsigned int iter = 1; iter < (unsigned int) argc; iter++) {
		std::istringstream argument(argv[iter]);

		switch(iter) {
			case 1: argument >> filename; break;
			case 2: argument >> radius; break;
			case 3: argument >> minumum_neighbors; break;
			default: break;
		}
	}

#if 1
	/* General information about running */
	std::cout << filename << " " << radius << " " << minumum_neighbors << std::endl;
#endif

	std::ifstream file_stream(filename.c_str(), std::fstream::in);
	if (!file_stream.is_open()) {
		std::cout << "Impossible to open file '" << filename.c_str() << "'" << std::endl;
		return 1;
	}

	std::string line;

	matrix * dataset = new matrix();

	while(std::getline(file_stream, line)) {
		std::istringstream parser(line);
		std::vector<double> point;

		double coordinate = 0.0;
		while(parser >> coordinate) {
			point.push_back(coordinate);
		}

		dataset->push_back(point);
	}

	file_stream.close();

	dbscan * solver = new dbscan(dataset, radius, minumum_neighbors);
	const vector<cluster *> * clusters = solver->process();

	for (vector<cluster *>::const_iterator cluster_iterator = clusters->begin(); cluster_iterator != clusters->end(); cluster_iterator++) {
		print_cluster(*cluster_iterator);
	}

	/* Noise always last array */
	print_cluster(solver->get_noise());

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return 0;
}
