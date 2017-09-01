import random
import math


class random_center_initializer:
    def __init__(self, data, amount_centers):
        self.__data = data;
        self.__amount = amount_centers;


    def initialize(self):
        return [ self.__create_center() for _ in range(len(self.__amount)) ];


    def __create_center(self):
        return [ random.random() for _ in range(len(self.__data[0])) ];


class kmeans_plusplus_initializer:

    def __init__(self, data, amount_centers):
        self.__data = data
        self.__amount = amount_centers

    @staticmethod
    def get_euclidean_distance(point1, point2):
        """
            Euclidean distance : d(q,p) = sqrt((q1 - p1)^2 + (q2 - p2)^2 + ...)
            :param point1: list with coordinated
            :param point2: list with coordinated
        """

        # Initialize distance
        distance = 0.0

        # Points should have equal size
        if len(point1) != len(point2):
            raise AttributeError('Try to calc Euclidean distance for points with different dimensions')

        # Calc (q1 - p1)^2 + (q2 - p2)^2 + ...
        for _p1, _p2 in zip(point1, point2):
            distance += (_p1 - _p2) ** 2

        # Calc sqrt
        distance = math.sqrt(distance)

        return distance

    @staticmethod
    def get_uniform(probabilities):
        """
        :param probabilities: List with segments in increasing sequence with val in [0, 1].
                    Example [0 0.1 0.2 0.3 1.0]
        :return: Index in 'probabilities'
        """

        # Initialize return value
        res_idx = None

        # Get random num in range [0, 1)
        random_num = random.random()

        # Find segment with  val1 < random_num < val2
        for _idx in range(len(probabilities)):

            if random_num < probabilities[_idx]:
                res_idx = _idx
                break

        if res_idx is None:
            print('Random number : ', random_num)
            print('Probabilities : ', probabilities)
            raise AttributeError('list "probabilities" should contains 1 as the end of last segment(s)')

        return res_idx

    def get_first_center(self):
        """  Get first center chosen uniformly at random from data """

        # Initialize list with uniform probabilities
        probabilities = []

        # Fill probability list
        for i in range(len(self.__data)):
            probabilities.append((i + 1) / len(self.__data))

        return self.__data[self.get_uniform(probabilities)]

    @staticmethod
    def calc_distance_to_nearest_center(data, centers):
        """   """

        # Initialize
        distance_data = []

        # For each data point x, compute D(x), the distance between x and the nearest center
        for _point in data:

            # Min dist to nearest center
            min_dist = float('inf')

            # For each center
            for _center in centers:
                min_dist = min(min_dist, kmeans_plusplus_initializer.get_euclidean_distance(_center, _point))

            # Add distance to nearest center into result list
            distance_data.append(min_dist)

        return distance_data

    @staticmethod
    def get_sum_for_normalize_distance(distance):
        """  """

        sum_distance = 0

        for _dist in distance:
            sum_distance += _dist ** 2

        return sum_distance

    @staticmethod
    def set_last_value_to_one(probabilities):
        """ """

        # Start from the last elem
        back_idx = - 1

        # All values equal to the last elem should be set to 1
        last_val = probabilities[back_idx]

        # for all elements or if a elem not equal to the last elem
        for _idx in range(-1, -len(probabilities) - 1):
            if probabilities[back_idx] == last_val:
                probabilities[back_idx] = 1
            else:
                break

    @staticmethod
    def get_probabilities_from_distance(distance):
        """   """

        # Normalize distance
        sum_for_normalize = kmeans_plusplus_initializer.get_sum_for_normalize_distance(distance)

        # Create list with probabilities

        # Initialize list with probabilities
        probabilities = []

        # Variable to accumulate probabilities
        prev_value = 0

        # Fill probabilities as :
        #   p[idx] = D[idx]^2 / sum_2
        #       where sum_2 = D[0]^2 + D[1]^2 + ...
        for _dist in distance:
            prev_value = (_dist ** 2) / sum_for_normalize + prev_value
            probabilities.append(prev_value)

        # Set last value to 1
        kmeans_plusplus_initializer.set_last_value_to_one(probabilities)

        return probabilities

    def initialize(self):
        """  kmeans++ method for center initialization  """

        # Should be at least 1 center
        if self.__amount <= 0:
            raise AttributeError('Amount of cluster centers should be at least 1')

        # Initialize result list by the first centers
        centers = [self.get_first_center()]

        # For each next center
        for _ in range(1, self.__amount):

            # Calc Distance for each data
            distance_data = self.calc_distance_to_nearest_center(data=self.__data, centers=centers)

            # Create list with probabilities
            probabilities = self.get_probabilities_from_distance(distance_data)
            print('Probability : ', probabilities)

            # Choose one new data point at random as a new center, using a weighted probability distribution
            ret_idx = self.get_uniform(probabilities)

            # Add new center
            centers.append(self.__data[ret_idx])

            print('Centers : ', centers)
            print('Return index : ', ret_idx)
            # where a point x is chosen with probability proportional to D(x)^2.

        # Is all centers are initialized
