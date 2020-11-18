"""!

@brief Cluster analysis algorithm: K-Medoids.
@details Implementation based on paper @cite inproceedings::cluster::kmedoids::1.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import numpy

from pyclustering.cluster.encoder import type_encoding

from pyclustering.utils import medoid
from pyclustering.utils.metric import distance_metric, type_metric

import pyclustering.core.kmedoids_wrapper as wrapper

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.metric_wrapper import metric_wrapper


class kmedoids:
    """!
    @brief Class represents clustering algorithm K-Medoids (PAM algorithm).
    @details PAM is a partitioning clustering algorithm that uses the medoids instead of centers like in case of K-Means
              algorithm. Medoid is an object with the smallest dissimilarity to all others in the cluster. PAM algorithm
              complexity is \f$O\left ( k\left ( n-k \right )^{2} \right )\f$.

    There is an example where PAM algorithm is used to cluster 'TwoDiamonds' data:
    @code
        from pyclustering.cluster.kmedoids import kmedoids
        from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # Load list of points for cluster analysis.
        sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

        # Initialize initial medoids using K-Means++ algorithm
        initial_medoids = kmeans_plusplus_initializer(sample, 2).initialize(return_index=True)

        # Create instance of K-Medoids (PAM) algorithm.
        kmedoids_instance = kmedoids(sample, initial_medoids)

        # Run cluster analysis and obtain results.
        kmedoids_instance.process()
        clusters = kmedoids_instance.get_clusters()
        medoids = kmedoids_instance.get_medoids()

        # Print allocated clusters.
        print("Clusters:", clusters)

        # Display clustering results.
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.append_cluster(initial_medoids, sample, markersize=12, marker='*', color='gray')
        visualizer.append_cluster(medoids, sample, markersize=14, marker='*', color='black')
        visualizer.show()
    @endcode

    @image html pam_clustering_two_diamonds.png "Fig. 1. K-Medoids (PAM) clustering results 'TwoDiamonds'."

    Metric for calculation distance between points can be specified by parameter additional 'metric':
    @code
        # create Minkowski distance metric with degree equals to '2'
        metric = distance_metric(type_metric.MINKOWSKI, degree=2)

        # create K-Medoids algorithm with specific distance metric
        kmedoids_instance = kmedoids(sample, initial_medoids, metric=metric)

        # run cluster analysis and obtain results
        kmedoids_instance.process()
        clusters = kmedoids_instance.get_clusters()
    @endcode

    Distance matrix can be used instead of sequence of points to increase performance and for that purpose parameter 'data_type' should be used:
    @code
        # calculate distance matrix for sample
        sample = read_sample(path_to_sample)
        matrix = calculate_distance_matrix(sample)

        # create K-Medoids algorithm for processing distance matrix instead of points
        kmedoids_instance = kmedoids(matrix, initial_medoids, data_type='distance_matrix')

        # run cluster analysis and obtain results
        kmedoids_instance.process()

        clusters = kmedoids_instance.get_clusters()
        medoids = kmedoids_instance.get_medoids()
    @endcode

    """
    
    
    def __init__(self, data, initial_index_medoids, tolerance=0.0001, ccore=True, **kwargs):
        """!
        @brief Constructor of clustering algorithm K-Medoids.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] initial_index_medoids (list): Indexes of intial medoids (indexes of points in input data).
        @param[in] tolerance (double): Stop condition: if maximum value of distance change of medoids of clusters is less than tolerance than algorithm will stop processing.
        @param[in] ccore (bool): If specified than CCORE library (C++ pyclustering library) is used for clustering instead of Python code.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric', 'data_type', 'itermax').

        <b>Keyword Args:</b><br>
            - metric (distance_metric): Metric that is used for distance calculation between two points.
            - data_type (string): Data type of input sample 'data' that is processed by the algorithm ('points', 'distance_matrix').
            - itermax (uint): Maximum number of iteration for cluster analysis.

        """
        self.__pointer_data = data
        self.__clusters = []
        self.__labels = [-1] * len(data)
        self.__medoid_indexes = initial_index_medoids[:]
        self.__distance_first_medoid = [float('inf')] * len(data)
        self.__distance_second_medoid = [float('inf')] * len(data)
        self.__tolerance = tolerance

        self.__metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))
        self.__data_type = kwargs.get('data_type', 'points')
        self.__itermax = kwargs.get('itermax', 200)

        self.__distance_calculator = self.__create_distance_calculator()

        self.__ccore = ccore and self.__metric.get_type() != type_metric.USER_DEFINED
        if self.__ccore:
            self.__ccore = ccore_library.workable()

        self.__verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Medoids algorithm.

        @return (kmedoids) Returns itself (K-Medoids instance).

        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_medoids()
        
        """
        
        if self.__ccore is True:
            ccore_metric = metric_wrapper.create_instance(self.__metric)
            self.__clusters, self.__medoid_indexes = wrapper.kmedoids(self.__pointer_data, self.__medoid_indexes, self.__tolerance, self.__itermax, ccore_metric.get_pointer(), self.__data_type)
        
        else:
            changes = float('inf')
            previous_deviation, current_deviation = float('inf'), float('inf')

            iterations = 0

            if self.__itermax > 0:
                current_deviation = self.__update_clusters()

            while (changes > self.__tolerance) and (iterations < self.__itermax):
                swap_cost = self.__swap_medoids()

                if swap_cost != float('inf'):
                    previous_deviation = current_deviation
                    current_deviation = self.__update_clusters()
                    changes = previous_deviation - current_deviation
                else:
                    return self

                iterations += 1

        return self


    def predict(self, points):
        """!
        @brief Calculates the closest cluster to each point.

        @param[in] points (array_like): Points for which closest clusters are calculated.

        @return (list) List of closest clusters for each point. Each cluster is denoted by index. Return empty
                 collection if 'process()' method was not called.

        An example how to calculate (or predict) the closest cluster to specified points.
        @code
            from pyclustering.cluster.kmedoids import kmedoids
            from pyclustering.samples.definitions import SIMPLE_SAMPLES
            from pyclustering.utils import read_sample

            # Load list of points for cluster analysis.
            sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

            # Initial medoids for sample 'Simple3'.
            initial_medoids = [4, 12, 25, 37]

            # Create instance of K-Medoids algorithm with prepared centers.
            kmedoids_instance = kmedoids(sample, initial_medoids)

            # Run cluster analysis.
            kmedoids_instance.process()

            # Calculate the closest cluster to following two points.
            points = [[0.35, 0.5], [2.5, 2.0]]
            closest_clusters = kmedoids_instance.predict(points)
            print(closest_clusters)
        @endcode

        """

        if len(self.__clusters) == 0:
            return []

        medoids = [self.__pointer_data[index] for index in self.__medoid_indexes]
        differences = numpy.zeros((len(points), len(medoids)))
        for index_point in range(len(points)):
            differences[index_point] = [self.__metric(points[index_point], center) for center in medoids]

        return numpy.argmin(differences, axis=1)


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_medoids()
        
        """
        
        return self.__clusters
    
    
    def get_medoids(self):
        """!
        @brief Returns list of medoids of allocated clusters represented by indexes from the input data.
        
        @see process()
        @see get_clusters()
        
        """

        return self.__medoid_indexes


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__pointer_data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__pointer_data))

        if len(self.__medoid_indexes) == 0:
            raise ValueError("Initial medoids are empty (size: '%d')." % len(self.__pointer_data))

        if self.__tolerance < 0:
            raise ValueError("Tolerance (current value: '%d') should be greater or equal to 0." %
                             self.__tolerance)

        if self.__itermax < 0:
            raise ValueError("Maximum iterations (current value: '%d') should be greater or equal to 0." %
                             self.__tolerance)


    def __create_distance_calculator(self):
        """!
        @brief Creates distance calculator in line with algorithms parameters.

        @return (callable) Distance calculator.

        """
        if self.__data_type == 'points':
            return lambda index1, index2: self.__metric(self.__pointer_data[index1], self.__pointer_data[index2])

        elif self.__data_type == 'distance_matrix':
            if isinstance(self.__pointer_data, numpy.matrix):
                return lambda index1, index2: self.__pointer_data.item((index1, index2))

            return lambda index1, index2: self.__pointer_data[index1][index2]

        else:
            raise TypeError("Unknown type of data is specified '%s'" % self.__data_type)


    def __update_clusters(self):
        """!
        @brief Calculate distance to each point from the each cluster.
        @details Nearest points are captured by according clusters and as a result clusters are updated.

        @return (double) Total deviation (distance from each point to its closest medoid).

        """

        total_deviation = 0.0
        self.__clusters = [[] for i in range(len(self.__medoid_indexes))]
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1
            dist_optim_first = float('Inf')
            dist_optim_second = float('Inf')
            
            for index in range(len(self.__medoid_indexes)):
                dist = self.__distance_calculator(index_point, self.__medoid_indexes[index])
                
                if dist < dist_optim_first:
                    dist_optim_second = dist_optim_first
                    index_optim = index
                    dist_optim_first = dist
                elif dist < dist_optim_second:
                    dist_optim_second = dist

            total_deviation += dist_optim_first
            self.__clusters[index_optim].append(index_point)
            self.__labels[index_point] = index_optim

            self.__distance_first_medoid[index_point] = dist_optim_first
            self.__distance_second_medoid[index_point] = dist_optim_second

        return total_deviation


    def __swap_medoids(self):
        """!
        @brief Swap existed medoid with non-medoid points in order to find the most optimal medoid.

        @return (double) Cost that is needed to swap two medoids.

        """

        optimal_swap_cost = float('inf')
        optimal_index_cluster = None
        optimal_index_medoid = None

        for index_cluster in range(len(self.__clusters)):
            for candidate_medoid_index in range(len(self.__pointer_data)):
                if (candidate_medoid_index in self.__medoid_indexes) or (self.__distance_first_medoid[candidate_medoid_index] == 0.0):
                    continue

                swap_cost = self.__calculate_swap_cost(candidate_medoid_index, index_cluster)
                if swap_cost < optimal_swap_cost:
                    optimal_swap_cost = swap_cost
                    optimal_index_cluster = index_cluster
                    optimal_index_medoid = candidate_medoid_index

        if optimal_index_cluster is not None:
            self.__medoid_indexes[optimal_index_cluster] = optimal_index_medoid

        return optimal_swap_cost


    def __calculate_swap_cost(self, index_candidate, cluster_index):
        """!
        @brief Calculates cost to swap `index_candidate` with the current medoid `cluster_index`.

        @param[in] index_candidate (uint): Index point that is considered as a medoid candidate.
        @param[in] cluster_index (uint): Index of a cluster where the current medoid is used for calculation.

        @return (double) Cost that is needed to swap medoids.

        """
        cost = 0.0

        for index_point in range(len(self.__pointer_data)):
            if index_point == index_candidate:
                continue

            candidate_distance = self.__distance_calculator(index_point, index_candidate)
            if self.__labels[index_point] == cluster_index:
                cost += min(candidate_distance, self.__distance_second_medoid[index_point]) - self.__distance_first_medoid[index_point]
            elif candidate_distance < self.__distance_first_medoid[index_point]:
                cost += candidate_distance - self.__distance_first_medoid[index_point]

        return cost - self.__distance_first_medoid[index_candidate]
