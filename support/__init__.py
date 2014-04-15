import time;
import numpy;

from PIL import Image;
from numpy import array;

import matplotlib.pyplot as plt;
from mpl_toolkits.mplot3d import Axes3D;


def read_sample(filename):
    "Return sample for clusterization"
    file = open(filename, 'r');

    sample = [[float(val) for val in line.split()] for line in file];
    
    file.close();
    return sample;

def average_neighbor_distance(points, num_neigh):
    if (num_neigh > len(points) - 1):
        raise NameError('Impossible to calculate average distance to neighbors when number of object is less than number of neighbors.');
    
    dist_matrix = [ [ 0.0 for i in range(len(points)) ] for j in range(len(points)) ];
    for i in range(0, len(points), 1):
        for j in range(i + 1, len(points), 1):
            distance = euclidean_distance(points[i], points[j]);
            dist_matrix[i][j] = distance;
            dist_matrix[j][i] = distance;
            
        dist_matrix[i] = sorted(dist_matrix[i]);
    
    total_distance = 0;
    for i in range(0, len(points), 1):
        # start from 0 due to - first element is distance to itself.
        for j in range(0, num_neigh, 1):
            total_distance += dist_matrix[i][j + 1];
            
    return ( total_distance / (num_neigh * len(points)) );
        

def euclidean_distance(a, b):
    "Return Euclidean distance between two points: 'a' and 'b'"
    "NOTE! This function for calculation is faster then standard function in ~100 times!"
    distance = euclidean_distance_sqrt(a, b);
    return distance**(0.5);


def euclidean_distance_sqrt(a, b):
    if ( ((type(a) == float) and (type(b) == float)) or ((type(a) == int) and (type(b) == int)) ):
        return (a - b)**2.0;
        
    dimension = len(a);
    # assert len(a) == len(b);
    
    distance = 0.0;
    for i in range(0, dimension):
        distance += (a[i] - b[i])**2.0;
        
    return distance;


def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock();
    result = fn(*args);
    t1 = time.clock();
    return t1 - t0, result;


def draw_clusters(data, clusters, noise = []):   
    # Get dimension
    dimension = 0;
    if ( (data is not None) and (clusters is not None) ):
        dimension = len(data[0]);
    elif ( (data is None) and (clusters is not None) ):
        dimension = len(clusters[0][0]);
    else:
        raise NameError('Data or clusters should be specified exactly.');
    
    "Draw clusters"
    colors = ['b', 'r', 'g', 'y', 'm', 'k', 'c'];
    if (len(clusters) > len(colors)):
        raise NameError('Impossible to represent clusters due to number of specified colors.');
    
    fig = plt.figure();
    axes = None;
    
    # Check for dimensions
    if (dimension == 2):
        axes = fig.add_subplot(111);
    elif (dimension == 3):
        axes = fig.gca(projection='3d');
    else:
        raise NameError('Drawer supports only 2d and 3d data representation');
    
    color_index = 0;
    for cluster in clusters:
        color = colors[color_index];
        marker_point = 'o';
        for item in cluster:
            if (dimension == 2):
                if (data is None):
                    axes.plot(item[0], item[1], color + marker_point);
                else:
                    axes.plot(data[item][0], data[item][1], color + marker_point);
                    
            elif (dimension == 3):
                if (data is None):
                    axes.scatter(item[0], item[1], item[2], c = color, marker = marker_point);
                else:
                    axes.scatter(data[item][0], data[item][1], data[item][2], c = color, marker = marker_point);
        
        color_index += 1;
    
    for item in noise:
        if (dimension == 2):
            if (data is None):
                axes.plot(item[0], item[1], 'wo');
            else:
                axes.plot(data[item][0], data[item][1], 'wo');
                
        elif (dimension == 3):
            if (data is None):
                axes.scatter(item[0], item[1], item[2], c = 'w', marker = 'o');
            else:
                axes.scatter(data[item][0], data[item][1], data[item][2], c = 'w', marker = 'o');
    
    plt.grid();
    plt.show();
    

def draw_dynamics(t, dyn, x_title = None, y_title = None, x_lim = None, y_lim = None):
    "Draw dynamics of neurons in the network"
    if (x_title is None): x_title = "Time";     
    if (y_title is None): y_title = "Dynamic";
    
    from matplotlib.font_manager import FontProperties;
    from matplotlib import rcParams;
    
    rcParams['font.sans-serif'] = ['Arial'];
    rcParams['font.size'] = 12;
    
    fig = plt.figure();
    axes = fig.add_subplot(111);
    
    surface_font = FontProperties();
    surface_font.set_name('Arial');
    surface_font.set_size('12');
    
    if (isinstance(dyn[0], list) is True):
        num_items = len(dyn[0]);
        for index in range(0, num_items, 1):       
            y = [item[index] for item in dyn];
            axes.plot(t, y, 'b-', linewidth=0.5); 
    else:
        axes.plot(t, dyn, 'b-', linewidth=0.5);     

    plt.ylabel(y_title, fontproperties=surface_font);
    plt.xlabel(x_title, fontproperties=surface_font);
    
    if (x_lim is not None): plt.xlin(x_lim[0], x_lim[1]);
    if (y_lim is not None): plt.ylim(y_lim[0], y_lim[1]);

    plt.grid();
    plt.show();


def draw_image_segments(source, clusters):
    image_source = Image.open(source);
    image_size = image_source.size;
  
    for cluster in clusters:
        stage_cluster = [(255, 255, 255)] * (image_size[0] * image_size[1]);
        for index in cluster:
            stage_cluster[index] = (0, 0, 0);
          
        stage = array(stage_cluster, numpy.uint8);
        stage = numpy.reshape(stage, image_size + ((3),)); # ((3),) it's size of RGB - third dimension.
        
        image_cluster = Image.fromarray(stage, 'RGB');  
        image_cluster.show();
        