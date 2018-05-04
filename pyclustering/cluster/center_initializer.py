"""!

@brief Collection of center initializers for algorithm that uses initial centers, for example, for K-Means or X-Means.
@details Implementation based on paper @cite article::kmeans++::1.
         
@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
@date 2014-2018
@copyright GNU Public License

@see pyclustering.cluster.kmeans
@see puclustering.cluster.xmeans

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


import numpy;
import random;

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
              out optimal initial centers.

    Algorithm can be divided into three steps. The first center is chosen from input data randomly with
    uniform distribution at the first step. At the second, probability to being center is calculated for each point:
    \f[p_{i}=\frac{D(x_{i})}{\sum_{j=0}^{N}D(x_{j})}\f]
    where \f$D(x_{i})\f$ is a distance from point \f$i\f$ to the closest center. Using this probabilities next center
    is chosen. The last step is repeated until required amount of centers is initialized.

    Pyclustering implementation of the algorithm provides feature to consider several candidates on the second
    step, for example:

    @code
        amount_centers = 4;
        amount_candidates = 3;
        initializer = kmeans_plusplus_initializer(sample, amount_centers, amount_candidates);
    @endcode

    If the farthest points should be used as centers then special constant 'FARTHEST_CENTER_CANDIDATE' should be used
    for that purpose, for example:
    @code
        amount_centers = 4;
        amount_candidates = kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE;
        initializer = kmeans_plusplus_initializer(sample, amount_centers, amount_candidates);
    @endcode

    There is an example of initial centers that were calculated by the K-Means++ method:

    @image html kmeans_plusplus_initializer_results.png
    
    Code example where initial centers are prepared for K-Means algorithm:
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


    ## Constant denotes that only points with highest probabilities should be considered as centers.
    FARTHEST_CENTER_CANDIDATE = "farthest";


    def __init__(self, data, amount_centers, amount_candidates = 1):
        """!
        @brief Creates K-Means++ center initializer instance.
        
        @param[in] data (array_like): List of points where each point is represented by list of coordinates.
        @param[in] amount_centers (uint): Amount of centers that should be initialized.
        @param[in] amount_candidates (uint): Amount of candidates that is considered as a center, if the farthest points (with the highest probability) should
                    be considered as centers then special constant should be used 'FARTHEST_CENTER_CANDIDATE'.

        @see FARTHEST_CENTER_CANDIDATE

        """
        
        self.__data = numpy.array(data);
        self.__amount = amount_centers;
        self.__candidates = amount_candidates;

        self.__check_parameters();


    def __check_parameters(self):
        """!
        @brief Checks input parameters of the algorithm and if something wrong then corresponding exception is thrown.

        """
        if (self.__amount <= 0) or (self.__amount > len(self.__data)):
            raise AttributeError("Amount of cluster centers should be at least 1 and should be less or equal to amount of points in data.");

        if self.__candidates != kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE:
            if (self.__candidates <= 0) or (self.__candidates > len(self.__data)):
                raise AttributeError("Amount of candidates centers should be at least 1 and should be less or equal to amount of points in data.");

        if len(self.__data) == 0:
            raise AttributeError("Data is empty.")


    def __calculate_shortest_distances(self, data, centers):
        """!
        @brief Calculates distance from each data point to nearest center.
        
        @param[in] data (numpy.array): Array of points for that initialization is performed.
        @param[in] centers (numpy.array): Array of points that represents centers.
        
        @return (numpy.array) List of distances to closest center for each data point.
        
        """

        dataset_differences = numpy.zeros((len(centers), len(data)));
        for index_center in range(len(centers)):
            dataset_differences[index_center] = numpy.sum(
                numpy.square(data - centers[index_center]), axis=1).T;

        shortest_distances = numpy.min(dataset_differences, axis=0);
        return shortest_distances;


    def __get_next_center(self, centers):
        """!
        @brief Calculates the next center for the data.

        @param[in] centers (array_like): Current initialized centers.

        @return (array_like) Next initialized center.

        """

        distances = self.__calculate_shortest_distances(data=self.__data, centers=centers);

        if self.__candidates == kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE:
            center_index = numpy.argmax(distances);
        else:
            probabilities = self.__calculate_probabilities(distances);
            center_index = self.__get_probable_center(distances, probabilities);

        return self.__data[center_index];


    def __calculate_probabilities(self, distances):
        """!
        @brief Calculates cumulative probabilities of being center of each point.

        @param[in] distances (array_like): Distances from each point to closest center.

        @return (array_like) Cumulative probabilities of being center of each point.

        """

        total_distance = numpy.sum(distances);
        if total_distance != 0.0:
            probabilities = distances / total_distance;
            return numpy.cumsum(probabilities);
        else:
            return numpy.zeros(len(distances));


    def __get_probable_center(self, distances, probabilities):
        """!
        @brief Calculates the next probable center considering amount candidates.

        @param[in] distances (array_like): Distances from each point to closest center.
        @param[in] probabilities (array_like): Cumulative probabilities of being center of each point.

        @return (uint) Index point that is next initialized center.

        """

        index_best_candidate = -1;
        for _ in range(self.__candidates):
            candidate_probability = random.random();
            index_candidate = 0;

            for index_object in range(len(probabilities)):
                if candidate_probability < probabilities[index_object]:
                    index_candidate = index_object;
                    break;

            if index_best_candidate == -1:
                index_best_candidate = index_candidate;
            elif distances[index_best_candidate] < distances[index_object]:
                index_best_candidate = index_candidate;

        return index_best_candidate;


    def initialize(self):
        """!
        @brief Calculates initial centers using K-Means++ method.
        
        @return (list) List of initialized initial centers.
        
        """

        index_center = random.randint(0, len(self.__data) - 1);
        centers = [ self.__data[ index_center ] ];

        # For each next center
        for _ in range(1, self.__amount):
            next_center = self.__get_next_center(centers);
            centers.append(next_center);

        return centers;