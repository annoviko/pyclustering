from pyclustering.nnet.som import som;
from pyclustering.nnet.som import type_conn, type_init;

from pyclustering.samples.definitions import IMAGE_DIGIT_SAMPLES;

from pyclustering.support import read_image, rgb2gray;

import random;

def digit_recognition():
    samples = [];
    decode_map = [];
    
    print("Digit images preprocessed...");
    
    for index_digit in range(0, 10, 1):
        list_file_digit_sample = IMAGE_DIGIT_SAMPLES.GET_LIST_IMAGE_SAMPLES(index_digit);
        
        for file_name in list_file_digit_sample:
            data = read_image(file_name);
            decode_map.append(index_digit);
            
            image_pattern = rgb2gray(data);
            for index_pixel in range(len(image_pattern)):
                if (image_pattern[index_pixel] > 128):
                    image_pattern[index_pixel] = 1;
                else:
                    image_pattern[index_pixel] = 0;
            
            samples += [ image_pattern ];
    
   
    print("SOM initialization...");
    network = som(2, 5, samples, 200, type_conn.grid_four, type_init.uniform_grid);
    
    print("SOM training...");
    network.train();
    
    print("Simulation...");
    for i in range(0, 10, 1):
        input_pattern = i * 15;
        index_neuron = network.simulate(samples[input_pattern]);
        
        decoded_capture_objects = [];
        
        print("Input pattern %s looks like:" % decode_map[input_pattern]);
        for index_capture_object in network.capture_objects[index_neuron]:
            # print("\t%s" % decode_map[index_capture_object]);
            decoded_capture_objects.append(decode_map[index_capture_object]);
        
        frequent_index = max(set(decoded_capture_objects), key = decoded_capture_objects.count);
        print("Most probably it's %s" % frequent_index);
            
        print("\n");
    
    
digit_recognition();