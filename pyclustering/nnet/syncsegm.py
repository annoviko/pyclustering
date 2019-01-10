"""!

@brief Double-layer oscillatory network with phase oscillator for image segmentation.
@details Implementation based on paper @cite inproceedings::nnet::syncsegm::1.
         
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

import warnings

from math import floor

try:
    from PIL import Image
except Exception as error_instance:
    warnings.warn("Impossible to import PIL (please, install 'PIL'), pyclustering's visualization "
                  "functionality is partially not available (details: '%s')." % str(error_instance))

from pyclustering.cluster.syncnet import syncnet

from pyclustering.nnet import solve_type, initial_type
from pyclustering.nnet.sync import sync_visualizer

from pyclustering.utils import read_image


class syncsegm_visualizer:
    """!
    @brief Result visualizer of double-layer oscillatory network 'syncsegm'.
    
    """
    
    @staticmethod
    def show_first_layer_dynamic(analyser):
        """!
        @brief Shows output dynamic of the first layer.
        
        @param[in] analyser (syncsegm_analyser): Analyser of output dynamic of the 'syncsegm' oscillatory network.
        
        """
        
        sync_visualizer.show_output_dynamic(analyser.get_first_layer_analyser());
    
    
    @staticmethod
    def show_second_layer_dynamic(analyser):
        """!
        @brief Shows output dynamic of the second layer.
        
        @param[in] analyser (syncsegm_analyser): Analyser of output dynamic of the 'syncsegm' oscillatory network.
        
        """
        
        second_layer_analysers = analyser.get_second_layer_analysers();
        analysers_sequence = [ object_segment_analyser['analyser'] for object_segment_analyser in second_layer_analysers ]
        
        sync_visualizer.show_output_dynamics(analysers_sequence);


class syncsegm_analyser:
    """!
    @brief Performs analysis of output dynamic of the double-layer oscillatory network 'syncsegm' to extract information about segmentation results.
    
    """
    
    def __init__(self, color_analyser, object_segment_analysers = None):
        """!
        @brief Constructor of the analyser.
        
        @param[in] color_analyser (list): Analyser of coloring segmentation results of the first layer.
        @param[in] object_segment_analysers (list): Analysers of objects on image segments - results of the second layer.
        
        """
        
        self.__color_analyser = color_analyser;
        self.__object_segment_analysers = object_segment_analysers;
    
    
    def get_first_layer_analyser(self):
        """!
        @brief Returns analyser of coloring segmentation of the first layer.
        
        """
        
        return self.__color_analyser;
    
    
    def get_second_layer_analysers(self):
        """!
        @brief Returns analysers of object segmentation of the second layer.
        
        """
        
        return self.__object_segment_analysers;
    
    
    def allocate_colors(self, eps = 0.01, noise_size = 1):
        """!
        @brief Allocates color segments.
        
        @param[in] eps (double): Tolerance level that define maximal difference between phases of oscillators in one segment.
        @param[in] noise_size (uint): Threshold that defines noise - segments size (in pixels) that is less then the threshold is considered as a noise.
        
        @return (list) Color segments where each color segment consists of indexes of pixels that forms color segment.
        
        """
        
        segments = self.__color_analyser.allocate_clusters(eps);
        real_segments = [cluster for cluster in segments if len(cluster) > noise_size];
        return real_segments;
    
    
    def allocate_objects(self, eps = 0.01, noise_size = 1):
        """!
        @brief Allocates object segments.
        
        @param[in] eps (double): Tolerance level that define maximal difference between phases of oscillators in one segment.
        @param[in] noise_size (uint): Threshold that defines noise - segments size (in pixels) that is less then the threshold is considered as a noise.
        
        @return (list) Object segments where each object segment consists of indexes of pixels that forms object segment.
        
        """
        
        if (self.__object_segment_analysers is None):
            return [];
        
        segments = [];
        for object_segment_analyser in self.__object_segment_analysers:
            indexes = object_segment_analyser['color_segment'];
            analyser = object_segment_analyser['analyser'];
            
            segments += analyser.allocate_clusters(eps, indexes);
        
        real_segments = [segment for segment in segments if len(segment) > noise_size];
        return real_segments;


class syncsegm:
    """!
    @brief Class represents segmentation algorithm syncsegm. 
    @details syncsegm is a bio-inspired algorithm that is based on double-layer oscillatory network that uses modified Kuramoto model.
             Algorithm extracts colors and colored objects. It uses only CCORE (C++ implementation of pyclustering) parts to implement the algorithm.
    
             CCORE option is True by default to use sync network in the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
    Example:
    @code
        # create oscillatory for image segmentaion - extract colors (radius 128) and objects (radius 4), 
        # and ignore noise (segments with size that is less than 10 pixels)
        algorithm = syncsegm(128, 4, 10);
        
        # extract segments (colors and objects)
        analyser = algorithm(path_to_file);
        
        # obtain segmentation results (only colors - from the first layer)
        color_segments = analyser.allocate_colors(0.01, 10);
        draw_image_mask_segments(path_to_file, color_segments);
        
        # obtain segmentation results (objects - from the second layer)
        object_segments = analyser.allocate_objects(0.01, 10);
        draw_image_mask_segments(path_to_file, object_segments);
    @endcode
    
    """
    
    def __init__(self, color_radius, object_radius, noise_size = 0, ccore = True):
        """!
        @brief Contructor of the oscillatory network SYNC for cluster analysis.
        
        @param[in] color_radius (double): Radius of color connectivity (color similarity) for the first layer.
        @param[in] object_radius (double): Radius of object connectivity (object similarity) for the second layer,
                   if 'None' then object segmentation is not performed (only color segmentation).
        @param[in] noise_size (double): Size of segment that should be considered as a noise and ignored by the second layer.
        @param[in] ccore (bool): If 'True' then C/C++ implementation is used to increase performance.
        
        """
        
        self.__color_radius     = color_radius;
        self.__object_radius    = object_radius;
        self.__noise_size       = noise_size;
        
        self.__order_color      = 0.9995;
        self.__order_object     = 0.999;
        
        self.__network  = None;
        self.__ccore    = ccore;
    
    
    def process(self, image_source, collect_dynamic = False, order_color = 0.9995, order_object = 0.999):
        """!
        @brief Performs image segmentation.
        
        @param[in] image_source (string): Path to image file that should be processed.
        @param[in] collect_dynamic (bool): If 'True' then whole dynamic of each layer of the network is collected.
        @param[in] order_color (double): Local synchronization order for the first layer - coloring segmentation.
        @param[in] order_object (double): Local synchronization order for the second layer - object segmentation.
        
        @return (syncsegm_analyser) Analyser of segmentation results by the network.
        
        """
        
        self.__order_color  = order_color
        self.__order_object = order_object
        
        data = read_image(image_source)
        color_analyser = self.__analyse_colors(data, collect_dynamic)
        
        if self.__object_radius is None:
            return syncsegm_analyser(color_analyser, None)
    
        object_segment_analysers = self.__analyse_objects(image_source, color_analyser, collect_dynamic)
        return syncsegm_analyser(color_analyser, object_segment_analysers)
    
    
    def __analyse_colors(self, image_data, collect_dynamic):
        """!
        @brief Performs color segmentation by the first layer.
        
        @param[in] image_data (array_like): Image sample as a array-like structure.
        @param[in] collect_dynamic (bool): If 'True' then whole dynamic of the first layer of the network is collected.
        
        @return (syncnet_analyser) Analyser of color segmentation results of the first layer.
        
        """
        
        network = syncnet(image_data, self.__color_radius, initial_phases = initial_type.RANDOM_GAUSSIAN, ccore = self.__ccore);
        analyser = network.process(self.__order_color, solve_type.FAST, collect_dynamic);
        
        return analyser;
    
    
    def __analyse_objects(self, image_source, color_analyser, collect_dynamic):
        """!
        @brief Performs object segmentation by the second layer.
        
        @param[in] image_source (string): Path to image file that should be processed.
        @param[in] color_analyser (syncnet_analyser): Analyser of color segmentation results.
        @param[in] collect_dynamic (bool): If 'True' then whole dynamic of the first layer of the network is collected.
        
        @return (map) Analysers of object segments.
        
        """
        
        # continue analysis
        pointer_image = Image.open(image_source);
        image_size = pointer_image.size;
        
        object_analysers = [];
        
        color_segments = color_analyser.allocate_clusters();
        
        for segment in color_segments:
            object_analyser = self.__analyse_color_segment(image_size, segment, collect_dynamic);
            if (object_analyser is not None):
                object_analysers.append( { 'color_segment': segment, 'analyser': object_analyser } );
    
        pointer_image.close();
        return object_analysers;
    
    
    def __analyse_color_segment(self, image_size, color_segment, collect_dynamic):
        """!
        @brief Performs object segmentation of separate segment.
        
        @param[in] image_size (list): Image size presented as a [width x height].
        @param[in] color_segment (list): Image segment that should be processed.
        @param[in] collect_dynamic (bool): If 'True' then whole dynamic of the second layer of the network is collected.
        
        @return (syncnet_analyser) Analyser of object segmentation results of the second layer.
        
        """
        coordinates = self.__extract_location_coordinates(image_size, color_segment);
        
        if (len(coordinates) < self.__noise_size):
            return None;
        
        network = syncnet(coordinates, self.__object_radius, initial_phases = initial_type.EQUIPARTITION, ccore = True);
        analyser = network.process(self.__order_object, solve_type.FAST, collect_dynamic);
        
        return analyser;
    
    
    def __extract_location_coordinates(self, image_size, color_segment):
        """!
        @brief Extracts coordinates of specified image segment.
        
        @param[in] image_size (list): Image size presented as a [width x height].
        @param[in] color_segment (list): Image segment whose coordinates should be extracted.
        
        @return (list) Coordinates of each pixel.
        
        """
        coordinates = [];
        for index in color_segment:
            y = floor(index / image_size[0]);
            x = index - y * image_size[0];
            
            coordinates.append([x, y]);
        
        return coordinates;
        