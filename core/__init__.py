import subprocess;
import os;
import re;

from ctypes import *;

from samples.definitions import SIMPLE_SAMPLES;

from support import read_sample;

from core.definitions import *;


# API that is required for interaction with DLL.
def create_pointer_data(sample):
    "Allocates memory for representing input data for processing that is described by structure 'data_representation' and returns pointer this structure."
    
    "(in) sample    - dataset for processing."
    
    "Returns pointer to the data for processing."
    
    input_data = data_representation();
    input_data.number_objects = len(sample);
    input_data.dimension = len(sample[0]);
    
    pointer_objects = (POINTER(c_double) * input_data.number_objects)();
     
    for index in range(0, input_data.number_objects):
        point = (c_double * input_data.dimension)();
        for dimension in range(0, input_data.dimension):
            point[dimension] = sample[index][dimension];
            
        pointer_objects[index] = cast(point, POINTER(c_double));
       
    input_data.pointer_objects = cast(pointer_objects, POINTER(POINTER(c_double)));
    input_data = pointer(input_data);
    
    return input_data;


# Implemented algorithms.
def dbscan(sample, eps, min_neighbors, return_noise = False):
    "Clustering algorithm DBSCAN returns allocated clusters and noise that are consisted from input data."
    
    "(in) data            - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) eps             - connectivity radius between points, points may be connected if distance between them less then the radius."
    "(in) min_neighbors   - minimum number of shared neighbors that is requied for establish links between points."
    "(in) return_noise    - if True than list of points that have been marked as noise will be returned."
    
    "If return_noise is False: Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    "If return_noise is True: Returns tuple of list of allicated clusters and list of points that are marked as noise."
    
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    result = ccore.dbscan_algorithm(pointer_data, c_double(eps), c_uint(min_neighbors));

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
    
    ccore.free_clustering_result(pointer_clustering_result);
    
    if (return_noise is True):
        return (list_of_clusters, noise);
    else:
        return list_of_clusters;


def hierarchical(sample, number_clusters):
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    result = ccore.hierarchical_algorithm(pointer_data, c_uint(number_clusters));
    
    pointer_clustering_result = cast(result, POINTER(clustering_result));    # clustering_result * clusters
    number_clusters = pointer_clustering_result[0].number_clusters;
    
    list_of_clusters = [];
    
    for index_cluster in range(0, number_clusters):
        clusters = cast(pointer_clustering_result[0].pointer_clusters, POINTER(cluster_representation));  # cluster_representation * cluster
        
        objects = cast(clusters[index_cluster].pointer_objects, POINTER(c_uint));   # cluster->objects (unsigned int *)
        
        list_of_clusters.append([]);
        pointer_container = list_of_clusters[index_cluster];

        for index_object in range(0, clusters[index_cluster].number_objects):
            pointer_container.append(objects[index_object]);
    
    ccore.free_clustering_result(pointer_clustering_result);
    return list_of_clusters;


# sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
# res = hierarchical(sample, 2);
# print(res);