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

    ## Minkowski distance, for more information see function 'minkowski_distance'.
    MINKOWSKI = 4;

    ## User defined function for distance calculation between two points.
    USER_DEFINED = 1000;


class distance_metric:
    """!
    @brief

    """
    def __init__(self, type, **kwargs):
        """!
        @brief Creates distance metric instance for calculation distance between two points.

        @param[in] type (type_metric):
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'func' and corresponding additional argument for
                    for specific metric types).

        Keyword Args:
            func (callable): Callable object with two arguments (point #1 and point #2) that is used only if metric is 'type_metric.USER_DEFINED'.
            degree (numeric): Only for 'type_metric.MINKOWSKI' - degree of Minkowski equation.

        """
        self.__type = type;
        self.__args = kwargs;
        self.__func = self.__get('func', None, self.__args);


    def __call__(self, point1, point2):
        """!
        @brief Calculates distance between two points.

        @param[in] point1 (list): The first point.
        @param[in] point2 (list): The second point.

        @return (double) Distance between two points.

        """
        if self.__type == type_metric.EUCLIDEAN:
            return euclidean_distance(point1, point2);

        elif self.__type == type_metric.EUCLIDEAN_SQUARE:
            return euclidean_distance_square(point1, point2);

        elif self.__type == type_metric.MANHATTAN:
            return manhattan_distance(point1, point2);

        elif self.__type == type_metric.CHEBYSHEV:
            return chebyshev_distance(point1, point2);

        elif self.__type == type_metric.MINKOWSKI:
            return minkowski_distance(point1, point2, self.__get('degree', 2, self.__args));

        elif self.__type == type_metric.USER_DEFINED:
            return self.__func(point1, point2);

        else:
            raise ValueError("Unknown type of metric: '%d'", self.__type);


    def __get(self, key, default_value, container):
        """!
        @brief Returns value from container by key if key is contained by 'container' otherwise default value.

        @param[in] key (string): Argument name (key in 'container') whose value is required.
        @param[in] default_value (any): Value that is returned if argument is not found in 'container'.
        @param[in] container (dict): Dictionary with arguments (key, value).

        @return (any) Value from container by key if key is contained by 'container' otherwise default value.

        """
        if key in container:
            return container[key];

        return default_value;


def euclidean_distance(point1, point2):
    """!
    @brief Calculate Euclidean distance between two vectors.
    @details The Euclidean between vectors (points) a and b is calculated by following formula:

    \f[
    dist(a, b) = \sqrt{ \sum_{i=0}^{N}(a_{i} - b_{i})^{2} };
    \f]

    Where N is a length of each vector.

    @param[in] point1 (list): The first vector.
    @param[in] point2 (list): The second vector.

    @return (double) Euclidean distance between two vectors.

    @see euclidean_distance_square, manhattan_distance, chebyshev_distance

    """
    distance = euclidean_distance_square(point1, point2);
    return distance ** 0.5;


def euclidean_distance_square(point1, point2):
    """!
    @brief Calculate square Euclidean distance between two vectors.

    \f[
    dist(a, b) = \sum_{i=0}^{N}(a_{i} - b_{i})^{2};
    \f]

    @param[in] point1 (list): The first vector.
    @param[in] point2 (list): The second vector.

    @return (double) Square Euclidean distance between two vectors.

    @see euclidean_distance, manhattan_distance, chebyshev_distance

    """
    distance = 0.0;
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2.0;

    return distance;


def manhattan_distance(point1, point2):
    """!
    @brief Calculate Manhattan distance between between two vectors.

    \f[
    dist(a, b) = \sum_{i=0}^{N}\left | a_{i} - b_{i} \right |;
    \f]

    @param[in] point1 (list): The first vector.
    @param[in] point2 (list): The second vector.

    @return (double) Manhattan distance between two vectors.

    @see euclidean_distance_square, euclidean_distance, chebyshev_distance

    """
    distance = 0.0;
    dimension = len(point1);

    for i in range(dimension):
        distance += abs(point1[i] - point2[i]);

    return distance;


def chebyshev_distance(point1, point2):
    """!
    @brief Calculate Chebyshev distance between between two vectors.

    \f[
    dist(a, b) = \max_{}i\left (\left | a_{i} - b_{i} \right |\right );
    \f]

    @param[in] point1 (list): The first vector.
    @param[in] point2 (list): The second vector.

    @return (double) Chebyshev distance between two vectors.

    @see euclidean_distance_square, euclidean_distance, minkowski_distance

    """
    distance = 0.0;
    dimension = len(point1);

    for i in range(dimension):
        distance = max(distance, abs(point1[i] - point2[i]));

    return distance;


def minkowski_distance(point1, point2, degree=2):
    """!
    @brief Calculate Minkowski distance between two vectors.

    \f[
    dist(a, b) = \sqrt[p]{ \sum_{i=0}^{N}\left(a_{i} - b_{i}\right)^{p} };
    \f]

    @param[in] point1 (list): The first vector.
    @param[in] point2 (list): The second vector.
    @param[in] degree (numeric): Degree of that is used for Minkowski distance.

    @return (double) Minkowski distance between two vectors.

    @see euclidean_distance

    """
    distance = 0.0;
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** degree;

    return distance ** (1.0 / degree);