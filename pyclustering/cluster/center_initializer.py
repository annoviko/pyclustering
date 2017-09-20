"""!

@brief Collection of center initializers for algorithm that uses initial centers, for example, for K-Means or X-Means.
@details Implementations based on articles:
         - K-Means++: The Advantages of careful seeding. D. Arthur, S. Vassilvitskii. 2007.
         
@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
@date 2014-2017
@copyright GNU Public License

@see kmeans
@see xmeans

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

import random;
import copy

from pyclustering.utils import euclidean_distance;


class random_center_initializer:
    """!
    @brief Random center initializer is for generation specified amount of random of centers for specified data.
    
    """

    def __init__(self, data, amount_centers):
        """!
        @brief Creates instance of random center initializer.
        
        @param[in] data (list): List of points where each point is represented by list of coordinates.
        @param[in] amount_centers (unit): Amount of centers that should be initialized.
        
        """
        
        self.__data = data;
        self.__amount = amount_centers;

        if self.__amount <= 0:
            raise AttributeError("Amount of cluster centers should be at least 1.");


    def initialize(self):
        """!
        @brief Generates random centers in line with input parameters.
        
        @return (list) List of centers where each center is represented by list of coordinates.
        
        """
        return [ self.__create_center() for _ in range(self.__amount) ];


    def __create_center(self):
        """!
        @brief Generates and returns random center.
        
        """
        return [ random.random() for _ in range(len(self.__data[0])) ];



class kmeans_plusplus_initializer:
    """!
    @brief K-Means++ is an algorithm for choosing the initial centers for algorithms like K-Means or X-Means.
    @details Clustering results are depends on initial centers in case of K-Means algorithm and even in case of X-Means.
              This method is used to find out optimal initial centers. There is an example of initial centers that were
              calculated by the K-Means++ method:
    
    @image html kmeans_plusplus_initializer_results.png
    
    Code example:
    @code
        # Read data 'SampleSimple3' from Simple Sample collection.
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
        
        # Calculate initial centers using K-Means++ method.
        centers = kmeans_plusplus_initializer(sample, 4).initialize();
        
        # Display initial centers.
        visualizer = cluster_visualizer();
        visualizer.append_cluster(sample);
        visualizer.append_cluster(centers, marker = '*', markersize = 10);
        visualizer.show();
        
        # Perform cluster analysis using K-Means algorithm with initial centers.
        kmeans_instance = kmeans(sample, centers);
        
        # Run clustering process and obtain result.
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();
    @endcode
    
    """
    
    def __init__(self, data, amount_centers):
        """!
        @brief Creates K-Means++ center initializer instance.
        
        @param[in] data (list): List of points where each point is represented by list of coordinates.
        @param[in] amount_centers (unit): Amount of centers that should be initialized.
        
        """
        
        self.__data = data;
        self.__amount = amount_centers;
        
        if self.__amount <= 0:
            raise AttributeError("Amount of cluster centers should be at least 1.");
    
    
    def __get_uniform(self, probabilities):
        """!
        @brief Returns index in probabilities.
        
        @param[in] probabilities (list): List with segments in increasing sequence with val in [0, 1], for example, [0 0.1 0.2 0.3 1.0].
        
        """

        # Initialize return value
        res_idx = None;

        # Get random num in range [0, 1)
        random_num = random.random();

        # Find segment with  val1 < random_num < val2
        for _idx in range(len(probabilities)):
            if random_num < probabilities[_idx]:
                res_idx = _idx;
                break;

        if res_idx is None:
            raise AttributeError("List 'probabilities' should contain 1 as the end of last segment(s)");

        return res_idx


    def __get_first_center(self):
        """!
        @brief Returns first center chosen uniformly at random from data.
        
        """

        # Initialize list with uniform probabilities
        probabilities = [];

        # Fill probability list
        for i in range(len(self.__data)):
            probabilities.append((i + 1) / len(self.__data));

        return self.__data[self.__get_uniform(probabilities)];


    def __calc_distance_to_nearest_center(self, data, centers):
        """!
        @brief Calculates distance from each data point to nearest center.
        
        @param[in] data (list): List of points where each point is represented by list of coordinates.
        @param[in] centers (list): List of points that represents centers and where each center is represented by list of coordinates.
        
        @return (list) List of distances to closest center for each data point.
        
        """

        # Initialize
        distance_data = [];

        # For each data point x, compute D(x), the distance between x and the nearest center
        for _point in data:

            # Min dist to nearest center
            min_dist = float('inf');

            # For each center
            for _center in centers:
                min_dist = min(min_dist, euclidean_distance(_center, _point));

            # Add distance to nearest center into result list
            distance_data.append(min_dist);

        return distance_data;


    def __get_sum_for_normalize_distance(self, distance):
        """!
        @brief Calculates square sum distance that is used for normalization.
        
        @param[in] distance (list): List of minimum distances from each point to nearest center.
        
        @return (float) Square sum distance.
        
        """

        sum_distance = 0.0;

        for _dist in distance:
            sum_distance += _dist ** 2;

        return sum_distance;


    def __set_last_value_to_one(self, probabilities):
        """!
        @brief Update probabilities for all points.
        @details All values of probability list equals to the last element are set to 1.
        
        @param[in] probabilities (list): List of minimum distances from each point to nearest center.
        
        """

        # All values equal to the last elem should be set to 1
        last_val = probabilities[-1];

        # for all elements or if a elem not equal to the last elem
        for _idx in range(-1, -len(probabilities) - 1, -1):
            if probabilities[_idx] == last_val:
                probabilities[_idx] = 1.0;
            else:
                break;

    def __get_probabilities_from_distance(self, distance):
        """!
        @brief Calculates probabilities from distance.
        @details Probabilities are filled by following expression:
        
        \f[
        p[i]=\frac{dist_{i}^2}{\sum_{i=0}^{N}dist_{i}};
        \f]
        
        @param[in] distance (list): List of minimum distances from each point to nearest center.
        
        @return (list) Weighted belonging probability for each point to its nearest center.
        
        """
        # Normalize distance
        sum_for_normalize = self.__get_sum_for_normalize_distance(distance);

        # Create list with probabilities

        # Initialize list with probabilities
        probabilities = [];

        # Variable to accumulate probabilities
        prev_value = 0;

        # Fill probabilities as :
        #   p[idx] = D[idx]^2 / sum_2
        #       where sum_2 = D[0]^2 + D[1]^2 + ...
        for _dist in distance:
            if sum_for_normalize > 0.0:
                prev_value = (_dist ** 2) / sum_for_normalize + prev_value;
            probabilities.append(prev_value);

        # Set last value to 1
        self.__set_last_value_to_one(probabilities);

        return probabilities;


    def initialize(self):
        """!
        @brief Calculates initial centers using K-Means++ method.
        
        @return (list) List of initialized initial centers.
        
        """
        # Initialize result list by the first centers
        centers = [self.__get_first_center()];

        # For each next center
        for _ in range(1, self.__amount):

            # Calc Distance for each data
            distance_data = self.__calc_distance_to_nearest_center(data = self.__data, centers = centers);

            # Create list with probabilities
            probabilities = self.__get_probabilities_from_distance(distance_data);
            # print('Probability : ', probabilities);

            # Choose one new data point at random as a new center, using a weighted probability distribution
            ret_idx = self.__get_uniform(probabilities);

            # Add new center
            centers.append(self.__data[ret_idx]);

        # Is all centers are initialized
        return centers;