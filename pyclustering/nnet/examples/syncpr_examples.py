"""!

@brief Examples of usage and demonstration of abilities of Phase Oscillatory Neural Network based on Kuramoto model.

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


from pyclustering.samples.definitions import IMAGE_SYMBOL_SAMPLES;

from pyclustering.utils import read_image, rgb2gray;

from pyclustering.nnet import solve_type;
from pyclustering.nnet.syncpr import syncpr, syncpr_visualizer;

import random;
import math;

def template_recognition_image(images, steps, time, corruption = 0.1):
    samples = [];
    
    for file_name in images:
        data = read_image(file_name);
                
        image_pattern = rgb2gray(data);
                
        for index_pixel in range(len(image_pattern)):
            if (image_pattern[index_pixel] < 128):
                image_pattern[index_pixel] = 1;
            else:
                image_pattern[index_pixel] = -1;
                
        samples += [ image_pattern ];
    
    net = syncpr(len(samples[0]), 0.3, 0.3, ccore = True);
    net.train(samples);
    
    # Recognize the each learned pattern
    for i in range(len(samples)):
        sync_output_dynamic = net.simulate(steps, time, samples[i], solve_type.RK4, True);
        syncpr_visualizer.show_output_dynamic(sync_output_dynamic);
        syncpr_visualizer.show_pattern(sync_output_dynamic, 10, 10);
        
        # corrupt a little bit by black and white pixels
        for _ in range( math.floor(len(samples[i]) * corruption) ):
            random.seed();
            random_pixel = math.floor(random.random() * len(samples[i]));
            samples[i][random_pixel] = 1;
            
            random_pixel = math.floor(random.random() * len(samples[i]));
            samples[i][random_pixel] = -1;
        
        sync_output_dynamic = net.simulate(steps, time, samples[i], solve_type.RK4, True);
        syncpr_visualizer.show_output_dynamic(sync_output_dynamic);
        syncpr_visualizer.show_pattern(sync_output_dynamic, 10, 10);

        syncpr_visualizer.animate_pattern_recognition(sync_output_dynamic, 10, 10, title = "Pattern Recognition");



def small_mind_image_recognition():
    """!
    @brief Trains network using letters 'M', 'I', 'N', 'D' and recognize each of them with and without noise.
    
    """
    images = [];
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_M;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_I;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_N;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_D;
    
    template_recognition_image(images, 100, 10, 0.2);
    
    
def small_abc_image_recognition():
    """!
    @brief Trains network using letters 'A', 'B', 'C', and recognize each of them with and without noise.
    
    """
    images = [];
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_A;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_B;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_C;
    
    template_recognition_image(images, 250, 25);
    
    
def small_ftk_image_recognition():
    """!
    @brief Trains network using letters 'F', 'T', 'K' and recognize each of them with and without noise.
    
    """
    images = [];
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_F;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_T;
    images += IMAGE_SYMBOL_SAMPLES.LIST_IMAGES_SYMBOL_K;
    
    template_recognition_image(images, 100, 10, 0.2);

small_mind_image_recognition();
small_abc_image_recognition();
small_ftk_image_recognition();