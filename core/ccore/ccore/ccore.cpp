#include <string>
#include <fstream>
#include <sstream>

#include "dbscan.h"

#include "interface_ccore.h"

clustering_result * dbscan_algorithm(const char * const path_file, const double radius, const unsigned int minumum_neighbors) {
	std::string filename(path_file);

	std::ifstream file_stream(filename.c_str(), std::fstream::in);
	if (!file_stream.is_open()) {
		std::cout << "Impossible to open file '" << filename.c_str() << "'" << std::endl;
		return NULL;
	}

	std::string line;

	std::vector<std::vector<double> > * dataset = new std::vector<std::vector<double> >();

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
	solver->process();

	const std::vector<cluster *> * clusters = solver->get_clusters();

	clustering_result * result = new clustering_result();
	result->size = clusters->size() + 1;
	result->clusters = new cluster_representation[result->size];

	/* Add cluster to returned structure */
	for (unsigned int index_cluster = 0; index_cluster < result->size - 1; index_cluster++) {

		result->clusters[index_cluster].size = (*clusters)[index_cluster]->size();
		result->clusters[index_cluster].objects = new unsigned int[result->clusters[index_cluster].size];

		for (unsigned int index_object = 0; index_object < result->clusters[index_cluster].size; index_object++) {
			result->clusters[index_cluster].objects[index_object] = (*(*clusters)[index_cluster])[index_object];
		}
	}

	/* Add noise as a last cluster */
	const std::vector<unsigned int> * noise = solver->get_noise();
	result->clusters[result->size - 1].size = noise->size();
	if (result->clusters[result->size - 1].size > 0) {
		result->clusters[result->size - 1].objects = new unsigned int[result->clusters[result->size - 1].size];
		for (unsigned int index_object = 0; index_object < noise->size(); index_object++) {
			result->clusters[result->size - 1].objects[index_object] = (*noise)[index_object];
		}
	}
	else {
		result->clusters[result->size - 1].size = 0;
		result->clusters[result->size - 1].objects = NULL;
	}
	
	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return result;
}