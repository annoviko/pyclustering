"""!

@brief Module provides various distance metrics - abstraction of the notion of distance in a metric space.

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


import numpy

from enum import IntEnum


class type_metric(IntEnum):
    """!
    @brief Enumeration of supported metrics in the module for distance calculation between two points.

    """

    ## Euclidean distance, for more information see function 'euclidean_distance'.
    EUCLIDEAN = 0

    ## Square Euclidean distance, for more information see function 'euclidean_distance_square'.
    EUCLIDEAN_SQUARE = 1

    ## Manhattan distance, for more information see function 'manhattan_distance'.
    MANHATTAN = 2

    ## Chebyshev distance, for more information see function 'chebyshev_distance'.
    CHEBYSHEV = 3

    ## Minkowski distance, for more information see function 'minkowski_distance'.
    MINKOWSKI = 4

    ## User defined function for distance calculation between two points.
    USER_DEFINED = 1000



class distance_metric:
    """!
    @brief Distance metric performs distance calculation between two points in line with encapsulated function, for
            example, euclidean distance or chebyshev distance, or even user-defined.

    @details

    Example of Euclidean distance metric:
    @code
        metric = distance_metric(type_metric.EUCLIDEAN)
        distance = metric([1.0, 2.5], [-1.2, 3.4])
    @endcode

    Example of Chebyshev distance metric:
    @code
        metric = distance_metric(type_metric.CHEBYSHEV)
        distance = metric([0.0, 0.0], [2.5, 6.0])
    @endcode

    In following example additional argument should be specified (generally, 'degree' is a optional argument that is
     equal to '2' by default) that is specific for Minkowski distance:
    @code
        metric = distance_metric(type_metric.MINKOWSKI, degree=4)
        distance = metric([4.0, 9.2, 1.0], [3.4, 2.5, 6.2])
    @endcode

    User may define its own function for distance calculation:
    @code
        user_function = lambda point1, point2: point1[0] + point2[0] + 2
        metric = distance_metric(type_metric.USER_DEFINED, func=user_function)
        distance = metric([2.0, 3.0], [1.0, 3.0])
    @endcode

    """
    def __init__(self, type, **kwargs):
        """!
        @brief Creates distance metric instance for calculation distance between two points.

        @param[in] type (type_metric):
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'numpy_usage' 'func' and corresponding additional argument for
                    for specific metric types).

        <b>Keyword Args:</b><br>
            - func (callable): Callable object with two arguments (point #1 and point #2) or (object #1 and object #2) in case of numpy usage.
                                This argument is used only if metric is 'type_metric.USER_DEFINED'.
            - degree (numeric): Only for 'type_metric.MINKOWSKI' - degree of Minkowski equation.
            - numpy_usage (bool): If True then numpy is used for calculation (by default is False).

        """
        self.__type = type
        self.__args = kwargs
        self.__func = self.__args.get('func', None)
        self.__numpy = self.__args.get('numpy_usage', False)

        self.__calculator = self.__create_distance_calculator()


    def __call__(self, point1, point2):
        """!
        @brief Calculates distance between two points.

        @param[in] point1 (list): The first point.
        @param[in] point2 (list): The second point.

        @return (double) Distance between two points.

        """
        return self.__calculator(point1, point2)


    def get_type(self):
        """!
        @brief Return type of distance metric that is used.

        @return (type_metric) Type of distance metric.

        """
        return self.__type


    def get_arguments(self):
        """!
        @brief Return additional arguments that are used by distance metric.

        @return (dict) Additional arguments.

        """
        return self.__args


    def get_function(self):
        """!
        @brief Return user-defined function for calculation distance metric.

        @return (callable): User-defined distance metric function.

        """
        return self.__func


    def enable_numpy_usage(self):
        """!
        @brief Start numpy for distance calculation.
        @details Useful in case matrices to increase performance.

        """
        self.__numpy = True
        self.__calculator = self.__create_distance_calculator()


    def disable_numpy_usage(self):
        """!
        @brief Stop using numpy for distance calculation.
        @details Useful in case of big amount of small data portion when numpy call is longer than calculation itself.

        """
        self.__numpy = False
        self.__calculator = self.__create_distance_calculator()


    def __create_distance_calculator(self):
        if self.__numpy is True:
            return self.__create_distance_calculator_numpy()

        return self.__create_distance_calculator_basic()


    def __create_distance_calculator_basic(self):
        """!
        @brief Creates distance metric calculator.

        @return (callable) Callable object of distance metric calculator.

        """
        if self.__type == type_metric.EUCLIDEAN:
            return euclidean_distance

        elif self.__type == type_metric.EUCLIDEAN_SQUARE:
            return euclidean_distance_square

        elif self.__type == type_metric.MANHATTAN:
            return manhattan_distance

        elif self.__type == type_metric.CHEBYSHEV:
            return chebyshev_distance

        elif self.__type == type_metric.MINKOWSKI:
            return lambda point1, point2: minkowski_distance(point1, point2, self.__args.get('degree', 2))

        elif self.__type == type_metric.USER_DEFINED:
            return self.__func

        else:
            raise ValueError("Unknown type of metric: '%d'", self.__type)


    def __create_distance_calculator_numpy(self):
        """!
        @brief Creates distance metric calculator that uses numpy.

        @return (callable) Callable object of distance metric calculator.

        """
        if self.__type == type_metric.EUCLIDEAN:
            return euclidean_distance_numpy

        elif self.__type == type_metric.EUCLIDEAN_SQUARE:
            return euclidean_distance_square_numpy

        elif self.__type == type_metric.MANHATTAN:
            return manhattan_distance_numpy

        elif self.__type == type_metric.CHEBYSHEV:
            return chebyshev_distance_numpy

        elif self.__type == type_metric.MINKOWSKI:
            return lambda object1, object2: minkowski_distance_numpy(object1, object2, self.__args.get('degree', 2))

        elif self.__type == type_metric.USER_DEFINED:
            return self.__func

        else:
            raise ValueError("Unknown type of metric: '%d'", self.__type)



def euclidean_distance(point1, point2):
    """!
    @brief Calculate Euclidean distance between two vectors.
    @details The Euclidean between vectors (points) a and b is calculated by following formula:

    \f[
    dist(a, b) = \sqrt{ \sum_{i=0}^{N}(a_{i} - b_{i})^{2} };
    \f]

    Where N is a length of each vector.

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.

    @return (double) Euclidean distance between two vectors.

    @see euclidean_distance_square, manhattan_distance, chebyshev_distance

    """
    distance = euclidean_distance_square(point1, point2)
    return distance ** 0.5


def euclidean_distance_numpy(object1, object2):
    """!
    @brief Calculate Euclidean distance between two objects using numpy.

    @param[in] object1 (array_like): The first array_like object.
    @param[in] object2 (array_like): The second array_like object.

    @return (double) Euclidean distance between two objects.

    """
    return numpy.sum(numpy.sqrt(numpy.square(object1 - object2)), axis=1).T


def euclidean_distance_square(point1, point2):
    """!
    @brief Calculate square Euclidean distance between two vectors.

    \f[
    dist(a, b) = \sum_{i=0}^{N}(a_{i} - b_{i})^{2};
    \f]

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.

    @return (double) Square Euclidean distance between two vectors.

    @see euclidean_distance, manhattan_distance, chebyshev_distance

    """
    distance = 0.0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2.0

    return distance


def euclidean_distance_square_numpy(object1, object2):
    """!
    @brief Calculate square Euclidean distance between two objects using numpy.

    @param[in] object1 (array_like): The first array_like object.
    @param[in] object2 (array_like): The second array_like object.

    @return (double) Square Euclidean distance between two objects.

    """
    return numpy.sum(numpy.square(object1 - object2), axis=1).T


def manhattan_distance(point1, point2):
    """!
    @brief Calculate Manhattan distance between between two vectors.

    \f[
    dist(a, b) = \sum_{i=0}^{N}\left | a_{i} - b_{i} \right |;
    \f]

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.

    @return (double) Manhattan distance between two vectors.

    @see euclidean_distance_square, euclidean_distance, chebyshev_distance

    """
    distance = 0.0
    dimension = len(point1)

    for i in range(dimension):
        distance += abs(point1[i] - point2[i])

    return distance


def manhattan_distance_numpy(object1, object2):
    """!
    @brief Calculate Manhattan distance between two objects using numpy.

    @param[in] object1 (array_like): The first array_like object.
    @param[in] object2 (array_like): The second array_like object.

    @return (double) Manhattan distance between two objects.

    """
    return numpy.sum(numpy.absolute(object1 - object2), axis=1).T


def chebyshev_distance(point1, point2):
    """!
    @brief Calculate Chebyshev distance between between two vectors.

    \f[
    dist(a, b) = \max_{}i\left (\left | a_{i} - b_{i} \right |\right );
    \f]

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.

    @return (double) Chebyshev distance between two vectors.

    @see euclidean_distance_square, euclidean_distance, minkowski_distance

    """
    distance = 0.0
    dimension = len(point1)

    for i in range(dimension):
        distance = max(distance, abs(point1[i] - point2[i]))

    return distance


def chebyshev_distance_numpy(object1, object2):
    """!
    @brief Calculate Chebyshev distance between two objects using numpy.

    @param[in] object1 (array_like): The first array_like object.
    @param[in] object2 (array_like): The second array_like object.

    @return (double) Chebyshev distance between two objects.

    """
    return numpy.max(numpy.absolute(object1 - object2), axis=1).T


def minkowski_distance(point1, point2, degree=2):
    """!
    @brief Calculate Minkowski distance between two vectors.

    \f[
    dist(a, b) = \sqrt[p]{ \sum_{i=0}^{N}\left(a_{i} - b_{i}\right)^{p} };
    \f]

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.
    @param[in] degree (numeric): Degree of that is used for Minkowski distance.

    @return (double) Minkowski distance between two vectors.

    @see euclidean_distance

    """
    distance = 0.0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** degree

    return distance ** (1.0 / degree)


def minkowski_distance_numpy(object1, object2, degree=2):
    """!
    @brief Calculate Minkowski distance between objects using numpy.

    @param[in] object1 (array_like): The first array_like object.
    @param[in] object2 (array_like): The second array_like object.
    @param[in] degree (numeric): Degree of that is used for Minkowski distance.

    @return (double) Minkowski distance between two object.

    """
    return numpy.sum(numpy.power(numpy.power(object1 - object2, degree), 1/degree), axis=1).T