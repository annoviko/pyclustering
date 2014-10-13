import time;
import numpy;

from PIL import Image;
from numpy import array;

import matplotlib.pyplot as plt;
from mpl_toolkits.mplot3d import Axes3D;

from sys import platform as _platform;
    

def read_sample(filename):
    "Returns sample for cluster analysis."
    
    "(in) filename        - path to file with data for cluster analysis."
    
    "Returns list of points where each point represented by list of coordinates."
    
    file = open(filename, 'r');

    sample = [[float(val) for val in line.split()] for line in file];
    
    file.close();
    return sample;


def read_image(filename):
    "Returns image as N-dimension (depends on the input image) matrix, where one element of list describes pixel."
    
    "(in) filename        - path to image."
    
    "Return list of pixels where each pixel described by list of RGB-values."
    
    image_source = Image.open(filename);
    data = [pixel for pixel in image_source.getdata()];
    
    del image_source;
    return data;


def rgb2gray(image_rgb_array):
    "Returns image as 1-dimension (gray colored) matrix, where one element of list describes pixel."
    
    "(in) image_rgb_array    - image represented by RGB list."
    
    "Returns image as gray colored matrix, where one element of list describes pixel."
    
    image_gray_array = [0.0] * len(image_rgb_array);
    for index in range(0, len(image_rgb_array), 1):
        image_gray_array[index] = float(image_rgb_array[index][0]) * 0.2989 + float(image_rgb_array[index][1]) * 0.5870 + float(image_rgb_array[index][2]) * 0.1140;
    
    return image_gray_array;
    

def average_neighbor_distance(points, num_neigh):
    "Returns average distance for establish links between specified number of neighbors."
    
    "(in) points        - input data, list of points where each point represented by list."
    
    "Returns average distance for establish links between 'num_neigh' in data set 'points'"
    
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


def heaviside(value):
    if (value >= 0): return 1;
    return 0;


def timedcall(fn, *args):
    "Call function with args; return the time in seconds and result."
    t0 = time.clock();
    result = fn(*args);
    t1 = time.clock();
    return t1 - t0, result;


def extract_number_oscillations(osc_dyn, index = 0, amplitute_threshold = 1.0):
    number_oscillations = 0;
    high_level_trigger = False;
    
    for values in osc_dyn:
        if ( (values[index] > amplitute_threshold) and (high_level_trigger is False) ):
            number_oscillations += 1;
            high_level_trigger = True;
        
        elif ( (values[index] < amplitute_threshold) and (high_level_trigger is True) ):
            high_level_trigger = False;
            
    return number_oscillations;


def draw_clusters(data, clusters, noise = [], marker_descr = '.', hide_axes = False):   
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
        for item in cluster:
            if (dimension == 2):
                if (data is None):
                    axes.plot(item[0], item[1], color + marker_descr);
                else:
                    axes.plot(data[item][0], data[item][1], color + marker_descr);
                    
            elif (dimension == 3):
                if (data is None):
                    axes.scatter(item[0], item[1], item[2], c = color, marker = marker_descr);
                else:
                    axes.scatter(data[item][0], data[item][1], data[item][2], c = color, marker = marker_descr);
        
        color_index += 1;
    
    for item in noise:
        if (dimension == 2):
            if (data is None):
                axes.plot(item[0], item[1], 'w' + marker_descr);
            else:
                axes.plot(data[item][0], data[item][1], 'w' + marker_descr);
                
        elif (dimension == 3):
            if (data is None):
                axes.scatter(item[0], item[1], item[2], c = 'w', marker = marker_descr);
            else:
                axes.scatter(data[item][0], data[item][1], data[item][2], c = 'w', marker = marker_descr);
    
    if (hide_axes is True):
        axes.xaxis.set_ticklabels([]);
        axes.yaxis.set_ticklabels([]);
        
        if (dimension == 3):
            axes.zaxis.set_ticklabels([]);
    
    plt.grid();
    plt.show();

    

