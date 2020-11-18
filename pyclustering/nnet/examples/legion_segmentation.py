"""!

@brief Examples of usage and demonstration of abilities of LEGION.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from PIL import Image;

from pyclustering.utils import draw_dynamics;
from pyclustering.utils import read_image, rgb2gray, draw_image_mask_segments;

from pyclustering.nnet.legion import legion_network, legion_parameters;
from pyclustering.nnet import *;

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES;

from pyclustering.cluster.dbscan import dbscan;


def template_segmentation_image(image_file, parameters, steps, time, ccore_flag = True):
    image = read_image(image_file);
    stimulus = rgb2gray(image);
    
    for pixel_index in range(len(stimulus)):
        if (stimulus[pixel_index] < 235): stimulus[pixel_index] = 1;
        else: stimulus[pixel_index] = 0;
    
    if (parameters is None):
        parameters = legion_parameters();
    
    net = legion_network(len(stimulus), parameters, conn_type.GRID_FOUR, ccore = ccore_flag);
    output_dynamic = net.simulate(steps, time, stimulus);
    
    ensembles = output_dynamic.allocate_sync_ensembles();
    
    draw_image_mask_segments(image_file, ensembles);
    # draw_dynamics(output_dynamic.time, output_dynamic.output, x_title = "Time", y_title = "x(t)", separate = ensembles);
    
    # just for checking correctness of results - let's use classical algorithm
    dbscan_instance = dbscan(image, 3, 4, True);
    dbscan_instance.process();
    trustable_clusters = dbscan_instance.get_clusters();
    
    draw_dynamics(output_dynamic.time, output_dynamic.output, x_title = "Time", y_title = "x(t)", separate = trustable_clusters);
    

def segmentation_image_simple1():
    "Perfect"
    parameters = legion_parameters();
    parameters.eps = 0.02;
    parameters.alpha = 0.005;
    parameters.betta = 0.1;
    parameters.gamma = 7.0;
    parameters.teta = 0.9;
    parameters.lamda = 0.1;
    parameters.teta_x = -0.5;
    parameters.teta_p = 7.0;
    parameters.Wz = 0.7;
    parameters.mu = 0.01;
    parameters.fi = 3.0;
    parameters.teta_xz = 0.1;
    parameters.teta_zx = 0.1;
    
    parameters.ENABLE_POTENTIONAL = False;
    
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE12, parameters, 2000, 2000, True);


segmentation_image_simple1();