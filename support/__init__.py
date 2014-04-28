import time;
import numpy;

from PIL import Image;
from numpy import array;

import matplotlib.pyplot as plt;
from matplotlib import colors;
from mpl_toolkits.mplot3d import Axes3D;

class type_graph_descr:
    GRAPH_UNKNOWN = 0;
    GRAPH_MATRIX_DESCR = 1;
    GRAPH_VECTOR_DESCR = 2;

class graph:
    __type_graph = None;
    __data = None;
    __space_description = None;
    __comments = None;
    
    def __init__(self, data, type_graph = None, space_descr = None, comments = None):
        self.__data = data;
        self.__space_descr = space_descr;
        self.__comments = comments;
        
        if (type_graph is not None):
            self.__type_graph = type_graph;
        else:
            self.__type_graph = type_graph_descr.GRAPH_MATRIX_DESCR;
            for row in self.__data:
                if (len(row) != len(self.__data)):
                    self.__type_graph = type_graph_descr.GRAPH_VECTOR_DESCR;
                    break;
                
                for element in row:
                    if ( (element != 0) or (element != 1) ):
                        self.__type_graph = type_graph_descr.GRAPH_VECTOR_DESCR;
        
    @property
    def data(self): return self.__data;
    
    @property
    def space_description(self): return self.__space_descr;
    
    @property
    def comments(self): return self.__comments;
    
    @property
    def type_graph_descr(self): return self.__type_graph;
    

def read_sample(filename):
    "Returns sample for clusterization"
    file = open(filename, 'r');

    sample = [[float(val) for val in line.split()] for line in file];
    
    file.close();
    return sample;


def read_graph(filename):
    "Read graph from file in GRPR format"
    file = open(filename, 'r');
    
    comments = "";
    space_descr = [];
    data = [];
    data_type = None;
    
    for line in file:
        if (line[0] == 'c'): 
            comments += line[1:]; 
        
        elif (line[0] == 'r'): 
            node_coordinates = [float(val) for val in line[1:].split()];
            if (len(node_coordinates) != 2):
                raise NameError('Invalid format of space description for node (only 2-dimension space is supported');
                
            space_descr.append( [float(val) for val in line[1:].split()] );
            
        
        elif (line[0] == 'm'):
            data_type = type_graph_descr.GRAPH_MATRIX_DESCR;
            data.append( [float(val) for val in line[1:].split()] );
        
        elif (line[0] == 'v'):
            data_type = type_graph_descr.GRAPH_VECTOR_DESCR;
            data.append( [float(val) for val in line[1:].split()] );
            
        elif (len(line.strip()) == 0): continue;
        
        else: 
            print(line);
            raise NameError('Invalid format of file with graph description');
    
    file.close();
    
    if (len(data) != len(space_descr)):
        raise NameError("Invalid format of file with graph - number of nodes is different in space representation and graph description");
    
    return graph(data, data_type, space_descr, comments);


def read_image(filename):
    "Returns image as N-dimension (depends on the input image) matrix, when one element describes pixel"
    
    "(in) filename    - path to image"
    image_source = Image.open(filename);
    data = [pixel for pixel in image_source.getdata()];
    
    del image_source;
    return data;


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
    
    if (x_lim is not None): plt.xlim(x_lim[0], x_lim[1]);
    if (y_lim is not None): plt.ylim(y_lim[0], y_lim[1]);

    plt.grid();
    plt.show();


