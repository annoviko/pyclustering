from math import floor;

from PIL import Image;

from support import draw_image_segments, read_image, draw_dynamics, timedcall;

from samples.definitions import IMAGE_SIMPLE_SAMPLES, IMAGE_MAP_SAMPLES;

from clustering.syncnet import syncnet;

from nnet import solve_type;

def template_segmentation_image(source, color_radius, object_radius, noise_size, show_dyn):    
    data = read_image(source);

    network = syncnet(data, color_radius, ccore = True);
    print("Network has been created");
    
    (ticks, (t, dyn)) = timedcall(network.process, 0.998, solve_type.FAST, show_dyn);
    # (t, dyn) = network.process(0.998, solve_type.FAST, show_dyn);
    
    print("Sample: ", source, "\t\tExecution time: ", ticks, "\n");
    
    if (show_dyn is True):
        draw_dynamics(t, dyn);
    
    clusters = network.get_clusters();
    real_clusters = [cluster for cluster in clusters if len(cluster) > noise_size];
    
    draw_image_segments(source, real_clusters);
    
    if (object_radius is None):
        return;
    
    # continue analysis
    pointer_image = Image.open(source);
    image_size = pointer_image.size;
    
    object_colored_clusters = [];
    for cluster in clusters:
        coordinates = [];
        for index in cluster:
            y = floor(index / image_size[0]);
            x = index - y * image_size[0];
            
            coordinates.append([x, y]);
        
        print(coordinates);
        
        # perform clustering analysis of the colored objects
        if (network is not None):
            del network;
            network = None;
        
        if (len(coordinates) < noise_size):
            continue;
        
        network = syncnet(coordinates, object_radius, ccore = True);
        network.process(0.998, solve_type.FAST, False);
        
        object_clusters = network.get_clusters();
        
        # decode it
        real_description_clusters = [];
        for object_cluster in object_clusters:
            real_description = [];
            for index_object in object_cluster:
                real_description.append(cluster[index_object]);
            
            real_description_clusters.append(real_description);
            
            if (len(real_description) > noise_size):
                object_colored_clusters.append(real_description);
            
        # draw_image_segments(source, [ cluster ]);
        # draw_image_segments(source, real_description_clusters);
    
    draw_image_segments(source, object_colored_clusters);
    
def segmentation_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_OBJECT1, 128, None, 10, show_dyn = False);
    
def segmentation_image_simple2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_OBJECT2, 128, None, 10, show_dyn = False);  
    
def segmentation_image_simple3():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_OBJECT3, 128, None, 10, show_dyn = False);
    
def segmentation_image_simple4():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_TWO_COLOR_SET, 128, None, 10, show_dyn = False);
    
def segmentation_image_letters1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_LETTERS1, 128, 4, 10, show_dyn = False);

def segmentation_image_letters2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_THREE_LETTERS2, 128, 4, 10, show_dyn = False);
  
def segmentation_image_beach():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH, 128, None, 10, show_dyn = False);

def segmentation_image_white_sea():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA, 16, None, 50, show_dyn = False);

def segmentation_image_white_sea_small():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA_SMALL, 16, None, 50, show_dyn = False);

segmentation_image_simple1();
segmentation_image_simple2();
segmentation_image_simple3();
segmentation_image_simple4();
segmentation_image_letters1();
segmentation_image_letters2();
segmentation_image_beach();

# segmentation_image_white_sea();    Don't run it - it requires a lot of resources.
segmentation_image_white_sea_small();