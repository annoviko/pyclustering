/**************************************************************************************************************

Cluster analysis algorithm: K-Means

Based on book description:
 - J.B.MacQueen. Some Methods for Classification and Analysis of Multivariate Observations. 1967.

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

#include "kmeans.h"
#include "support.h"

#include <algorithm>
#include <limits>

#define FAST_SOLUTION

kmeans::kmeans(const std::vector<std::vector<double> > * const data, const std::vector<std::vector<double> > * const initial_centers, const double minimum_change) {
	dataset = (std::vector<std::vector<double> > * const) data;

	centers = new std::vector<std::vector<double> >( (*initial_centers) );

	clusters = new std::vector<std::vector<unsigned int> * >();
	for (unsigned int index = 0; index < centers->size(); index++) {
		clusters->push_back(new std::vector<unsigned int>());
	}


#ifdef FAST_SOLUTION
	tolerance = minimum_change * minimum_change;
#else
	tolerance = minimum_change;
#endif
}

kmeans::~kmeans(void) {
	if (centers != NULL) {
		delete centers;
		centers = NULL;
	}

	if (clusters != NULL) {
		for (std::vector<std::vector<unsigned int> * >::const_iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
			delete (*iter);
		}

		delete clusters;
		clusters = NULL;
	}
}


void kmeans::process(void) {
	double current_change = std::numeric_limits<double>::max();

	while(current_change > tolerance) {
		update_clusters();
		current_change = update_centers();
	}
}

void kmeans::update_clusters(void) {
	/* clear content of clusters. */
	for (std::vector<std::vector<unsigned int> *>::iterator iter = clusters->begin(); iter != clusters->end(); iter++) {
		(*iter)->clear();
	}

	/* fill clusters again in line with centers. */
	for (unsigned int index_object = 0; index_object < dataset->size(); index_object++) {
		double		minimum_distance = std::numeric_limits<double>::max();
		unsigned int	suitable_index_cluster = 0;

		for (unsigned int index_cluster = 0; index_cluster < clusters->size(); index_cluster++) {
#ifdef FAST_SOLUTION
			double distance = euclidean_distance_sqrt( &(*centers)[index_cluster], &(*dataset)[index_object] );
#else
			double distance = euclidean_distance( &(*centers)[index_cluster], &(*dataset)[index_object] );
#endif
			if (distance < minimum_distance) {
				minimum_distance = distance;
				suitable_index_cluster = index_cluster;
			}
		}

		(*clusters)[suitable_index_cluster]->push_back(index_object);
	}

    /* if there is clusters that are not able to capture objects */
    for (size_t index_cluster = clusters->size() - 1; index_cluster != (size_t) -1; index_cluster--) {
        if ((*clusters)[index_cluster]->empty()) {
            clusters->erase(clusters->begin() + index_cluster);
        }
    }
}

double kmeans::update_centers(void) {
	double maximum_change = 0;
	
    /* check if number of clusters has been changed */
    if (clusters->size() < centers->size()) {
        centers->erase(centers->begin() + clusters->size(), centers->end());
    }

	/* for each cluster */
	for (unsigned int index_cluster = 0; index_cluster < clusters->size(); index_cluster++) {
		std::vector<double> total((*centers)[index_cluster].size(), 0);

		/* for each object in cluster */
		for (std::vector<unsigned int>::const_iterator object_index_iterator = (*clusters)[index_cluster]->begin(); object_index_iterator < (*clusters)[index_cluster]->end(); object_index_iterator++) {
			/* for each dimension */
			for (unsigned int dimension = 0; dimension < total.size(); dimension++) {
				total[dimension] += (*dataset)[*object_index_iterator][dimension];
			}
		}

		/* average for each dimension */
		for (std::vector<double>::iterator dimension_iterator = total.begin(); dimension_iterator != total.end(); dimension_iterator++) {
			*dimension_iterator = *dimension_iterator / (*clusters)[index_cluster]->size();
		}

#ifdef FAST_SOLUTION
		double distance = euclidean_distance_sqrt( &(*centers)[index_cluster], (std::vector<double> *) &total );
#else
		double distance = euclidean_distance( &(*centers)[index_cluster], (std::vector<double> *) &total );
#endif

		if (distance > maximum_change) {
			maximum_change = distance;
		}

		std::copy(total.begin(), total.end(), (*centers)[index_cluster].begin());
	}

	return maximum_change;
}
