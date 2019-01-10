"""!

@brief  Examples of usage and demonstration of abilities of Pulse Coupled Neural Network in image segmentation.

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
from PIL import Image;

from pyclustering.utils import read_image, rgb2gray, draw_image_mask_segments;

from pyclustering.nnet.pcnn import pcnn_network, pcnn_parameters, pcnn_visualizer;
from pyclustering.nnet import *;

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES, IMAGE_MAP_SAMPLES, IMAGE_REAL_SAMPLES;


def template_segmentation_image(image, parameters, simulation_time, brightness, scale_color = True, fastlinking = False, show_spikes = False, ccore_flag = True):
    image_source = Image.open(image);
    image_size = image_source.size;
    
    width = image_size[0];
    height = image_size[1];
    
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
            if (scale_color is True):
                stimulus[pixel_index] = 1.0 - ((float(stimulus[pixel_index]) - minimum_stimulus) / delta);
            else:
                stimulus[pixel_index] = float(stimulus[pixel_index]) / 255;
    
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
        
        parameters.FAST_LINKING = fastlinking;
    
    net = pcnn_network(len(stimulus), parameters, conn_type.GRID_EIGHT, height = height, width = width, ccore = ccore_flag);
    output_dynamic = net.simulate(simulation_time, stimulus);
    
    pcnn_visualizer.show_output_dynamic(output_dynamic);
    
    ensembles = output_dynamic.allocate_sync_ensembles();
    draw_image_mask_segments(image, ensembles);
    
    pcnn_visualizer.show_time_signal(output_dynamic);
    
    if (show_spikes is True):
        spikes = output_dynamic.allocate_spike_ensembles();
        draw_image_mask_segments(image, spikes);
        
        pcnn_visualizer.animate_spike_ensembles(output_dynamic, image_size);
    
    
def segmentation_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, None, 47, 235);

def segmentation_image_simple2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE02, None, 47, 235);

def segmentation_image_simple6():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE06, None, 47, 128);

def segmentation_image_black_thin_lines1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THIN_BLACK_LINES01, None, 47, 128);

def segmentation_image_black_thin_lines2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THIN_BLACK_LINES02, None, 47, 128);

def segmentation_image_black_thin_lines3():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THIN_BLACK_LINES03, None, 47, 128);

def segmentation_gray_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, None, 47, None, True, False, True);

def segmentation_gray_image_simple5():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE05, None, 47, None, True, False, True);    

def segmentation_gray_image_beach():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH, None, 94, None, True, False, True);    

def segmentation_gray_image_building():
    "Long processing"
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BUILDING, None, 47, None, True, False, True);


def segmentation_fast_linking_image_beach():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH, None, 47, None, False, True, True); 

def segmentation_fast_linking_image_building():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BUILDING, None, 47, None, False, True, True); 

def segmentation_fast_linking_image_fruits():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_FRUITS_SMALL, None, 47, None, False, True, True); 

def segmentation_fast_linking_white_sea():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA_SMALL, None, 47, None, False, True, True); 

def segmentation_fast_linking_nil():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_NILE_SMALL, None, 47, None, False, True, True); 

def segmentation_fast_linking_field_flowers():
    parameters = pcnn_parameters();

    parameters.AF = 0.1;
    parameters.AL = 0.1;
    parameters.AT = 0.8;
    parameters.VF = 1.0;
    parameters.VL = 1.0;
    parameters.VT = 80.0;
    parameters.W = 1.0;
    parameters.M = 1.0;
    
    parameters.FAST_LINKING = True;
    
    template_segmentation_image(IMAGE_REAL_SAMPLES.IMAGE_FIELD_FLOWER, parameters, 80, None, False, True, True); 


# Examples of simple image segmentation
segmentation_image_simple1();
segmentation_image_simple2();
segmentation_image_simple6();

# Line allocation
segmentation_image_black_thin_lines1();
segmentation_image_black_thin_lines2();
segmentation_image_black_thin_lines3();

# More complex image segmentation examples
segmentation_gray_image_simple1();
segmentation_gray_image_simple5();
segmentation_gray_image_beach();
segmentation_gray_image_building();

# Fast linking usage examples
segmentation_fast_linking_image_beach();
segmentation_fast_linking_image_building();
segmentation_fast_linking_image_fruits();
segmentation_fast_linking_white_sea();
segmentation_fast_linking_nil();
segmentation_fast_linking_field_flowers();