"""!

@brief Examples of usage and demonstration of abilities of SYNC-SOM algorithm in image segmentation.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from PIL import Image;

from pyclustering.utils import draw_image_mask_segments, read_image, draw_dynamics;
from pyclustering.utils import timedcall;

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES;

from pyclustering.cluster.syncsom import syncsom;

def template_segmentation_image(source, map_som_size = [5, 5], radius = 128.0, sync_order = 0.998, show_dyn = False, show_som_map = False):
    data = read_image(source);
    
    network = syncsom(data, map_som_size[0], map_som_size[1], 1.0);
    (ticks, (dyn_time, dyn_phase)) = timedcall(network.process, show_dyn, sync_order);
    print("Sample: ", source, "\t\tExecution time: ", ticks, "\t\tWinners: ", network.som_layer.get_winner_number(), "\n");
    
    if (show_dyn is True):
        draw_dynamics(dyn_time, dyn_phase);
    
    clusters = network.get_clusters();
    draw_image_mask_segments(source, clusters);
    
    
def segmentation_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, show_dyn = True);
    
def segmentation_image_simple2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE02, show_dyn = True);   
   
def segmentation_image_simple3():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE03, show_dyn = True);
    
def segmentation_image_simple4():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE04, show_dyn = True);
    
def segmentation_image_beach():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH, show_dyn = True);
    
    
segmentation_image_simple1();
segmentation_image_simple2();
segmentation_image_simple3();
segmentation_image_simple4();
segmentation_image_beach();