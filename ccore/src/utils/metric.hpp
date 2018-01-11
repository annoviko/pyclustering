/**
*
* Copyright (C) 2014-2018    Andrei Novikov (pyclustering@yandex.ru)
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


#include <vector>


namespace ccore {

namespace utils {

namespace metric {


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


}

}

}