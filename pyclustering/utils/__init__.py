"""!

@brief Utils that are used by modules of pyclustering.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""

import time
import numpy
import warnings

from numpy import array

try:
    from PIL import Image
except Exception as error_instance:
    warnings.warn("Impossible to import PIL (please, install 'PIL'), pyclustering's visualization "
                  "functionality is partially not available (details: '%s')." % str(error_instance))

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))

from sys import platform as _platform

from pyclustering.utils.metric import distance_metric, type_metric


## The number \f$pi\f$ is a mathematical constant, the ratio of a circle's circumference to its diameter.
pi = 3.1415926535


def read_sample(filename):
    """!
    @brief Returns data sample from simple text file.
    @details This function should be used for text file with following format:
    @code
    point_1_coord_1 point_1_coord_2 ... point_1_coord_n
    point_2_coord_1 point_2_coord_2 ... point_2_coord_n
    ... ...
    @endcode
    
    @param[in] filename (string): Path to file with data.
    
    @return (list) Points where each point represented by list of coordinates.
    
    """
    
    file = open(filename, 'r')

    sample = [[float(val) for val in line.split()] for line in file if len(line.strip()) > 0]
    
    file.close()
    return sample


def calculate_distance_matrix(sample, metric=distance_metric(type_metric.EUCLIDEAN)):
    """!
    @brief Calculates distance matrix for data sample (sequence of points) using specified metric (by default Euclidean distance).

    @param[in] sample (array_like): Data points that are used for distance calculation.
    @param[in] metric (distance_metric): Metric that is used for distance calculation between two points.

    @return (list) Matrix distance between data points.

    """

    amount_rows = len(sample)
    return [[metric(sample[i], sample[j]) for j in range(amount_rows)] for i in range(amount_rows)]


def read_image(filename):
    """!
    @brief Returns image as N-dimension (depends on the input image) matrix, where one element of list describes pixel.
    
    @param[in] filename (string): Path to image.
    
    @return (list) Pixels where each pixel described by list of RGB-values.
    
    """
    
    with Image.open(filename) as image_source:
        data = [list(pixel) for pixel in image_source.getdata()]
        return data


def rgb2gray(image_rgb_array):
    """!
    @brief Returns image as 1-dimension (gray colored) matrix, where one element of list describes pixel.
    @details Luma coding is used for transformation and that is calculated directly from gamma-compressed primary intensities as a weighted sum:
    
    \f[Y = 0.2989R + 0.587G + 0.114B\f]
    
    @param[in] image_rgb_array (list): Image represented by RGB list.
    
    @return (list) Image as gray colored matrix, where one element of list describes pixel.
    
    @code
        colored_image = read_image(file_name);
        gray_image = rgb2gray(colored_image);
    @endcode
    
    @see read_image()
    
    """
    
    image_gray_array = [0.0] * len(image_rgb_array);
    for index in range(0, len(image_rgb_array), 1):
        image_gray_array[index] = float(image_rgb_array[index][0]) * 0.2989 + float(image_rgb_array[index][1]) * 0.5870 + float(image_rgb_array[index][2]) * 0.1140;
    
    return image_gray_array;


def stretch_pattern(image_source):
    """!
    @brief Returns stretched content as 1-dimension (gray colored) matrix with size of input image.
    
    @param[in] image_source (Image): PIL Image instance.
    
    @return (list, Image) Stretched image as gray colored matrix and source image.
    
    """
    wsize, hsize = image_source.size;
    
    # Crop digit exactly
    (ws, hs, we, he) = gray_pattern_borders(image_source);
    image_source = image_source.crop((ws, hs, we, he));
    
    # Stretch it to initial sizes
    image_source = image_source.resize((wsize, hsize), Image.ANTIALIAS);
    
    # Transform image to simple array
    data = [pixel for pixel in image_source.getdata()];
    image_pattern = rgb2gray(data);
    
    return (image_pattern, image_source);


def gray_pattern_borders(image):
    """!
    @brief Returns coordinates of gray image content on the input image.
    
    @param[in] image (Image): PIL Image instance that is processed.
    
    @return (tuple) Returns coordinates of gray image content as (width_start, height_start, width_end, height_end).
    
    """
    
    width, height = image.size;
    
    width_start = width;
    width_end = 0;
    height_start = height;
    height_end = 0;
    
    row, col = 0, 0;
    for pixel in image.getdata():
        value = float(pixel[0]) * 0.2989 + float(pixel[1]) * 0.5870 + float(pixel[2]) * 0.1140;
        
        if (value < 128):
            if (width_end < col): 
                width_end = col;
            
            if (height_end < row):
                height_end = row;
        
            if (width_start > col):
                width_start = col;
            
            if (height_start > row):
                height_start = row;
        
        col += 1;
        if (col >= width):
            col = 0;
            row += 1;

    return (width_start, height_start, width_end + 1, height_end + 1);


def average_neighbor_distance(points, num_neigh):
    """!
    @brief Returns average distance for establish links between specified number of nearest neighbors.
    
    @param[in] points (list): Input data, list of points where each point represented by list.
    @param[in] num_neigh (uint): Number of neighbors that should be used for distance calculation.
    
    @return (double) Average distance for establish links between 'num_neigh' in data set 'points'.
    
    """
    
    if num_neigh > len(points) - 1:
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
        # start from 0 - first element is distance to itself.
        for j in range(0, num_neigh, 1):
            total_distance += dist_matrix[i][j + 1];
            
    return ( total_distance / (num_neigh * len(points)) );


def medoid(data, indexes=None, **kwargs):
    """!
    @brief Calculate medoid for input points using Euclidean distance.
    
    @param[in] data (list): Set of points for that median should be calculated.
    @param[in] indexes (list): Indexes of input set of points that will be taken into account during median calculation.
    @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric', 'data_type').

    <b>Keyword Args:</b><br>
        - metric (distance_metric): Metric that is used for distance calculation between two points.
        - data_type (string): Data type of input sample 'data' (available values: 'points', 'distance_matrix').

    @return (uint) index of point in input set that corresponds to median.
    
    """
    
    index_median = None
    distance = float('Inf')

    metric = kwargs.get('metric', type_metric.EUCLIDEAN_SQUARE)
    data_type = kwargs.get('data_type', 'points')

    if data_type == 'points':
        calculator = lambda index1, index2: metric(data[index1], data[index2])
    elif data_type == 'distance_matrix':
        if isinstance(data, numpy.matrix):
            calculator = lambda index1, index2: data.item(index1, index2)

        else:
            calculator = lambda index1, index2: data[index1][index2]
    else:
        raise TypeError("Unknown type of data is specified '%s'." % data_type)

    if indexes is None:
        range_points = range(len(data))
    else:
        range_points = indexes
    
    for index_candidate in range_points:
        distance_candidate = 0.0
        for index in range_points:
            distance_candidate += calculator(index_candidate, index)
        
        if distance_candidate < distance:
            distance = distance_candidate
            index_median = index_candidate
    
    return index_median


def euclidean_distance(a, b):
    """!
    @brief Calculate Euclidean distance between vector a and b. 
    @details The Euclidean between vectors (points) a and b is calculated by following formula:
    
    \f[
    dist(a, b) = \sqrt{ \sum_{i=0}^{N}(b_{i} - a_{i})^{2}) };
    \f]
    
    Where N is a length of each vector.
    
    @param[in] a (list): The first vector.
    @param[in] b (list): The second vector.
    
    @return (double) Euclidian distance between two vectors.
    
    @note This function for calculation is faster then standard function in ~100 times!
    
    """
    
    distance = euclidean_distance_square(a, b);
    return distance**(0.5);


def euclidean_distance_square(a, b):
    """!
    @brief Calculate square Euclidian distance between vector a and b.
    
    @param[in] a (list): The first vector.
    @param[in] b (list): The second vector.
    
    @return (double) Square Euclidian distance between two vectors.
    
    """  
    
    if ( ((type(a) == float) and (type(b) == float)) or ((type(a) == int) and (type(b) == int)) ):
        return (a - b)**2.0;
    
    distance = 0.0;
    for i in range(0, len(a)):
        distance += (a[i] - b[i])**2.0;
        
    return distance;


def manhattan_distance(a, b):
    """!
    @brief Calculate Manhattan distance between vector a and b.
    
    @param[in] a (list): The first cluster.
    @param[in] b (list): The second cluster.
    
    @return (double) Manhattan distance between two vectors.
    
    """
    
    if ( ((type(a) == float) and (type(b) == float)) or ((type(a) == int) and (type(b) == int)) ):
        return abs(a - b);
    
    distance = 0.0;
    dimension = len(a);
    
    for i in range(0, dimension):
        distance += abs(a[i] - b[i]);
    
    return distance;


def average_inter_cluster_distance(cluster1, cluster2, data = None):
    """!
    @brief Calculates average inter-cluster distance between two clusters.
    @details Clusters can be represented by list of coordinates (in this case data shouldn't be specified),
             or by list of indexes of points from the data (represented by list of points), in this case 
             data should be specified.
             
    @param[in] cluster1 (list): The first cluster where each element can represent index from the data or object itself.
    @param[in] cluster2 (list): The second cluster where each element can represent index from the data or object itself.
    @param[in] data (list): If specified than elements of clusters will be used as indexes,
               otherwise elements of cluster will be considered as points.
    
    @return (double) Average inter-cluster distance between two clusters.
    
    """
    
    distance = 0.0;
    
    if (data is None):
        for i in range(len(cluster1)):
            for j in range(len(cluster2)):
                distance += euclidean_distance_square(cluster1[i], cluster2[j]);
    else:
        for i in range(len(cluster1)):
            for j in range(len(cluster2)):
                distance += euclidean_distance_square(data[ cluster1[i]], data[ cluster2[j]]);
    
    distance /= float(len(cluster1) * len(cluster2));
    return distance ** 0.5;


def average_intra_cluster_distance(cluster1, cluster2, data=None):
    """!
    @brief Calculates average intra-cluster distance between two clusters.
    @details Clusters can be represented by list of coordinates (in this case data shouldn't be specified),
             or by list of indexes of points from the data (represented by list of points), in this case 
             data should be specified.
    
    @param[in] cluster1 (list): The first cluster.
    @param[in] cluster2 (list): The second cluster.
    @param[in] data (list): If specified than elements of clusters will be used as indexes,
               otherwise elements of cluster will be considered as points.
    
    @return (double) Average intra-cluster distance between two clusters.
    
    """
        
    distance = 0.0
    
    for i in range(len(cluster1) + len(cluster2)):
        for j in range(len(cluster1) + len(cluster2)):
            if data is None:
                # the first point
                if i < len(cluster1):
                    first_point = cluster1[i]
                else:
                    first_point = cluster2[i - len(cluster1)]
                
                # the second point
                if j < len(cluster1):
                    second_point = cluster1[j]
                else:
                    second_point = cluster2[j - len(cluster1)]
                
            else:
                # the first point
                if i < len(cluster1):
                    first_point = data[cluster1[i]]
                else:
                    first_point = data[cluster2[i - len(cluster1)]]
            
                if j < len(cluster1):
                    second_point = data[cluster1[j]]
                else:
                    second_point = data[cluster2[j - len(cluster1)]]
            
            distance += euclidean_distance_square(first_point, second_point)
    
    distance /= float((len(cluster1) + len(cluster2)) * (len(cluster1) + len(cluster2) - 1.0))
    return distance ** 0.5


def variance_increase_distance(cluster1, cluster2, data = None):
    """!
    @brief Calculates variance increase distance between two clusters.
    @details Clusters can be represented by list of coordinates (in this case data shouldn't be specified),
             or by list of indexes of points from the data (represented by list of points), in this case 
             data should be specified.
    
    @param[in] cluster1 (list): The first cluster.
    @param[in] cluster2 (list): The second cluster.
    @param[in] data (list): If specified than elements of clusters will be used as indexes,
               otherwise elements of cluster will be considered as points.
    
    @return (double) Average variance increase distance between two clusters.
    
    """
    
    # calculate local sum
    if data is None:
        member_cluster1 = [0.0] * len(cluster1[0])
        member_cluster2 = [0.0] * len(cluster2[0])
        
    else:
        member_cluster1 = [0.0] * len(data[0])
        member_cluster2 = [0.0] * len(data[0])
    
    for i in range(len(cluster1)):
        if data is None:
            member_cluster1 = list_math_addition(member_cluster1, cluster1[i])
        else:
            member_cluster1 = list_math_addition(member_cluster1, data[ cluster1[i] ])

    for j in range(len(cluster2)):
        if data is None:
            member_cluster2 = list_math_addition(member_cluster2, cluster2[j])
        else:
            member_cluster2 = list_math_addition(member_cluster2, data[ cluster2[j] ])
    
    member_cluster_general = list_math_addition(member_cluster1, member_cluster2)
    member_cluster_general = list_math_division_number(member_cluster_general, len(cluster1) + len(cluster2))
    
    member_cluster1 = list_math_division_number(member_cluster1, len(cluster1))
    member_cluster2 = list_math_division_number(member_cluster2, len(cluster2))
    
    # calculate global sum
    distance_general = 0.0
    distance_cluster1 = 0.0
    distance_cluster2 = 0.0
    
    for i in range(len(cluster1)):
        if data is None:
            distance_cluster1 += euclidean_distance_square(cluster1[i], member_cluster1)
            distance_general += euclidean_distance_square(cluster1[i], member_cluster_general)
            
        else:
            distance_cluster1 += euclidean_distance_square(data[ cluster1[i]], member_cluster1)
            distance_general += euclidean_distance_square(data[ cluster1[i]], member_cluster_general)
    
    for j in range(len(cluster2)):
        if data is None:
            distance_cluster2 += euclidean_distance_square(cluster2[j], member_cluster2)
            distance_general += euclidean_distance_square(cluster2[j], member_cluster_general)
            
        else:
            distance_cluster2 += euclidean_distance_square(data[ cluster2[j]], member_cluster2)
            distance_general += euclidean_distance_square(data[ cluster2[j]], member_cluster_general)
    
    return distance_general - distance_cluster1 - distance_cluster2


def calculate_ellipse_description(covariance, scale = 2.0):
    """!
    @brief Calculates description of ellipse using covariance matrix.
    
    @param[in] covariance (numpy.array): Covariance matrix for which ellipse area should be calculated.
    @param[in] scale (float): Scale of the ellipse.
    
    @return (float, float, float) Return ellipse description: angle, width, height.
    
    """
    
    eigh_values, eigh_vectors = numpy.linalg.eigh(covariance)
    order = eigh_values.argsort()[::-1]
    
    values, vectors = eigh_values[order], eigh_vectors[order]
    angle = numpy.degrees(numpy.arctan2(*vectors[:,0][::-1]))

    if 0.0 in values:
        return 0, 0, 0

    width, height = 2.0 * scale * numpy.sqrt(values)
    return angle, width, height


def data_corners(data, data_filter = None):
    """!
    @brief Finds maximum and minimum corner in each dimension of the specified data.
    
    @param[in] data (list): List of points that should be analysed.
    @param[in] data_filter (list): List of indexes of the data that should be analysed,
                if it is 'None' then whole 'data' is analysed to obtain corners.
    
    @return (list) Tuple of two points that corresponds to minimum and maximum corner (min_corner, max_corner).
    
    """
    
    dimensions = len(data[0])
    
    bypass = data_filter
    if bypass is None:
        bypass = range(len(data))
    
    maximum_corner = list(data[bypass[0]][:])
    minimum_corner = list(data[bypass[0]][:])
    
    for index_point in bypass:
        for index_dimension in range(dimensions):
            if data[index_point][index_dimension] > maximum_corner[index_dimension]:
                maximum_corner[index_dimension] = data[index_point][index_dimension]
            
            if data[index_point][index_dimension] < minimum_corner[index_dimension]:
                minimum_corner[index_dimension] = data[index_point][index_dimension]
    
    return minimum_corner, maximum_corner


def norm_vector(vector):
    """!
    @brief Calculates norm of an input vector that is known as a vector length.
    
    @param[in] vector (list): The input vector whose length is calculated.
    
    @return (double) vector norm known as vector length.
    
    """
    
    length = 0.0
    for component in vector:
        length += component * component
    
    length = length ** 0.5
    
    return length


def heaviside(value):
    """!
    @brief Calculates Heaviside function that represents step function.
    @details If input value is greater than 0 then returns 1, otherwise returns 0.
    
    @param[in] value (double): Argument of Heaviside function.
    
    @return (double) Value of Heaviside function.
    
    """
    if (value > 0.0): 
        return 1.0;
    
    return 0.0;


def timedcall(executable_function, *args):
    """!
    @brief Executes specified method or function with measuring of execution time.
    
    @param[in] executable_function (pointer): Pointer to function or method.
    @param[in] args (*): Arguments of called function or method.
    
    @return (tuple) Execution time and result of execution of function or method (execution_time, result_execution).
    
    """
    
    time_start = time.clock();
    result = executable_function(*args);
    time_end = time.clock();
    
    return (time_end - time_start, result);


def extract_number_oscillations(osc_dyn, index = 0, amplitude_threshold = 1.0):
    """!
    @brief Extracts number of oscillations of specified oscillator.
    
    @param[in] osc_dyn (list): Dynamic of oscillators.
    @param[in] index (uint): Index of oscillator in dynamic.
    @param[in] amplitude_threshold (double): Amplitude threshold when oscillation is taken into account, for example,
                when oscillator amplitude is greater than threshold then oscillation is incremented.
    
    @return (uint) Number of oscillations of specified oscillator.
    
    """
    
    number_oscillations = 0;
    waiting_differential = False;
    threshold_passed = False;
    high_level_trigger = True if (osc_dyn[0][index] > amplitude_threshold) else False;
    
    for values in osc_dyn:
        if ( (values[index] >= amplitude_threshold) and (high_level_trigger is False) ):
            high_level_trigger = True;
            threshold_passed = True;
        
        elif ( (values[index] < amplitude_threshold) and (high_level_trigger is True) ):
            high_level_trigger = False;
            threshold_passed = True;
        
        if (threshold_passed is True):
            threshold_passed = False;
            if (waiting_differential is True and high_level_trigger is False):
                number_oscillations += 1;
                waiting_differential = False;

            else:
                waiting_differential = True;
        
    return number_oscillations;


def allocate_sync_ensembles(dynamic, tolerance = 0.1, threshold = 1.0, ignore = None):
    """!
    @brief Allocate clusters in line with ensembles of synchronous oscillators where each
           synchronous ensemble corresponds to only one cluster.
    
    @param[in] dynamic (dynamic): Dynamic of each oscillator.
    @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
    @param[in] threshold (double): Amlitude trigger when spike is taken into account.
    @param[in] ignore (bool): Set of indexes that shouldn't be taken into account.
    
    @return (list) Grours (lists) of indexes of synchronous oscillators, for example, 
            [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
            
    """
    
    descriptors = [ [] for _ in range(len(dynamic[0])) ];
    
    # Check from the end for obtaining result
    for index_dyn in range(0, len(dynamic[0]), 1):
        if ((ignore is not None) and (index_dyn in ignore)):
            continue;
        
        time_stop_simulation = len(dynamic) - 1;
        active_state = False;
        
        if (dynamic[time_stop_simulation][index_dyn] > threshold):
            active_state = True;
            
        # if active state is detected, it means we don't have whole oscillatory period for the considered oscillator, should be skipped.
        if (active_state is True):
            while ( (dynamic[time_stop_simulation][index_dyn] > threshold) and (time_stop_simulation > 0) ):
                time_stop_simulation -= 1;
            
            # if there are no any oscillation than let's consider it like noise
            if (time_stop_simulation == 0):
                continue;
            
            # reset
            active_state = False;
        
        desc = [0, 0, 0]; # end, start, average time of oscillation
        for t in range(time_stop_simulation, 0, -1):
            if ( (dynamic[t][index_dyn] > threshold) and (active_state is False) ):
                desc[0] = t;
                active_state = True;
            elif ( (dynamic[t][index_dyn] < threshold) and (active_state is True) ):
                desc[1] = t;
                active_state = False;
                
                break;
        
        if (desc == [0, 0, 0]):
            continue;
        
        desc[2] = desc[1] + (desc[0] - desc[1]) / 2.0;
        descriptors[index_dyn] = desc;
    
    
    # Cluster allocation
    sync_ensembles = [];
    desc_sync_ensembles = [];
    
    for index_desc in range(0, len(descriptors), 1):
        if (descriptors[index_desc] == []):
            continue;
        
        if (len(sync_ensembles) == 0):
            desc_ensemble = descriptors[index_desc];
            reducer = (desc_ensemble[0] - desc_ensemble[1]) * tolerance;
            
            desc_ensemble[0] = desc_ensemble[2] + reducer;
            desc_ensemble[1] = desc_ensemble[2] - reducer;
            
            desc_sync_ensembles.append(desc_ensemble);
            sync_ensembles.append([ index_desc ]);
        else:
            oscillator_captured = False;
            for index_ensemble in range(0, len(sync_ensembles), 1):
                if ( (desc_sync_ensembles[index_ensemble][0] > descriptors[index_desc][2]) and (desc_sync_ensembles[index_ensemble][1] < descriptors[index_desc][2])):
                    sync_ensembles[index_ensemble].append(index_desc);
                    oscillator_captured = True;
                    break;
                
            if (oscillator_captured is False):
                desc_ensemble = descriptors[index_desc];
                reducer = (desc_ensemble[0] - desc_ensemble[1]) * tolerance;
        
                desc_ensemble[0] = desc_ensemble[2] + reducer;
                desc_ensemble[1] = desc_ensemble[2] - reducer;
        
                desc_sync_ensembles.append(desc_ensemble);
                sync_ensembles.append([ index_desc ]);
    
    return sync_ensembles;
    
    
def draw_clusters(data, clusters, noise = [], marker_descr = '.', hide_axes = False, axes = None, display_result = True):
    """!
    @brief Displays clusters for data in 2D or 3D.
    
    @param[in] data (list): Points that are described by coordinates represented.
    @param[in] clusters (list): Clusters that are represented by lists of indexes where each index corresponds to point in data.
    @param[in] noise (list): Points that are regarded to noise.
    @param[in] marker_descr (string): Marker for displaying points.
    @param[in] hide_axes (bool): If True - axes is not displayed.
    @param[in] axes (ax) Matplotlib axes where clusters should be drawn, if it is not specified (None) then new plot will be created.
    @param[in] display_result (bool): If specified then matplotlib axes will be used for drawing and plot will not be shown.
    
    @return (ax) Matplotlib axes where drawn clusters are presented.
    
    """
    # Get dimension
    dimension = 0;
    if ( (data is not None) and (clusters is not None) ):
        dimension = len(data[0]);
    elif ( (data is None) and (clusters is not None) ):
        dimension = len(clusters[0][0]);
    else:
        raise NameError('Data or clusters should be specified exactly.');
    
    "Draw clusters"
    colors = [ 'red', 'blue', 'darkgreen', 'brown', 'violet', 
               'deepskyblue', 'darkgrey', 'lightsalmon', 'deeppink', 'yellow',
               'black', 'mediumspringgreen', 'orange', 'darkviolet', 'darkblue',
               'silver', 'lime', 'pink', 'gold', 'bisque' ];
               
    if (len(clusters) > len(colors)):
        raise NameError('Impossible to represent clusters due to number of specified colors.');
    
    fig = plt.figure();
    
    if (axes is None):
        # Check for dimensions
        if ((dimension) == 1 or (dimension == 2)):
            axes = fig.add_subplot(111);
        elif (dimension == 3):
            axes = fig.gca(projection='3d');
        else:
            raise NameError('Drawer supports only 2d and 3d data representation');
    
    color_index = 0;
    for cluster in clusters:
        color = colors[color_index];
        for item in cluster:
            if (dimension == 1):
                if (data is None):
                    axes.plot(item[0], 0.0, color = color, marker = marker_descr);
                else:
                    axes.plot(data[item][0], 0.0, color = color, marker = marker_descr);
            
            if (dimension == 2):
                if (data is None):
                    axes.plot(item[0], item[1], color = color, marker = marker_descr);
                else:
                    axes.plot(data[item][0], data[item][1], color = color, marker = marker_descr);
                    
            elif (dimension == 3):
                if (data is None):
                    axes.scatter(item[0], item[1], item[2], c = color, marker = marker_descr);
                else:
                    axes.scatter(data[item][0], data[item][1], data[item][2], c = color, marker = marker_descr);
        
        color_index += 1;
    
    for item in noise:
        if (dimension == 1):
            if (data is None):
                axes.plot(item[0], 0.0, 'w' + marker_descr);
            else:
                axes.plot(data[item][0], 0.0, 'w' + marker_descr);

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
    
    axes.grid(True);
    
    if (hide_axes is True):
        axes.xaxis.set_ticklabels([]);
        axes.yaxis.set_ticklabels([]);
        
        if (dimension == 3):
            axes.zaxis.set_ticklabels([]);
    
    if (display_result is True):
        plt.show();

    return axes;


def draw_dynamics(t, dyn, x_title = None, y_title = None, x_lim = None, y_lim = None, x_labels = True, y_labels = True, separate = False, axes = None):
    """!
    @brief Draw dynamics of neurons (oscillators) in the network.
    @details It draws if matplotlib is not specified (None), othewise it should be performed manually.
    
    @param[in] t (list): Values of time (used by x axis).
    @param[in] dyn (list): Values of output of oscillators (used by y axis).
    @param[in] x_title (string): Title for Y.
    @param[in] y_title (string): Title for X.
    @param[in] x_lim (double): X limit.
    @param[in] y_lim (double): Y limit.
    @param[in] x_labels (bool): If True - shows X labels.
    @param[in] y_labels (bool): If True - shows Y labels.
    @param[in] separate (list): Consists of lists of oscillators where each such list consists of oscillator indexes that will be shown on separated stage.
    @param[in] axes (ax): If specified then matplotlib axes will be used for drawing and plot will not be shown.
    
    @return (ax) Axes of matplotlib.
    
    """
         
    number_lines = 0;
    
    stage_xlim = None;
    if (x_lim is not None):
        stage_xlim = x_lim;
    elif (len(t) > 0):
        stage_xlim = [0, t[len(t) - 1]];
    
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
                
                if (index_stage != -1):
                    if (index_stage != number_lines - 1):
                        axes[index_stage].get_xaxis().set_visible(False);
                              
                    axes[index_stage].plot(t, y, 'b-', linewidth = 0.5); 
                    set_ax_param(axes[index_stage], x_title, y_title, stage_xlim, y_lim, x_labels, y_labels, True);
                
            else:
                axes.plot(t, y, 'b-', linewidth = 0.5);
                set_ax_param(axes, x_title, y_title, stage_xlim, y_lim, x_labels, y_labels, True);
    else:
        axes.plot(t, dyn, 'b-', linewidth = 0.5);
        set_ax_param(axes, x_title, y_title, stage_xlim, y_lim, x_labels, y_labels, True);
    
    if (dysplay_result is True):
        plt.show();
    
    return axes;


def set_ax_param(ax, x_title = None, y_title = None, x_lim = None, y_lim = None, x_labels = True, y_labels = True, grid = True):
    """!
    @brief Sets parameters for matplotlib ax.
    
    @param[in] ax (Axes): Axes for which parameters should applied.
    @param[in] x_title (string): Title for Y.
    @param[in] y_title (string): Title for X.
    @param[in] x_lim (double): X limit.
    @param[in] y_lim (double): Y limit.
    @param[in] x_labels (bool): If True - shows X labels.
    @param[in] y_labels (bool): If True - shows Y labels.
    @param[in] grid (bool): If True - shows grid.
    
    """
    from matplotlib.font_manager import FontProperties;
    from matplotlib import rcParams;
    
    if (_platform == "linux") or (_platform == "linux2"):
        rcParams['font.sans-serif'] = ['Liberation Serif'];
    else:
        rcParams['font.sans-serif'] = ['Arial'];
        
    rcParams['font.size'] = 12;
        
    surface_font = FontProperties();
    if (_platform == "linux") or (_platform == "linux2"):
        surface_font.set_name('Liberation Serif');
    else:
        surface_font.set_name('Arial');
        
    surface_font.set_size('12');
    
    if (y_title is not None): ax.set_ylabel(y_title, fontproperties = surface_font);
    if (x_title is not None): ax.set_xlabel(x_title, fontproperties = surface_font);
    
    if (x_lim is not None): ax.set_xlim(x_lim[0], x_lim[1]);
    if (y_lim is not None): ax.set_ylim(y_lim[0], y_lim[1]);
    
    if (x_labels is False): ax.xaxis.set_ticklabels([]);
    if (y_labels is False): ax.yaxis.set_ticklabels([]);
    
    ax.grid(grid);


def draw_dynamics_set(dynamics, xtitle = None, ytitle = None, xlim = None, ylim = None, xlabels = False, ylabels = False):
    """!
    @brief Draw lists of dynamics of neurons (oscillators) in the network.
    
    @param[in] dynamics (list): List of network outputs that are represented by values of output of oscillators (used by y axis).
    @param[in] xtitle (string): Title for Y.
    @param[in] ytitle (string): Title for X.
    @param[in] xlim (double): X limit.
    @param[in] ylim (double): Y limit.
    @param[in] xlabels (bool): If True - shows X labels.
    @param[in] ylabels (bool): If True - shows Y labels.
    
    """
    # Calculate edge for confortable representation.
    number_dynamics = len(dynamics);
    if (number_dynamics == 1):
        draw_dynamics(dynamics[0][0], dynamics[0][1], xtitle, ytitle, xlim, ylim, xlabels, ylabels);
        return;
    
    number_cols = int(numpy.ceil(number_dynamics ** 0.5));
    number_rows = int(numpy.ceil(number_dynamics / number_cols));

    real_index = 0, 0;
    double_indexer = True;
    if ( (number_cols == 1) or (number_rows == 1) ):
        real_index = 0;
        double_indexer = False;
    
    (_, axarr) = plt.subplots(number_rows, number_cols);
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


def draw_image_color_segments(source, clusters, hide_axes = True):
    """!
    @brief Shows image segments using colored image.
    @details Each color on result image represents allocated segment. The first image is initial and other is result of segmentation.
    
    @param[in] source (string): Path to image.
    @param[in] clusters (list): List of clusters (allocated segments of image) where each cluster
                                consists of indexes of pixel from source image.
    @param[in] hide_axes (bool): If True then axes will not be displayed.
    
    """
        
    image_source = Image.open(source);
    image_size = image_source.size;
    
    (fig, axarr) = plt.subplots(1, 2);
    
    plt.setp([ax for ax in axarr], visible = False);
    
    available_colors = [ (0, 162, 232),   (34, 177, 76),   (237, 28, 36),
                         (255, 242, 0),   (0, 0, 0),       (237, 28, 36),
                         (255, 174, 201), (127, 127, 127), (185, 122, 87), 
                         (200, 191, 231), (136, 0, 21),    (255, 127, 39),
                         (63, 72, 204),   (195, 195, 195), (255, 201, 14),
                         (239, 228, 176), (181, 230, 29),  (153, 217, 234),
                         (112, 146, 180) ];
    
    image_color_segments = [(255, 255, 255)] * (image_size[0] * image_size[1]);
    
    for index_segment in range(len(clusters)):
        for index_pixel in clusters[index_segment]:
            image_color_segments[index_pixel] = available_colors[index_segment];
    
    stage = array(image_color_segments, numpy.uint8);
    stage = numpy.reshape(stage, (image_size[1], image_size[0]) + ((3),)); # ((3),) it's size of RGB - third dimension.
    image_cluster = Image.fromarray(stage, 'RGB');
    
    axarr[0].imshow(image_source, interpolation = 'none');
    axarr[1].imshow(image_cluster, interpolation = 'none');
    
    for i in range(2):
        plt.setp(axarr[i], visible = True);
        
        if (hide_axes is True):
            axarr[i].xaxis.set_ticklabels([]);
            axarr[i].yaxis.set_ticklabels([]);
            axarr[i].xaxis.set_ticks_position('none');
            axarr[i].yaxis.set_ticks_position('none');
    
    plt.show();


def draw_image_mask_segments(source, clusters, hide_axes = True):
    """!
    @brief Shows image segments using black masks.
    @details Each black mask of allocated segment is presented on separate plot.
             The first image is initial and others are black masks of segments.
    
    @param[in] source (string): Path to image.
    @param[in] clusters (list): List of clusters (allocated segments of image) where each cluster
                                consists of indexes of pixel from source image.
    @param[in] hide_axes (bool): If True then axes will not be displayed.
    
    """
    if (len(clusters) == 0):
        print("Warning: Nothing to draw - list of clusters is empty.")
        return;
        
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
    
    if (hide_axes is True):
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
        stage = numpy.reshape(stage, (image_size[1], image_size[0]) + ((3),)); # ((3),) it's size of RGB - third dimension.
        
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


def linear_sum(list_vector):
    """!
    @brief Calculates linear sum of vector that is represented by list, each element can be represented by list - multidimensional elements.
    
    @param[in] list_vector (list): Input vector.
    
    @return (list|double) Linear sum of vector that can be represented by list in case of multidimensional elements.
    
    """
    dimension = 1
    linear_sum = 0.0
    list_representation = (type(list_vector[0]) == list)
    
    if list_representation is True:
        dimension = len(list_vector[0])
        linear_sum = [0] * dimension
        
    for index_element in range(0, len(list_vector)):
        if (list_representation is True):
            for index_dimension in range(0, dimension):
                linear_sum[index_dimension] += list_vector[index_element][index_dimension]
        else:
            linear_sum += list_vector[index_element]

    return linear_sum


def square_sum(list_vector):
    """!
    @brief Calculates square sum of vector that is represented by list, each element can be represented by list - multidimensional elements.
    
    @param[in] list_vector (list): Input vector.
    
    @return (double) Square sum of vector.
    
    """
    
    square_sum = 0.0
    list_representation = (type(list_vector[0]) == list)
        
    for index_element in range(0, len(list_vector)):
        if list_representation is True:
            square_sum += sum(list_math_multiplication(list_vector[index_element], list_vector[index_element]))
        else:
            square_sum += list_vector[index_element] * list_vector[index_element]
         
    return square_sum

    
def list_math_subtraction(a, b):
    """!
    @brief Calculates subtraction of two lists.
    @details Each element from list 'a' is subtracted by element from list 'b' accordingly.
    
    @param[in] a (list): List of elements that supports mathematical subtraction.
    @param[in] b (list): List of elements that supports mathematical subtraction.
    
    @return (list) Results of subtraction of two lists.
    
    """
    return [a[i] - b[i] for i in range(len(a))];


def list_math_substraction_number(a, b):
    """!
    @brief Calculates subtraction between list and number.
    @details Each element from list 'a' is subtracted by number 'b'.
    
    @param[in] a (list): List of elements that supports mathematical subtraction.
    @param[in] b (list): Value that supports mathematical subtraction.
    
    @return (list) Results of subtraction between list and number.
    
    """        
    return [a[i] - b for i in range(len(a))];  


def list_math_addition(a, b):
    """!
    @brief Addition of two lists.
    @details Each element from list 'a' is added to element from list 'b' accordingly.
    
    @param[in] a (list): List of elements that supports mathematic addition..
    @param[in] b (list): List of elements that supports mathematic addition..
    
    @return (list) Results of addtion of two lists.
    
    """    
    return [a[i] + b[i] for i in range(len(a))];


def list_math_addition_number(a, b):
    """!
    @brief Addition between list and number.
    @details Each element from list 'a' is added to number 'b'.
    
    @param[in] a (list): List of elements that supports mathematic addition.
    @param[in] b (double): Value that supports mathematic addition.
    
    @return (list) Result of addtion of two lists.
    
    """    
    return [a[i] + b for i in range(len(a))];


def list_math_division_number(a, b):
    """!
    @brief Division between list and number.
    @details Each element from list 'a' is divided by number 'b'.
    
    @param[in] a (list): List of elements that supports mathematic division.
    @param[in] b (double): Value that supports mathematic division.
    
    @return (list) Result of division between list and number.
    
    """    
    return [a[i] / b for i in range(len(a))];


def list_math_division(a, b):
    """!
    @brief Division of two lists.
    @details Each element from list 'a' is divided by element from list 'b' accordingly.
    
    @param[in] a (list): List of elements that supports mathematic division.
    @param[in] b (list): List of elements that supports mathematic division.
    
    @return (list) Result of division of two lists.
    
    """    
    return [a[i] / b[i] for i in range(len(a))];


def list_math_multiplication_number(a, b):
    """!
    @brief Multiplication between list and number.
    @details Each element from list 'a' is multiplied by number 'b'.
    
    @param[in] a (list): List of elements that supports mathematic division.
    @param[in] b (double): Number that supports mathematic division.
    
    @return (list) Result of division between list and number.
    
    """    
    return [a[i] * b for i in range(len(a))];


def list_math_multiplication(a, b):
    """!
    @brief Multiplication of two lists.
    @details Each element from list 'a' is multiplied by element from list 'b' accordingly.
    
    @param[in] a (list): List of elements that supports mathematic multiplication.
    @param[in] b (list): List of elements that supports mathematic multiplication.
    
    @return (list) Result of multiplication of elements in two lists.
    
    """        
    return [a[i] * b[i] for i in range(len(a))];
