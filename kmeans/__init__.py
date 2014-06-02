import matplotlib.pyplot as plt;
import matplotlib.lines as mlines;
from mpl_toolkits.mplot3d import Axes3D;

from support import euclidean_distance, list_math_addition, list_math_division_number;

def kmeans(data, centers):
    "Clustering algorithm K-Means returns allocated clusters and noise that are consisted from input data."
    
    "(in) data        - input data that is presented as list of points (objects), each point should be represented by list or tuple."
    "(in) centers     - inital coordinates of centers of clusters that are represented by list: [center1, center2, ...]."
    
    "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    
    changes = 1;
    clusters = [];
    
    # Check for dimension
    if (len(data[0]) != len(centers[0])):
        raise NameError('Dimension of the input data and dimension of the initial cluster centers must be equal.');
    
    while (changes > 0.05):
        clusters = update_clusters(data, centers);
        updated_centers = update_centers(data, clusters);
    
        changes = max([euclidean_distance(centers[index], updated_centers[index]) for index in range(len(centers))]);
        centers = updated_centers;
    
    return (clusters, centers);

    
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
            dist = euclidean_distance(data[index_point], centers[index]);
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



def draw_clusters(data, clusters, centers, start_centers = None):
    "Public function. Draw clusters and specified intial and final cluster centers."
    
    "(in) data              - input data - list of objects (points) where each point is described by list of coordinates."
    "(in) clusters          - list of clusters where each cluster is described by list of point indexes from input data."
    "(in) centers           - list of cluster centers where each cluster center is described by list of coordinates."
    "(in) start_clusters    - list of initial cluster centers. Optional argument and can be omitted."
    
    colors = ['b', 'r', 'g', 'y', 'm', 'k', 'c'];
    if (len(clusters) > len(colors)):
        raise NameError('Impossible to represent clusters due to number of specified colors.');
    
    fig = plt.figure();
    axes = None;
    
    # Check for dimensions
    if (len(data[0]) == 2):
        axes = fig.add_subplot(111);
    elif (len(data[0]) == 3):
        axes = fig.gca(projection='3d');
    else:
        raise NameError('Dwawer supports only 2d and 3d data representation');
    
    color_index = 0;
    for index_cluster in range(len(clusters)):
        color = colors[color_index];
        for index in clusters[index_cluster]:
            if (len(data[0]) == 2):
                axes.plot(data[index][0], data[index][1], color + 'o');
            elif (len(data[0]) == 3):
                axes.scatter(data[index][0], data[index][1], data[index][2], c = color, marker = 'o');
        
        if (len(data[0]) == 2):
            axes.plot(centers[index_cluster][0], centers[index_cluster][1], c = color, marker = '*', markersize = 15);
            if (start_centers is not None):
                axes.plot(start_centers[index_cluster][0], start_centers[index_cluster][1], c = color, marker = '*', markersize = 15, fillstyle = 'none');
        elif (len(data[0]) == 3):
            axes.scatter(centers[index_cluster][0], centers[index_cluster][1], centers[index_cluster][2], c = color, marker = '*', s = 150);
            if (start_centers is not None):
                axes.scatter(start_centers[index_cluster][0], start_centers[index_cluster][1], start_centers[index_cluster][2], c = color, marker = '*', s = 150, alpha = 0.1);
        
        color_index += 1;
    
    plt.grid();
    plt.show();


