"""!

@brief Examples of usage and demonstration of abilities of LEGION.

@authors Andrei Novikov (spb.andr@yandex.ru)
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

from PIL import Image;

from pyclustering.support import draw_dynamics;

from pyclustering.nnet.legion import legion_network, legion_parameters;
from pyclustering.nnet import *;

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES;

from pyclustering.support import read_image, rgb2gray, draw_image_mask_segments;


def template_segmentation_image(image, parameters, steps, time, ccore_flag = True):
    stimulus = read_image(image);
    stimulus = rgb2gray(stimulus);
    
    for pixel_index in range(len(stimulus)):
        if (stimulus[pixel_index] < 235): stimulus[pixel_index] = 1;
        else: stimulus[pixel_index] = 0;
    
    if (parameters is None):
        parameters = legion_parameters();
    
    net = legion_network(len(stimulus), parameters, conn_type.GRID_FOUR, ccore = ccore_flag);
    output_dynamic = net.simulate(steps, time, stimulus);
    
    ensembles = output_dynamic.allocate_sync_ensembles();
    
    draw_image_mask_segments(image, ensembles);
    draw_dynamics(output_dynamic.time, output_dynamic.output, x_title = "Time", y_title = "x(t)", separate = ensembles);
    

def segmentation_image_simple1():
    parameters = legion_parameters();
    parameters.teta_p = 7.0;
    parameters.teta_x = -1.04;
    parameters.Wz = 3.0;
    parameters.eps = 0.03;
    template_segmentation_image(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, parameters, 2000, 1000, True);
    

segmentation_image_simple1();