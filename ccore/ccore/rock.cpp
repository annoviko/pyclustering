/**************************************************************************************************************

Cluster analysis algorithm: ROCK

Based on article description:
 - S.Guha, R.Rastogi, K.Shim. ROCK: A Robust Clustering Algorithm for Categorical Attributes. 1999.

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

#include "rock.h"
#include "support.h"

#include <cmath>
#include <climits>
#include <iostream>

#define FAST_SOLUTION

rock::rock(const std::vector<std::vector<double> > * const data, const double radius, const unsigned int num_clusters, const double threshold) {
	dataset = (std::vector<std::vector<double> > * const) data;

	vector_clusters = NULL;	/* result will be set after the calculation */

	clusters = new std::list<std::vector<unsigned int> *>();
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

	/* pointer of clusters can be freed by list and by vector representation */
	bool trigger_clean_cluster = true;

	if (clusters != NULL) {
		/* possible if process() isn't called, therefore clusters should be cleared here */
		trigger_clean_cluster = false;

		for (std::list<std::vector<unsigned int> *>::const_iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
			delete (*iter);
		}

		delete clusters;
		clusters = NULL;
	}

	if (vector_clusters != NULL) {
		if (trigger_clean_cluster == true) {
			for (std::vector<std::vector<unsigned int> *>::const_iterator iter = vector_clusters->begin(); iter != vector_clusters->end(); iter++) {
				delete (*iter);
			}			
		}

		delete vector_clusters;
		vector_clusters = NULL;
	}
}

void rock::process(void) {
	while( (number_clusters < clusters->size()) && (merge_cluster()) ) { }

	vector_clusters = new std::vector<std::vector<unsigned int> *>();
	//std::copy(clusters->begin(), clusters->end(), std::back_inserter(vector_clusters));
	vector_clusters->insert(vector_clusters->begin(), clusters->begin(), clusters->end());

	/* no need to store list anymore */
	delete clusters;
	clusters = NULL;
}

bool rock::merge_cluster(void) {
	std::list<std::vector<unsigned int> *>::iterator cluster1 = clusters->end();
	std::list<std::vector<unsigned int> *>::iterator cluster2 = clusters->end();

	double maximum_goodness = 0;

	for (std::list<std::vector<unsigned int> *>::iterator i = clusters->begin(); i != clusters->end(); i++) {
		std::list<std::vector<unsigned int> *>::iterator next = i;
		for (std::list<std::vector<unsigned int> *>::iterator j = ++next; j != clusters->end(); j++) {
			double goodness = calculate_goodness(i, j);
			if (goodness > maximum_goodness) {
				maximum_goodness = goodness;

				cluster1 = i;
				cluster2 = j;
			}
		}
	}

	if (cluster1 == cluster2) {
		return false;	/* clusters are totally separated (no links between them), it's impossible to made a desicion which of them should be merged */
	}

	(*cluster1)->insert((*cluster1)->end(), (*cluster2)->begin(), (*cluster2)->end());
	clusters->erase(cluster2);
	
	return true;
}

unsigned int rock::calculate_links(std::list<std::vector<unsigned int> *>::iterator & cluster1, std::list<std::vector<unsigned int> *>::iterator & cluster2) const {
	unsigned int number_links = 0;
	for (std::vector<unsigned int>::const_iterator i = (*cluster1)->begin(); i != (*cluster1)->end(); i++) {
		for (std::vector<unsigned int>::const_iterator j = (*cluster2)->begin(); j != (*cluster2)->end(); j++) {
			number_links += (*adjacency_matrix)[*i][*j];
		}
	}

	return number_links;
}

double rock::calculate_goodness(std::list<std::vector<unsigned int> *>::iterator & cluster1, std::list<std::vector<unsigned int> *>::iterator & cluster2) const {
	const double number_links = calculate_links(cluster1, cluster2);
	
	const double size_cluster1 = (*cluster1)->size();
	const double size_cluster2 = (*cluster2)->size();

	return number_links / ( std::pow( size_cluster1 + size_cluster2, degree_normalization ) - 
		std::pow( size_cluster1, degree_normalization ) -
		std::pow( size_cluster2, degree_normalization ) );
}
