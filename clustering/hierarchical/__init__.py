from support import euclidean_distance_sqrt;
from support import read_sample;
from support import draw_clusters;

from support import timedcall;

import core;
 
def hierarchical(data, number_clusters, ccore = False):
    "Clustering algorithm hierarchical returns allocated clusters and noise that are consisted from input data."
    
    "(in) data               - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) number_clusters    - number of cluster that should be allocated."
    "(in) ccore              - if True than DLL CCORE (C++ solution) will be used for solving the problem."
    
    "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    
    if (ccore is True):
        return core.hierarchical(data, number_clusters);    
    
    centers = data.copy();
    clusters = [[index] for index in range(0, len(data))];

    iterator = 0;
   
    while (len(clusters) > number_clusters):
        indexes = find_nearest_clusters(clusters, centers);
        
        clusters[indexes[0]] += clusters[indexes[1]];
        centers[indexes[0]] = calculate_center(data, clusters[indexes[0]]);
        
        clusters.pop(indexes[1]);   # remove merged cluster.
        centers.pop(indexes[1]);    # remove merged center.
        
        iterator += 1;
   
    return clusters;
   
   
def find_nearest_clusters(clusters, centers):
    "Private function that is used by 'hierarchical'. Returns indexes of two clusters whose distance is the smallest."
    
    "(in) clusters    - list of clusters that are represented by lists."
    "(in) centers     - list of cluster centers that are represented by list."
    
    "Returns list with two indexes of two clusters whose distance is the smallest."
    
    min_dist = 0;
    indexes = None;
   
    for index1 in range(0, len(centers)):
        for index2 in range(index1 + 1, len(centers)):
            distance = euclidean_distance_sqrt(centers[index1], centers[index2]);
            if ( (distance < min_dist) or (indexes == None) ):
                min_dist = distance;
                indexes = [index1, index2];
   
    return indexes;
 

def calculate_center(data, cluster):
    "Private function that is used by 'hierarchical'. Returns new value of the center of the cluster."
    
    "(in) data        - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) cluster     - list of indexes (cluster) of objects from the input data."
    
    "Returns new value of the center of the specified cluster."
    
    dimension = len(data[cluster[0]]);
    center = [0] * dimension;
    for index_point in cluster:
        for index_dimension in range(0, dimension):
            center[index_dimension] += data[index_point][index_dimension];
    
    for index_dimension in range(0, dimension):
        center[index_dimension] /= len(cluster);
        
    return center;
