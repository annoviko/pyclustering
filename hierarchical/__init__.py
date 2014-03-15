from support import euclidean_distance;
from support import read_sample;
from support import draw_clusters;

from support import timedcall;
 
def hierarchical(data, number_clusters):
    centers = data.copy();
    clusters = [[index] for index in range(0, len(data))];

    time_sum_find_cluster = 0;
    time_sum_center = 0;
    iterator = 0;
   
    while (len(clusters) > number_clusters):
        indexes = find_nearest_clusters(clusters, centers);
        #(ticks, indexes) = timedcall(find_nearest_clusters, clusters, centers);
        #time_sum_find_cluster += ticks;
        
        clusters[indexes[0]] += clusters[indexes[1]];
        centers[indexes[0]] = calculate_center(data, clusters[indexes[0]]);
        #(ticks, centers[indexes[0]]) = timedcall(calculate_center, data, clusters[indexes[0]]);
        #time_sum_center += ticks;
        
        clusters.pop(indexes[1]);   # remove merged cluster.
        centers.pop(indexes[1]);    # remove merged center.
        
        iterator += 1;
   
    #print("Find average time: ", time_sum_find_cluster / iterator, " summary: ", time_sum_find_cluster);
    #print("Calc average time: ", time_sum_center / iterator, " summary: ", time_sum_center);
    return clusters;
   
def find_nearest_clusters(clusters, centers):
    min_dist = 0;
    indexes = None;
   
    for index1 in range(0, len(centers)):
        for index2 in range(index1 + 1, len(centers)):
            distance = euclidean_distance(centers[index1], centers[index2]);
            if ( (distance < min_dist) or (indexes == None) ):
                min_dist = distance;
                indexes = [index1, index2];
   
    return indexes;
 

def calculate_center(data, cluster):
    dimension = len(data[cluster[0]]);
    center = [0] * dimension;
    for index_point in cluster:
        for index_dimension in range(0, dimension):
            center[index_dimension] += data[index_point][index_dimension];
    
    for index_dimension in range(0, dimension):
        center[index_dimension] /= len(cluster);
        
    return center;
            
   
   
# sample = read_sample('../samples/SampleTwoDiamonds.txt');
# (ticks, clusters) = timedcall(hierarchical, sample, 2);
# #print("Total time: ", ticks);
# draw_clusters(sample, clusters);