def draw_dynamics(t, dyn, x_title = None, y_title = None, x_lim = None, y_lim = None, x_labels = True, y_labels = True, separate = False, axes = None):
    "Draw dynamics of neurons in the network"   
    from matplotlib.font_manager import FontProperties;
    from matplotlib import rcParams;
    
    if (_platform == "linux") or (_platform == "linux2"):
        rcParams['font.sans-serif'] = ['Liberation Serif'];
    else:
        rcParams['font.sans-serif'] = ['Arial'];
        
    rcParams['font.size'] = 12;
    
    number_lines = 0;
    
    if ( (isinstance(separate, bool) is True) and (separate is True) ):
        if (isinstance(dyn[0], list) is True):
            number_lines = len(dyn[0]);
        else:
            number_lines = 1;
            
    elif (isinstance(separate, list) is True):
        number_lines = len(separate);
        
    else:
        number_lines = 1;
    
    dysplay_result = False;
    if (axes is None):
        dysplay_result = True;
        (fig, axes) = plt.subplots(number_lines, 1);
    
    if (number_lines > 1):
        for index_stage in range(number_lines):
            axes[index_stage].get_xaxis().set_visible(False);
            axes[index_stage].get_yaxis().set_visible(False);
    
    surface_font = FontProperties();
    if (_platform == "linux") or (_platform == "linux2"):
        surface_font.set_name('Liberation Serif');
    else:
        surface_font.set_name('Arial');
        
    surface_font.set_size('12');
    
    # Check if we have more than one dynamic
    if (isinstance(dyn[0], list) is True):
        num_items = len(dyn[0]);
        for index in range(0, num_items, 1):       
            y = [item[index] for item in dyn];
            
            if (number_lines > 1): 
                index_stage = -1;
                
                # Find required axes for the y
                if (isinstance(separate, bool) is True):
                    index_stage = index;
                    
                elif (isinstance(separate, list) is True):
                    for index_group in range(0, len(separate), 1):
                        if (index in separate[index_group]): 
                            index_stage = index_group;
                            break;
                
                if (index_stage == -1):
                    raise NameError('Index ' + str(index) + ' is not specified in the separation list.');
                              
                axes[index_stage].plot(t, y, 'b-', linewidth = 0.5); 
                
            else:
                axes.plot(t, y, 'b-', linewidth = 0.5);
    else:
        axes.plot(t, dyn, 'b-', linewidth = 0.5);     

    if (y_title is not None): axes.set_ylabel(y_title, fontproperties = surface_font);
    if (x_title is not None): axes.set_xlabel(x_title, fontproperties = surface_font);
    
    if (x_lim is not None): axes.set_xlim(x_lim[0], x_lim[1]);
    if (y_lim is not None): axes.set_ylim(y_lim[0], y_lim[1]);
    
    if (x_labels is False): axes.xaxis.set_ticklabels([]);
    if (y_labels is False): axes.yaxis.set_ticklabels([]);

    axes.grid(True);
    
    if (dysplay_result is True):
        plt.show();
    
    return axes;


def draw_dynamics_set(dynamics, xtitle = None, ytitle = None, xlim = None, ylim = None, xlabels = False, ylabels = False):
    # Calculate edge for confortable representation.
    number_dynamics = len(dynamics);
    
    number_cols = int(numpy.ceil(number_dynamics ** 0.5));
    number_rows = int(numpy.ceil(number_dynamics / number_cols));
    

    real_index = 0, 0;
    double_indexer = True;
    if ( (number_cols == 1) or (number_rows == 1) ):
        real_index = 0;
        double_indexer = False;
    
    (fig, axarr) = plt.subplots(number_rows, number_cols);
    #plt.setp([ax for ax in axarr], visible = False);
    
    for dynamic in dynamics:
        axarr[real_index] = draw_dynamics(dynamic[0], dynamic[1], xtitle, ytitle, xlim, ylim, xlabels, ylabels, axes = axarr[real_index]);
        #plt.setp(axarr[real_index], visible = True);
        
        if (double_indexer is True):
            real_index = real_index[0], real_index[1] + 1;
            if (real_index[1] >= number_cols):
                real_index = real_index[0] + 1, 0; 
        else:
            real_index += 1;
            
    plt.show();


