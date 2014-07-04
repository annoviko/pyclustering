#include "rock.h"
#include "support.h"

#include <cmath>
#include <climits>
#include <iostream>

#define FAST_SOLUTION

rock::rock(const std::vector<std::vector<double> > * const data, const double radius, const unsigned int num_clusters, const double threshold) {
	dataset = (std::vector<std::vector<double> > * const) data;

	clusters = new std::vector<std::vector<unsigned int> *>();
	for (unsigned int index = 0; index < data->size(); index++) {
		clusters->push_back(new std::vector<unsigned int>(1, index));
	}

	number_clusters = num_clusters;
	degree_normalization = 1.0 + 2.0 * ( (1.0 - threshold) / (1.0 + threshold) );

#ifdef FAST_SOLUTION
	double radius_connectivity = radius * radius;
#else
	double radius_connectivity = radius;
#endif

	adjacency_matrix = new std::vector<std::vector<unsigned int> >( data->size(), std::vector<unsigned int>(data->size(), 0) );
	for (unsigned int i = 0; i < data->size(); i++) {
		for (unsigned int j = i + 1; j < data->size(); j++) {
#ifdef FAST_SOLUTION
			double distance = euclidean_distance_sqrt(&(*data)[i], &(*data)[j]);
#else
			double distance = euclidean_distance(&(*data)[i], &(*data)[j]);
#endif
			if (distance < radius_connectivity) {
				(*adjacency_matrix)[i][j] = 1;
				(*adjacency_matrix)[j][i] = 1;
			}
			else {
				(*adjacency_matrix)[i][j] = 0;
				(*adjacency_matrix)[j][i] = 0;
			}
		}
	}
}

rock::~rock() {
	if (adjacency_matrix != NULL) {
		delete adjacency_matrix;
		adjacency_matrix = NULL;
	}

	if (clusters != NULL) {
		delete clusters;
		clusters = NULL;
	}
}

void rock::process(void) {
	while( (number_clusters < clusters->size()) && (merge_cluster()) ) { }
}

bool rock::merge_cluster(void) {
	unsigned int cluster_index1 = -1;
	unsigned int cluster_index2 = -1;

	double maximum_goodness = 0;

	for (unsigned int i = 0; i < clusters->size(); i++) {
		for (unsigned int j = i + 1; j < clusters->size(); j++) {
			double goodness = calculate_goodness(i, j);
			if (goodness > maximum_goodness) {
				maximum_goodness = goodness;

				cluster_index1 = i;
				cluster_index2 = j;
			}
		}
	}

	if (cluster_index1 == cluster_index2) {
		return false;	/* clusters are totally separated (no links between them), it's impossible to made a desicion which of them should be merged */
	}

	(*clusters)[cluster_index1]->insert( (*clusters)[cluster_index1]->end(), (*clusters)[cluster_index2]->begin(), (*clusters)[cluster_index2]->end() );
	clusters->erase(clusters->begin() + cluster_index2);	/* inefficient operation compared to the one performed for the same operation by other kinds of sequence containers (such as list or forward_list). */
	
	return true;
}

unsigned int rock::calculate_links(const unsigned int index_cluster1, const unsigned int index_cluster2) const {
	unsigned int number_links = 0;
	for (unsigned int i = 0; i < (*clusters)[index_cluster1]->size(); i++) {
		for (unsigned int j = 0; j < (*clusters)[index_cluster2]->size(); j++) {
			unsigned int index_object1 = (*((*clusters)[index_cluster1]))[i];
			unsigned int index_object2 = (*((*clusters)[index_cluster2]))[j];

			number_links += (*adjacency_matrix)[index_object1][index_object2];
		}
	}

	return number_links;
}

double rock::calculate_goodness(const unsigned int index_cluster1, const unsigned int index_cluster2) const {
	const double number_links = calculate_links(index_cluster1, index_cluster2);
	
	const double size_cluster1 = (*clusters)[index_cluster1]->size();
	const double size_cluster2 = (*clusters)[index_cluster2]->size();

	return number_links / ( std::pow( size_cluster1 + size_cluster2, degree_normalization ) - 
		std::pow( size_cluster1, degree_normalization ) -
		std::pow( size_cluster2, degree_normalization ) );
}