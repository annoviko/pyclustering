"""!

@brief Cluster analysis algorithm: ROCK
@details Implementation based on paper @cite inproceedings::rock::1.

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


from pyclustering.cluster.encoder import type_encoding

from pyclustering.utils import euclidean_distance

from pyclustering.core.wrapper import ccore_library

import pyclustering.core.rock_wrapper as wrapper


class rock:
    """!
    @brief Class represents clustering algorithm ROCK.

    Example:
    @code
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.cluster.rock import rock
        from pyclustering.samples.definitions import FCPS_SAMPLES
        from pyclustering.utils import read_sample

        # Read sample for clustering from file.
        sample = read_sample(FCPS_SAMPLES.SAMPLE_HEPTA)

        # Create instance of ROCK algorithm for cluster analysis. Seven clusters should be allocated.
        rock_instance = rock(sample, 1.0, 7)

        # Run cluster analysis.
        rock_instance.process()

        # Obtain results of clustering.
        clusters = rock_instance.get_clusters()

        # Visualize clustering results.
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    @endcode
       
    """
    
    def __init__(self, data, eps, number_clusters, threshold=0.5, ccore=True):
        """!
        @brief Constructor of clustering algorithm ROCK.
        
        @param[in] data (list): Input data - list of points where each point is represented by list of coordinates.
        @param[in] eps (double): Connectivity radius (similarity threshold), points are neighbors if distance between them is less than connectivity radius.
        @param[in] number_clusters (uint): Defines number of clusters that should be allocated from the input data set.
        @param[in] threshold (double): Value that defines degree of normalization that influences on choice of clusters for merging during processing.
        @param[in] ccore (bool): Defines should be CCORE (C++ pyclustering library) used instead of Python code or not.
        
        """
        
        self.__pointer_data = data
        self.__eps = eps
        self.__number_clusters = number_clusters
        self.__threshold = threshold
        
        self.__clusters = None
        
        self.__ccore = ccore
        if self.__ccore:
            self.__ccore = ccore_library.workable()

        self.__verify_arguments()

        self.__degree_normalization = 1.0 + 2.0 * ((1.0 - threshold) / (1.0 + threshold))

        self.__adjacency_matrix = None
        self.__create_adjacency_matrix()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of ROCK algorithm.

        @return (rock) Returns itself (ROCK instance).
        
        @see get_clusters()
        
        """
        
        # TODO: (Not related to specification, just idea) First iteration should be investigated. Euclidean distance should be used for clustering between two 
        # points and rock algorithm between clusters because we consider non-categorical samples. But it is required more investigations.
        
        if self.__ccore is True:
            self.__clusters = wrapper.rock(self.__pointer_data, self.__eps, self.__number_clusters, self.__threshold)
        
        else:  
            self.__clusters = [[index] for index in range(len(self.__pointer_data))]
            
            while len(self.__clusters) > self.__number_clusters:
                indexes = self.__find_pair_clusters(self.__clusters)
                
                if indexes != [-1, -1]:
                    self.__clusters[indexes[0]] += self.__clusters[indexes[1]]
                    self.__clusters.pop(indexes[1])   # remove merged cluster.
                else:
                    break  # totally separated clusters have been allocated
        return self

    
    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
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


    def __find_pair_clusters(self, clusters):
        """!
        @brief Returns pair of clusters that are best candidates for merging in line with goodness measure.
               The pair of clusters for which the above goodness measure is maximum is the best pair of clusters to be merged.
               
        @param[in] clusters (list): List of clusters that have been allocated during processing, each cluster is represented by list of indexes of points from the input data set.
        
        @return (list) List that contains two indexes of clusters (from list 'clusters') that should be merged on this step.
                It can be equals to [-1, -1] when no links between clusters.
        
        """
        
        maximum_goodness = 0.0
        cluster_indexes = [-1, -1]
        
        for i in range(0, len(clusters)):
            for j in range(i + 1, len(clusters)):
                goodness = self.__calculate_goodness(clusters[i], clusters[j])
                if goodness > maximum_goodness:
                    maximum_goodness = goodness
                    cluster_indexes = [i, j]
        
        return cluster_indexes


    def __calculate_links(self, cluster1, cluster2):
        """!
        @brief Returns number of link between two clusters. 
        @details Link between objects (points) exists only if distance between them less than connectivity radius.
        
        @param[in] cluster1 (list): The first cluster.
        @param[in] cluster2 (list): The second cluster.
        
        @return (uint) Number of links between two clusters.
        
        """
        
        number_links = 0
        
        for index1 in cluster1:
            for index2 in cluster2:
                number_links += self.__adjacency_matrix[index1][index2]
                
        return number_links
            

    def __create_adjacency_matrix(self):
        """!
        @brief Creates 2D adjacency matrix (list of lists) where each element described existence of link between points (means that points are neighbors).
        
        """
        
        size_data = len(self.__pointer_data)
        
        self.__adjacency_matrix = [[0 for i in range(size_data)] for j in range(size_data)]
        for i in range(0, size_data):
            for j in range(i + 1, size_data):
                distance = euclidean_distance(self.__pointer_data[i], self.__pointer_data[j])
                if (distance <= self.__eps):
                    self.__adjacency_matrix[i][j] = 1
                    self.__adjacency_matrix[j][i] = 1
        
    

    def __calculate_goodness(self, cluster1, cluster2):
        """!
        @brief Calculates coefficient 'goodness measurement' between two clusters. The coefficient defines level of suitability of clusters for merging.
        
        @param[in] cluster1 (list): The first cluster.
        @param[in] cluster2 (list): The second cluster.
        
        @return Goodness measure between two clusters.
        
        """
        
        number_links = self.__calculate_links(cluster1, cluster2)
        devider = (len(cluster1) + len(cluster2)) ** self.__degree_normalization - len(cluster1) ** self.__degree_normalization - len(cluster2) ** self.__degree_normalization
        
        return number_links / devider


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__pointer_data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__pointer_data))

        if self.__eps < 0:
            raise ValueError("Connectivity radius (current value: '%d') should be greater or equal to 0." % self.__eps)

        if self.__threshold < 0 or self.__threshold > 1:
            raise ValueError("Threshold (current value: '%d') should be in range (0, 1)." % self.__threshold)

        if (self.__number_clusters is not None) and (self.__number_clusters <= 0):
            raise ValueError("Amount of clusters (current value: '%d') should be greater than 0." %
                             self.__number_clusters)
