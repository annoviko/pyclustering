import matplotlib.pyplot as plt;
import matplotlib.lines as mlines;
from mpl_toolkits.mplot3d import Axes3D;

import scipy.spatial;

from support import euclidean_distance;

def kmeans(data, centers):
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
    centers = [[] for i in range(len(clusters))];
    
    for index in range(len(clusters)):
        point_sum = [0] * len(data[0]);
        
        for index_point in clusters[index]:
            point_sum = vec_sum(point_sum, data[index_point]);
            
        centers[index] = vec_dev(point_sum, len(clusters[index]));
        
    return centers;
    
            
def vec_diff(a, b):
    return [a[i] - b[i] for i in range(len(a))];


def vec_sum(a, b):
    return [a[i] + b[i] for i in range(len(a))];


def vec_dev(a, b):
    return [a[i] / b for i in range(len(a))];


def draw_clusters(data, clusters, centers, start_centers = []):   
    "Draw clusters"
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
            if (start_centers != []):
                axes.plot(start_centers[index_cluster][0], start_centers[index_cluster][1], c = color, marker = '*', markersize = 15, fillstyle = 'none');
        elif (len(data[0]) == 3):
            axes.scatter(centers[index_cluster][0], centers[index_cluster][1], centers[index_cluster][2], c = color, marker = '*', s = 150);
            if (start_centers != []):
                axes.scatter(start_centers[index_cluster][0], start_centers[index_cluster][1], start_centers[index_cluster][2], c = color, marker = '*', s = 150, alpha = 0.1);
        
        color_index += 1;
    
    plt.grid();
    plt.show();


