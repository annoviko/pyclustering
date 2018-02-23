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


#include <cmath>
#include <exception>
#include <functional>
#include <string>
#include <vector>


namespace ccore {

namespace utils {

namespace metric {


/**
 *
 * @brief   Encapsulates distance calculation function between two objects.
 *
 */
template <typename TypeContainer>
using distance_functor = std::function<double(const TypeContainer &, const TypeContainer &)>;


/**
 *
 * @brief   Private function that is used to check input arguments that are used for distance calculation.
 *
 * @param[in] point1: point #1 that is represented by coordinates.
 * @param[in] point2: point #2 that is represented by coordinates.
 *
 */
template <typename TypeContainer>
static void check_common_distance_arguments(const TypeContainer & point1, const TypeContainer & point2) {
    if (point1.size() != point2.size()) {
        throw std::invalid_argument("Impossible to calculate distance between object with different sizes ("
                + std::to_string(point1.size()) + ", "
                + std::to_string(point2.size()) + ").");
    }
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
template <typename TypeContainer>
double euclidean_distance_square(const TypeContainer & point1, const TypeContainer & point2) {
    check_common_distance_arguments(point1, point2);

    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = point1.begin();

    for (auto & dim_point2 : point2) {
        double difference = (*iter_point1 - dim_point2);
        distance += difference * difference;

        iter_point1++;
    }

    return distance;
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
template <typename TypeContainer>
double euclidean_distance(const TypeContainer & point1, const TypeContainer & point2) {
    return std::sqrt(euclidean_distance_square(point1, point2));
}


/**
 *
 * @brief   Calculates Manhattan distance between points.
 *
 * @param[in] point1: point #1 that is represented by coordinates.
 * @param[in] point2: point #2 that is represented by coordinates.
 *
 * @return  Returns Manhattan distance between points.
 *
 */
template <typename TypeContainer>
double manhattan_distance(const TypeContainer & point1, const TypeContainer & point2) {
    check_common_distance_arguments(point1, point2);

    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = point1.begin();

    for (auto & dim_point2 : point2) {
        distance += std::abs(*iter_point1 - dim_point2);
        iter_point1++;
    }

    return distance;
}


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
