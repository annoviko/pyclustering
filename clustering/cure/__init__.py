import numpy;

from decimal import *;

from support import kdtree;
from support import read_sample;
from support import euclidean_distance;
from support import euclidean_distance_sqrt;
from support import draw_clusters;

import core;

class cure_cluster:   
    "Representation of CURE cluster."
    
    def __init__(self, point = None):
        if (point is not None):
            self.points = [ point ];
            self.mean = point;
            self.rep = [ point ];
        else:
            self.points = [ ];
            self.mean = None;
            self.rep = [ ];
            
        self.closest = None;
        self.distance = numpy.Inf;      # calculation of distance is really complexity operation (even square distance), so let's store distance to closest cluster.
        
    def __repr__(self):
        return "%s, %s" % (self.distance, self.points);
        

def cure(data, number_cluster, number_represent_points = 5, compression = 0.5, ccore = False):
    "Clustering algorithm CURE returns allocated clusters and noise that are consisted from input data."
    
    "(in) data                       - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) number_cluster             - number of clusters that should be allocated."
    "(in) number_represent_points    - number of representation points for each cluster."
    "(in) compression                - coefficient defines level of shrinking of representation points toward the mean of the new created cluster after merging on each step."
    "(in) ccore                      - if True than DLL CCORE (C++ solution) will be used for solving the problem."
    
    "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    
    if (ccore is True):
        return core.cure(data, number_cluster, number_represent_points, compression);
    
    queue = create_queue(data);     # queue
    tree = create_kdtree(queue);    # create k-d tree
    
    while (len(queue) > number_cluster):
        cluster1 = queue[0];            # cluster that has nearest neighbor.
        cluster2 = cluster1.closest;    # closest cluster.
        
        #print("Merge decision: \n\t", cluster1, "\n\t", cluster2);
        
        queue.remove(cluster1);
        queue.remove(cluster2);
        
        delete_represented_points(cluster1, tree);
        delete_represented_points(cluster2, tree);

        merged_cluster = merge_clusters(cluster1, cluster2, number_represent_points, compression);

        insert_represented_points(merged_cluster, tree);
        
        merged_cluster.closest = queue[0];  # arbitrary cluster from queue
        merged_cluster.distance = cluster_distance(merged_cluster, merged_cluster.closest);
        
        #print("New cluster with temp. nearest: ", merged_cluster);
        
        # Pointers to clusters that should be relocated is stored here.
        cluster_relocation_requests = [];
        
        for item in queue:
            distance = cluster_distance(merged_cluster, item);
            # Check if distance between new cluster and current is the best than now.
            if (distance < merged_cluster.distance):
                merged_cluster.closest = item;
                merged_cluster.distance = distance;
            
            # Check if current cluster has removed neighbor.
            if ( (item.closest is cluster1) or (item.closest is cluster2) ):
                # If previous distance was less then distance to new cluster then nearest cluster should be found in the tree.
                #print("Update: ", item);
                if (item.distance < distance):
                    (item.closest, item.distance) = closest_cluster(item, distance, tree);
                    
                    # TODO: investigation of root cause is required.
                    # Itself and merged cluster should be always in list of neighbors in line with specified radius.
                    # But merged cluster may not be in list due to error calculation, therefore it should be added
                    # manually.
                    if (item.closest is None):
                        item.closest = merged_cluster;
                        item.distance = distance;
                    
                # Otherwise new cluster is nearest.
                else:
                    item.closest = merged_cluster;
                    item.distance = distance;
                
                cluster_relocation_requests.append(item);
                #relocate_cluster(queue, item);
            elif (item.distance > distance):
                #print("Update: ", item);
                item.closest = merged_cluster;
                item.ditance = distance;
                
                cluster_relocation_requests.append(item);
        
        # New cluster and updated clusters should relocated in queue
        insert_cluster(queue, merged_cluster);
        [relocate_cluster(queue, item) for item in cluster_relocation_requests];

    # Change cluster representation
    clusters = [ cure_cluster_unit.points for cure_cluster_unit in queue ];
    return clusters;




def insert_cluster(queue, cluster):
    "Private function that is used by cure. Insert cluster to list in line with sequence order (distance). Thus list should be always sorted."
    
    "(in) queue       - list of CURE clusters."
    "(in) cluster     - CURE cluster that should be inserted."
    
    for index in range(len(queue)):
        if (cluster.distance < queue[index].distance):
            queue.insert(index, cluster);
            return;

    queue.append(cluster);


def relocate_cluster(queue, cluster):
    "Private function that is used by cure. Relocate cluster in list in line with distance order. Helps list to be sorted."
    
    "(in) queue       - list of CURE clusters."
    "(in) cluster     - CURE cluster that should be relocated."
    
    queue.remove(cluster);
    insert_cluster(queue, cluster);


def closest_cluster(cluster, distance, tree):
    "Private function that is used by cure. Returns closest cluster to the specified cluster in line with distance."
    
    "(in) cluster     - CURE cluster for which nearest cluster should be found."
    "(in) distance    - closest distance to the previous cluster."
    "(in) tree        - k-d tree where representation points of clusters are stored."
    
    "Returns tuple (nearest CURE cluster, nearest distance) if nearest cluster has been found, otherwise None is returned."
    
    nearest_cluster = None;
    nearest_distance = numpy.Inf;
    
    for point in cluster.rep:
        # Nearest nodes should be returned (at least it will return itself).
        nearest_nodes = tree.find_nearest_dist_nodes(point, distance);
        for (candidate_distance, kdtree_node) in nearest_nodes:
            if ( (candidate_distance < nearest_distance) and (kdtree_node is not None) and (kdtree_node.payload is not cluster) ):
                nearest_distance = candidate_distance;
                nearest_cluster = kdtree_node.payload;
                
    return (nearest_cluster, nearest_distance);


