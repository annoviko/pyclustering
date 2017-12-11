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


#include "utils.hpp"

#include <chrono>
#include <random>


double heaviside(const double value) {
    if (value >= 0.0) { return 1.0; }
    return 0.0;
}


double euclidean_distance_sqrt(const std::vector<double> * const point1, const std::vector<double> * const point2) {
    double distance = 0.0;
    for (std::size_t dimension = 0; dimension < point1->size(); dimension++) {
        double difference = (point1->data()[dimension] - point2->data()[dimension]);
        distance += difference * difference;
    }

  return distance;
}


double euclidean_distance_sqrt(const std::vector<double> & point1, const std::vector<double> & point2) {
    return euclidean_distance_sqrt(&point1, &point2);
}


double euclidean_distance(const std::vector<double> * const point1, const std::vector<double> * const point2) {
    double distance = 0.0;

    for (std::size_t dimension = 0; dimension < point1->size(); dimension++) {
        double difference = (point1->data()[dimension] - point2->data()[dimension]);
        distance += difference * difference;
    }

    return std::sqrt(distance);
}


double euclidean_distance(const std::vector<double> & point1, const std::vector<double> & point2) {
    return euclidean_distance(&point1, &point2);
}


double average_neighbor_distance(const std::vector<std::vector<double> > * points, const std::size_t num_neigh) {
    std::vector<std::vector<double> > dist_matrix( points->size(), std::vector<double>(points->size(), 0.0) );
    for (std::size_t i = 0; i < points->size(); i++) {
        for (std::size_t j = i + 1; j < points->size(); j++) {
            double distance = euclidean_distance( &(*points)[i], &(*points)[j] );
            dist_matrix[i][j] = distance;
            dist_matrix[j][i] = distance;
        }

        std::sort(dist_matrix[i].begin(), dist_matrix[i].end());
    }

    double total_distance = 0.0;
    for (std::size_t i = 0; i < points->size(); i++) {
        for (std::size_t j = 0; j < num_neigh; j++) {
            total_distance += dist_matrix[i][j + 1];
        }
    }

    return total_distance / ( (double) num_neigh * (double) points->size() );
}


namespace utils {

namespace random {


double generate_normal_random(const double p_from, const double p_to) {
    unsigned seed = (unsigned) std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine generator(seed);

    std::normal_distribution<double> distribution(p_from, p_to);
    return distribution(generator);
}


}

}
