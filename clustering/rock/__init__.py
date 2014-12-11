'''

Cluster analysis algorithm: ROCK

Based on article description:
 - S.Guha, R.Rastogi, K.Shim. ROCK: A Robust Clustering Algorithm for Categorical Attributes. 1999.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from support import euclidean_distance;
from support import read_sample;

import core;


class rock:
    __pointer_data = None;
    __clusters = None;
    
    __number_clusters = 0;
    __threshold = 0;
    __eps = 0;
    
    __degree_normalization = 0;
    __adjacency_matrix = None;
    
    __clusters = None;
    
    __ccore = False;
    
    def __init__(self, data, eps, number_clusters, threshold = 0.5, ccore = False):
        "Constructor of clustering algorithm ROCK."
        
        "(in) data                - input data - list of points where each point is represented by list of coordinates."
        "(in) eps                 - connectivity radius (similarity threshold), points are neighbors if distance between them is less than connectivity radius."
        "(in) number_clusters     - defines number of clusters that should be allocated from the input data set."
        "(in) threshold           - value that defines degree of normalization that influences on choice of clusters for merging during processing."
        "(in) ccore               - defines should be CCORE C++ library used instead of Python code or not."
        
        self.__pointer_data = data;
        self.__eps = eps;
        self.__number_clusters = number_clusters;
        self.__threshold = threshold;
        
        self.__clusters = None;
        
        self.__ccore = ccore;
        
        self.__degree_normalization = 1.0 + 2.0 * ( (1.0 - threshold) / (1.0 + threshold) );
        self.__create_adjacency_matrix();
        
        
    def process(self):
        "Performs cluster analysis in line with rules of ROCK algorithm. Results of clustering can be obtained using corresponding gets methods."
        
        # TODO: (Not related to specification, just idea) First iteration should be investigated. Euclidean distance should be used for clustering between two 
        # points and rock algorithm between clusters because we consider non-categorical samples. But it is required more investigations.
        
        if (self.__ccore is True):
            self.__clusters = core.rock(self.__pointer_data, self.__eps, self.__number_clusters, self.__threshold);
        
        else:  
            self.__clusters = [[index] for index in range(len(self.__pointer_data))];
            
            while (len(self.__clusters) > self.__number_clusters):
                indexes = self.__find_pair_clusters(self.__clusters);
                
                if (indexes != [-1, -1]):
                    self.__clusters[indexes[0]] += self.__clusters[indexes[1]];
                    self.__clusters.pop(indexes[1]);   # remove merged cluster.
                else:
                    break;  # totally separated clusters have been allocated
    
    
    def get_clusters(self):
        "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
        
        return self.__clusters;


    def __find_pair_clusters(self, clusters):
        "Returns pair of clusters that are best candidates for merging in line with goodness measure."
        "The pair of clusters for which the above goodness measure is maximum is the best pair of clusters to be merged."
        
        "(in) clusters                 - list of cluster that have been allocated during processing, each cluster is represented by list of indexes of points from the input data set."

        "Returns list that contains two indexes of clusters (from list 'clusters') that should be merged on this step. It can be equals to [-1, -1] when number of links between"
        "all clusters doesn't exist."
        
        maximum_goodness = 0.0;
        cluster_indexes = [-1, -1];
        
        for i in range(0, len(clusters)):
            for j in range(i + 1, len(clusters)):
                goodness = self.__calculate_goodness(clusters[i], clusters[j]);
                if (goodness > maximum_goodness):
                    maximum_goodness = goodness;
                    cluster_indexes = [i, j];
        
        return cluster_indexes;


    def __calculate_links(self, cluster1, cluster2):
        "Returns number of link between two clusters. Link between objects (points) exists only if distance between them less than connectivity radius."
        
        "(in) cluster1                - cluster that is represented by list contains indexes of objects (points) from input data set."
        "(in) cluster2                - cluster that is represented by list contains indexes of objects (points) from input data set."
        
        "Returns number of links between two clusters."
        
        number_links = 0;
        
        for index1 in cluster1:
            for index2 in cluster2:
                number_links += self.__adjacency_matrix[index1][index2];
                
        return number_links;
            

    def __create_adjacency_matrix(self):
        "Returns 2D matrix (list of lists) where each element described existence of link between points (marks them as neighbors)."
    
        "Returns adjacency matrix for the input data set in line with connectivity radius."
        
        size_data = len(self.__pointer_data);
        
        self.__adjacency_matrix = [ [ 0 for i in range(size_data) ] for j in range(size_data) ];
        for i in range(0, size_data):
            for j in range(i + 1, size_data):
                distance = euclidean_distance(self.__pointer_data[i], self.__pointer_data[j]);
                if (distance <= self.__eps):
                    self.__adjacency_matrix[i][j] = 1;
                    self.__adjacency_matrix[j][i] = 1;
        
    

    def __calculate_goodness(self, cluster1, cluster2):
        "Calculates coefficient 'goodness measurement' between two clusters. The coefficient defines level of suitability of clusters for merging."
        
        "(in) cluster1                - cluster that is represented by list contains indexes of objects (points) from input data set."
        "(in) cluster2                - cluster that is represented by list contains indexes of objects (points) from input data set."
        
        "Returns goodness measure between two clusters."
        
        number_links = self.__calculate_links(cluster1, cluster2);
        devider = (len(cluster1) + len(cluster2)) ** self.__degree_normalization - len(cluster1) ** self.__degree_normalization - len(cluster2) ** self.__degree_normalization;
        
        return (number_links / devider);
