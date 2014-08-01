import numpy;

import core;

from support import euclidean_distance, euclidean_distance_sqrt, list_math_addition, list_math_division_number;

def kmeans(data, centers, tolerance = 0.025, ccore = False):
    "Clustering algorithm K-Means returns allocated clusters and noise that are consisted from input data."
    
    "(in) data        - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) centers     - initial coordinates of centers of clusters that are represented by list: [center1, center2, ...]."
    "(in) tolerance   - stop condition: if maximum value of change of centers of clusters is less than tolerance than algorithm will stop processing."
    
    "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    
    if (ccore is True):
        return core.kmeans(data, centers, tolerance);
    
    changes = numpy.Inf;
    clusters = [];
    
    stop_condition = tolerance * tolerance;   # Fast solution
    #stop_condition = tolerance;              # Slow solution
    
    # Check for dimension
    if (len(data[0]) != len(centers[0])):
        raise NameError('Dimension of the input data and dimension of the initial cluster centers must be equal.');
    
    while (changes > stop_condition):
        clusters = update_clusters(data, centers);
        updated_centers = update_centers(data, clusters);
    
        #changes = max([euclidean_distance(centers[index], updated_centers[index]) for index in range(len(centers))]);        # Slow solution
        changes = max([euclidean_distance_sqrt(centers[index], updated_centers[index]) for index in range(len(centers))]);    # Fast solution
        
        centers = updated_centers;
    
    return clusters;

    
def update_clusters(data, centers):
    "Private function that is used by kmeans. Calculate Euclidean distance to each point from the each cluster."
    "Nearest points are captured by according clusters and as a result clusters are updated."
    
    "(in) data         - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) centers      - coordinates of centers of clusters that are represented by list: [center1, center2, ...]."
    
    "Returns updated clusters as list of clusters. Each cluster contains indexes of objects from data."
    
    clusters = [[] for i in range(len(centers))];
    for index_point in range(len(data)):
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
    "Private function that is used by kmeans. Update centers of clusters in line with contained objects."
    
    "(in) data         - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) clusters     - list of clusters that contain indexes of objects from data."
    
    "Returns updated centers as list of centers."
    
    centers = [[] for i in range(len(clusters))];
    
    for index in range(len(clusters)):
        point_sum = [0] * len(data[0]);
        
        for index_point in clusters[index]:
            point_sum = list_math_addition(point_sum, data[index_point]);
            
        centers[index] = list_math_division_number(point_sum, len(clusters[index]));
        
    return centers;


