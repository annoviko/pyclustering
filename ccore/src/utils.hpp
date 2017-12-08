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

#pragma once

#include <stdexcept>

#include <string>
#include <fstream>
#include <sstream>

#include <stack>
#include <vector>
#include <cmath>
#include <algorithm>

#include "nnet/network.hpp"


namespace utils {


/**
 *
 * @brief   Mathematical constant pi.
 *
 */
const double pi = 3.14159265358979323846;

}


/**
 *
 * @brief   Calculates Heaviside function.
 * @details If value >= 0.0 then 1.0 is returned, otherwise 0.0 is returned.
 *
 * @param[in] value: Input argument of the Heaviside function.
 *
 * @return  Returns result of Heaviside function.
 *
 */
double heaviside(const double value);


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
double euclidean_distance_sqrt(const std::vector<double> * const point1, const std::vector<double> * const point2);

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
double euclidean_distance_sqrt(const std::vector<double> & point1, const std::vector<double> & point2);


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
double euclidean_distance(const std::vector<double> * const point1, const std::vector<double> * const point2);


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
double euclidean_distance(const std::vector<double> & point1, const std::vector<double> & point2);


/**
 *
 * @brief   Returns average distance for establish links between specified number of neighbors.
 *
 * @param[in] points:    Input data.
 * @param[in] num_neigh: Number of neighbors.
 *
 * @return  Returns average distance for establish links between 'num_neigh' in data set 'points'.
 *
 */
double average_neighbor_distance(const std::vector<std::vector<double> > * points, const std::size_t num_neigh);


namespace utils {

namespace random {


/**
 *
 * @brief   Returns random value using specified mean and deviation using normal distribution.
 *
 * @param[in] p_mean: Mean.
 * @param[in] p_dev:  Standard deviation.
 *
 * @return  Returns random variable.
 *
 */
double generate_normal_random(const double p_mean = 0.0, const double p_dev = 1.0);


}

}