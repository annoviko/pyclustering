"""!

@brief Examples of usage and demonstration of abilities of DBSCAN algorithm in image segmentation.

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

from math import floor;

from PIL import Image;

from pyclustering.utils import draw_image_mask_segments, draw_image_color_segments, read_image;

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES, IMAGE_MAP_SAMPLES, IMAGE_REAL_SAMPLES;

from pyclustering.cluster.dbscan import dbscan;


def template_segmentation_image(source, color_radius, color_neighbors, object_radius, object_neighbors, noise_size):    
    data = read_image(source);

    dbscan_instance = dbscan(data, color_radius, color_neighbors, True);
    print("Segmentation: '", source, "', Dimensions:", len(data[0]));
    dbscan_instance.process();
    
    clusters = dbscan_instance.get_clusters();
    
    real_clusters = [cluster for cluster in clusters if len(cluster) > noise_size];
    
    print("Draw allocated color segments (back mask representation)...");
    draw_image_mask_segments(source, real_clusters);
    
    print("Draw allocated color segments (color segment representation)...");
    draw_image_color_segments(source, real_clusters);
    
    if (object_radius is None):
        return;
    
    # continue analysis
    pointer_image = Image.open(source);
    image_size = pointer_image.size;
    
    object_colored_clusters = [];
    
    for cluster in clusters:
        coordinates = [];
        for index in cluster:
            y = int(floor(index / image_size[0]));
            x = index - y * image_size[0];
            
            coordinates.append([x, y]);
        
        # perform clustering analysis of the colored objects
        if (len(coordinates) < noise_size):
            continue;
        
        dbscan_instance = dbscan(coordinates, object_radius, object_neighbors, True);
        dbscan_instance.process();
    
        object_clusters = dbscan_instance.get_clusters();
        
        # decode it
        real_description_clusters = [];
        for object_cluster in object_clusters:
            real_description = [];
            for index_object in object_cluster:
                real_description.append(cluster[index_object]);
            
            real_description_clusters.append(real_description);
            
            if (len(real_description) > noise_size):
                object_colored_clusters.append(real_description);
    
    print("Draw allocated object segments (back mask representation)...");
    draw_image_mask_segments(source, object_colored_clusters);
    
    print("Draw allocated object segments (color segment representation)...");
    draw_image_color_segments(source, object_colored_clusters);
    

def segmentation_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, 128, 4, None, None, 10);
    
def segmentation_image_simple2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE02, 128, 4, None, None, 10);  
    
def segmentation_image_simple3():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE03, 128, 4, None, None, 10);
    
def segmentation_image_simple4():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE04, 128, 4, None, None, 10);
    
def segmentation_image_simple5():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE05, 128, 4, 4, 10, 4);

def segmentation_image_simple6():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE06, 128, 4, 4, 10, 4);
  
def segmentation_image_simple7():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE07, 128, 5, 4, 10, 4);
  
def segmentation_image_simple8():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE08, 128, 5, 4, 10, 4);

def segmentation_image_simple9():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE09, 128, 4, 4, 10, 4);

def segmentation_image_simple10():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE10, 128, 5, 4, 10, 4);  

def segmentation_image_simple11():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE11, 64, 10, 4, 10, 4);

def segmentation_image_beach():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH, 128, 4, None, None, 10);
    
def segmentation_image_building():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BUILDING, 16, 10, 10, 10, 10);

def segmentation_image_fruits_small():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_FRUITS_SMALL, 15, 10, 2, 4, 20);

def segmentation_image_white_sea():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA, 8, 16, None, None, 30);

def segmentation_image_white_sea_small():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA_SMALL, 8, 16, None, None, 10);
    
def segmentation_image_nile():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_NILE, 5, 11, None, None, 30);
    
def segmentation_image_nile_small():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_NILE_SMALL, 5, 11, 10, 5, 10);

def segmentation_image_map_buildings():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_BUILDINGS, 8, 10, None, None, 5);

def segmentation_image_flower_field():
    template_segmentation_image(IMAGE_REAL_SAMPLES.IMAGE_FIELD_FLOWER, 8, 8, None, None, 5);

def segmentation_image_tree_field():
    template_segmentation_image(IMAGE_REAL_SAMPLES.IMAGE_FIELD_TREE, 11, 4, None, None, 5);
    

   
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
segmentation_image_simple11();
segmentation_image_beach();
segmentation_image_building();
segmentation_image_fruits_small();
 
segmentation_image_white_sea();
segmentation_image_white_sea_small();
segmentation_image_nile();
segmentation_image_nile_small();
segmentation_image_map_buildings();

segmentation_image_flower_field();
segmentation_image_tree_field();