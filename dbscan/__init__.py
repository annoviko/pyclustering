import matplotlib.pyplot as plt;
from mpl_toolkits.mplot3d import Axes3D;

from support import euclidean_distance;
from support import read_sample;
from support import draw_clusters;

# BUG: dbscan SampleSimple1.txt 0.5 4 (number of nodes in the input data is not equal to number nodes that were placed in clusters and noise.
# Fix has been implemented in core.dbscan.
def dbscan(data, eps, min_neighbors, draw = False, return_noise = False):
    "Return allocated clusters and noise that are consisted from input data."
    "This algorithm was invented in 1996."
    "Format object in data: ([index] [coordinates])"
    
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
    
    if (draw == True):
        draw_clusters(data, clusters, noise);
    
    if (return_noise == True):
        return (clusters, noise);
    else:
        return clusters;


def expand_cluster(data, visited, belong, point, eps, min_neighbors):
    "Return structure (cluster, noise) or None"
    visited[point] = True;
    neighbors = neighbor_indexes(data, point, eps);
    
    if (len(neighbors) >= min_neighbors):
        
        cluster = list();
        
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
    
    return None;
            
        
def neighbor_indexes(data, point, eps):
    "Return list of indexes of neighbors of specified point"
    return [i for i in range(0, len(data)) if euclidean_distance(data[point], data[i]) <= eps and data[i] != data[point]];
