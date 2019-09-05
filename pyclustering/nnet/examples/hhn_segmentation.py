"""!

@brief Segmentation example of Hodgkin-Huxley oscillatory network for image segmentation.

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


import numpy
import os.path
import pickle

from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from pyclustering.cluster.dbscan import dbscan

from pyclustering.nnet.dynamic_visualizer import dynamic_visualizer
from pyclustering.nnet.hhn import hhn_network, hhn_parameters

from pyclustering.samples.definitions import IMAGE_SIMPLE_SAMPLES

from pyclustering.utils import read_image, rgb2gray



def animate_segmentation(dyn_time, dyn_peripheral, image, delay_mask=100, step=5, movie_file=None):
    image_source = Image.open(image)
    image_size = image_source.size
    
    figure = plt.figure()

    image_pixel_fired = [-1] * (image_size[0] * image_size[1])
    
    basic_transparence_value = 255

    y_global_max = float('-Inf')
    y_global_min = float('+Inf')
    for dyn in dyn_peripheral:
        y_max = max(dyn)
        if (y_global_max < y_max):
            y_global_max = y_max
        
        y_min = min(dyn)
        if (y_global_min > y_min):
            y_global_min = y_min

    print(y_global_min, y_global_max)
    ylim = [y_global_min - abs(y_global_min) * 0.1, y_global_max + abs(y_global_max) * 0.05]

    def init_frame():
        return frame_generation(0)

    def frame_generation(index_iteration):
        print(index_iteration)
        
        figure.clf()
        
        figure.suptitle("Hodgkin-Huxley Network (iteration: " + str(index_iteration) +")", fontsize = 18, fontweight = 'bold')
        
        ax1 = figure.add_subplot(121)
        ax2 = figure.add_subplot(122)
        
        end_iteration = index_iteration
        if (end_iteration > len(dyn_peripheral)):
            end_iteration = len(dyn_peripheral)
        
        dynamic_length = 100
        begin_iteration = end_iteration - dynamic_length
        if begin_iteration < 0:
            begin_iteration = 0
        
        # Display output dynamic
        xlim = [dyn_time[begin_iteration], dyn_time[begin_iteration + dynamic_length]]
        visualizer = dynamic_visualizer(1, x_title="Time", y_title="V", x_lim=xlim, y_lim=ylim)
        
        dyn_time_segment = [ dyn_time[i] for i in range(begin_iteration, end_iteration, 1) ]
        dyn_peripheral_segment = [ dyn_peripheral[i] for i in range(begin_iteration, end_iteration, 1) ]
        
        visualizer.append_dynamic(dyn_time_segment, dyn_peripheral_segment)
        visualizer.show(ax1, False)
        
        visualize_segmenetation(end_iteration, ax2, step)
        
        return [ figure.gca() ]
    
    def visualize_segmenetation(t, segm_axis, step):
        image_result = image_source.copy()
        image_cluster = None
        
        if (t > step):
            t -= step
        
        for _ in range(step):
            image_color_segments = [(255, 255, 255, 0)] * (image_size[0] * image_size[1])
            for index_pixel in range(len(image_pixel_fired)):
                fire_time = image_pixel_fired[index_pixel]
                if ( (fire_time > 0) and (t - fire_time < delay_mask) ):
                    color_value = 0 + (t - fire_time)
                    transparence = basic_transparence_value - (t - fire_time)
                    if (transparence < 0):
                        transparence = 0
                    
                    image_color_segments[index_pixel] = (color_value, color_value, color_value, transparence)
            
            for index_oscillator in range(len(dyn_peripheral[t])):
                if (dyn_peripheral[t][index_oscillator] > 0):
                    image_color_segments[index_oscillator] = (0, 0, 0, basic_transparence_value)
                    image_pixel_fired[index_oscillator] = t
            
            stage = numpy.array(image_color_segments, numpy.uint8)
            stage = numpy.reshape(stage, image_size + ((4),)) # ((3),) it's size of RGB - third dimension.
            
            image_cluster = Image.fromarray(stage, 'RGBA')
            t += 1
            
        image_result.paste(image_cluster, (0, 0), image_cluster)
        return segm_axis.imshow(image_result)
    
    iterations = range(1, len(dyn_peripheral), step)
    segmentation_animation = animation.FuncAnimation(figure, frame_generation, iterations, init_func=None, interval = 1, repeat_delay = 3000)
    
    if (not movie_file):
        segmentation_animation.save(movie_file, writer = 'ffmpeg', fps = 20, bitrate = 3000)
    else:
        plt.show()


def template_image_segmentation(image_file, steps, time, dynamic_file_prefix):
    image = read_image(image_file);
    stimulus = rgb2gray(image);

    params = hhn_parameters();
    params.deltah = 650;
    params.w1 = 0.1;
    params.w2 = 9.0;
    params.w3 = 5.0;
    params.threshold = -10;

    stimulus = [255.0 - pixel for pixel in stimulus];
    divider = max(stimulus) / 50.0;
    stimulus = [int(pixel / divider) for pixel in stimulus];

    t, dyn_peripheral, dyn_central = None, None, None;

    if ( not os.path.exists(dynamic_file_prefix + 'dynamic_time.txt') or
         not os.path.exists(dynamic_file_prefix + 'dynamic_peripheral.txt') or
         not os.path.exists(dynamic_file_prefix + 'dynamic_dyn_central.txt') ):
        
        print("File with output dynamic is not found - simulation will be performed - it may take some time, be patient.");

        net = hhn_network(len(stimulus), stimulus, params, ccore=True);

        (t, dyn_peripheral, dyn_central) = net.simulate(steps, time);

        print("Store dynamic to save time for simulation next time.");

        with open(dynamic_file_prefix + 'dynamic_time.txt', 'wb') as file_descriptor:
            pickle.dump(t, file_descriptor);

        with open(dynamic_file_prefix + 'dynamic_peripheral.txt', 'wb') as file_descriptor:
            pickle.dump(dyn_peripheral, file_descriptor);

        with open(dynamic_file_prefix + 'dynamic_dyn_central.txt', 'wb') as file_descriptor:
            pickle.dump(dyn_central, file_descriptor);
    else:
        print("Load output dynamic from file.");
        
        with open (dynamic_file_prefix + 'dynamic_time.txt', 'rb') as file_descriptor:
            t = pickle.load(file_descriptor);

        with open (dynamic_file_prefix + 'dynamic_peripheral.txt', 'rb') as file_descriptor:
            dyn_peripheral = pickle.load(file_descriptor);

        with open (dynamic_file_prefix + 'dynamic_dyn_central.txt', 'rb') as file_descriptor:
            dyn_central = pickle.load(file_descriptor);

    animate_segmentation(t, dyn_peripheral, image_file, 200);

    # just for checking correctness of results - let's use classical algorithm
    if (False):
        dbscan_instance = dbscan(image, 3, 4, True);
        dbscan_instance.process();
        trustable_clusters = dbscan_instance.get_clusters();
    
        amount_canvases = len(trustable_clusters) + 2;
        visualizer = dynamic_visualizer(amount_canvases, x_title = "Time", y_title = "V", y_labels = False);
        visualizer.append_dynamics(t, dyn_peripheral, 0, trustable_clusters);
        visualizer.append_dynamics(t, dyn_central, amount_canvases - 2, True);
        visualizer.show();


def segmentation_image_simple1():
    template_image_segmentation(IMAGE_SIMPLE_SAMPLES.IMAGE_SIMPLE01, 7000, 600, "simple1")


segmentation_image_simple1()