"""!

@brief Collection of center initializers for algorithm that uses initial centers, for example, for K-Means or X-Means.
@details Implementations based on articles:
         - K-Means++: The Advantages of careful seeding. D. Arthur, S. Vassilvitskii. 2007.
         
@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
@date 2014-2018
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
    @details K-Means++ algorithm guarantees an approximation ratio O(log k). Clustering results are depends on
              initial centers in case of K-Means algorithm and even in case of X-Means. This method is used to find
              out optimal initial centers. There is an example of initial centers that were calculated by the
              K-Means++ method:
    
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


    def initialize(self):
        """!
        @brief Calculates initial centers using K-Means++ method.
        
        @return (list) List of initialized initial centers.
        
        """
        # Initialize result list by the first centers
        index_center = random.randint(0, len(self.__data) - 1);
        centers = [ self.__data[ index_center ] ];

        # For each next center
        for _ in range(1, self.__amount):
            # Calc Distance for each data
            distance_data = self.__calc_distance_to_nearest_center(data = self.__data, centers = centers);

            center_index = 0;
            longest_distance = 0.0;
            for index_distance in range(len(distance_data)):
                if (longest_distance < distance_data[index_distance]):
                    center_index = index_distance;
                    longest_distance = distance_data[index_distance];

            centers.append(self.__data[center_index]);

        return centers;