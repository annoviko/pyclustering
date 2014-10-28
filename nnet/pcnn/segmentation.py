from support import draw_dynamics;

from nnet.pcnn import pcnn_network, pcnn_parameters;
from nnet import *;

from samples.definitions import IMAGE_SIMPLE_SAMPLES;

from support import read_image, rgb2gray, draw_image_segments;

def template_segmentation_image(image, parameters, simulation_time, brightness):
    stimulus = read_image(image);
    stimulus = rgb2gray(stimulus);
    
    if (brightness != None):
        for pixel_index in range(len(stimulus)):
            if (stimulus[pixel_index] < brightness): stimulus[pixel_index] = 1;
            else: stimulus[pixel_index] = 0;
    else:
        maximum_stimulus = float(max(stimulus));
        minimum_stimulus = float(min(stimulus));
        delta = maximum_stimulus - minimum_stimulus;
        
        for pixel_index in range(len(stimulus)):
            stimulus[pixel_index] = 1.0 - ((float(stimulus[pixel_index]) - minimum_stimulus) / delta);
    
    if (parameters is None):
        parameters = pcnn_parameters();
    
        parameters.AF = 0.1;
        parameters.AL = 0.1;
        parameters.AT = 0.8;
        parameters.VF = 1.0;
        parameters.VL = 1.0;
        parameters.VT = 30.0;
        parameters.W = 1.0;
        parameters.M = 1.0;
    
    net = pcnn_network(len(stimulus), stimulus, parameters, conn_type.GRID_EIGHT);
    (t, y) = net.simulate(simulation_time, None, None, True);
    
    draw_dynamics(t, y, x_title = "Time", y_title = "y(t)");
    
    ensembles = net.allocate_sync_ensembles();
    draw_image_segments(image, ensembles);
    
def segmentation_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, None, 47, 235);
    
def segmentation_image_simple2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE02, None, 47, 235);

def segmentation_image_simple6():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE06, None, 47, 128);
    
def segmentation_image_beach():
    "Long processing"
    parameters = pcnn_parameters();
    
    parameters.AF = 0.1;
    parameters.AL = 0.1;
    parameters.AT = 0.8;
    parameters.VF = 1.0;
    parameters.VL = 1.0;
    parameters.VT = 30.0;
    parameters.W = 1.0;
    parameters.M = 1.0;
        
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BUILDING, parameters, 47, None);


segmentation_image_simple1();
segmentation_image_simple2();
segmentation_image_simple6();
segmentation_image_beach();