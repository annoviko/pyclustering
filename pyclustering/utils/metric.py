"""!

@brief Module provides various metrics - abstraction of the notion of distance in a metric space.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""


from enum import IntEnum;

import collections;


class type_metric(IntEnum):
    """!
    @brief Enumeration of supported metrics in the module for distance calculation between two points.

    """

    ## Euclidean distance, for more information see function 'euclidean_distance'.
    EUCLIDEAN = 0;

    ## Square Euclidean distance, for more information see function 'euclidean_distance_square'.
    EUCLIDEAN_SQUARE = 1;

    ## Manhattan distance, for more information see function 'manhattan_distance'.
    MANHATTAN = 2;

    ## Chebyshev distance, for more information see function 'chebyshev_distance'.
    CHEBYSHEV = 3;

    ## User defined function for distance calculation between two points.
    USER_DEFINED = 1000;


def calculate_metric(point1, point2, metric, func=None):
    """!
    @brief Calculates metric between two points in line with specified metric function.

    @param[in] point1 (numeric|list): The first point.
    @param[in] point2 (numeric|list): The second point.
    @param[in] metric (type_metric): Metric that is used for distance calculation between two points.
    @param[in] func (callable): Used only if metric is 'type_metric.USER_DEFINED' and represents callable object
                with two arguments: 'point1' and 'point2', notation is: 'func(point1, point2)'.

    @return (double) Distance between two points.

    """
    if metric == type_metric.EUCLIDEAN:
        return euclidean_distance(point1, point2);

    elif metric == type_metric.EUCLIDEAN_SQUARE:
        return euclidean_distance_square(point1, point2);

    elif metric == type_metric.MANHATTAN:
        return manhattan_distance(point1, point2);

    elif metric == type_metric.CHEBYSHEV:
        return chebyshev_distance(point1, point2);

    elif metric == type_metric.USER_DEFINED:
        return func(point1, point2);

    else:
        raise ValueError("Unknown type of metric: '%d'", metric);


def euclidean_distance(point1, point2):
    """!
    @brief Calculate Euclidean distance between vectors.
    @details The Euclidean between vectors (points) a and b is calculated by following formula:

    \f[
    dist(a, b) = \sqrt{ \sum_{i=0}^{N}(a_{i} - b_{i})^{2}) };
    \f]

    Where N is a length of each vector.

    @param[in] point1 (numeric|list): The first vector.
    @param[in] point2 (numeric|list): The second vector.

    @return (double) Euclidean distance between two vectors.

    """

    distance = euclidean_distance_square(point1, point2);
    return distance ** 0.5;


def euclidean_distance_square(point1, point2):
    """!
    @brief Calculate square Euclidean distance between vectors.

    \f[
    dist(a, b) = \sum_{i=0}^{N}(a_{i} - b_{i})^{2});
    \f]

    @param[in] point1 (numeric|list): The first vector.
    @param[in] point2 (numeric|list): The second vector.

    @return (double) Square Euclidean distance between two vectors.

    """

    if isinstance(point1, collections.Iterable):
        distance = 0.0;
        for i in range(len(point1)):
            distance += (point1[i] - point2[i]) ** 2.0;

        return distance;

    return (point1 - point2) ** 2.0;


def manhattan_distance(point1, point2):
    """!
    @brief Calculate Manhattan distance between vector a and b.

    \f[
    dist(a, b) = \sum_{i=0}^{N}\left | a_{i} - b_{i} \right |;
    \f]

    @param[in] point1 (numeric|list): The first vector.
    @param[in] point2 (numeric|list): The second vector.

    @return (double) Manhattan distance between two vectors.

    """

    if isinstance(point1, collections.Iterable):
        distance = 0.0;
        dimension = len(point1);

        for i in range(dimension):
            distance += abs(point1[i] - point2[i]);

        return distance;

    return abs(point1 - point2);


def chebyshev_distance(point1, point2):
    """!
    @brief Calculate Chebyshev distance between vector a and b.

    \f[
    dist(a, b) = \max_{}i\left (\left | a_{i} - b_{i} \right |\right );
    \f]

    @param[in] point1 (numeric|list): The first vector.
    @param[in] point2 (numeric|list): The second vector.

    @return (double) Chebyshev distance between two vectors.

    """
    if isinstance(point1, collections.Iterable):
        distance = 0.0;
        dimension = len(point1);

        for i in range(dimension):
            distance = max(distance, abs(point1[i] - point2[i]));

        return distance;

    return abs(point1 - point2);