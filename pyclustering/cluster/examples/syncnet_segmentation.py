"""!

@brief Examples of usage and demonstration of abilities of Sync algorithm in image segmentation.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2015
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

from math import floor;

from PIL import Image;

from pyclustering.utils import draw_image_mask_segments, read_image, draw_dynamics, draw_dynamics_set, timedcall;

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES, IMAGE_MAP_SAMPLES;

from pyclustering.cluster.syncnet import syncnet;

from pyclustering.nnet import solve_type;
from pyclustering.nnet.sync import sync_visualizer;


def template_segmentation_image(source, color_radius, object_radius, noise_size, show_dyn):    
    data = read_image(source);
    print("Pixel dimension: ", len(data[0]));

    network = syncnet(data, color_radius, ccore = True);
    print("Network has been created");
    
    (ticks, analyser) = timedcall(network.process, 0.9995, solve_type.FAST, show_dyn);
    
    print("Sample: ", source, "\t\tExecution time: ", ticks, "\n");
    
    if (show_dyn is True):
        sync_visualizer.show_output_dynamic(analyser);
    
    clusters = analyser.allocate_clusters();
    real_clusters = [cluster for cluster in clusters if len(cluster) > noise_size];
    
    draw_image_mask_segments(source, real_clusters);
    
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
        analyser = network.process(0.999, solve_type.FAST, show_dyn);
        
        if (show_dyn is True):
            object_colored_dynamics.append( (analyser.time, analyser.output) );
        
        object_clusters = analyser.allocate_clusters();
        
        # decode it
        real_description_clusters = [];
        for object_cluster in object_clusters:
            real_description = [];
            for index_object in object_cluster:
                real_description.append(cluster[index_object]);
            
            real_description_clusters.append(real_description);
            
            if (len(real_description) > noise_size):
                object_colored_clusters.append(real_description);
            
        # draw_image_mask_segments(source, [ cluster ]);
        # draw_image_mask_segments(source, real_description_clusters);
    
    draw_image_mask_segments(source, object_colored_clusters);
    
    if (show_dyn is True):
        draw_dynamics_set(object_colored_dynamics, None, None, None, [0, 2 * 3.14], False, False);
    
    
    
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
    
def segmentation_image_building():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BUILDING, 16, 10, 10, show_dyn = False);

def segmentation_image_fruits_small():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_FRUITS_SMALL, 16, 4, 20, show_dyn = False);

def segmentation_image_white_sea():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA, 16, None, 50, show_dyn = False);

def segmentation_image_white_sea_small():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA_SMALL, 20, None, 50, show_dyn = False);
    
def segmentation_image_nile():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_NILE, 16, None, 50, show_dyn = False);
    
def segmentation_image_nile_small():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_NILE_SMALL, 50, None, 50, show_dyn = False);


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
segmentation_image_building();
segmentation_image_fruits_small();
 
segmentation_image_white_sea();
segmentation_image_white_sea_small();
segmentation_image_nile();
segmentation_image_nile_small();