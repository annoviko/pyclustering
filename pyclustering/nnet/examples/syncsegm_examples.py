"""!

@brief Examples of usage and demonstration of abilities of multi-layer oscillatory network based on Kuramoto model for image segmentation.

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


from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES, IMAGE_MAP_SAMPLES

from pyclustering.nnet.syncsegm import syncsegm, syncsegm_visualizer

from pyclustering.utils import draw_image_mask_segments


def template_segmentation_image(source, color_radius, object_radius, noise_size, show_dyn):
    algorithm = syncsegm(color_radius, object_radius, noise_size, False)
    analyser = algorithm.process(source, show_dyn)
    
    color_segments = analyser.allocate_colors(0.01, noise_size)
    draw_image_mask_segments(source, color_segments)
    
    if object_radius is not None:
        object_segments = analyser.allocate_objects(0.01, noise_size)
        draw_image_mask_segments(source, object_segments)
    
    if show_dyn is True:
        syncsegm_visualizer.show_first_layer_dynamic(analyser)
        syncsegm_visualizer.show_second_layer_dynamic(analyser)


def segmentation_image_simple1():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, 128, None, 10, show_dyn = False)
    
def segmentation_image_simple2():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE02, 128, None, 10, show_dyn = False)
    
def segmentation_image_simple3():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE03, 128, None, 10, show_dyn = False)
    
def segmentation_image_simple4():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE04, 128, None, 10, show_dyn = False)
    
def segmentation_image_simple5():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE05, 128, 4, 10, show_dyn = False)

def segmentation_image_simple6():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE06, 128, 4, 10, show_dyn = True)
  
def segmentation_image_simple7():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE07, 128, 5, 10, show_dyn = False)
  
def segmentation_image_simple8():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE08, 128, 5, 10, show_dyn = False)

def segmentation_image_simple9():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE09, 128, 4, 10, show_dyn = False)

def segmentation_image_simple10():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE10, 128, 5, 10, show_dyn = False)

def segmentation_image_beach():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BEACH, 128, None, 10, show_dyn = False)
    
def segmentation_image_building():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_BUILDING, 16, 10, 10, show_dyn = False)

def segmentation_image_fruits_small():
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE_FRUITS_SMALL, 16, 4, 20, show_dyn = False)

def segmentation_image_white_sea():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA, 16, None, 50, show_dyn = False)

def segmentation_image_white_sea_small():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA_SMALL, 20, None, 50, show_dyn = False)
    
def segmentation_image_nile():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_NILE, 16, None, 50, show_dyn = False)
    
def segmentation_image_nile_small():
    template_segmentation_image(IMAGE_MAP_SAMPLES.IMAGE_NILE_SMALL, 50, None, 50, show_dyn = False)


segmentation_image_simple1()
segmentation_image_simple2()
segmentation_image_simple3()
segmentation_image_simple4()
segmentation_image_simple5()
segmentation_image_simple6()
segmentation_image_simple7()
segmentation_image_simple8()
segmentation_image_simple9()
segmentation_image_simple10()
segmentation_image_beach()
segmentation_image_building()
segmentation_image_fruits_small()
 
segmentation_image_white_sea()
segmentation_image_white_sea_small()
segmentation_image_nile()
segmentation_image_nile_small()