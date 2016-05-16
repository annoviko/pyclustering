"""!

@brief Cluster analysis algorithm: DBSCAN.
@details Implementation based on article:
         - M.Ester, H.Kriegel, J.Sander, X.Xiaowei. A density-based algorithm for discovering clusters in large spatial databases with noise. 1996.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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


from pyclustering.utils import euclidean_distance_sqrt;

import pyclustering.core.dbscan_wrapper as wrapper;

class dbscan:
    """!
    @brief Class represents clustering algorithm DBSCAN.
    
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
    
    def __init__(self, data, eps, neighbors, ccore = False):
        """!
        @brief Constructor of clustering algorithm DBSCAN.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] eps (double): Connectivity radius between points, points may be connected if distance between them less then the radius.
        @param[in] neighbors (uint): minimum number of shared neighbors that is required for establish links between points.
        @param[in] ccore (bool): if True than DLL CCORE (C++ solution) will be used for solving the problem.
        
        """
        self.__pointer_data = data;
        self.__eps = eps;
        self.__sqrt_eps = eps * eps;
        self.__neighbors = neighbors;
        
        self.__visited = [False] * len(self.__pointer_data);
        self.__belong = [False] * len(self.__pointer_data);
        
        self.__clusters = [];
        self.__noise = [];
        
        self.__ccore = ccore;

    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of DBSCAN algorithm.
        
        @see get_clusters()
        @see get_noise()
        
        """
        
        if (self.__ccore is True):
            (self.__clusters, self.__noise) = wrapper.dbscan(self.__pointer_data, self.__eps, self.__neighbors, True);
            
        else:
            for i in range(0, len(self.__pointer_data)):
                if (self.__visited[i] == False):
                     
                    cluster = self.__expand_cluster(i);    # Fast mode
                    if (cluster != None):
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


    def __expand_cluster(self, point):
        """!
        @brief Expands cluster from specified point in the input data space.
        
        @param[in] point (list): Index of a point from the data.

        @return (list) Return tuple of list of indexes that belong to the same cluster and list of points that are marked as noise: (cluster, noise), or None if nothing has been expanded.
        
        """
        
        cluster = None;
        self.__visited[point] = True;
        neighbors = self.__neighbor_indexes(point);
         
        if (len(neighbors) >=self.__neighbors):
             
            cluster = [];
            cluster.append(point);
             
            self.__belong[point] = True;
             
            for i in neighbors:
                if (self.__visited[i] == False):
                    self.__visited[i] = True;
                    next_neighbors = self.__neighbor_indexes(i);
                     
                    if (len(next_neighbors) >= self.__neighbors):
                        # if some node has less then minimal number of neighbors than we shouldn't look at them
                        # because maybe it's a noise.
                        neighbors += [k for k in next_neighbors if ( (k in neighbors) == False)];
                 
                if (self.__belong[i] == False):
                    cluster.append(i);
                    self.__belong[i] = True;
             
        return cluster;

    def __neighbor_indexes(self, point):
        """!
        @brief Return list of indexes of neighbors of specified point for the data.
        
        @param[in] point (list): An index of a point for which potential neighbors should be returned in line with connectivity radius.
        
        @return (list) Return list of indexes of neighbors in line the connectivity radius.
        
        """
        
        # return [i for i in range(0, len(data)) if euclidean_distance(data[point], data[i]) <= eps and data[i] != data[point]];    # Slow mode
        return [i for i in range(0, len(self.__pointer_data)) if euclidean_distance_sqrt(self.__pointer_data[point], self.__pointer_data[i]) <= self.__sqrt_eps and self.__pointer_data[i] != self.__pointer_data[point]]; # Fast mode