def insert_represented_points(cluster, tree):
    "Private function that is used by cure. Insert representation points to the k-d tree."
    
    "(in) cluster    - CURE cluster whose representation points should be inserted."
    "(in) tree       - k-d tree where representation points are stored."
    
    for point in cluster.rep:
        tree.insert(point, cluster);


def delete_represented_points(cluster, tree):   
    "Private function that is used by cure. Remove representation points of clusters from the k-d tree."
    
    "(in) cluster    - CURE cluster whose representation points should be removed."
    "(in) tree       - k-d tree where representation points are stored."
    
    for point in cluster.rep:
        tree.remove(point);


def merge_clusters(cluster1, cluster2, number_represent_points, compression):
    "Private function that is used by cure. Merges two clusters and returns new merged cluster. Representation points and mean points are calculated for the new cluster."
    
    "(in) cluster1                   - CURE cluster that should be merged with cluster2."
    "(in) cluster2                   - CURE cluster that should be merged with cluster1."
    "(in) number_represent_points    - number of representation points for each cluster."
    "(in) compression                - coefficient defines level of shrinking of representation points toward the mean of the new created cluster after merging on each step."
    
    "Returns new merged CURE cluster."
    
    merged_cluster = cure_cluster();
    
    merged_cluster.points = cluster1.points + cluster2.points;
    
    # merged_cluster.mean = ( len(cluster1.points) * cluster1.mean + len(cluster2.points) * cluster2.mean ) / ( len(cluster1.points) + len(cluster2.points) );
    dimension = len(cluster1.mean);
    merged_cluster.mean = [0] * dimension;
    for index in range(dimension):
        merged_cluster.mean[index] = ( len(cluster1.points) * cluster1.mean[index] + len(cluster2.points) * cluster2.mean[index] ) / ( len(cluster1.points) + len(cluster2.points) );
    
    temporary = list(); # TODO: Set should be used in line with specification (article), but list is not hashable object therefore it's impossible to use list in this fucking set!
    
    for index in range(number_represent_points):
        maximal_distance = 0;
        maximal_point = None;
        
        for point in merged_cluster.points:
            minimal_distance = 0;
            if (index == 0):
                minimal_distance = euclidean_distance(point, merged_cluster.mean);
                #minimal_distance = euclidean_distance_sqrt(point, merged_cluster.mean);
            else:
                minimal_distance = euclidean_distance(point, temporary[0]);
                #minimal_distance = cluster_distance(cure_cluster(point), cure_cluster(temporary[0]));
                
            if (minimal_distance >= maximal_distance):
                maximal_distance = minimal_distance;
                maximal_point = point;
    
        if (maximal_point not in temporary):
            temporary.append(maximal_point);
            
    for point in temporary:
        representative_point = [0] * dimension;
        for index in range(dimension):
            representative_point[index] = point[index] + compression * (merged_cluster.mean[index] - point[index]);
            
        merged_cluster.rep.append(representative_point);
    
    return merged_cluster;


def create_queue(data):
    "Private function that is used by cure. Create queue (list) of sorted clusters by distance between them, where first cluster has the nearest neighbor."
    "At the first iteration each cluster contains only one point."
    
    "(in) data        - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    
    "Returns create queue (list) of sorted clusters by distance between them."
    
    queue = [cure_cluster(point) for point in data];
    
    # set closest clusters
    for i in range(0, len(queue)):
        minimal_distance = numpy.Inf;
        closest_index_cluster = -1;
        
        for k in range(0, len(queue)):
            if (i != k):
                dist = cluster_distance(queue[i], queue[k]);
                if (dist < minimal_distance):
                    minimal_distance = dist;
                    closest_index_cluster = k;
        
        queue[i].closest = queue[closest_index_cluster];
        queue[i].distance = minimal_distance;
    
    # sort clusters
    queue.sort(key = lambda x: x.distance, reverse = False);
    return queue;
    

def create_kdtree(queue):
    "Private function that is used by cure. Create k-d tree in line with created clusters."
    "At the first iteration contains all points from the input data set."
    
    "(in) queue    - list of CURE clusters whose representation points should be used for creation k-d tree."
    
    "Return k-d tree of representation points of CURE clusters."
    
    tree = kdtree.kdtree();
    for current_cluster in queue:
        for representative_point in current_cluster.rep:
            tree.insert(representative_point, current_cluster);    
            
    return tree;


def cluster_distance(cluster1, cluster2):
    "Private function that is used by several function related to the CURE algorithm. Return minimal distance between clusters. Representative points are used for that."
    
    "(in) cluster1        - CURE cluster 1."
    "(in) cluster2        - CURE cluster 2."
    
    "Returns Euclidean distance between two clusters that is defined by minimum distance between representation points of two clusters."
    
    distance = numpy.Inf;
    for i in range(0, len(cluster1.rep)):
        for k in range(0, len(cluster2.rep)):
            #dist = euclidean_distance_sqrt(cluster1.rep[i], cluster2.rep[k]);   # Fast mode
            dist = euclidean_distance(cluster1.rep[i], cluster2.rep[k]);        # Slow mode
            if (dist < distance):
                distance = dist;
                
    return distance;
