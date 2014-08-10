import numpy;
import math;

from support import euclidean_distance, euclidean_distance_sqrt;
from support import list_math_addition_number, list_math_addition, list_math_division_number;


def xmeans(data, centers, kmax = 20, ccore = False):
    clusters = [];
    while ( len(centers) < kmax ):
        current_cluster_number = len(centers);
        
        (clusters, centers) = improve_parameters(data, centers);
        allocated_centers = improve_structure(data, clusters, centers);
        
        if (current_cluster_number == len(allocated_centers)):
            break;
        else:
            centers = allocated_centers;
    
    return clusters;


def improve_parameters(data, centers, available_indexes = None, tolerance = 0.025):
    changes = numpy.Inf;
    
    stop_condition = tolerance * tolerance;   # Fast solution
    #stop_condition = tolerance;              # Slow solution
    
    clusters = [];
    
    while (changes > stop_condition):
        clusters = update_clusters(data, centers, available_indexes);
        updated_centers = update_centers(data, clusters);
    
        #changes = max([euclidean_distance(centers[index], updated_centers[index]) for index in range(len(centers))]);        # Slow solution
        changes = max([euclidean_distance_sqrt(centers[index], updated_centers[index]) for index in range(len(centers))]);    # Fast solution
        
        centers = updated_centers;
    
    return (clusters, centers);

    
def improve_structure(data, clusters, centers):
    difference = 0.001;
    
    # split each cluster (parent) into two clusters
    child_centers = [];
    child_clusters = [None] * ( len(clusters) * 2 );
    for index_cluster in range(len(clusters)):
        child_centers.append(list_math_addition_number(centers[index_cluster], -difference));
        child_centers.append(list_math_addition_number(centers[index_cluster], difference));
    
    # solve k-means problem for each parent cluster
    parent_scores = [0.0] * len(clusters);
    child_scores = [0.0] * len(child_centers);
    
    for index_parent_cluster in range(len(clusters)):
        index_child1 = index_parent_cluster * 2;
        index_child2 = index_child1 + 1;
        
        (parent_child_clusters, parent_child_centers) = improve_parameters(data, [ child_centers[index_child1], child_centers[index_child2] ], clusters[index_parent_cluster]);
        
        child_centers[index_child1] = parent_child_centers[0];
        child_centers[index_child2] = parent_child_centers[1];
        
        child_clusters[index_child1] = parent_child_clusters[0];
        child_clusters[index_child2] = parent_child_clusters[1];
    
        # Calculate splitting criterion
        result_parent_scores = splitting_criterion(data, [ clusters[index_parent_cluster] ], [ centers[index_parent_cluster] ]);
        result_child_scores = splitting_criterion(data, parent_child_clusters, child_centers);
        
        parent_scores[index_parent_cluster] = result_parent_scores[0];
        child_scores[index_child1] = result_child_scores[0];
        child_scores[index_child2] = result_child_scores[1];
                
        print("Scores: parent = ", result_parent_scores, "child = ", result_child_scores);
    
    # Reallocate number of centers (clusters) in line with scores
    allocated_centers = [];
    for index_parent in range(0, len(clusters), 1):
        index_child1 = index_parent * 2;
        index_child2 = index_child1 + 1;
        
        # TODO: Check that it's right way for comparison
        print(index_parent, parent_scores[index_parent], child_scores[index_child1], child_scores[index_child2]);
        if (parent_scores[index_parent] > child_scores[index_child1] + child_scores[index_child2]):
            allocated_centers.append(centers[index_parent]);
        else:
            allocated_centers.append(child_centers[index_child1]);
            allocated_centers.append(child_centers[index_child2]);
    
    return allocated_centers;


def splitting_criterion(data, clusters, centers):
    scores = [0.0] * len(clusters);     # splitting criterions for each cluster
    dimension = len(data[0]);
    
    # estimation of the noise variance in the data set
    sigma = [0.0] * len(clusters);
    for index_cluster in range(0, len(clusters), 1):
        for index_object in clusters[index_cluster]:
            sigma[index_cluster] += euclidean_distance_sqrt(data[index_object], centers[index_cluster]);
    
        sigma[index_cluster] /= (len(data) - len(clusters));

    # splitting criterion for each cluster
    for index_cluster in range(0, len(clusters), 1):
        n = len(clusters[index_cluster]);
        
        if (n > 1):
            scores[index_cluster] = n * math.log10(n) - n * math.log10(len(data)) - n * math.log10(2.0 * numpy.pi) / 2.0 - n * dimension * math.log10(sigma[index_cluster]) / 2.0 - (n - len(clusters)) / 2.0;
    
    return scores;


def update_clusters(data, centers, available_indexes = None):    
    bypass = None;
    if (available_indexes is None):
        bypass = range(len(data));
    else:
        bypass = available_indexes;
    
    clusters = [[] for i in range(len(centers))];
    for index_point in bypass:
        index_optim = -1;
        dist_optim = 0.0;
        
        for index in range(len(centers)):
            # dist = euclidean_distance(data[index_point], centers[index]);         # Slow solution
            dist = euclidean_distance_sqrt(data[index_point], centers[index]);      # Fast solution
            
            if ( (dist < dist_optim) or (index is 0)):
                index_optim = index;
                dist_optim = dist;
        
        clusters[index_optim].append(index_point);
        
    return clusters;
        

def update_centers(data, clusters):
    centers = [[] for i in range(len(clusters))];
    
    for index in range(len(clusters)):
        point_sum = [0] * len(data[0]);
        
        for index_point in clusters[index]:
            point_sum = list_math_addition(point_sum, data[index_point]);
            
        centers[index] = list_math_division_number(point_sum, len(clusters[index]));
        
    return centers;
