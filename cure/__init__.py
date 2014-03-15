import numpy;

from decimal import *;

from scipy.spatial import KDTree;

from support import kdtree;
from support import read_sample;
from support import euclidean_distance;
from support import euclidean_distance_sqrt;
from support import draw_clusters;

class cluster:   
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
        

def cure(data, number_cluster, number_represent_points = 5, compression = 0.5):
    "CURE algorithm. Return formed clusters from input data set."
    queue = create_queue(data);     # queue
    tree = create_kdtree(queue);    # create k-d tree
    
    while (len(queue) > number_cluster):
        cluster1 = queue[0];            # cluster that has nearest neighbor.
        cluster2 = cluster1.closest;    # closest cluster.
        
        #print("Merge decision: \n\t", cluster1, "\n\t", cluster2);
        
        queue.remove(cluster1);
        queue.remove(cluster2);

        merged_cluster = merge_clusters(cluster1, cluster2, number_represent_points, compression);

        delete_represented_points(cluster1, tree);
        delete_represented_points(cluster2, tree);
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
        
        # DEBUG stuff
#         result_cluster_insertion = merged_cluster in queue;
#         assert result_cluster_insertion is True;
#         print("New cluster ", merged_cluster, " has been inserted to the queue: ", result_cluster_insertion, "\n\n");
#         check_links(queue, tree);

    return queue;


# DEBUG ONLY
def check_links(queue, tree):
    for item in queue:
        if (item.closest not in queue):
            print("Assertion:");
            print("item = ", item);
            print("item.closest = ", item.closest, " is not in queue");
        
        assert item.closest in queue;
        assert item.closest is not item;
        
        for rep in item.rep:
            node = tree.find_node(rep);
            assert None != node;
            assert item is node.payload;


def insert_cluster(queue, cluster):
    "Insert cluster to queue in line with order"
    for index in range(len(queue)):
        if (cluster.distance < queue[index].distance):
            queue.insert(index, cluster);
            return;

    queue.append(cluster);


def relocate_cluster(queue, cluster):
    "Relocate cluster in queue in line with order"
    queue.remove(cluster);
    insert_cluster(queue, cluster);


def closest_cluster(cluster, distance, tree):
    "Return closest cluster to the specified cluster in line with distance"
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
    for point in cluster.rep:
        tree.insert(point, cluster);


def delete_represented_points(cluster, tree):   
    for point in cluster.rep:
        tree.find_node(point);
        tree.remove(point);


def merge_clusters(cluster1, cluster2, number_represent_points, compression):
    merged_cluster = cluster();
    
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
                minimal_distance = cluster_distance(cluster(point), cluster(temporary[0]));
                
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
    "Create queue (list) of sorted clusters by distance between them, where first cluster has the nearest neighbor"
    queue = [cluster(point) for point in data];
    
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
    "Create k-d tree in line with created clusters"
    tree = kdtree.kdtree();
    for current_cluster in queue:
        for representative_point in current_cluster.rep:
            tree.insert(representative_point, current_cluster);    
            
    return tree;


def cluster_distance(cluster1, cluster2):
    "Return minimal distance between clusters. Representative points are used for that"
    distance = numpy.Inf;
    for i in range(0, len(cluster1.rep)):
        for k in range(0, len(cluster2.rep)):
            #dist = euclidean_distance_sqrt(cluster1.rep[i], cluster2.rep[k]);   # Fast mode
            dist = euclidean_distance(cluster1.rep[i], cluster2.rep[k]);        # Slow mode
            if (dist < distance):
                distance = dist;
                
    return distance;


    
# sample = read_sample('../samples/SampleLsun.txt');
# cure_clusters = cure(sample, 3);
#    
# clusters = [ cure_cluster.points for cure_cluster in cure_clusters ];
#    
# draw_clusters(None, clusters);
