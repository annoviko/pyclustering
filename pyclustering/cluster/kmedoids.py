"""!

@brief Cluster analysis algorithm: K-Medoids.
@details Implementation based on papers @cite book::algorithms_for_clustering_data, @cite book::finding_groups_in_data.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
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

from pyclustering.cluster.encoder import type_encoding

from pyclustering.utils import medoid
from pyclustering.utils.metric import distance_metric, type_metric

import pyclustering.core.kmedoids_wrapper as wrapper

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.metric_wrapper import metric_wrapper


class kmedoids:
    """!
    @brief Class represents clustering algorithm K-Medoids.
    @details The algorithm is less sensitive to outliers tham K-Means. The principle difference between K-Medoids and K-Medians is that
             K-Medoids uses existed points from input data space as medoids, but median in K-Medians can be unreal object (not from
             input data space).
    
    Clustering example:
    @code
        from pyclustering.cluster.kmedoids import kmedoids
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # Load list of points for cluster analysis.
        sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

        # Set random initial medoids.
        initial_medoids = [1, 500]

        # Create instance of K-Medoids algorithm.
        kmedoids_instance = kmedoids(sample, initial_medoids)

        # Run cluster analysis and obtain results.
        kmedoids_instance.process()
        clusters = kmedoids_instance.get_clusters()

        # Show allocated clusters.
        print(clusters)

        # Display clusters.
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    @endcode

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
    
    
    def __init__(self, data, initial_index_medoids, tolerance=0.001, ccore=True, **kwargs):
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
        self.__medoid_indexes = initial_index_medoids
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
            iterations = 0

            while changes > self.__tolerance and iterations < self.__itermax:
                self.__clusters = self.__update_clusters()
                update_medoid_indexes = self.__update_medoids()

                changes = max([self.__distance_calculator(self.__medoid_indexes[index], update_medoid_indexes[index]) for index in range(len(update_medoid_indexes))])

                self.__medoid_indexes = update_medoid_indexes

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

        medoids = [ self.__pointer_data[index] for index in self.__medoid_indexes ]
        differences = numpy.zeros((len(points), len(medoids)))
        for index_point in range(len(points)):
            differences[index_point] = [ self.__metric(points[index_point], center) for center in medoids ]

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
        
        @return (list) updated clusters as list of clusters where each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[self.__medoid_indexes[i]] for i in range(len(self.__medoid_indexes))]
        for index_point in range(len(self.__pointer_data)):
            if index_point in self.__medoid_indexes:
                continue

            index_optim = -1
            dist_optim = float('Inf')
            
            for index in range(len(self.__medoid_indexes)):
                dist = self.__distance_calculator(index_point, self.__medoid_indexes[index])
                
                if dist < dist_optim:
                    index_optim = index
                    dist_optim = dist
            
            clusters[index_optim].append(index_point)
        
        return clusters
    
    
    def __update_medoids(self):
        """!
        @brief Find medoids of clusters in line with contained objects.
        
        @return (list) list of medoids for current number of clusters.
        
        """

        medoid_indexes = [-1] * len(self.__clusters)
        
        for index in range(len(self.__clusters)):
            medoid_index = medoid(self.__pointer_data, self.__clusters[index], metric=self.__metric, data_type=self.__data_type)
            medoid_indexes[index] = medoid_index
             
        return medoid_indexes
