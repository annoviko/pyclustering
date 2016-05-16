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

#include "utils.hpp"

std::vector<std::vector<double> > * read_sample(const char * const path_file) {
	std::string filename(path_file);

	std::ifstream file_stream(filename.c_str(), std::fstream::in);
	if (!file_stream.is_open()) {
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

	return dataset;
}


std::vector<std::vector<double> > * read_sample(const data_representation * const sample) {
	std::vector<double> point(sample->dimension, 0);
	std::vector<std::vector<double> > * dataset = new std::vector<std::vector<double> >(sample->size, point);

	for (unsigned int index = 0; index < sample->size; index++) {
		for (unsigned int dimension = 0; dimension < sample->dimension; dimension++) {
			point[dimension] = sample->objects[index][dimension];
		}

		(*dataset)[index] = point;
	}

	return dataset;
}


clustering_result * create_clustering_result(const std::vector<std::vector<unsigned int> *> * const clusters) {
	clustering_result * result = new clustering_result();

	if (clusters == NULL) {
		result->size = 0;
		result->clusters = NULL;
	}
	else {
		result->size = clusters->size();
		result->clusters = new cluster_representation[result->size];
	}

	for (unsigned int index_cluster = 0; index_cluster < result->size; index_cluster++) {
		result->clusters[index_cluster].size = (*clusters)[index_cluster]->size();
		if (result->clusters[index_cluster].size > 0) {
			result->clusters[index_cluster].objects = new unsigned int[result->clusters[index_cluster].size];

			for (unsigned int index_object = 0; index_object < result->clusters[index_cluster].size; index_object++) {
				result->clusters[index_cluster].objects[index_object] = (*(*clusters)[index_cluster])[index_object];
			}
		}
		else {
			result->clusters[index_cluster].objects = NULL;
		}
	}

	return result;
}


clustering_result * create_clustering_result(const std::vector<std::vector<unsigned int> > & clusters) {
	clustering_result * result = new clustering_result();

	result->size = clusters.size();
	result->clusters = new cluster_representation[result->size];

	for (unsigned int index_cluster = 0; index_cluster < result->size; index_cluster++) {
		result->clusters[index_cluster].size = clusters[index_cluster].size();
		if (result->clusters[index_cluster].size > 0) {
			result->clusters[index_cluster].objects = new unsigned int[result->clusters[index_cluster].size];

			for (unsigned int index_object = 0; index_object < result->clusters[index_cluster].size; index_object++) {
				result->clusters[index_cluster].objects[index_object] = clusters[index_cluster][index_object];
			}
		}
		else {
			result->clusters[index_cluster].objects = NULL;
		}
	}

	return result;
}


double average_neighbor_distance(const std::vector<std::vector<double> > * points, const unsigned int num_neigh) {
	std::vector<std::vector<double> > dist_matrix( points->size(), std::vector<double>(points->size(), 0.0) );
	for (unsigned int i = 0; i < points->size(); i++) {
		for (unsigned int j = i + 1; j < points->size(); j++) {
			double distance = euclidean_distance( &(*points)[i], &(*points)[j] );
			dist_matrix[i][j] = distance;
			dist_matrix[j][i] = distance;
		}
		std::sort(dist_matrix[i].begin(), dist_matrix[i].end());
	}

	double total_distance = 0.0;
	for (unsigned int i = 0; i < points->size(); i++) {
		for (unsigned int j = 0; j < num_neigh; j++) {
			total_distance += dist_matrix[i][j + 1];
		}
	}

	return total_distance / ( (double) num_neigh * (double) points->size() );
}
