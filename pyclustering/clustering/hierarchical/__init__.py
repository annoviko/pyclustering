'''

Cluster analysis algorithm: Classical Hierarchical Algorithm

Based on article description:
 - K.Anil, J.C.Dubes, R.C.Dubes. Algorithms for Clustering Data. 1988.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from pyclustering.support import euclidean_distance_sqrt;
from pyclustering.support import read_sample;
from pyclustering.support import draw_clusters;

from pyclustering.support import timedcall;

import pyclustering.core.wrapper as wrapper;


class hierarchical:
    __pointer_data = None;
    __number_clusters = 0;
    
    __ccore = False;
    
    __clusters = None;
    __centers = None;
    
    def __init__(self, data, number_clusters, ccore):
        "Constructor of clustering algorithm hierarchical."
         
        "(in) data               - input data that is presented as list of points (objects), each point should be represented by list or tuple."
        "(in) number_clusters    - number of cluster that should be allocated."
        "(in) ccore              - if True than DLL CCORE (C++ solution) will be used for solving the problem."
         
        "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."        
        
        self.__pointer_data = data;
        self.__number_clusters = number_clusters;
        self.__ccore = None;
        
        self.__clusters = [];
        self.__centers = [];
        
    
    def process(self):
        if (self.__ccore is True):
            self.__clusters = wrapper.hierarchical(self.__pointer_data, self.__number_clusters); 
        else:        
            self.__centers = self.__pointer_data.copy();
            self.__clusters = [[index] for index in range(0, len(self.__pointer_data))];
            
            current_number_clusters = len(self.__clusters);
            
            while (current_number_clusters > self.__number_clusters):
                indexes = self.__find_nearest_clusters();
                 
                self.__clusters[indexes[0]] += self.__clusters[indexes[1]];
                self.__centers[indexes[0]] = self.__calculate_center(self.__clusters[indexes[0]]);
                 
                self.__clusters.pop(indexes[1]);   # remove merged cluster.
                self.__centers.pop(indexes[1]);    # remove merged center.
                
                current_number_clusters = len(self.__clusters);
        
        
    def get_clusters(self):
        "Performs cluster analysis in line with rules of heirarchical algorithm. Results of clustering can be obtained using corresponding gets methods."
        
        return self.__clusters;


    def __find_nearest_clusters(self):
        "Returns list with two indexes of two clusters whose distance is the smallest."       
        
        min_dist = 0;
        indexes = None;
        
        for index1 in range(0, len(self.__centers)):
            for index2 in range(index1 + 1, len(self.__centers)):
                distance = euclidean_distance_sqrt(self.__centers[index1], self.__centers[index2]);
                if ( (distance < min_dist) or (indexes == None) ):
                    min_dist = distance;
                    indexes = [index1, index2];
        
        return indexes; 
    
           
    def __calculate_center(self, cluster):
        "Returns new value of the center of the specified cluster."
         
        dimension = len(self.__pointer_data[cluster[0]]);
        center = [0] * dimension;
        for index_point in cluster:
            for index_dimension in range(0, dimension):
                center[index_dimension] += self.__pointer_data[index_point][index_dimension];
         
        for index_dimension in range(0, dimension):
            center[index_dimension] /= len(cluster);
             
        return center;
