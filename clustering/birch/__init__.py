'''

Cluster analysis algorithm: BIRCH

Based on article description:
 - T.Zhang, R.Ramakrishnan, M.Livny. BIRCH: An Efficient Data Clustering Method for Very Large Databases. 1996.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from support import euclidean_distance_sqrt;

class birch:
    __pointer_data = None;
    
    def __init__(self, data):
        self.__pointer_data = data;
        
    def process(self):
        pass;
    
    def get_clusters(self):
        pass;
    
    def __get_centroid(self, cluster):
        "Calculates centroid of the specified cluster."
        
        "(in) cluster    - list of indexes that belong to cluster."
        
        "Returns centroid of the cluster as a list."
        
        dimension = len(cluster[0]);
        centroid = [0] * dimension;
        
        for index_dimension in range(0, dimension):
            for index_object in cluster:   
                centroid[index_dimension] += self.__pointer_data[index_object][index_dimension];
            
            centroid[index_dimension] /= len(cluster);
    
    
    def __get_radius(self, centroid, cluster):
        "Calculates radius of the specified cluster."
        
        "(in) cluster    - list of indexes that belong to cluster."
        
        "Returns radius of the cluster as a list."
                
        radius = 0.0;
        
        for index_object in cluster:
            radius += euclidean_distance_sqrt(self.__pointer_data[index_object], centroid);
        
        radius /= len(cluster);
        return radius ** (0.5);
    
    
    def __get_diameter(self, cluster):
        "Calculates diameter of the specified cluster."
        
        "(in) cluster    - list of indexes that belong to cluster."
        
        "Returns diameter of the cluster as a list."
        
        diameter = 0.0;
        
        for i in range(0, len(cluster)):
            for j in range(i + 1, len(cluster)):
                index_first = cluster[i];
                index_second = cluster[j];
                
                diameter += euclidean_distance_sqrt(self.__pointer_data[index_first], self.__pointer_data[index_second]);
        
        diameter /= len(cluster) * (len(cluster) - 1);
        return diameter ** (0.5);
    
    
    def __average_inter_cluster_distance(self, cluster1, cluster2):
        pass;
    
    def __average_intra_cluster_distance(self, cluster1, cluster2):
        pass;
    
    def __variance_increase_distance(self, cluster1, cluster2):
        pass;
                