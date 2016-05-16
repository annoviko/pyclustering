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


#include <cmath>
#include <limits>
#include <iostream>

#include "cluster/xmeans.hpp"

#include "utils.hpp"


xmeans::xmeans(const std::vector<std::vector<double> > & data, const std::vector<std::vector<double> > & initial_centers, const unsigned int kmax, const double minimum_change) :
m_clusters(initial_centers.size(), std::vector<unsigned int>()),
m_centers(initial_centers),
m_maximum_clusters(kmax)
{
#ifdef FAST_SOLUTION
	m_tolerance = minimum_change * minimum_change;
#else
	m_tolerance = minimum_change;
#endif
	
	m_dataset = (std::vector<std::vector<double> > *) &data;
}

xmeans::~xmeans(void) { }

void xmeans::process(void) {
	unsigned int current_number_clusters = m_clusters.size();
	const std::vector<unsigned int> dummy;

	while (current_number_clusters < m_maximum_clusters) {
	    improve_parameters(m_clusters, m_centers, dummy);
		improve_structure();

		if (current_number_clusters == m_centers.size()) {
			break;
		}

		current_number_clusters = m_centers.size();
	}
}

void xmeans::improve_parameters(std::vector<std::vector<unsigned int> > & improved_clusters, std::vector<std::vector<double> > & improved_centers, const std::vector<unsigned int> & available_indexes) {
	double current_change = std::numeric_limits<double>::max();

	while(current_change > m_tolerance) {
		update_clusters(improved_clusters, improved_centers, available_indexes);
		current_change = update_centers(improved_clusters, improved_centers);
	}
}


void xmeans::improve_structure() {
	const double difference = 0.001;
	std::vector<std::vector<double> > allocated_centers;

	for (unsigned int index = 0; index < m_clusters.size(); index++) {
		std::vector<std::vector<double> > parent_child_centers;
		parent_child_centers.push_back( m_centers[index] );	/* the first child		*/
		parent_child_centers.push_back( m_centers[index] );	/* the second child		*/

		/* change location of each child (total number of children is two) */
		for (unsigned int dimension = 0; dimension < parent_child_centers[0].size(); dimension++) {
			parent_child_centers[0][dimension] -= difference;
			parent_child_centers[1][dimension] += difference;
		}

		/* solve k-means problem for children where data of parent are used */
		std::vector<std::vector<unsigned int> > parent_child_clusters(2, std::vector<unsigned int>());

		improve_parameters(parent_child_clusters, parent_child_centers, m_clusters[index]);

		/* splitting criterion */
		std::vector<std::vector<unsigned int> > parent_cluster(1, m_clusters[index]);
		std::vector<std::vector<double> > parent_center(1, m_centers[index]);

		double parent_scores = splitting_criterion(parent_cluster, parent_center);
		double child_scores = splitting_criterion(parent_child_clusters, parent_child_centers);

		/* take the best representation of the considered data */
		if (parent_scores > child_scores) {
			allocated_centers.push_back(m_centers[index]);
		}
		else {
			allocated_centers.push_back(parent_child_centers[0]);
			allocated_centers.push_back(parent_child_centers[1]);
		}
	}

	/* update current centers */
	m_centers.clear();
	for (unsigned int index = 0; index < allocated_centers.size(); index++) {
	    m_centers.push_back(allocated_centers[index]);
	}
}


