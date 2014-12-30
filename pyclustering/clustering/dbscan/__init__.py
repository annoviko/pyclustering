'''

Cluster analysis algorithm: DBSCAN

Based on article description:
 - M.Ester, H.Kriegel, J.Sander, X.Xiaowei. A density-based algorithm for discovering clusters in large spatial databases with noise. 1996.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from pyclustering.support import euclidean_distance, euclidean_distance_sqrt;
from pyclustering.support import read_sample;

import pyclustering.core.wrapper as wrapper;

class dbscan:
    __pointer_data = None;
    __eps = 0;
    __sqrt_eps = 0;
    __neighbors = 0;
    
    __clusters = None;
    __noise = None;
    
    __visited = None;
    __belong = None;
    
    __ccore = False;
    
    
    def __init__(self, data, eps, neighbors, ccore):
        "Constructor of clustering algorithm DBSCAN."
         
        "(in) data            - input data that is presented as list of points (objects), each point should be represented by list or tuple."
        "(in) eps             - connectivity radius between points, points may be connected if distance between them less then the radius."
        "(in) neighbors       - minimum number of shared neighbors that is required for establish links between points."
        "(in) ccore           - if True than DLL CCORE (C++ solution) will be used for solving the problem."
    
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
        "Performs cluster analysis in line with rules of DBSCAN algorithm. Results of clustering can be obtained using corresponding gets methods."
        
        if (self.__ccore is True):
            result = wrapper.dbscan(self.__pointer_data, self.__eps, self.__neighbors, True);
            self.__clusters = result[0];
            self.__noise = result[1];
            
            del result;
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
        "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
        
        return self.__clusters;
    
    
    def get_noise(self):
        "Returns list of index that are marked as a noise."

        return self.__noise;


    def __expand_cluster(self, point):
        "Expands cluster from specified point in the input data space."
         
        "(in) point         - index of the point from the data."

        "Return tuple of list of indexes that belong to the same cluster and list of points that are marked as noise: (cluster, noise), or None if nothing has been expanded."
        
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
        "Return list of indexes of neighbors of specified point for the data."
         
        "(in) point       - index of point for which potential neighbors should be returned for the data in line with connectivity radius."
         
        "Return list of indexes of neighbors in line the connectivity radius."
        # return [i for i in range(0, len(data)) if euclidean_distance(data[point], data[i]) <= eps and data[i] != data[point]];    # Slow mode
        return [i for i in range(0, len(self.__pointer_data)) if euclidean_distance_sqrt(self.__pointer_data[point], self.__pointer_data[i]) <= self.__sqrt_eps and self.__pointer_data[i] != self.__pointer_data[point]]; # Fast mode
