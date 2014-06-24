import matplotlib.pyplot as plt;
from mpl_toolkits.mplot3d import Axes3D;

from support import euclidean_distance;
from support import read_sample;
from support import draw_clusters;

import core;

def dbscan(data, eps, min_neighbors, return_noise = False, ccore = False):
    "Clustering algorithm DBSCAN returns allocated clusters and noise that are consisted from input data."
    
    "(in) data            - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) eps             - connectivity radius between points, points may be connected if distance between them less then the radius."
    "(in) min_neighbors   - minimum number of shared neighbors that is requied for establish links between points."
    "(in) return_noise    - if True than list of points that have been marked as noise will be returned."
    
    "If return_noise is False: Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    "If return_noise is True: Returns tuple of list of allicated clusters and list of points that are marked as noise."
   
    noise = list();
    clusters = list();
    
    visited = [False] * len(data);
    belong = [False] * len(data);
    
    for i in range(0, len(data)):
        if (visited[i] == False):
            
            cluster = expand_cluster(data, visited, belong, i, eps, min_neighbors);
            if (cluster != None):
                clusters.append(cluster);
            else:
                noise.append(i);
                belong[i] = True;
    
    if (return_noise == True):
        return (clusters, noise);
    else:
        return clusters;


def expand_cluster(data, visited, belong, point, eps, min_neighbors):
    "Private function that is used by dbscan. It expands cluster in the input data space."
    
    "(in) data          - input data set that is presented by list of points."
    "(in) visited       - list where points are marked as visited or not, size of the list equals to list of data and index of element the visited list corresponds to index of element from the data."
    "(in) belong        - list where points are marked as belonging to cluster or noise list."
    "(in) point         - index of the point from the data."
    "(in) eps           - connectivity radius between points, points may be connected if distance between them less then the radius."
    "(in) min_neighbors - if True than list of points that have been marked as noise will be returned."
    
    "Return tuple of list of indexes that belong to the same cluster and list of points that are marked as noise: (cluster, noise), or None if nothing has been expanded."
    cluster = None;
    visited[point] = True;
    neighbors = neighbor_indexes(data, point, eps);
    
    if (len(neighbors) >= min_neighbors):
        
        cluster = [];
        cluster.append(point);
        
        belong[point] = True;
        
        for i in neighbors:
            if (visited[i] == False):
                
                visited[i] = True;
                next_neighbors = neighbor_indexes(data, i, eps);
                
                if (len(next_neighbors) >= min_neighbors):
                    # if some node has less then minimal number of neighbors than we shouldn't look at them
                    # because maybe it's a noise.
                    neighbors += [k for k in next_neighbors if ( (k in neighbors) == False)];
            
            if (belong[i] == False):
                cluster.append(i);
                belong[i] = True;
        
    return cluster;
            
        
def neighbor_indexes(data, point, eps):
    "Private function that is used by dbscan. Return list of indexes of neighbors of specified point for the data."
    
    "(in) data        - input data for clustering."
    "(in) point       - index of point for which potential neighbors should be returned for the data in line with connectivity radius."
    "(in) eps         - connectivity radius between points, points may be connected if distance between them less then the radius."
    
    "Return list of indexes of neighbors in line the connectivity radius."
    return [i for i in range(0, len(data)) if euclidean_distance(data[point], data[i]) <= eps and data[i] != data[point]];
