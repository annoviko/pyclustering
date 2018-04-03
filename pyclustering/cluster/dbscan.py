"""!

@brief Cluster analysis algorithm: DBSCAN.
@details Implementation based on article:
         - M.Ester, H.Kriegel, J.Sander, X.Xiaowei. A density-based algorithm for discovering clusters in large spatial databases with noise. 1996.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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


from enum import Enum;

from pyclustering.container.kdtree import kdtree;

from pyclustering.cluster.encoder import type_encoding;

from pyclustering.core.wrapper import ccore_library;

from pyclustering.utils import get_argument;

import pyclustering.core.dbscan_wrapper as wrapper;



class dbscan_data_type(Enum):
    """!
    @brief Enumeration of DBSCAN input data types that is used for processing: points, adjacency matrix.

    """

    ## Input data is represented by points that are contained by array like container, for example, by list.
    POINTS = 0;

    ## Input data is represented by distance matrix between points.
    DISTANCE_MATRIX = 1;


class dbscan:
    """!
    @brief Class represents clustering algorithm DBSCAN.
    @details This DBSCAN algorithm is KD-tree optimized.
             
             CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
    Example:
    @code
        # sample for cluster analysis (represented by list)
        sample = read_sample(path_to_sample);
        
        # create object that uses CCORE for processing
        dbscan_instance = dbscan(sample, 0.5, 3, True);
        
        # cluster analysis
        dbscan_instance.process();
        
        # obtain results of clustering
        clusters = dbscan_instance.get_clusters();
        noise = dbscan_instance.get_noise();
    @endcode
    
    """
    
    def __init__(self, data, eps, neighbors, ccore = True, **kwargs):
        """!
        @brief Constructor of clustering algorithm DBSCAN.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] eps (double): Connectivity radius between points, points may be connected if distance between them less then the radius.
        @param[in] neighbors (uint): minimum number of shared neighbors that is required for establish links between points.
        @param[in] ccore (bool): if True than DLL CCORE (C++ solution) will be used for solving the problem.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'data_type').

        Keyword Args:
            data_type (dbscan_data_type): Data type of input sample 'data' that is processed by the algorithm (simple sequence of points or distance matrix).
        
        """
        
        self.__pointer_data = data;
        self.__kdtree = None;
        self.__eps = eps;
        self.__sqrt_eps = eps * eps;
        self.__neighbors = neighbors;
        
        self.__visited = [False] * len(self.__pointer_data);
        self.__belong = [False] * len(self.__pointer_data);

        self.__data_type = get_argument('data_type', dbscan_data_type.POINTS, **kwargs);

        self.__clusters = [];
        self.__noise = [];
        
        self.__ccore = ccore;
        if (self.__ccore):
            self.__ccore = ccore_library.workable();


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of DBSCAN algorithm.
        
        @see get_clusters()
        @see get_noise()
        
        """
        
        if self.__ccore is True:
            (self.__clusters, self.__noise) = wrapper.dbscan(self.__pointer_data, self.__eps, self.__neighbors, True);
            
        else:
            if self.__data_type == dbscan_data_type.POINTS:
                self.__kdtree = kdtree(self.__pointer_data, range(len(self.__pointer_data)));

            for i in range(0, len(self.__pointer_data)):
                if self.__visited[i] is False:
                     
                    cluster = self.__expand_cluster(i);
                    if cluster is not None:
                        self.__clusters.append(cluster);
                    else:
                        self.__noise.append(i);
                        self.__belong[i] = True;


    def get_clusters(self):
        """!
        @brief Returns allocated clusters.
        
        @remark Allocated clusters can be returned only after data processing (use method process()). Otherwise empty list is returned.
        
        @return (list) List of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_noise()
        
        """
        
        return self.__clusters;


    def get_noise(self):
        """!
        @brief Returns allocated noise.
        
        @remark Allocated noise can be returned only after data processing (use method process() before). Otherwise empty list is returned.
        
        @return (list) List of indexes that are marked as a noise.
        
        @see process()
        @see get_clusters()
        
        """

        return self.__noise;


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION;


    def __expand_cluster(self, index_point):
        """!
        @brief Expands cluster from specified point in the input data space.
        
        @param[in] index_point (list): Index of a point from the data.

        @return (list) Return tuple of list of indexes that belong to the same cluster and list of points that are marked as noise: (cluster, noise), or None if nothing has been expanded.
        
        """
        
        cluster = None;
        self.__visited[index_point] = True;
        neighbors = self.__neighbor_indexes(index_point);
         
        if len(neighbors) >= self.__neighbors:
            cluster = [ index_point ];
             
            self.__belong[index_point] = True;
             
            for i in neighbors:
                if self.__visited[i] is False:
                    self.__visited[i] = True;
                    next_neighbors = self.__neighbor_indexes(i);
                     
                    if len(next_neighbors) >= self.__neighbors:
                        # if some node has less then minimal number of neighbors than we shouldn't look at them
                        # because maybe it's a noise.
                        neighbors += [k for k in next_neighbors if ( (k in neighbors) == False)];
                 
                if self.__belong[i] is False:
                    cluster.append(i);
                    self.__belong[i] = True;
             
        return cluster;

    def __neighbor_indexes(self, index_point):
        """!
        @brief Return list of indexes of neighbors of specified point for the data.
        
        @param[in] index_point (list): An index of a point for which potential neighbors should be returned in line with connectivity radius.
        
        @return (list) Return list of indexes of neighbors in line the connectivity radius.
        
        """

        if self.__data_type == dbscan_data_type.POINTS:
            kdnodes = self.__kdtree.find_nearest_dist_nodes(self.__pointer_data[index_point], self.__eps);
            return [node_tuple[1].payload for node_tuple in kdnodes if node_tuple[1].payload != index_point];

        else:
            distances = self.__pointer_data[index_point];
            return [ index_neighbor for index_neighbor in range(len(distances))
                     if ( (distances[index_neighbor] <= self.__eps) and (index_neighbor != index_point) ) ];
