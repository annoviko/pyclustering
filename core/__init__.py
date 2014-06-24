import subprocess;
import os;
import re;

from samples.definitions import SIMPLE_SAMPLES;

from ctypes import *;


class cluster_representation(Structure):
    "Decription of cluster in memory"
    _fields_ = [("number_objects", c_uint), ("pointer_objects", POINTER(c_uint))]
    
class clustering_result(Structure):
    "Description of result of clustering in memory"
    _fields_ = [("number_clusters", c_uint), ("pointer_clusters", POINTER(cluster_representation))]
    


def dbscan(path_to_file, eps, min_neighbors, return_noise = False):   
    ccore = cdll.LoadLibrary("./ccore/x64/Release/ccore.dll");
    result = ccore.dbscan_algorithm(c_char_p(path_to_file.encode()), c_double(eps), c_uint(min_neighbors));
    
    list_of_clusters = [];
    noise = [];
    
    pointer_clustering_result = cast(result, POINTER(clustering_result));    # clustering_result * clusters
    number_clusters = pointer_clustering_result[0].number_clusters;
    
    for index_cluster in range(0, number_clusters):
        clusters = cast(pointer_clustering_result[0].pointer_clusters, POINTER(cluster_representation));  # cluster_representation * cluster
        
        objects = cast(clusters[index_cluster].pointer_objects, POINTER(c_uint));   # cluster->objects (unsigned int *)
        
        pointer_container = None;
        if (index_cluster < (number_clusters - 1)):
            list_of_clusters.append([]);
            pointer_container = list_of_clusters[index_cluster];
        else:
            pointer_container = noise;
            
        for index_object in range(0, clusters[index_cluster].number_objects):
            pointer_container.append(objects[index_object]);
    
    if (return_noise is True):
        return (list_of_clusters, noise);
    else:
        return list_of_clusters;


dbscan(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 2);