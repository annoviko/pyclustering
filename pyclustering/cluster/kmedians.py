"""!

@brief Cluster analysis algorithm: K-Medians
@details Implementation based on paper @cite book::algorithms_for_clustering_data.

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


import math
import numpy

from pyclustering.cluster.encoder import type_encoding

from pyclustering.utils.metric import distance_metric, type_metric

import pyclustering.core.kmedians_wrapper as wrapper

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.metric_wrapper import metric_wrapper


class kmedians:
    """!
    @brief Class represents clustering algorithm K-Medians.
    @details The algorithm is less sensitive to outliers than K-Means. Medians are calculated instead of centroids.
    
    Example:
    @code
        from pyclustering.cluster.kmedians import kmedians
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # Load list of points for cluster analysis.
        sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

        # Create instance of K-Medians algorithm.
        initial_medians = [[0.0, 0.1], [2.5, 0.7]]
        kmedians_instance = kmedians(sample, initial_medians)

        # Run cluster analysis and obtain results.
        kmedians_instance.process()
        clusters = kmedians_instance.get_clusters()
        medians = kmedians_instance.get_medians()

        # Visualize clustering results.
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.append_cluster(initial_medians, marker='*', markersize=10)
        visualizer.append_cluster(medians, marker='*', markersize=10)
        visualizer.show()
    @endcode
    
    """
    
    def __init__(self, data, initial_medians, tolerance=0.001, ccore=True, **kwargs):
        """!
        @brief Constructor of clustering algorithm K-Medians.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] initial_medians (list): Initial coordinates of medians of clusters that are represented by list: [center1, center2, ...].
        @param[in] tolerance (double): Stop condition: if maximum value of change of centers of clusters is less than tolerance than algorithm will stop processing
        @param[in] ccore (bool): Defines should be CCORE library (C++ pyclustering library) used instead of Python code or not.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric', 'itermax').

        <b>Keyword Args:</b><br>
            - metric (distance_metric): Metric that is used for distance calculation between two points.
            - itermax (uint): Maximum number of iterations for cluster analysis.
        
        """
        self.__pointer_data = numpy.array(data)
        self.__clusters = []
        self.__medians = numpy.array(initial_medians)
        self.__tolerance = tolerance
        self.__total_wce = 0

        self.__itermax = kwargs.get('itermax', 100)
        self.__metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))
        if self.__metric is None:
            self.__metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)

        self.__ccore = ccore and self.__metric.get_type() != type_metric.USER_DEFINED
        if self.__ccore:
            self.__ccore = ccore_library.workable()

        self.__verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Medians algorithm.

        @return (kmedians) Returns itself (K-Medians instance).

        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_medians()
        
        """
        
        if self.__ccore is True:
            ccore_metric = metric_wrapper.create_instance(self.__metric)
            self.__clusters, self.__medians = wrapper.kmedians(self.__pointer_data, self.__medians, self.__tolerance, self.__itermax, ccore_metric.get_pointer())

        else:
            changes = float('inf')
             
            # Check for dimension
            if len(self.__pointer_data[0]) != len(self.__medians[0]):
                raise NameError('Dimension of the input data and dimension of the initial medians must be equal.')

            iterations = 0
            while changes > self.__tolerance and iterations < self.__itermax:
                self.__clusters = self.__update_clusters()
                updated_centers = self.__update_medians()
             
                changes = max([self.__metric(self.__medians[index], updated_centers[index]) for index in range(len(updated_centers))])
                 
                self.__medians = updated_centers

                iterations += 1

        self.__calculate_total_wce()

        return self


    def predict(self, points):
        """!
        @brief Calculates the closest cluster to each point.

        @param[in] points (array_like): Points for which closest clusters are calculated.

        @return (list) List of closest clusters for each point. Each cluster is denoted by index. Return empty
                 collection if 'process()' method was not called.

        An example how to calculate (or predict) the closest cluster to specified points.
        @code
            from pyclustering.cluster.kmedians import kmedians
            from pyclustering.samples.definitions import SIMPLE_SAMPLES
            from pyclustering.utils import read_sample

            # Load list of points for cluster analysis.
            sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

            # Initial centers for sample 'Simple3'.
            initial_medians = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]

            # Create instance of K-Medians algorithm with prepared centers.
            kmedians_instance = kmedians(sample, initial_medians)

            # Run cluster analysis.
            kmedians_instance.process()

            # Calculate the closest cluster to following two points.
            points = [[0.25, 0.2], [2.5, 4.0]]
            closest_clusters = kmedians_instance.predict(points)
            print(closest_clusters)
        @endcode

        """

        if len(self.__clusters) == 0:
            return []

        differences = numpy.zeros((len(points), len(self.__medians)))
        for index_point in range(len(points)):
            differences[index_point] = [ self.__metric(points[index_point], center) for center in self.__medians ]

        return numpy.argmin(differences, axis=1)


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_medians()
        
        """
        
        return self.__clusters
    
    
    def get_medians(self):
        """!
        @brief Returns list of centers of allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """

        if isinstance(self.__medians, list):
            return self.__medians

        return self.__medians.tolist()


    def get_total_wce(self):
        """!
        @brief Returns sum of metric errors that depends on metric that was used for clustering (by default SSE - Sum of Squared Errors).
        @details Sum of metric errors is calculated using distance between point and its center:
                 \f[error=\sum_{i=0}^{N}distance(x_{i}-center(x_{i}))\f]

        @see process()
        @see get_clusters()

        """

        return self.__total_wce


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def __update_clusters(self):
        """!
        @brief Calculate Manhattan distance to each point from the each cluster. 
        @details Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters where each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for i in range(len(self.__medians))]
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1
            dist_optim = 0.0
             
            for index in range(len(self.__medians)):
                dist = self.__metric(self.__pointer_data[index_point], self.__medians[index])
                 
                if (dist < dist_optim) or (index == 0):
                    index_optim = index
                    dist_optim = dist
             
            clusters[index_optim].append(index_point)
            
        # If cluster is not able to capture object it should be removed
        clusters = [cluster for cluster in clusters if len(cluster) > 0]
        
        return clusters
    

    def __calculate_total_wce(self):
        """!
        @brief Calculate total within cluster errors that is depend on metric that was chosen for K-Medians algorithm.

        """

        dataset_differences = self.__calculate_dataset_difference(len(self.__clusters))

        self.__total_wce = 0
        for index_cluster in range(len(self.__clusters)):
            for index_point in self.__clusters[index_cluster]:
                self.__total_wce += dataset_differences[index_cluster][index_point]


    def __calculate_dataset_difference(self, amount_clusters):
        """!
        @brief Calculate distance from each point to each cluster center.

        """
        self.__metric.enable_numpy_usage()
        dataset_differences = numpy.zeros((amount_clusters, len(self.__pointer_data)))
        for index_center in range(amount_clusters):
            if self.__metric.get_type() != type_metric.USER_DEFINED:
                dataset_differences[index_center] = self.__metric(self.__pointer_data, self.__medians[index_center])
            else:
                dataset_differences[index_center] = [self.__metric(point, self.__medians[index_center])
                                                      for point in self.__pointer_data]
        self.__metric.disable_numpy_usage()
        return dataset_differences


    def __update_medians(self):
        """!
        @brief Calculate medians of clusters in line with contained objects.
        
        @return (list) list of medians for current number of clusters.
        
        """
         
        medians = [[] for i in range(len(self.__clusters))]
         
        for index in range(len(self.__clusters)):
            medians[index] = [0.0 for i in range(len(self.__pointer_data[0]))]
            length_cluster = len(self.__clusters[index])
            
            for index_dimension in range(len(self.__pointer_data[0])):
                sorted_cluster = sorted(self.__clusters[index], key=lambda x: self.__pointer_data[x][index_dimension])
                
                relative_index_median = int(math.floor((length_cluster - 1) / 2))
                index_median = sorted_cluster[relative_index_median]
                
                if (length_cluster % 2) == 0:
                    index_median_second = sorted_cluster[relative_index_median + 1]
                    medians[index][index_dimension] = (self.__pointer_data[index_median][index_dimension] + self.__pointer_data[index_median_second][index_dimension]) / 2.0
                    
                else:
                    medians[index][index_dimension] = self.__pointer_data[index_median][index_dimension]
             
        return medians


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__pointer_data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__pointer_data))

        if len(self.__medians) == 0:
            raise ValueError("Initial medians are empty (size: '%d')." % len(self.__pointer_data))

        if self.__tolerance < 0:
            raise ValueError("Tolerance (current value: '%d') should be greater or equal to 0." %
                             self.__tolerance)

        if self.__itermax < 0:
            raise ValueError("Maximum iterations (current value: '%d') should be greater or equal to 0." %
                             self.__tolerance)
