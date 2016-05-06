"""!

@brief Unit-test for double-layer oscillatory network 'syncsegm' for image segmentation based on Kuramoto model.

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

import unittest;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.nnet.syncsegm import syncsegm, syncsegm_visualizer;

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES;


class Test(unittest.TestCase):
    def templatesyncsegmSegmentation(self, image_source, radius_color, radius_object, noise_size, expected_color_segments, expected_object_segments, collect_dynamic):
        result_testing = False;
        
        for _ in range(0, 3, 1):
            algorithm = syncsegm(radius_color, radius_object, noise_size);
            analyser = algorithm.process(image_source, collect_dynamic, 0.9995, 0.9995);
            
            color_segments = analyser.allocate_colors();
            object_segments = analyser.allocate_objects(0.2);
            
            if ( (len(color_segments) != expected_color_segments) or (len(object_segments) != expected_object_segments) ):
                continue;
            
            if (collect_dynamic is True):
                syncsegm_visualizer.show_first_layer_dynamic(analyser);
                syncsegm_visualizer.show_second_layer_dynamic(analyser);
            
            result_testing = True;
            break;
        
        assert result_testing;
    
    
    def testImageSegmentationSimple13(self):
        self.templatesyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE13, 225, 5, 0, 2, 4, False);
    
    def testImageSegmentationSimple15(self):
        self.templatesyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE15, 225, 6, 0, 2, 3, False);
    
    def testImageSegmentationSimple16(self):
        self.templatesyncsegmSegmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE16, 225, 2, 0, 2, 3, True);
    
if __name__ == "__main__":
    unittest.main();