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


#include <algorithm>
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
 * @brief   Encapsulates distance metric calculation function between two objects.
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
 * @brief   Calculates Chebyshev distance between points.
 *
 * @param[in] point1: point #1 that is represented by coordinates.
 * @param[in] point2: point #2 that is represented by coordinates.
 *
 * @return  Returns Chebyshev distance between points.
 *
 */
template <typename TypeContainer>
double chebyshev_distance(const TypeContainer & point1, const TypeContainer & point2) {
    check_common_distance_arguments(point1, point2);

    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = point1.begin();

    for (auto & dim_point2 : point2) {
        distance = std::max(distance, std::abs(*iter_point1 - dim_point2));
        iter_point1++;
    }

    return distance;
}


/**
 *
 * @brief   Calculates square of Minkowski distance between points.
 *
 * @param[in] p_point1: point #1 that is represented by coordinates.
 * @param[in] p_point2: point #2 that is represented by coordinates.
 * @param[in] p_degree: degree of Minkownski equation.
 *
 * @return  Returns square of Minkowski distance between points.
 *
 */
template <typename TypeContainer>
double minkowski_distance(const TypeContainer & p_point1, const TypeContainer & p_point2, const double p_degree) {
    check_common_distance_arguments(p_point1, p_point2);

    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = p_point1.begin();

    for (auto & dim_point2 : p_point2) {
        double difference = (*iter_point1 - dim_point2);
        distance += std::pow(difference, p_degree);

        iter_point1++;
    }

    return std::pow(distance, 1.0 / p_degree);
}


/**
 *
 * @brief   Calculates distance matrix using points container.
 *
 * @param[in]  p_points: input data that is represented by points.
 * @param[out] p_distance_matrix: output distance matrix of points.
 *
 */
template <typename TypeContainer>
void distance_matrix(const TypeContainer & p_points, TypeContainer & p_distance_matrix) {
    using TypeElement = typename TypeContainer::value_type;
    
    p_distance_matrix = TypeContainer(p_points.size(), TypeElement(p_points.size(), 0.0));

    for (std::size_t i = 0; i < p_points.size(); i++) {
        for (std::size_t j = i + 1; j < p_points.size(); j++) {
            const double distance = euclidean_distance(p_points.at(i), p_points.at(j));
            p_distance_matrix[i][j] = distance;
            p_distance_matrix[j][i] = distance;
        }
    }
}


/**
 *
 * @brief   Basic distance metric provides interface for calculation distance between objects in line with
 *           specific metric.
 *
 */
template <typename TypeContainer>
class distance_metric {
protected:
    distance_functor<TypeContainer> m_functor = nullptr;

public:
    distance_metric(void) = default;

    distance_metric(const distance_functor<TypeContainer> & p_functor) : m_functor(p_functor) { }

    distance_metric(const distance_metric & p_other) = default;

    distance_metric(distance_metric && p_other) = default;

    virtual ~distance_metric(void) = default;

public:
   /**
    *
    * @brief   Performs calculation of distance metric between two points.
    *
    * @param[in] p_point1: the first iterable point.
    * @param[in] p_point2: the second iterable point.
    *
    * @return  Calculated distance between two points.
    *
    */
    double operator()(const TypeContainer & p_point1, const TypeContainer & p_point2) const {
        return m_functor(p_point1, p_point2);
    }

public:
    operator bool() const {
        return m_functor != nullptr;
    }

    distance_metric<TypeContainer>& operator=(const distance_metric<TypeContainer>& p_other) {
        if (this != &p_other) {
            m_functor = p_other.m_functor;
        }

        return *this;
    }
};


/**
 *
 * @brief   Euclidean distance metric calculator between two points.
 *
 */
template <typename TypeContainer>
class euclidean_distance_metric : public distance_metric<TypeContainer> {
public:
    euclidean_distance_metric(void) :
        distance_metric<TypeContainer>(std::bind(euclidean_distance<TypeContainer>, std::placeholders::_1, std::placeholders::_2))
    { }
};


