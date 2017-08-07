/**
*
* Copyright (C) 2014-2017    Andrei Novikov (pyclustering@yandex.ru)
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

#ifndef _SUPPORT_H_
#define _SUPPORT_H_

#include <stdexcept>

#include <string>
#include <fstream>
#include <sstream>

#include <stack>
#include <vector>
#include <cmath>
#include <algorithm>

#include "nnet/network.hpp"


typedef struct differential_result {
	double time;
	double value;
} differential_result;


inline double pi(void) { return (double) 3.14159265358979323846; }


inline double heaviside(const double value) {
	if (value >= 0.0) { return 1.0; }
	return 0.0;
}


/**
 *
 * @brief   Calculates square of Euclidean distance between points.
 *
 * @param[in] point1: pointer to point #1 that is represented by coordinates.
 * @param[in] point2: pointer to point #2 that is represented by coordinates.
 *
 * @return  Returns square of Euclidean distance between points.
 *
 */
inline double euclidean_distance_sqrt(const std::vector<double> * const point1, const std::vector<double> * const point2) {
	double distance = 0.0;
	/* assert(point1->size() != point1->size()); */
	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return distance;
}

/**
 *
 * @brief   Calculates square of Euclidean distance between points.
 *
 * @param[in] point1: point #1 that is represented by coordinates.
 * @param[in] point2: point #2 that is represented by coordinates.
 *
 * @return  Returns square of Euclidean distance between points.
 *
 */
inline double euclidean_distance_sqrt(const std::vector<double> & point1, const std::vector<double> & point2) {
    return euclidean_distance_sqrt(&point1, &point2);
}

/**
 *
 * @brief   Calculates Euclidean distance between points.
 *
 * @param[in] point1: pointer to point #1 that is represented by coordinates.
 * @param[in] point2: pointer to point #2 that is represented by coordinates.
 *
 * @return  Returns Euclidean distance between points.
 *
 */
inline double euclidean_distance(const std::vector<double> * const point1, const std::vector<double> * const point2) {
	double distance = 0.0;

	for (unsigned int dimension = 0; dimension < point1->size(); dimension++) {
		double difference = (point1->data()[dimension] - point2->data()[dimension]);
		distance += difference * difference;
	}

	return std::sqrt(distance);
}

/**
 *
 * @brief   Calculates Euclidean distance between points.
 *
 * @param[in] point1: point #1 that is represented by coordinates.
 * @param[in] point2: point #2 that is represented by coordinates.
 *
 * @return  Returns Euclidean distance between points.
 *
 */
inline double euclidean_distance(const std::vector<double> & point1, const std::vector<double> & point2) {
    return euclidean_distance(&point1, &point2);
}

/***********************************************************************************************
 *
 * @brief   Returns average distance for establish links between specified number of neighbors.
 *
 * @param   (in) points         - input data.
 * @param   (in) num_neigh      - number of neighbors.
 *
 * @return  Returns average distance for establish links between 'num_neigh' in data set 'points'.
 *
 ***********************************************************************************************/
double average_neighbor_distance(const std::vector<std::vector<double> > * points, const unsigned int num_neigh);

#endif
