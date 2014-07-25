#ifndef _SUPPORT_H_
#define _SUPPORT_H_

#include <string>
#include <fstream>
#include <sstream>

#include <vector>
#include <cmath>

#include "interface_ccore.h"


typedef struct differential_result {
	double time;
	double value;
} differential_result;


inline double euclidean_distance_sqrt(const std::vector<double> * const point1, const std::vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return distance;
}

inline double euclidean_distance(const std::vector<double> * const point1, const std::vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return std::sqrt(distance);
}

std::vector<std::vector<double> > * read_sample(const char * const path_file);

std::vector<std::vector<double> > * read_sample(const data_representation * const sample);

clustering_result * create_clustering_result(const std::vector<std::vector<unsigned int> *> * const clusters);

#endif