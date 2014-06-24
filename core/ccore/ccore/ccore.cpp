#include <string>
#include <fstream>
#include <sstream>

#include "dbscan.h"
#include "support.h"

#include "interface_ccore.h"

clustering_result * dbscan_algorithm(const char * const path_file, const double radius, const unsigned int minumum_neighbors) {
	std::vector<std::vector<double> > * dataset = read_sample(path_file);

	dbscan * solver = new dbscan(dataset, radius, minumum_neighbors);
	solver->process();

	std::vector<std::vector<unsigned int> *> * clusters = solver->get_clusters();
	clusters->push_back(solver->get_noise());

	clustering_result * result = create_clustering_result(clusters);

	delete solver; solver = NULL;
	delete dataset; dataset = NULL;

	return result;
}