def draw_image_segments(source, clusters):
    image_source = Image.open(source);
    image_size = image_source.size;
    
    # Calculate edge for confortable representation.
    number_clusters = len(clusters) + 1; # show with the source image
    
    number_cols = int(numpy.ceil(number_clusters ** 0.5));
    number_rows = int(numpy.ceil(number_clusters / number_cols));
    

    real_index = 0, 0;
    double_indexer = True;
    if ( (number_cols == 1) or (number_rows == 1) ):
        real_index = 0;
        double_indexer = False;
    
    (fig, axarr) = plt.subplots(number_rows, number_cols);
    plt.setp([ax for ax in axarr], visible = False);
    
    axarr[real_index].imshow(image_source, interpolation = 'none');
    plt.setp(axarr[real_index], visible = True);
    
    if (double_indexer is True):
        real_index = 0, 1;
    else:
        real_index += 1;
    
    for cluster in clusters:
        stage_cluster = [(255, 255, 255)] * (image_size[0] * image_size[1]);
        for index in cluster:
            stage_cluster[index] = (0, 0, 0);
          
        stage = array(stage_cluster, numpy.uint8);
        stage = numpy.reshape(stage, image_size + ((3),)); # ((3),) it's size of RGB - third dimension.
        
        image_cluster = Image.fromarray(stage, 'RGB');
        
        axarr[real_index].imshow(image_cluster, interpolation = 'none');
        plt.setp(axarr[real_index], visible = True);
        
        if (double_indexer is True):
            real_index = real_index[0], real_index[1] + 1;
            if (real_index[1] >= number_cols):
                real_index = real_index[0] + 1, 0; 
        else:
            real_index += 1;
        
    plt.show();
    
    
def draw_graph(graph_instance, map_coloring = None):
    fig = plt.figure();
    axes = fig.add_subplot(111);
    
    available_colors = ['#00a2e8', '#22b14c', '#ed1c24',
                        '#fff200', '#000000', '#a349a4',
                        '#ffaec9', '#7f7f7f', '#b97a57',
                        '#c8bfe7', '#880015', '#ff7f27',
                        '#3f48cc', '#c3c3c3', '#ffc90e',
                        '#efe4b0', '#b5e61d', '#99d9ea',
                        '#7092b4', '#ffffff'];
              
    if (map_coloring is not None):
        if (len(map_coloring) > len(available_colors)):
            raise NameError('Impossible to represent colored graph due to number of specified colors.');
    
    x_maximum = -numpy.Inf;
    x_minimum = numpy.Inf;
    y_maximum = -numpy.Inf;
    y_minimum = numpy.Inf;
    
    for i in range(0, len(graph_instance.space_description), 1):
        if (graph_instance.type_graph_descr == type_graph_descr.GRAPH_MATRIX_DESCR):
            for j in range(i, len(graph_instance.space_description), 1):    # draw connection between two points only one time
                if (graph_instance.data[i][j] == 1):
                    axes.plot([graph_instance.space_description[i][0], graph_instance.space_description[j][0]], [graph_instance.space_description[i][1], graph_instance.space_description[j][1]], 'k-', linewidth = 1.5);
                    
        elif (graph_instance.type_graph_descr == type_graph_descr.GRAPH_VECTOR_DESCR):
            for j in graph_instance.data[i]:
                if (i > j):     # draw connection between two points only one time
                    axes.plot([graph_instance.space_description[i][0], graph_instance.space_description[j][0]], [graph_instance.space_description[i][1], graph_instance.space_description[j][1]], 'k-', linewidth = 1.5);   
            
        color_node = 'b';
        if (map_coloring is not None):
            color_node = colors.hex2color(available_colors[map_coloring[i]]);
        
        axes.plot(graph_instance.space_description[i][0], graph_instance.space_description[i][1], color = color_node, marker = 'o', markersize = 20);
    
        if (x_maximum < graph_instance.space_description[i][0]): x_maximum = graph_instance.space_description[i][0];
        if (x_minimum > graph_instance.space_description[i][0]): x_minimum = graph_instance.space_description[i][0];  
        if (y_maximum < graph_instance.space_description[i][1]): y_maximum = graph_instance.space_description[i][1]; 
        if (y_minimum > graph_instance.space_description[i][1]): y_minimum = graph_instance.space_description[i][1];
    
    plt.xlim(x_minimum - 0.5, x_maximum + 0.5);
    plt.ylim(y_minimum - 0.5, y_maximum + 0.5);
    
    plt.show();