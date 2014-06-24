import subprocess;
import os;
import re;

from ctypes import *;

from samples.definitions import SIMPLE_SAMPLES;

from support import read_sample;


# Global variable.
PATH_DLL_CCORE_WIN64 = "./ccore/x64/ccore.dll";


# Structures that are required for exchaging with DLL.
class cluster_representation(Structure):
    "Decription of cluster in memory"
    _fields_ = [("number_objects", c_uint), ("pointer_objects", POINTER(c_uint))];
    
class clustering_result(Structure):
    "Description of result of clustering in memory"
    _fields_ = [("number_clusters", c_uint), ("pointer_clusters", POINTER(cluster_representation))];

class data_representation(Structure):
    "Description of input data"
    _fields_ = [("number_objects", c_uint), ("pointer_objects", POINTER(c_double))];


# API that is required for interaction with DLL.
def create_pointer_data(path_to_file):
    "Allocates memory for representing input data for processing that is described by structure 'data_representation' and returns pointer this structure."
    
    "(in) path_to_file    - path to file with data for processing, for example for clustering."
    
    "Returns pointer to the data for processing."
    
    sample = read_sample(path_to_file);
    
    input_data = data_representation();
    input_data.number_objects = len(sample);
    input_data.pointer_objects = (c_double * input_data.number_objects);
    
    for index in range(0, sample):
        input_data.pointer_objects[index] = sample[index];
    
    return input_data;


# Implemented algorithms.
def dbscan(path_to_file, eps, min_neighbors, return_noise = False):
    "Clustering algorithm DBSCAN returns allocated clusters and noise that are consisted from input data."
    
    "(in) data            - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) eps             - connectivity radius between points, points may be connected if distance between them less then the radius."
    "(in) min_neighbors   - minimum number of shared neighbors that is requied for establish links between points."
    "(in) return_noise    - if True than list of points that have been marked as noise will be returned."
    
    "If return_noise is False: Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    "If return_noise is True: Returns tuple of list of allicated clusters and list of points that are marked as noise."
        
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
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