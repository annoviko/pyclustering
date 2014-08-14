from PIL import Image;

from support import draw_image_segments, read_image;

from samples.definitions import IMAGE_SIMPLE_SAMPLES;

from clustering.syncnet import syncnet;

from nnet import solve_type;

def template_segmentation_image(source, show_dyn):    
    data = read_image(source);

    network = syncnet(data, 50, ccore = True);
    network.process(0.998, solve_type.FAST, False);
    clusters = network.get_clusters();
    
    draw_image_segments(source, clusters);
    
def segmentation_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_OBJECT1, show_dyn = False);
    
def segmentation_image_simple2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_OBJECT2, show_dyn = False);  
    
def segmentation_image_simple3():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_OBJECT3, show_dyn = False);
    
def segmentation_image_simple4():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_TWO_COLOR_SET, show_dyn = False);
    
def segmentation_image_beach():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH, show_dyn = False);
    
segmentation_image_simple1();
segmentation_image_simple2();
segmentation_image_simple3();
segmentation_image_simple4();
segmentation_image_beach();