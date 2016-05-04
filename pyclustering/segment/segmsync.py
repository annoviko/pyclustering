"""!

@brief Segmentation algorithm based on multi-layer oscillatory network with phase oscillator.
@details Implementation based on article:
         - A.Novikov, E.Benderskaya. Oscillatory Network Based on Kuramoto Model for Image Segmentation. 2015.
         
@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

from pyclustering.cluster.syncnet import syncnet;

from pyclustering.nnet import solve_type;

from pyclustering.utils import read_image;


class segmsync_analyser:
    def __init__(self, color_analyser, object_segment_analysers = None):
        self.__color_analyser = color_analyser;
        self.__object_segment_analysers = object_segment_analysers;
    
    
    def allocate_colors(self, noise_size):
        segments = self.__color_analyser.allocate_clusters();
        real_segments = [cluster for cluster in segments if len(cluster) > noise_size];
        return real_segments;
    
    
    def allocate_objects(self, eps = 0.01, noise_size):
        if (self.__object_segment_analysers is None):
            return [];
        
        segments = [];
        for object_segment_analyser in self.__object_segment_analysers:
            indexes = object_segment_analyser['color_segment'];
            analyser = object_segment_analyser['analyser'];
            
            segments += analyser.allocate_clusters(eps, indexes);
        
        real_segments = [segment for segment in segments if len(segment) > noise_size];
        return real_segments;


class segmsync:
    def __init__(self, color_radius, object_radius, noise_size):
        self.__color_radius     = color_radius;
        self.__object_radius    = object_radius;
        self.__noise_size       = noise_size;
        
        self.__network = None;
    
    
    def process(self, image_source, collect_dynamic = False):
        data = read_image(image_source);
        color_analyser = self.__analyse_colors(data, collect_dynamic);
        
        if (self.__object_radius is None):
            return segmsync_analyser(color_analyser, None);
    
        object_segment_analysers = self.__analyse_objects(data, color_analyser, collect_dynamic);
        return segmsync_analyser(color_analyser, object_segment_analysers);
    
    
    def __analyse_colors(self, image_source, collect_dynamic):
        network = syncnet(image_source, self.__color_radius, ccore = True);
        analyser = network.process(0.9995, solve_type.FAST, collect_dynamic);
        
        return analyser;
    
    
    def __analyse_objects(self, image_source, color_analyser, collect_dynamic):
        # continue analysis
        pointer_image = Image.open(image_source);
        image_size = pointer_image.size;
        
        object_analysers = [];
        
        color_segments = color_analyser.allocate_clusters();
        
        for segment in color_segments:
            object_analyser = self.__analyse_color_segment(image_size, segment, collect_dynamic);
            object_analysers.append( { 'color_segment': segment, 'analyser': object_analyser } );
    
        return object_analysers;
    
    
    def __analyse_color_segment(self, image_size, color_segment, collect_dynamic):
        coordinates = self.__extract_location_coordinates(image_size, color_segment);
        
        if (len(coordinates) < self.__noise_size):
            return None;
        
        network = syncnet(coordinates, self.__object_radius, ccore = True);
        analyser = network.process(0.999, solve_type.FAST, collect_dynamic);
        
        return analyser;
    
    
    def __extract_location_coordinates(self, image_size, color_segment):
        coordinates = [];
        for index in color_segment:
            y = floor(index / image_size[0]);
            x = index - y * image_size[0];
            
            coordinates.append([x, y]);
        
        return coordinates;
        