from PIL import Image;

from support import draw_image_segments, read_image, draw_dynamics;
from support import timedcall;

from samples.definitions import IMAGE_SIMPLE_SAMPLES;

from syncsom import syncsom;

def template_segmentation_image(source, map_som_size = [5, 5], average_neighbors = 5, sync_order = 0.998, show_dyn = False, show_som_map = False):
    data = read_image(source);
    
    network = syncsom(data, map_som_size[0], map_som_size[1]);
    (ticks, (dyn_time, dyn_phase)) = timedcall(network.process, average_neighbors, show_dyn, sync_order);
    print("Sample: ", source, "\t\tExecution time: ", ticks, "\t\tWinners: ", network.som_layer.get_winner_number(), "\n");
    
    if (show_dyn is True):
        draw_dynamics(dyn_time, dyn_phase);
    
    clusters = network.get_clusters();
    draw_image_segments(source, clusters);
    
    
def segmentation_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_OBJECT1);
    
def segmentation_image_simple2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_OBJECT2);   
   
def segmentation_image_simple3():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_OBJECT3);
    
def segmentation_image_simple4():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_TWO_COLOR_SET);
    
segmentation_image_simple1();
segmentation_image_simple2();
segmentation_image_simple3();
segmentation_image_simple4();