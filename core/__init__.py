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


def extract_clusters(ccore_result):
    "Parse clustering result that is provided by the CCORE. Return Python list of clusters."
    
    "(in) ccore_result    - pointer to clustering result that has been returned by CCORE."
    
    "Returns Python list of clusters."
    
    pointer_clustering_result = cast(ccore_result, POINTER(clustering_result));    # clustering_result * clusters
    number_clusters = pointer_clustering_result[0].number_clusters;
    
    list_of_clusters = [];
    
    for index_cluster in range(0, number_clusters):
        clusters = cast(pointer_clustering_result[0].pointer_clusters, POINTER(cluster_representation));  # cluster_representation * cluster
        
        objects = cast(clusters[index_cluster].pointer_objects, POINTER(c_uint));   # cluster->objects (unsigned int *)
        
        list_of_clusters.append([]);
        pointer_container = list_of_clusters[index_cluster];

        for index_object in range(0, clusters[index_cluster].number_objects):
            pointer_container.append(objects[index_object]);
    
    return list_of_clusters;


def extract_dynamics(ccore_result):
    "Parse dynamic result that is provided by the CCORE. Return Python tuple that represent dynamics (times, dynamic)."
    
    "(in) ccore_result    - pointer to dynamic result that has been returned by CCORE."
    
    "Returns Python tuple dynamic (times, dynamic)."
    
    pointer_dynamic_result = cast(ccore_result, POINTER(dynamic_result));   # dynamic_result * pointer_dynamic_result
    size_dynamic = pointer_dynamic_result[0].size_dynamic;
    size_network = pointer_dynamic_result[0].size_network;
    
    pointer_time = cast(pointer_dynamic_result[0].times, POINTER(c_double));
    pointer_pointer_dynamic = cast(pointer_dynamic_result[0].dynamic, POINTER(POINTER(c_double)));
    
    times = [];
    dynamic = [];
    
    for index in range(0, size_dynamic):
        times.append(pointer_time[index]);
        dynamic.append([]);
        
        pointer_dynamic = cast(pointer_pointer_dynamic[index], POINTER(c_double));
        
        for object_dynamic in range(0, size_network):
            dynamic[index].append(pointer_dynamic[object_dynamic]);
        
    return (times, dynamic);

# Implemented algorithms.
def dbscan(sample, eps, min_neighbors, return_noise = False):
    "Clustering algorithm DBSCAN returns allocated clusters and noise that are consisted from input data. Calculation is performed via CCORE."
    
    "(in) data            - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) eps             - connectivity radius between points, points may be connected if distance between them less then the radius."
    "(in) min_neighbors   - minimum number of shared neighbors that is requied for establish links between points."
    "(in) return_noise    - if True than list of points that have been marked as noise will be returned."
    
    "If return_noise is False: Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    "If return_noise is True: Returns tuple of list of allicated clusters and list of points that are marked as noise."
    
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    result = ccore.dbscan_algorithm(pointer_data, c_double(eps), c_uint(min_neighbors));

    list_of_clusters = extract_clusters(result);
    ccore.free_clustering_result(result);
    
    noise = list_of_clusters[len(list_of_clusters) - 1];
    list_of_clusters.remove(noise);
    
    if (return_noise is True):
        return (list_of_clusters, noise);
    else:
        return list_of_clusters;


def hierarchical(sample, number_clusters):
    "Clustering algorithm hierarchical returns allocated clusters and noise that are consisted from input data. Calculation is performed via CCORE."
    
    "(in) data               - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) number_clusters    - number of cluster that should be allocated."
    
    "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    result = ccore.hierarchical_algorithm(pointer_data, c_uint(number_clusters));
    
    list_of_clusters = extract_clusters(result);
    
    ccore.free_clustering_result(result);
    return list_of_clusters;


def kmeans(sample, centers, tolerance):
    "Clustering algorithm K-Means returns allocated clusters. Calculation is performed via CCORE."
    
    "(in) data        - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) centers     - initial coordinates of centers of clusters that are represented by list: [center1, center2, ...]."
    "(in) tolerance   - stop condition: if maximum value of change of centers of clusters is less than tolerance than algorithm will stop processing."
    
    "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    
    pointer_data = create_pointer_data(sample);
    pointer_centers = create_pointer_data(centers);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    result = ccore.kmeans_algorithm(pointer_data, pointer_centers, c_double(tolerance));
    
    list_of_clusters = extract_clusters(result);
    
    ccore.free_clustering_result(result);
    return list_of_clusters;


