"""!

@brief Cluster analysis algorithm: agglomerative algorithm.
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


from enum import IntEnum;

from pyclustering.cluster.encoder import type_encoding;

from pyclustering.utils import euclidean_distance_square;

from pyclustering.core.wrapper import ccore_library

import pyclustering.core.agglomerative_wrapper as wrapper;


class type_link(IntEnum):
    """!
    @brief Enumerator of types of link between clusters.
    
    """

    ## Distance between the two nearest objects in clusters is considered as a link, so-called SLINK method (the single-link clustering method).
    SINGLE_LINK = 0
    
    ## Distance between the farthest objects in clusters is considered as a link, so-called CLINK method (the complete-link clustering method).
    COMPLETE_LINK = 1
    
    ## Average distance between objects in clusters is considered as a link.
    AVERAGE_LINK = 2
    
    ## Distance between centers of clusters is considered as a link.
    CENTROID_LINK = 3


class agglomerative:
    """!
    @brief Class represents agglomerative algorithm for cluster analysis.
    @details Agglomerative algorithm considers each data point (object) as a separate cluster at the beggining and
              step by step finds the best pair of clusters for merge until required amount of clusters is obtained.
    
    Example of agglomerative algorithm where centroid link is used:
    @code
        from pyclustering.cluster.agglomerative import agglomerative, type_link
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.samples.definitions import FCPS_SAMPLES
        from pyclustering.utils import read_sample

        # Sample for cluster analysis (represented by list)
        sample = read_sample(FCPS_SAMPLES.SAMPLE_TARGET)

        # Create object that uses python code only
        agglomerative_instance = agglomerative(sample, 6, type_link.SINGLE_LINK, ccore=True)

        # Cluster analysis
        agglomerative_instance.process()

        # Obtain results of clustering
        clusters = agglomerative_instance.get_clusters()

        # Visualize clustering results
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    @endcode
    
    There is example of clustering 'LSUN' sample:
    @code
        from pyclustering.cluster.agglomerative import agglomerative, type_link
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.samples.definitions import FCPS_SAMPLES
        from pyclustering.utils import read_sample

        # sample Lsun for cluster analysis
        lsun_sample = read_sample(FCPS_SAMPLES.SAMPLE_LSUN)

        # create instance of the algorithm that will use ccore library (the last argument)
        agglomerative_instance = agglomerative(lsun_sample, 3, type_link.SINGLE_LINK, True)

        # start processing
        agglomerative_instance.process()

        # get result and visualize it
        lsun_clusters = agglomerative_instance.get_clusters()
        visualizer = cluster_visualizer()
        visualizer.append_clusters(lsun_clusters, lsun_sample)
        visualizer.show()
    @endcode
    
    Example of agglomerative clustering using different links:
    @image html agglomerative_lsun_clustering_single_link.png
    
    """
    
    def __init__(self, data, number_clusters, link = None, ccore = True):
        """!
        @brief Constructor of agglomerative hierarchical algorithm.
        
        @param[in] data (list): Input data that is presented as a list of points (objects), each point should be represented by list, for example
                    [[0.1, 0.2], [0.4, 0.5], [1.3, 0.9]].
        @param[in] number_clusters (uint): Number of clusters that should be allocated.
        @param[in] link (type_link): Link type that is used for calculation similarity between objects and clusters, if it is not specified centroid link will be used by default.
        @param[in] ccore (bool): Defines should be CCORE (C++ pyclustering library) used instead of Python code or not (by default it is 'False').
        
        """  
        
        self.__pointer_data = data
        self.__number_clusters = number_clusters
        self.__similarity = link

        self.__verify_arguments()

        if self.__similarity is None:
            self.__similarity = type_link.CENTROID_LINK
        
        self.__clusters = []
        self.__ccore = ccore
        if self.__ccore:
            self.__ccore = ccore_library.workable()

        if self.__similarity == type_link.CENTROID_LINK:
            self.__centers = self.__pointer_data.copy()    # used in case of usage of centroid links

    
    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of agglomerative algorithm and similarity.

        @return (agglomerative) Returns itself (Agglomerative instance).

        @see get_clusters()
        
        """
        
        if self.__ccore is True:
            self.__clusters = wrapper.agglomerative_algorithm(self.__pointer_data, self.__number_clusters, self.__similarity)

        else:
            self.__clusters = [[index] for index in range(0, len(self.__pointer_data))]
            
            current_number_clusters = len(self.__clusters)
                
            while current_number_clusters > self.__number_clusters:
                self.__merge_similar_clusters()
                current_number_clusters = len(self.__clusters)

        return self

    
    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @remark Results of clustering can be obtained using corresponding gets methods.
        
        @return (list) List of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        
        """
        
        return self.__clusters
    
    
    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def __merge_similar_clusters(self):
        """!
        @brief Merges the most similar clusters in line with link type.
        
        """
        
        if self.__similarity == type_link.AVERAGE_LINK:
            self.__merge_by_average_link()
        
        elif self.__similarity == type_link.CENTROID_LINK:
            self.__merge_by_centroid_link()
        
        elif self.__similarity == type_link.COMPLETE_LINK:
            self.__merge_by_complete_link()
        
        elif self.__similarity == type_link.SINGLE_LINK:
            self.__merge_by_signle_link()
        
        else:
            raise NameError('Not supported similarity is used')
    
    
    def __merge_by_average_link(self):
        """!
        @brief Merges the most similar clusters in line with average link type.
        
        """
        
        minimum_average_distance = float('Inf')
        
        for index_cluster1 in range(0, len(self.__clusters)):
            for index_cluster2 in range(index_cluster1 + 1, len(self.__clusters)):
                
                # Find farthest objects
                candidate_average_distance = 0.0
                for index_object1 in self.__clusters[index_cluster1]:
                    for index_object2 in self.__clusters[index_cluster2]:
                        candidate_average_distance += euclidean_distance_square(self.__pointer_data[index_object1], self.__pointer_data[index_object2])
                
                candidate_average_distance /= (len(self.__clusters[index_cluster1]) + len(self.__clusters[index_cluster2]))
                
                if candidate_average_distance < minimum_average_distance:
                    minimum_average_distance = candidate_average_distance
                    indexes = [index_cluster1, index_cluster2]
        
        self.__clusters[indexes[0]] += self.__clusters[indexes[1]]
        self.__clusters.pop(indexes[1])   # remove merged cluster.
        
    
    def __merge_by_centroid_link(self):
        """!
        @brief Merges the most similar clusters in line with centroid link type.
        
        """
        
        minimum_centroid_distance = float('Inf')
        indexes = None
        
        for index1 in range(0, len(self.__centers)):
            for index2 in range(index1 + 1, len(self.__centers)):
                distance = euclidean_distance_square(self.__centers[index1], self.__centers[index2])
                if distance < minimum_centroid_distance:
                    minimum_centroid_distance = distance
                    indexes = [index1, index2]
        
        self.__clusters[indexes[0]] += self.__clusters[indexes[1]]
        self.__centers[indexes[0]] = self.__calculate_center(self.__clusters[indexes[0]])
         
        self.__clusters.pop(indexes[1])   # remove merged cluster.
        self.__centers.pop(indexes[1])    # remove merged center.
    
    
    def __merge_by_complete_link(self):
        """!
        @brief Merges the most similar clusters in line with complete link type.
        
        """
        
        minimum_complete_distance = float('Inf')
        indexes = None
        
        for index_cluster1 in range(0, len(self.__clusters)):
            for index_cluster2 in range(index_cluster1 + 1, len(self.__clusters)):
                candidate_maximum_distance = self.__calculate_farthest_distance(index_cluster1, index_cluster2)
                
                if candidate_maximum_distance < minimum_complete_distance:
                    minimum_complete_distance = candidate_maximum_distance
                    indexes = [index_cluster1, index_cluster2]

        self.__clusters[indexes[0]] += self.__clusters[indexes[1]]
        self.__clusters.pop(indexes[1])   # remove merged cluster.
    
    
    def __calculate_farthest_distance(self, index_cluster1, index_cluster2):
        """!
        @brief Finds two farthest objects in two specified clusters in terms and returns distance between them.
        
        @param[in] (uint) Index of the first cluster.
        @param[in] (uint) Index of the second cluster.
        
        @return The farthest euclidean distance between two clusters.
        
        """
        candidate_maximum_distance = 0.0
        for index_object1 in self.__clusters[index_cluster1]:
            for index_object2 in self.__clusters[index_cluster2]:
                distance = euclidean_distance_square(self.__pointer_data[index_object1], self.__pointer_data[index_object2])
                
                if distance > candidate_maximum_distance:
                    candidate_maximum_distance = distance
    
        return candidate_maximum_distance
    
    
    def __merge_by_signle_link(self):
        """!
        @brief Merges the most similar clusters in line with single link type.
        
        """
        
        minimum_single_distance = float('Inf')
        indexes = None
        
        for index_cluster1 in range(0, len(self.__clusters)):
            for index_cluster2 in range(index_cluster1 + 1, len(self.__clusters)):
                candidate_minimum_distance = self.__calculate_nearest_distance(index_cluster1, index_cluster2)
                
                if candidate_minimum_distance < minimum_single_distance:
                    minimum_single_distance = candidate_minimum_distance
                    indexes = [index_cluster1, index_cluster2]

        self.__clusters[indexes[0]] += self.__clusters[indexes[1]]
        self.__clusters.pop(indexes[1])   # remove merged cluster.
    
    
    def __calculate_nearest_distance(self, index_cluster1, index_cluster2):
        """!
        @brief Finds two nearest objects in two specified clusters and returns distance between them.
        
        @param[in] (uint) Index of the first cluster.
        @param[in] (uint) Index of the second cluster.
        
        @return The nearest euclidean distance between two clusters.
        
        """
        candidate_minimum_distance = float('Inf')
        
        for index_object1 in self.__clusters[index_cluster1]:
            for index_object2 in self.__clusters[index_cluster2]:
                distance = euclidean_distance_square(self.__pointer_data[index_object1], self.__pointer_data[index_object2])
                if distance < candidate_minimum_distance:
                    candidate_minimum_distance = distance
        
        return candidate_minimum_distance
    
    
    def __calculate_center(self, cluster):
        """!
        @brief Calculates new center.
        
        @return (list) New value of the center of the specified cluster.
        
        """
         
        dimension = len(self.__pointer_data[cluster[0]])
        center = [0] * dimension
        for index_point in cluster:
            for index_dimension in range(0, dimension):
                center[index_dimension] += self.__pointer_data[index_point][index_dimension]
         
        for index_dimension in range(0, dimension):
            center[index_dimension] /= len(cluster)
             
        return center


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__pointer_data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__pointer_data))

        if self.__number_clusters <= 0:
            raise ValueError("Amount of cluster (current value: '%d') for allocation should be greater than 0." %
                             self.__number_clusters)
