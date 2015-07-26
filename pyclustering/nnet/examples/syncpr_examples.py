"""!

@brief Examples of usage and demonstration of abilities of Phase Oscillatory Neural Network based on Kuramoto model.

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


from pyclustering.samples.definitions import IMAGE_SYMBOL_SAMPLES;

from pyclustering.utils import read_image, rgb2gray;

from pyclustering.nnet import solve_type;
from pyclustering.nnet.syncpr import syncpr, syncpr_visualizer;

import random;
import math;

def template_recognition_image(images):
    samples = [];
    
    for file_name in images:
        data = read_image(file_name);
                
        image_pattern = rgb2gray(data);
                
        for index_pixel in range(len(image_pattern)):
            if (image_pattern[index_pixel] < 128):
                image_pattern[index_pixel] = 1.0;
            else:
                image_pattern[index_pixel] = -1.0;
                
        samples += [ image_pattern ];
    
    net = syncpr(len(samples[0]), 0.15, 0.15);
    net.train(samples);
    
    # Recognize the each learned pattern
    for i in range(len(samples)):
        sync_output_dynamic = net.simulate(100, 20, samples[i], solve_type.FAST, True);
        syncpr_visualizer.show_output_dynamic(sync_output_dynamic);
        syncpr_visualizer.show_pattern(sync_output_dynamic, 10, 10);
        
        # corrupt a little bit by noise the image
        for k in range( math.floor(len(samples[i]) * 0.1) ):
            random.seed();
            random_pixel = math.floor(random.random() * len(samples[i]));
            samples[i][random_pixel] = 1.0;
        
        sync_output_dynamic = net.simulate(100, 20, samples[i], solve_type.FAST, True);
        syncpr_visualizer.show_pattern(sync_output_dynamic, 10, 10);
            
        

def small_image_recognition():
    images = [];
    for i in range(0, 1, 1):
        images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_M;
        images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_I;
#         images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_N;
#         images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_D;
    
    template_recognition_image(images);
    

small_image_recognition();