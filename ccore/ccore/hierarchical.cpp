/**************************************************************************************************************

Cluster analysis algorithm: Classical Hierarchical Algorithm

Based on article description:
 - K.Anil, J.C.Dubes, R.C.Dubes. Algorithms for Clustering Data. 1988.

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

#include "hierarchical.h"

#include "support.h"

#if 1
#define FAST_SOLUTION
#endif

hierarchical_cluster::hierarchical_cluster(const std::vector<std::vector<double> > * const data, const unsigned int index, const std::vector<double> * const point) {
	dataset = (std::vector<std::vector<double> > *) data;
	center = new std::vector<double>(*point);
	indexes = new std::vector<unsigned int>(1, index);
}

hierarchical_cluster::~hierarchical_cluster(void) {
	dataset = NULL;

	if (center != NULL) {
		delete center; 
		center = NULL;
	}

	if (indexes != NULL) {
		delete indexes; 
		indexes = NULL;
	}
}

void hierarchical_cluster::append(const hierarchical_cluster * const cluster2) {
	indexes->insert(indexes->end(), cluster2->get_indexes()->begin(), cluster2->get_indexes()->end());

	/* update center */
	for (unsigned int dimension = 0; dimension < center->size(); dimension++) {
		(*center)[dimension] = 0.0;
		for (std::vector<unsigned int>::const_iterator iter = indexes->begin(); iter != indexes->end(); iter++) {
			(*center)[dimension] += (*dataset)[*iter][dimension];
		}

		(*center)[dimension] /= indexes->size();
	}
}

hierarchical::hierarchical(const std::vector<std::vector<double> > * const dataset, unsigned int cluster_number) {
	data = (std::vector<std::vector<double> > *) dataset;
	clusters = new std::list<hierarchical_cluster *>();

	standard_clusters = NULL;

	number_clusters = cluster_number;

	for (unsigned int index = 0; index < dataset->size(); index++) {
		hierarchical_cluster * data_cluster = new hierarchical_cluster(dataset, index, &(dataset->data()[index]));
		clusters->push_back(data_cluster);
	}
}

hierarchical::~hierarchical(void) {
	data = NULL;

	if (clusters != NULL) {
		for (std::list<hierarchical_cluster *>::const_iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
			delete (*iter);
		}

		delete clusters;
		clusters = NULL;
	}

	if (standard_clusters != NULL) {
		delete standard_clusters;
		standard_clusters = NULL;
	}
}

void hierarchical::process(void) {
	while(clusters->size() > number_clusters) {
		merge_nearest_clusters();
	}

	if (standard_clusters != NULL) {
		delete standard_clusters;
		standard_clusters = NULL;
	}

	if (clusters->size() > 0) {
		standard_clusters = new std::vector<std::vector<unsigned int> * >();
		for (std::list<hierarchical_cluster *>::const_iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
			standard_clusters->push_back( (std::vector<unsigned int> *) (*iter)->get_indexes() );
		}
	}
}

void hierarchical::merge_nearest_clusters(void) {
	double minimum_distance = INFINITY;
	std::list<hierarchical_cluster *>::iterator candidate1, candidate2;

	for(std::list<hierarchical_cluster *>::iterator iter1 = clusters->begin(); iter1 != clusters->end(); iter1++) {
		std::list<hierarchical_cluster *>::iterator iter2 = iter1;
		for(++iter2; iter2 != clusters->end(); iter2++) {
#ifndef FAST_SOLUTION
			double distance = euclidean_distance_sqrt((*iter1)->get_center(), (*iter2)->get_center());
#else
			double distance = euclidean_distance((*iter1)->get_center(), (*iter2)->get_center());
#endif
			if (distance < minimum_distance) {
				candidate1 = iter1;
				candidate2 = iter2;
				minimum_distance = distance;
			}
		}
	}

	((hierarchical_cluster *) (*candidate1))->append(*candidate2);
	clusters->erase(candidate2);
}
