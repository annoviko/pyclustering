from math import floor;

from PIL import Image;

from support import draw_image_segments, read_image, draw_dynamics, draw_dynamics_set, timedcall;

from samples.definitions import IMAGE_SIMPLE_SAMPLES, IMAGE_MAP_SAMPLES;

from clustering.syncnet import syncnet;

from nnet import solve_type;

def template_segmentation_image(source, color_radius, object_radius, noise_size, show_dyn):    
    data = read_image(source);

    network = syncnet(data, color_radius, ccore = True);
    print("Network has been created");
    
    (ticks, (t, dyn)) = timedcall(network.process, 0.9995, solve_type.FAST, show_dyn);
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
    object_colored_dynamics = [];
    total_dyn = [];
    
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
        (t, dyn) = network.process(0.999, solve_type.FAST, show_dyn);
        
        if (show_dyn is True):
            object_colored_dynamics.append( (t, dyn) );
        
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
    
    if (show_dyn is True):
        draw_dynamics_set(object_colored_dynamics, None, None, None, [0, 2 * 3.14], False, False);
    
    
    
def memory_measurement(source, radius):
    import time;
    
    data = read_image(source);
    
    print("Network is created");
    #network = syncnet(data, radius, ccore = True);
    #del network;
    #network = syncnet(data, radius, ccore = True);
    time.sleep(15);
    
    print("Network is destoyed");
    #del network;
    
    time.sleep(15);
    
def segmentation_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, 128, None, 10, show_dyn = False);
    
def segmentation_image_simple2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE02, 128, None, 10, show_dyn = False);  
    
def segmentation_image_simple3():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE03, 128, None, 10, show_dyn = False);
    
def segmentation_image_simple4():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE04, 128, None, 10, show_dyn = False);
    
def segmentation_image_simple5():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE05, 128, 4, 10, show_dyn = False);

def segmentation_image_simple6():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE06, 128, 4, 10, show_dyn = True);
  
def segmentation_image_simple7():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE07, 128, 5, 10, show_dyn = False);
  
def segmentation_image_simple8():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE08, 128, 5, 10, show_dyn = False);

def segmentation_image_simple9():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE09, 128, 4, 10, show_dyn = False);

def segmentation_image_simple10():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE10, 128, 5, 10, show_dyn = False);  

def segmentation_image_beach():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH, 128, None, 10, show_dyn = False);

def segmentation_image_white_sea():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA, 16, None, 50, show_dyn = False);

def segmentation_image_white_sea_small():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA_SMALL, 20, None, 50, show_dyn = False);
    
def segmentation_image_nile():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_NILE, 16, None, 50, show_dyn = False);
    
def segmentation_image_nile_small():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_NILE_SMALL, 50, None, 50, show_dyn = False);

# memory_measurement(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, 128);
# memory_measurement(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA_SMALL, 16);

segmentation_image_simple1();
segmentation_image_simple2();
segmentation_image_simple3();
segmentation_image_simple4();
segmentation_image_simple5();
segmentation_image_simple6();
segmentation_image_simple7();
segmentation_image_simple8();
segmentation_image_simple9();
segmentation_image_simple10();
segmentation_image_beach();
 
segmentation_image_white_sea();
segmentation_image_white_sea_small();
segmentation_image_nile();
segmentation_image_nile_small();