double xmeans::splitting_criterion(const std::vector<std::vector<unsigned int> > & analysed_clusters, const std::vector<std::vector<double> > & analysed_centers) const {
	std::vector<double> scores(analysed_centers.size(), 0.0);

	double dimension = analysed_centers[0].size();
	double sigma = 0.0;
	unsigned int K = analysed_centers.size();
	unsigned int N = 0;

	for (unsigned int index_cluster = 0; index_cluster < analysed_clusters.size(); index_cluster++) {
		for (std::vector<unsigned int>::const_iterator index_object = analysed_clusters[index_cluster].begin(); index_object != analysed_clusters[index_cluster].end(); index_object++) {
			sigma += euclidean_distance( &(*m_dataset)[*index_object], &(analysed_centers[index_cluster]) );
		}

		N += analysed_clusters[index_cluster].size();
	}

	sigma /= (double) (N - K);

	/* splitting criterion */
	for (unsigned int index_cluster = 0; index_cluster < analysed_centers.size(); index_cluster++) {
		double n = (double) analysed_clusters[index_cluster].size();
		scores[index_cluster] = n * std::log(n) - n * std::log(N) - n * std::log(2.0 * pi()) / 2.0 - n * dimension * std::log(sigma) / 2.0 - (n - K) / 2.0;
	}

	double score = 0.0;
	for (std::vector<double>::iterator cluster_score = scores.begin(); cluster_score != scores.end(); cluster_score++) {
		score += (*cluster_score);
	}

	return score;
}

void xmeans::update_clusters(std::vector<std::vector<unsigned int> > & analysed_clusters, const std::vector<std::vector<double> > & analysed_centers, const std::vector<unsigned int> & available_indexes) {
	analysed_clusters.clear();
	analysed_clusters.resize(analysed_centers.size(), std::vector<unsigned int>());
	
	if (available_indexes.empty()) {
		for (unsigned int index_object = 0; index_object < m_dataset->size(); index_object++) {
			unsigned int index_cluster = find_proper_cluster(analysed_centers, (*m_dataset)[index_object]);
			analysed_clusters[index_cluster].push_back(index_object);
		}
	}
	else {
		for (std::vector<unsigned int>::const_iterator index_object = available_indexes.begin(); index_object != available_indexes.end(); index_object++) {
			unsigned int index_cluster = find_proper_cluster(analysed_centers, (*m_dataset)[*index_object]);
			analysed_clusters[index_cluster].push_back(*index_object);
		}
	}
}

unsigned int xmeans::find_proper_cluster(const std::vector<std::vector<double> > & analysed_centers, const std::vector<double> & point) const {
	unsigned int index_optimum = 0;
	double distance_optimum = std::numeric_limits<double>::max();
	
	for (unsigned int index_cluster = 0; index_cluster < analysed_centers.size(); index_cluster++) {
#ifdef FAST_SOLUTION
		double distance = euclidean_distance_sqrt( &point, &(analysed_centers[index_cluster]) );
#else
		double distance = euclidean_distance( &point, &(analysed_centers[index_cluster]) );
#endif

		if (distance < distance_optimum) {
			index_optimum = index_cluster;
			distance_optimum = distance;
		}
	}

	return index_optimum;
}

double xmeans::update_centers(const std::vector<std::vector<unsigned int> > & analysed_clusters, std::vector<std::vector<double> > & analysed_centers) {
	double maximum_change = 0;
	
	/* for each cluster */
	for (unsigned int index_cluster = 0; index_cluster < analysed_clusters.size(); index_cluster++) {
		std::vector<double> total(analysed_centers[index_cluster].size(), 0);

		/* for each object in cluster */
		for (std::vector<unsigned int>::const_iterator object_index_iterator = analysed_clusters[index_cluster].begin(); object_index_iterator < analysed_clusters[index_cluster].end(); object_index_iterator++) {
			/* for each dimension */
			for (unsigned int dimension = 0; dimension < total.size(); dimension++) {
				total[dimension] += (*m_dataset)[*object_index_iterator][dimension];
			}
		}

		/* average for each dimension */
		for (std::vector<double>::iterator dimension_iterator = total.begin(); dimension_iterator != total.end(); dimension_iterator++) {
			*dimension_iterator = *dimension_iterator / analysed_clusters[index_cluster].size();
		}

#ifdef FAST_SOLUTION
		double distance = euclidean_distance_sqrt( &(analysed_centers[index_cluster]), &total );
#else
		double distance = euclidean_distance( &(analysed_centers[index_cluster]), &total );
#endif

		if (distance > maximum_change) {
			maximum_change = distance;
		}

		std::copy(total.begin(), total.end(), analysed_centers[index_cluster].begin());
	}

	return maximum_change;
}
