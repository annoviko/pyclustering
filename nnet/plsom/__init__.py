import math;
import numpy;
import copy;

from nnet.som import *;

class plsom(som):
    _maximal_difference = None;     # r - used for the calculation scaling variable.
    _autostop_condition = None;     # condition (tolerance) - when process should be stopped.
    _scaling_constant = None;       # beta - constant that is used for neighborhood function.
    
    def __init__(self, rows, cols, data, conn_type = type_conn.grid_eight, init_type = type_init.uniform_grid):
        super().__init__(rows, cols, data, 0, conn_type, init_type);
        
        self._autostop_condition = 0.001;
        self._maximal_difference = 0;
        
        
        self._scaling_constant = 0.1;
    
    
    def _competition(self, x):
        "Return neuron winner (distance, neuron index)"
        index = 0;
        minimum = numpy.Inf;
        
        for i in range(self._size):
            candidate = euclidean_distance(self._weights[i], x);
            if (candidate < minimum):
                index = i;
                minimum = candidate;
        
        # Used by scaling variable
        if (self._maximal_difference < minimum):
            self._maximal_difference = minimum;
            
        return index;
    
    def _adaptation(self, index, x):
        "Change weight of neurons in line with won neuron"
        dimension = len(self._weights[0]);
        
        # Scaling variable
        scaling = 1;
        if (self._maximal_difference != 0):
            scaling = euclidean_distance(self._weights[index], x) / self._maximal_difference;
        
        # Neighborhood function
        neighborhood_function = (self._scaling_constant - 1) * scaling + 1;
        sqrt_neighborhood_function = neighborhood_function ** 2;
        
        if (self._conn_type == type_conn.func_neighbor):
            for neuron_index in range(self._size):
                sqrt_distance = self._sqrt_distances[index][neuron_index];

                influence = math.exp( -( sqrt_distance / sqrt_neighborhood_function ) );
                    
                for i in range(dimension):
                    delta_weight = scaling * influence * (x[i] - self._weights[neuron_index][i]);                    
                    self._weights[neuron_index][i] = self._weights[neuron_index][i] + delta_weight
                    
        else:
            for i in range(dimension):
                self._weights[index][i] = self._weights[index][i] + scaling * (x[i] - self._weights[index][i]); 
                
            for neighbor_index in self._neighbors[index]: 
                sqrt_distance = self._sqrt_distances[index][neighbor_index]
                
                influence = math.exp( -( sqrt_distance / sqrt_neighborhood_function ) );

                for i in range(dimension):
                    delta_weight = scaling * influence * (x[i] - self._weights[neighbor_index][i]);
                    self._weights[neighbor_index][i] = self._weights[neighbor_index][i] + delta_weight;  

    
                            
    def train(self):       
        dimension = len(self._weights[0]);
        
        maximal_adaptation = numpy.Inf; 
        previous_weights = None;
        
        while (maximal_adaptation > self._autostop_condition):
            previous_weights = [item[:] for item in self._weights];    # copy
            
            # Clear all registered achievement due to new iteration
            for i in range(self._size):
                self._award[i] = 0;
                self._capture_objects[i].clear();
            
            # Train
            for i in range(len(self._data)):
                # Step 1: Competition:
                index = self._competition(self._data[i]);
                
                # Step 2: Adaptation:
                self._adaptation(index, self._data[i]);
        
                # Registration should be performed every step in PLSOM
                self._award[index] += 1;
                self._capture_objects[index].append(i);

            maximal_adaptation = 0.0;
            for neuron_index in range(self._size):
                for dim in range(dimension):
                    current_adaptation = previous_weights[neuron_index][dim] - self._weights[neuron_index][dim];
                    
                    if (current_adaptation < 0): current_adaptation = -current_adaptation;
                    
                    if (maximal_adaptation < current_adaptation):
                        maximal_adaptation = current_adaptation;
            
            #print("maximal_adaptation = ", maximal_adaptation);
            #print(previous_weights);
            #print(self._weights);
            #self.show_network(belongs = True);



# sample = read_sample('../../../Samples/SampleSimple3.txt');
# network = plsom(5, 5, sample, type_conn.grid_four);
# #network.show_network();
#        
# network.train();
# network.show_network();