def rock(sample, eps, number_clusters, threshold):
    "Clustering algorithm ROCK returns allocated clusters and noise that are consisted from input data. Calculation is performed via CCORE."
    
    "(in) data                - input data - list of points where each point is represented by list of coordinates."
    "(in) eps                 - connectivity radius (similarity threshold), points are neighbors if distance between them is less than connectivity radius."
    "(in) number_clusters     - defines number of clusters that should be allocated from the input data set."
    "(in) threshold           - value that defines degree of normalization that influences on choice of clusters for merging during processing."
    
    "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    result = ccore.rock_algorithm(pointer_data, c_double(eps), c_uint(number_clusters), c_double(threshold));
    
    list_of_clusters = extract_clusters(result);
    
    ccore.free_clustering_result(result);
    return list_of_clusters;    


def xmeans(sample, centers, kmax, tolerance):
    "Clustering algorithm X-Means returns allocated clusters. Calculation is performed via CCORE."
    
    "(in) data        - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) centers     - initial coordinates of centers of clusters that are represented by list: [center1, center2, ...]."
    "(in) kmax        - maximum number of clusters that can be allocated."
    
    "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    
    pointer_data = create_pointer_data(sample);
    pointer_centers = create_pointer_data(centers);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    result = ccore.xmeans_algorithm(pointer_data, pointer_centers, c_uint(kmax), c_double(tolerance));
    
    list_of_clusters = extract_clusters(result);
    
    ccore.free_clustering_result(result);
    return list_of_clusters;


def create_sync_network(num_osc, weight, frequency, qcluster, type_conn, initial_phases):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    pointer_network = ccore.create_sync_network(c_uint(num_osc), c_double(weight), c_double(frequency), c_uint(qcluster), c_uint(type_conn), c_uint(initial_phases));
    
    return pointer_network;


def simulate_sync_network(pointer_network, steps, time, solution, collect_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    ccore_dynamic_result = ccore.simulate_sync_network(pointer_network, c_uint(steps), c_double(time), c_uint(solution), c_bool(collect_dynamic));
    
    python_dynamic_result = extract_dynamics(ccore_dynamic_result);
    ccore.free_dynamic_result(ccore_dynamic_result);
    
    return python_dynamic_result;


def simulate_dynamic_sync_network(pointer_network, order, solution, collect_dynamic, step, int_step, threshold_changes):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    ccore_dynamic_result = ccore.simulate_dynamic_sync_network(pointer_network, c_double(order), c_uint(solution), c_bool(collect_dynamic), c_double(step), c_double(int_step), c_double(threshold_changes));
    
    python_dynamic_result = extract_dynamics(ccore_dynamic_result);
    ccore.free_dynamic_result(ccore_dynamic_result);
    
    return python_dynamic_result;    


def allocate_sync_ensembles_sync_network(pointer_network, tolerance):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    ccore_cluster_result = ccore.allocate_sync_ensembles_sync_network(pointer_network, c_double(tolerance));
    
    list_of_clusters = extract_clusters(ccore_cluster_result);
    
    ccore.free_clustering_result(ccore_cluster_result);
    return list_of_clusters; 


def sync_order(pointer_network):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    ccore.sync_order.restype = c_double;
    
    return ccore.sync_order(pointer_network);
    
    
def sync_local_order(pointer_network):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    ccore.sync_local_order.restype = c_double;
    
    return ccore.sync_local_order(pointer_network);


def create_syncnet(sample, radius, initial_phases, enable_conn_weight):
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    pointer_network = ccore.create_syncnet(pointer_data, c_double(radius), c_uint(initial_phases), c_bool(enable_conn_weight));
    
    return pointer_network;


def process_syncnet(network_pointer, order, solution, collect_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    ccore_dynamic_result = ccore.process_syncnet(network_pointer, c_double(order), c_uint(solution), c_bool(collect_dynamic));

    python_dynamic_result = extract_dynamics(ccore_dynamic_result);
    ccore.free_dynamic_result(ccore_dynamic_result);
    
    return python_dynamic_result;    


def get_clusters_syncnet(pointer_network, tolerance):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    ccore_cluster_result = ccore.get_clusters_syncnet(pointer_network, c_double(tolerance));
    
    list_of_clusters = extract_clusters(ccore_cluster_result);
    
    ccore.free_clustering_result(ccore_cluster_result);
    return list_of_clusters; 


def destroy_object(pointer_object):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_WIN64);
    ccore.destroy_object(pointer_object);


# from support import draw_dynamics, draw_clusters;
# from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;
#   
# sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
# clusters = xmeans(sample, [ [0.2, 0.1], [4.0, 1.0] ], 20, 0.025);
#  
# draw_clusters(sample, clusters);
