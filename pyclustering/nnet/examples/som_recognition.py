"""!

@brief Example of application for digit recognition based on self-organized feature map.
       Digits for 0 to 9 can be recognized. The application has GUI that provides following 
       function: learning, drawing, recognition, dump saving/loading. 

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

from pyclustering.nnet.som import som, type_conn;

from pyclustering.samples.definitions import IMAGE_DIGIT_SAMPLES;

from pyclustering.utils import read_image, rgb2gray;


from tkinter import *;
from tkinter import messagebox;

import math;
import pickle;
import os;
import random;

class recognizer:
    __network = None;
    
    def __init__(self):
        self.__decode_map = [];
    
        for index_digit in range(0, 10, 1):
            list_file_digit_sample = IMAGE_DIGIT_SAMPLES.GET_LIST_IMAGE_SAMPLES(index_digit);
            
            for file_name in list_file_digit_sample:
                self.__decode_map.append(index_digit);
    
    
    def train(self):
        samples = [];
        
        print("Digit images preprocessing...");
        
        for index_digit in range(0, 10, 1):
            list_file_digit_sample = IMAGE_DIGIT_SAMPLES.GET_LIST_IMAGE_SAMPLES(index_digit);
            
            for file_name in list_file_digit_sample:
                data = read_image(file_name);
                
                image_pattern = rgb2gray(data);
                
                for index_pixel in range(len(image_pattern)):
                    if (image_pattern[index_pixel] < 128):
                        image_pattern[index_pixel] = 1;
                    else:
                        image_pattern[index_pixel] = 0;
                
                samples += [ image_pattern ];
        
       
        print("SOM initialization...");
        self.__network = som(2, 5, type_conn.grid_four, None, True);
        
        print("SOM training...");
        self.__network.train(samples, 300);
        
        print("SOM is ready...");
        
    def recognize(self, input_pattern):
        index_neuron = self.__network.simulate(input_pattern);
            
        decoded_capture_objects = [];
            
        for index_capture_object in self.__network.capture_objects[index_neuron]:
            # print("\t%s" % decode_map[index_capture_object]);
            decoded_capture_objects.append(self.__decode_map[index_capture_object]);
            
        frequent_index = max(set(decoded_capture_objects), key = decoded_capture_objects.count);
        print(decoded_capture_objects);
        return frequent_index;
        
    def save_knowledge(self):
        result_saving = False;
        
        if (self.__network is not None):
            file_network_dump = open("knowledge_recognition_memory_dump", "wb");
            pickle.dump(self.__network, file_network_dump);
            result_saving = True;
            
        return result_saving;
    
    def load_knowledge(self):
        result_loading = False;
        
        if (os.path.isfile("knowledge_recognition_memory_dump") is True):
            file_network_dump = open("knowledge_recognition_memory_dump", "rb");
            self.__network = pickle.load(file_network_dump);
            
            result_loading = True;
        
        return result_loading;


class digit_application:
    __color = "#000000";
    
    __widget = None;
    
    __user_pattern = None;
    __recognizer = None;
    
    __master = None;
    
    def __init__(self):
        self.__master = Tk();
        self.__master.title("Recognition");
        
        self.__widget = Canvas(self.__master, width = 320, height = 320);
        self.__widget.pack(expand = YES, fill = BOTH);
        self.__widget.bind("<B1-Motion>", self.__paint);
        
        button_recognize = Button(self.__master, text = "Recognize", command = self.click_recognize, width = 25);
        button_recognize.pack(side = BOTTOM);
        
        button_recognize = Button(self.__master, text = "Random Image", command = self.click_image_load, width = 25);
        button_recognize.pack(side = BOTTOM);
        
#         button_save = Button(self.__master, text = "Save", command = self.click_save, width = 25);
#         button_save.pack(side = BOTTOM);
#         
#         button_load = Button(self.__master, text = "Load", command = self.click_load, width = 25);
#         button_load.pack(side = BOTTOM);
        
        button_train = Button(self.__master, text = "Train", command = self.click_train, width = 25);
        button_train.pack(side = BOTTOM);
        
        button_clean = Button(self.__master, text = "Clean", command = self.click_clean, width = 25);
        button_clean.pack(side = BOTTOM);
        
        self.__user_pattern = [ 0 for i in range(32 * 32) ];
        self.__recognizer = recognizer();

    def __paint(self, event):
        # calculate square that is belong this click
        if ( (event.x >= 0) and (event.x < 320) and (event.y >= 0) and (event.y < 320) ):
            x1, y1 = math.floor(event.x / 10), math.floor(event.y / 10);
            
            self.__user_pattern[y1 * 32 + x1] = 1;
            
            index2 = (y1 + 1) * 32 + x1;
            index3 = y1 * 32 + (x1 + 1);
            index4 = (y1 + 1) * 32 + (x1 + 1);
            
            
            if (index2 < len(self.__user_pattern)): 
                self.__user_pattern[index2] = 1;
            if (index3 < len(self.__user_pattern)): 
                self.__user_pattern[index3] = 1;
            if (index4 < len(self.__user_pattern)): 
                self.__user_pattern[index4] = 1;
            
            display_x1, display_y1 = x1 * 10, y1 * 10;
            display_x2, display_y2 = display_x1 + 20, display_y1 + 20;
            
            self.__widget.create_rectangle(display_x1, display_y1, display_x2, display_y2, fill = self.__color, width = 0);

    def click_train(self):
        self.__recognizer.train();

    def click_load(self):
        if (self.__recognizer.load_knowledge() is not True):
            messagebox.showwarning("Recognition - Knowledge Loading", "Knowledge represented by self-organized feature map has not been "
                                   "load from hardware to recognizer due to lack of saved dump of that object. "
                                   "Please save knowledge dump after training and after that it will be possible "
                                   "to use load it at any time.");
    
    def click_save(self):
        if (self.__recognizer.save_knowledge() is not True):
            messagebox.showwarning("Recognition - Knowledge Saving", "Knowledge represented by self-organized feature map has been created "
                                   "because training has been performed. Please train recognizer and after save result of training.");

    def click_recognize(self):               
        digit_index = self.__recognizer.recognize(self.__user_pattern);
        messagebox.showinfo("Recognition - Result", "Most probably input digit is " + str(digit_index));

    def click_clean(self):
        self.__user_pattern = [ 0 for i in range(32 * 32) ];
        Canvas.delete(self.__widget, "all");
        
    def click_image_load(self):
        self.__user_pattern = [ 0 for i in range(32 * 32) ];
        Canvas.delete(self.__widget, "all");
        
        index_digit = int(math.floor(random.random() * 10));
        list_file_digit_sample = IMAGE_DIGIT_SAMPLES.GET_LIST_IMAGE_SAMPLES(index_digit);
        
        index_image = int(math.floor( random.random() * len(list_file_digit_sample) ));
        file_name = list_file_digit_sample[index_image];
        data = read_image(file_name);
                
        image_pattern = rgb2gray(data);
        for y in range(32):
            for x in range(32):
                linear_index = y * 32 + x;
                if (image_pattern[linear_index] < 128):
                    self.__user_pattern[linear_index] = 1;
                    self.__widget.create_rectangle(x * 10, y * 10, x * 10 + 10, y * 10 + 10, fill = self.__color, width = 0);
        
    def start(self):  
        mainloop();

app = digit_application();
app.start();

# digit_recognition();