def draw_image_segments(source, clusters, hide_axes = True):
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
    
    axarr[real_index].xaxis.set_ticklabels([]);
    axarr[real_index].yaxis.set_ticklabels([]);
    axarr[real_index].xaxis.set_ticks_position('none');
    axarr[real_index].yaxis.set_ticks_position('none');
            
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
        
        if (hide_axes is True):
            axarr[real_index].xaxis.set_ticklabels([]);
            axarr[real_index].yaxis.set_ticklabels([]);
            
            axarr[real_index].xaxis.set_ticks_position('none');
            axarr[real_index].yaxis.set_ticks_position('none');
        
        if (double_indexer is True):
            real_index = real_index[0], real_index[1] + 1;
            if (real_index[1] >= number_cols):
                real_index = real_index[0] + 1, 0; 
        else:
            real_index += 1;

            
    plt.show();
    
    
def list_math_subtraction(a, b):
    "Subtraction of two lists. Each element from list 'a' is subtracted by element from list 'b' accordingly."
    
    "(in) a    - list of elements that supports mathematical subtraction."
    "(in) b    - list of elements that supports mathematical subtraction."
    
    "Returns list with results of subtraction of two lists."
    
    return [a[i] - b[i] for i in range(len(a))];


def list_math_substraction_number(a, b):
    "Subtraction between list and number. Each element from list 'a' is subtracted by number 'b'."
    
    "(in) a    - list of elements that supports mathematical subtraction."
    "(in) b    - value that supports mathematical subtraction."
    
    "Returns list with results of subtraction of two lists." 
    
    return [a[i] - b for i in range(len(a))];  


def list_math_addition(a, b):
    "Addition of two lists. Each element from list 'a' is added to element from list 'b' accordingly."
    
    "(in) a    - list of elements that supports mathematic addition."
    "(in) b    - list of elements that supports mathematic addition."
    
    "Returns list with results of addtion of two lists."
    
    return [a[i] + b[i] for i in range(len(a))];


def list_math_addition_number(a, b):
    "Addition between list and number. Each element from list 'a' is added to number 'b'."
    
    "(in) a    - list of elements that supports mathematic addition."
    "(in) b    - value that supports mathematic addition."
    
    "Returns list with results of addtion of two lists."
    
    return [a[i] + b for i in range(len(a))];


def list_math_division_number(a, b):
    "Division between list and number. Each element from list 'a' is divided by number 'b'."
    
    "(in) a    - list of elements that supports mathematic division."
    "(in) b    - value that supports mathematic division."
    
    "Returns list with results of division between list and number."
    
    return [a[i] / b for i in range(len(a))];


def list_math_division(a, b):
    "Division of two lists. Each element from list 'a' is divided by element from list 'b' accordingly."
    
    "(in) a    - list of elements that supports mathematic division."
    "(in) b    - list of elements that supports mathematic division."
    
    "Returns list with results of division of two lists."
    
    return [a[i] / b[i] for i in range(len(a))];


def list_math_multiplication_number(a, b):
    "Multiplication between list and number. Each element from list 'a' is multiplied by number 'b'."
    
    "(in) a    - list of elements that supports mathematic division."
    "(in) b    - number that supports mathematic division."
    
    "Returns list with results of division between list and number."
    
    return [a[i] * b for i in range(len(a))];


def list_math_multiplication(a, b):
    "Multiplication of two lists. Each element from list 'a' is multiplied by element from list 'b' accordingly."
    
    "(in) a    - list of elements that supports mathematic multiplication."
    "(in) b    - number that supports mathematic multiplication."
    
    "Returns list with results of multiplication between list and number."
        
    return [a[i] * b[i] for i in range(len(a))];
 