/**
 *
 * @brief   Square Euclidean distance metric calculator between two points.
 *
 */
template <typename TypeContainer>
class euclidean_distance_square_metric : public distance_metric<TypeContainer> {
public:
    euclidean_distance_square_metric(void) :
        distance_metric<TypeContainer>(std::bind(euclidean_distance_square<TypeContainer>, std::placeholders::_1, std::placeholders::_2))
    { }
};


/**
 *
 * @brief   Manhattan distance metric calculator between two points.
 *
 */
template <typename TypeContainer>
class manhattan_distance_metric : public distance_metric<TypeContainer> {
public:
    manhattan_distance_metric(void) :
        distance_metric<TypeContainer>(std::bind(manhattan_distance<TypeContainer>, std::placeholders::_1, std::placeholders::_2))
    { }
};


/**
 *
 * @brief   Chebyshev distance metric calculator between two points.
 *
 */
template <typename TypeContainer>
class chebyshev_distance_metric : public distance_metric<TypeContainer> {
public:
    chebyshev_distance_metric(void) :
        distance_metric<TypeContainer>(std::bind(chebyshev_distance<TypeContainer>, std::placeholders::_1, std::placeholders::_2))
    { }
};


/**
 *
 * @brief   Minkowski distance metric calculator between two points.
 *
 */
template <typename TypeContainer>
class minkowski_distance_metric : public distance_metric<TypeContainer> {
public:
  /**
   *
   * @brief   Constructor of Minkowski distance metric.
   *
   * @param[in] p_degree: degree of Minkowski equation.
   *
   */
    minkowski_distance_metric(const double p_degree) :
        distance_metric<TypeContainer>(std::bind(minkowski_distance<TypeContainer>, std::placeholders::_1, std::placeholders::_2, p_degree))
    { }
};


/**
 *
 * @brief   Distance metric factory provides services for creation available metric in the 'ccore::utils::metric' and also user-defined.
 *
 */
template <typename TypeContainer>
class distance_metric_factory {
public:
  /**
   *
   * @brief   Creates Euclidean distance metric.
   *
   * @return  Euclidean distance metric.
   *
   */
    static distance_metric<TypeContainer> euclidean(void) {
        return euclidean_distance_metric<TypeContainer>();
    }

   /**
   *
   * @brief   Creates square Euclidean distance metric.
   *
   * @return  Square Euclidean distance metric
   *
   */
    static distance_metric<TypeContainer> euclidean_square(void) {
        return euclidean_distance_square_metric<TypeContainer>();
    }

   /**
   *
   * @brief   Creates Manhattan distance metric.
   *
   * @return  Manhattan distance metric.
   *
   */
    static distance_metric<TypeContainer> manhattan(void) {
        return manhattan_distance_metric<TypeContainer>();
    }

   /**
   *
   * @brief   Creates Chebyshev distance metric.
   *
   * @return  Chebyshev distance metric.
   *
   */
    static distance_metric<TypeContainer> chebyshev(void) {
        return chebyshev_distance_metric<TypeContainer>();
    }

   /**
   *
   * @brief   Creates Minkowski distance metric.
   *
   * @param[in] p_degree: degree of Minkowski equation.
   *
   * @return  Minkowski distance metric.
   *
   */
    static distance_metric<TypeContainer> minkowski(const double p_degree) {
        return minkowski_distance_metric<TypeContainer>(p_degree);
    }

   /**
   *
   * @brief   Creates user-defined distance metric.
   *
   * @param[in] p_functor: user-defined metric for calculation distance between two points.
   *
   * @return  User-defined distance metric.
   *
   */
    static distance_metric<TypeContainer> user_defined(const distance_functor<TypeContainer> & p_functor) {
        return distance_metric<TypeContainer>(p_functor);
    }
};


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
