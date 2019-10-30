/**
*
* @authors Andrei Novikov (pyclustering@yandex.ru)
* @date 2014-2019
* @copyright GNU Public License
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


#include <pyclustering/definitions.hpp>

#include <algorithm>
#include <cmath>
#include <exception>
#include <functional>
#include <string>
#include <vector>


namespace pyclustering {

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
    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = point1.begin();

    for (const auto & dim_point2 : point2) {
        double difference = (*iter_point1 - dim_point2);
        distance += difference * difference;

        ++iter_point1;
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
    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = point1.begin();

    for (const auto & dim_point2 : point2) {
        distance += std::abs(*iter_point1 - dim_point2);
        ++iter_point1;
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
    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = point1.begin();

    for (const auto & dim_point2 : point2) {
        distance = std::max(distance, std::abs(*iter_point1 - dim_point2));
        ++iter_point1;
    }

    return distance;
}


/**
 *
 * @brief   Calculates Minkowski distance between points.
 *
 * @param[in] p_point1: point #1 that is represented by coordinates.
 * @param[in] p_point2: point #2 that is represented by coordinates.
 * @param[in] p_degree: degree of Minkownski equation.
 *
 * @return  Returns Minkowski distance between points.
 *
 */
template <typename TypeContainer>
double minkowski_distance(const TypeContainer & p_point1, const TypeContainer & p_point2, const double p_degree) {
    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = p_point1.begin();

    for (const auto & dim_point2 : p_point2) {
        double difference = (*iter_point1 - dim_point2);
        distance += std::pow(difference, p_degree);

        ++iter_point1;
    }

    return std::pow(distance, 1.0 / p_degree);
}


/**
 *
 * @brief   Calculates Canberra distance between points.
 *
 * @param[in] point1: point #1 that is represented by coordinates.
 * @param[in] point2: point #2 that is represented by coordinates.
 *
 * @return  Returns Canberra distance between points.
 *
 */
template <typename TypeContainer>
double canberra_distance(const TypeContainer & point1, const TypeContainer & point2) {
    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = point1.begin();

    for (const auto & dim_point2 : point2) {
        const auto dim_point1 = *iter_point1;

        const double divider = std::abs(dim_point1) + std::abs(dim_point2);
        if (divider == 0) {
            continue;
        }

        distance += std::abs(dim_point1 - dim_point2) / divider;
        ++iter_point1;
    }

    return distance;
}


/**
 *
 * @brief   Calculates Chi square distance between points.
 *
 * @param[in] point1: point #1 that is represented by coordinates.
 * @param[in] point2: point #2 that is represented by coordinates.
 *
 * @return  Returns Chi square distance between points.
 *
 */
template <typename TypeContainer>
double chi_square_distance(const TypeContainer & point1, const TypeContainer & point2) {
    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = point1.begin();

    for (const auto & dim_point2 : point2) {
        const auto dim_point1 = *iter_point1;

        const double divider = std::abs(dim_point1) + std::abs(dim_point2);
        if (divider == 0) {
            continue;
        }

        distance += std::pow(dim_point1 - dim_point2, 2) / divider;
        ++iter_point1;
    }

    return distance;
}


/**
 *
 * @brief   Calculates Gower distance between points.
 *
 * @param[in] p_point1: point #1 that is represented by coordinates.
 * @param[in] p_point2: point #2 that is represented by coordinates.
 * @param[in] p_max_range: max range in each data dimension.
 *
 * @return  Returns Gower distance between points.
 *
 */
template <typename TypeContainer>
double gower_distance(const TypeContainer & p_point1, const TypeContainer & p_point2, const TypeContainer & p_max_range) {
    double distance = 0.0;
    typename TypeContainer::const_iterator iter_point1 = p_point1.begin();
    typename TypeContainer::const_iterator iter_range  = p_max_range.begin();

    for (const auto & dim_point2 : p_point2) {
        if (*iter_range != 0.0) {
            distance += std::abs(*iter_point1 - dim_point2) / *iter_range;
        }

        ++iter_point1;
        ++iter_range;
    }

    return distance / p_point1.size();
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
    distance_metric() = default;

    explicit distance_metric(const distance_functor<TypeContainer> & p_functor) : m_functor(p_functor) { }

    distance_metric(const distance_metric & p_other) = default;

    distance_metric(distance_metric && p_other) = default;

    virtual ~distance_metric() = default;

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
    euclidean_distance_metric() :
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
    euclidean_distance_square_metric() :
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
    manhattan_distance_metric() :
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
    chebyshev_distance_metric() :
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
    explicit minkowski_distance_metric(const double p_degree) :
        distance_metric<TypeContainer>(std::bind(minkowski_distance<TypeContainer>, std::placeholders::_1, std::placeholders::_2, p_degree))
    { }
};


/**
 *
 * @brief   Canberra distance metric calculator between two points.
 *
 */
template <typename TypeContainer>
class canberra_distance_metric : public distance_metric<TypeContainer> {
public:
    canberra_distance_metric() :
        distance_metric<TypeContainer>(std::bind(canberra_distance<TypeContainer>, std::placeholders::_1, std::placeholders::_2))
    { }
};


