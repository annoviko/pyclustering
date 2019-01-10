"""!

@brief Templates for tests of SyncPR (oscillatory network based on Kuramoto model for pattern recognition).

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


# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.tests.assertion import assertion

from pyclustering.nnet.syncsegm import syncsegm, syncsegm_visualizer

from pyclustering.utils import draw_image_mask_segments


class SyncsegmTestTemplates:
    @staticmethod
    def templateSyncsegmSegmentation(image_source, radius_color, radius_object, noise_size, expected_color_segments, expected_object_segments, collect_dynamic, ccore_flag):
        result_testing = False
        color_segments, object_segments = [], []

        for _ in range(0, 10, 1):
            algorithm = syncsegm(radius_color, radius_object, noise_size, ccore=ccore_flag)
            analyser = algorithm.process(image_source, collect_dynamic, 0.9995, 0.9995)
            
            color_segments = analyser.allocate_colors()
            object_segments = analyser.allocate_objects(0.2)

            if (len(color_segments) != expected_color_segments) or (len(object_segments) != expected_object_segments):
                continue
            
            result_testing = True
            break

        assertion.eq(expected_color_segments, len(color_segments))
        assertion.eq(expected_object_segments, len(object_segments))
        assertion.true(result_testing)


    @staticmethod
    def templateSyncsegmVisulizationNoFailure(image_source, radius_color, radius_object, noise_size, expected_color_segments, expected_object_segments, collect_dynamic, ccore_flag):
        algorithm = syncsegm(radius_color, radius_object, noise_size, ccore=ccore_flag)
        analyser = algorithm.process(image_source, collect_dynamic, 0.9995, 0.9995)
        
        color_segments = analyser.allocate_colors(0.01, noise_size)
        draw_image_mask_segments(image_source, color_segments)
        
        object_segments = analyser.allocate_objects(0.01, noise_size)
        draw_image_mask_segments(image_source, object_segments)
        
        syncsegm_visualizer.show_first_layer_dynamic(analyser)
        syncsegm_visualizer.show_second_layer_dynamic(analyser)