"""!

@brief Cluster analysis algorithm: DBSCAN.
@details Implementation based on paper @cite inproceedings::dbscan::1.

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


from pyclustering.container.kdtree import kdtree

from pyclustering.cluster.encoder import type_encoding

from pyclustering.core.wrapper import ccore_library

import pyclustering.core.dbscan_wrapper as wrapper


class dbscan:
    """!
    @brief Class represents clustering algorithm DBSCAN.
    @details This DBSCAN algorithm is KD-tree optimized.
             
             CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
    Example:
    @code
        from pyclustering.cluster.dbscan import dbscan
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # Sample for cluster analysis.
        sample = read_sample(FCPS_SAMPLES.SAMPLE_CHAINLINK)

        # Create DBSCAN algorithm.
        dbscan_instance = dbscan(sample, 0.7, 3)

        # Start processing by DBSCAN.
        dbscan_instance.process()

        # Obtain results of clustering.
        clusters = dbscan_instance.get_clusters()
        noise = dbscan_instance.get_noise()

        # Visualize clustering results
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.append_cluster(noise, sample, marker='x')
        visualizer.show()
    @endcode
    
    """
    
    def __init__(self, data, eps, neighbors, ccore=True, **kwargs):
        """!
        @brief Constructor of clustering algorithm DBSCAN.
        
        @param[in] data (list): Input data that is presented as list of points or distance matrix (defined by parameter
                   'data_type', by default data is considered as a list of points).
        @param[in] eps (double): Connectivity radius between points, points may be connected if distance between them less then the radius.
        @param[in] neighbors (uint): minimum number of shared neighbors that is required for establish links between points.
        @param[in] ccore (bool): if True than DLL CCORE (C++ solution) will be used for solving the problem.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'data_type').

        <b>Keyword Args:</b><br>
            - data_type (string): Data type of input sample 'data' that is processed by the algorithm ('points', 'distance_matrix').
        
        """
        
        self.__pointer_data = data
        self.__kdtree = None
        self.__eps = eps
        self.__sqrt_eps = eps * eps
        self.__neighbors = neighbors

        self.__visited = [False] * len(self.__pointer_data)
        self.__belong = [False] * len(self.__pointer_data)

        self.__data_type = kwargs.get('data_type', 'points')

        self.__clusters = []
        self.__noise = []

        self.__neighbor_searcher = self.__create_neighbor_searcher(self.__data_type)

        self.__ccore = ccore
        if self.__ccore:
            self.__ccore = ccore_library.workable()

        self.__verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of DBSCAN algorithm.

        @return (dbscan) Returns itself (DBSCAN instance).

        @see get_clusters()
        @see get_noise()
        
        """
        
        if self.__ccore is True:
            (self.__clusters, self.__noise) = wrapper.dbscan(self.__pointer_data, self.__eps, self.__neighbors, self.__data_type)
            
        else:
            if self.__data_type == 'points':
                self.__kdtree = kdtree(self.__pointer_data, range(len(self.__pointer_data)))

            for i in range(0, len(self.__pointer_data)):
                if self.__visited[i] is False:
                    cluster = self.__expand_cluster(i)
                    if cluster is not None:
                        self.__clusters.append(cluster)

            for i in range(0, len(self.__pointer_data)):
                if self.__belong[i] is False:
                    self.__noise.append(i)

        return self


    def get_clusters(self):
        """!
        @brief Returns allocated clusters.
        
        @remark Allocated clusters can be returned only after data processing (use method process()). Otherwise empty list is returned.
        
        @return (list) List of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_noise()
        
        """
        
        return self.__clusters


    def get_noise(self):
        """!
        @brief Returns allocated noise.
        
        @remark Allocated noise can be returned only after data processing (use method process() before). Otherwise empty list is returned.
        
        @return (list) List of indexes that are marked as a noise.
        
        @see process()
        @see get_clusters()
        
        """

        return self.__noise


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

        if self.__eps < 0:
            raise ValueError("Connectivity radius (current value: '%d') should be greater or equal to 0." % self.__eps)


    def __create_neighbor_searcher(self, data_type):
        """!
        @brief Returns neighbor searcher in line with data type.

        @param[in] data_type (string): Data type (points or distance matrix).

        """
        if data_type == 'points':
            return self.__neighbor_indexes_points
        elif data_type == 'distance_matrix':
            return self.__neighbor_indexes_distance_matrix
        else:
            raise TypeError("Unknown type of data is specified '%s'" % data_type)


    def __expand_cluster(self, index_point):
        """!
        @brief Expands cluster from specified point in the input data space.
        
        @param[in] index_point (list): Index of a point from the data.

        @return (list) Return tuple of list of indexes that belong to the same cluster and list of points that are marked as noise: (cluster, noise), or None if nothing has been expanded.
        
        """
        
        cluster = None
        self.__visited[index_point] = True
        neighbors = self.__neighbor_searcher(index_point)
         
        if len(neighbors) >= self.__neighbors:
            cluster = [index_point]
             
            self.__belong[index_point] = True
             
            for i in neighbors:
                if self.__visited[i] is False:
                    self.__visited[i] = True

                    next_neighbors = self.__neighbor_searcher(i)
                     
                    if len(next_neighbors) >= self.__neighbors:
                        neighbors += [k for k in next_neighbors if ( (k in neighbors) == False) and k != index_point]
                 
                if self.__belong[i] is False:
                    cluster.append(i)
                    self.__belong[i] = True

        return cluster


    def __neighbor_indexes_points(self, index_point):
        """!
        @brief Return neighbors of the specified object in case of sequence of points.

        @param[in] index_point (uint): Index point whose neighbors are should be found.

        @return (list) List of indexes of neighbors in line the connectivity radius.

        """
        kdnodes = self.__kdtree.find_nearest_dist_nodes(self.__pointer_data[index_point], self.__eps)
        return [node_tuple[1].payload for node_tuple in kdnodes if node_tuple[1].payload != index_point]


    def __neighbor_indexes_distance_matrix(self, index_point):
        """!
        @brief Return neighbors of the specified object in case of distance matrix.

        @param[in] index_point (uint): Index point whose neighbors are should be found.

        @return (list) List of indexes of neighbors in line the connectivity radius.

        """
        distances = self.__pointer_data[index_point]
        return [index_neighbor for index_neighbor in range(len(distances))
                if ((distances[index_neighbor] <= self.__eps) and (index_neighbor != index_point))]