/**
 *
 * @brief   Chi square distance metric calculator between two points.
 *
 */
template <typename TypeContainer>
class chi_square_distance_metric : public distance_metric<TypeContainer> {
public:
    chi_square_distance_metric() :
        distance_metric<TypeContainer>(std::bind(chi_square_distance<TypeContainer>, std::placeholders::_1, std::placeholders::_2))
    { }
};


/**
 *
 * @brief   Gower distance metric calculator between two points.
 *
 */
template <typename TypeContainer>
class gower_distance_metric : public distance_metric<TypeContainer> {
public:
  /**
   *
   * @brief   Constructor of Gower distance metric.
   *
   * @param[in] p_max_range: max range in each data dimension.
   *
   */
    explicit gower_distance_metric(const TypeContainer & p_max_range) :
        distance_metric<TypeContainer>(std::bind(gower_distance<TypeContainer>, std::placeholders::_1, std::placeholders::_2, p_max_range))
    { }
};


/**
 *
 * @brief   Distance metric factory provides services for creation available metric in the 'pyclustering::utils::metric' and also user-defined.
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
    static distance_metric<TypeContainer> euclidean() {
        return euclidean_distance_metric<TypeContainer>();
    }

   /**
   *
   * @brief   Creates square Euclidean distance metric.
   *
   * @return  Square Euclidean distance metric
   *
   */
    static distance_metric<TypeContainer> euclidean_square() {
        return euclidean_distance_square_metric<TypeContainer>();
    }

   /**
   *
   * @brief   Creates Manhattan distance metric.
   *
   * @return  Manhattan distance metric.
   *
   */
    static distance_metric<TypeContainer> manhattan() {
        return manhattan_distance_metric<TypeContainer>();
    }

   /**
   *
   * @brief   Creates Chebyshev distance metric.
   *
   * @return  Chebyshev distance metric.
   *
   */
    static distance_metric<TypeContainer> chebyshev() {
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
   * @brief   Creates Canberra distance metric.
   *
   * @return  Canberra distance metric.
   *
   */
    static distance_metric<TypeContainer> canberra() {
        return canberra_distance_metric<TypeContainer>();
    }

   /**
   *
   * @brief   Creates Chi square distance metric.
   *
   * @return  Chi square distance metric.
   *
   */
    static distance_metric<TypeContainer> chi_square() {
        return chi_square_distance_metric<TypeContainer>();
    }

   /**
   *
   * @brief   Creates Gower distance metric.
   *
   * @param[in] p_max_range: max range in each data dimension.
   *
   * @return  Gower distance metric.
   *
   */
    static distance_metric<TypeContainer> gower(const TypeContainer & p_max_range) {
        return gower_distance_metric<TypeContainer>(p_max_range);
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


/**
 *
 * @brief   Finds farthest distance between points in specified container (data).
 *
 * @param[in] p_container: input data.
 * @param[in] p_metric: metric that is used for distance calculation between points.
 *
 * @return  Returns farthest distance between points.
 *
 */
template <typename TypeContainer>
double farthest_distance(const TypeContainer & p_container, const distance_metric<point> & p_metric)
{
    double distance = 0;
    for (std::size_t i = 0; i < p_container.size(); i++) {
        for (std::size_t j = i + 1; j < p_container.size(); j++) {
            double candidate_distance = p_metric(p_container[i], p_container[j]);
            if (candidate_distance > distance) {
                distance = candidate_distance;
            }
        }
    }

    return distance;
}


/**
 *
 * @brief   Calculates distance matrix using points container using Euclidean distance.
 *
 * @param[in]  p_points: input data that is represented by points.
 * @param[in]  p_metric: metric for distance calculation between points.
 * @param[out] p_distance_matrix: output distance matrix of points.
 *
 */
template <typename TypeContainer>
void distance_matrix(const TypeContainer & p_points, const distance_metric<point> & p_metric, TypeContainer & p_distance_matrix) {
    using TypeElement = typename TypeContainer::value_type;
    
    p_distance_matrix = TypeContainer(p_points.size(), TypeElement(p_points.size(), 0.0));

    for (std::size_t i = 0; i < p_points.size(); i++) {
        for (std::size_t j = i + 1; j < p_points.size(); j++) {
            const double distance = p_metric(p_points.at(i), p_points.at(j));
            p_distance_matrix[i][j] = distance;
            p_distance_matrix[j][i] = distance;
        }
    }
}


/**
 *
 * @brief   Calculates distance matrix using points container using Euclidean distance.
 *
 * @param[in]  p_points: input data that is represented by points.
 * @param[out] p_distance_matrix: output distance matrix of points.
 *
 */
template <typename TypeContainer>
void distance_matrix(const TypeContainer & p_points, TypeContainer & p_distance_matrix) {
    distance_matrix(p_points, distance_metric_factory<point>::euclidean(), p_distance_matrix);
}


}

}

}
