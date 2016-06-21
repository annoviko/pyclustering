"""!

@brief Chaotic Neural Network
@details Based on article description:
         - 

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

import matplotlib.pyplot as plt;
import matplotlib.animation as animation;

import math;
import random;
import numpy;

from enum import IntEnum;

from pyclustering.utils import euclidean_distance_sqrt, average_neighbor_distance, heaviside, draw_dynamics;


class type_conn(IntEnum):
    """!
    @brief Enumeration of connection types for Chaotic Neural Network.
    
    @see cnn_network
    
    """
    
    ## All oscillators have connection with each other.
    ALL_TO_ALL  = 0,
    
    ## Connections between oscillators are created in line with Delaunay triangulation.
    TRIANGULATION_DELAUNAY = 1,


class cnn_dynamic:
    def __init__(self, output = [], time = []):
        self.output = output;
        self.time = time;


    def __len__(self):
        return len(self.output);


    def allocate_observation_matrix(self):
        number_neurons = len(self.output[0]);
        observation_matrix = [];
        
        for iteration in range(len(self.output)):
            obervation_column = [];
            for index_neuron in range(number_neurons):
                obervation_column.append(heaviside(self.output[iteration][index_neuron]));
            
            observation_matrix.append(obervation_column);
        
        return observation_matrix;


class cnn_visualizer:
    @staticmethod
    def show_output_dynamic(cnn_output_dynamic):
        draw_dynamics(cnn_output_dynamic.time, cnn_output_dynamic.output, x_title = "t", y_title = "x");
    
    
    @staticmethod
    def show_dynamic_matrix(cnn_output_dynamic):
        plt.imshow(cnn_output_dynamic.output, cmap = plt.get_cmap('gray'), interpolation='None', vmin = 0.0, vmax = 1.0); 
        plt.show();
    
    
    @staticmethod
    def show_observation_matrix(cnn_output_dynamic):
        observation_matrix = cnn_output_dynamic.allocate_observation_matrix();
        plt.imshow(observation_matrix, cmap = plt.get_cmap('gray'), interpolation='None', vmin = 0.0, vmax = 1.0); 
        plt.show();


class cnn_network:
    def __init__(self, num_osc, conn_type = type_conn.ALL_TO_ALL, amount_neighbors = 3):
        self.__num_osc = num_osc;
        self.__conn_type = conn_type;
        self.__amount_neighbors = amount_neighbors;
        
        self.__average_distance = 0.0;
        self.__weights = None;
        self.__weights_summary = None;
        
        self.__output = [ random.random() for _ in range(num_osc) ];
    
    
    def __len__(self):
        return self.__num_osc;
    
    
    def simulate(self, steps, stimulus):
        self.__create_weights(stimulus);
        
        dynamic = cnn_dynamic([], []);
        dynamic.output.append(self.__output);
        dynamic.time.append(0);
        
        for step in range(1, steps, 1):
            self.__output = self.__calculate_states();
            
            dynamic.output.append(self.__output);
            dynamic.time.append(step);
            
        return dynamic;
    
    
    def __calculate_states(self):
        output = [ 0.0 for _ in range(self.__num_osc) ];
        
        for i in range(self.__num_osc):
            output[i] = self.__neuron_evolution(i);
        
        return output;
    
    
    def __neuron_evolution(self, index):
        value = 0.0;
        #state = 1.0 - 2.0 * (self.__output[index] ** 2);
        
        for index_neighbor in range(self.__num_osc):
            value += self.__weights[index][index_neighbor] * (1.0 - 2.0 * (self.__output[index_neighbor] ** 2));
        
        return value / self.__weights_summary[index];
    
    
    def __create_weights(self, stimulus):
        self.__average_distance = average_neighbor_distance(stimulus, self.__amount_neighbors);
        print("Average distance: ", self.__average_distance);
        
        self.__weights = [ [ 0.0 for _ in range(len(stimulus)) ] for _ in range(len(stimulus)) ];
        self.__weights_summary = [ 0.0 for _ in range(self.__num_osc) ];
        
        if (self.__conn_type == type_conn.ALL_TO_ALL):
            self.__create_weights_all_to_all(stimulus);
        
        elif (self.__conn_type == type_conn.TRIANGULATION_DELAUNAY):
            self.__create_weights_delaunay_triangulation(stimulus);
    
    
    def __create_weights_all_to_all(self, stimulus):
        for i in range(len(stimulus)):
            for j in range(i + 1, len(stimulus)):
                weight = self.__calculate_weight(stimulus[i], stimulus[j]);
                print(i, j, weight, stimulus[i], stimulus[j]);
                
                self.__weights[i][j] = weight;
                self.__weights[j][i] = weight;
                
                self.__weights_summary[i] += weight;
                self.__weights_summary[j] += weight;
    
    
    def __create_weights_delaunay_triangulation(self, stimulus):
        pass;
    
    
    def __calculate_weight(self, oscillator_location1, oscillator_location2):
        distance = euclidean_distance_sqrt(oscillator_location1, oscillator_location2);
        return math.exp(-distance / (2.0 * self.__average_distance));
