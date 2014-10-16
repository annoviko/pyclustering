import numpy;

import core;

from nnet import *;

from clustering.syncnet import syncnet;
from support import average_neighbor_distance, read_sample;

class hsyncnet(syncnet):
    _number_clusters = 0;    
    __ccore_network_pointer = None;      # Pointer to CCORE HSyncNet implementation of the network.
    
    def __init__(self, source_data, number_clusters, osc_initial_phases = initial_type.RANDOM_GAUSSIAN, ccore = False):
        "Costructor of the oscillatory network hSync."
        
        "(in) number_clusters     - number of clusters that should be allocated."
        "(in) source_data         - input data set defines structure of the network."
        "(in) osc_initial_phases  - type of initialization of initial values of phases of oscillators."
        
        if (ccore is True):
            self.__ccore_network_pointer = core.create_hsyncnet(source_data, number_clusters, osc_initial_phases);
        else: 
            super().__init__(source_data, 0, initial_phases = osc_initial_phases);
            self._number_clusters = number_clusters;
    
    
    def __del__(self):
        "Destructor of oscillatory network hierachical Sync."
        if (self.__ccore_network_pointer is not None):
            core.destroy_hsyncnet_network(self.__ccore_network_pointer);
            self.__ccore_network_pointer = None;
            
            
    def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False):
        "Performs clustering of input data set in line with input parameters."
        
        "(in) order               - level of local synchronization between oscillator that defines end of process of synchronization, range [0..1]."
        "(in) solution            - type of solving differential equation: ode45, usual diff, etc."
        "(in) collect_dynamic     - if True - return whole history of process synchronization otherwise - final state (when process of clustering is over)."
        
        "Returns dynamic of the network as tuple (time, oscillator_phases) that depends on collect_dynamic parameters."
        
        if (self.__ccore_network_pointer is not None):
            return core.process_hsyncnet(self.__ccore_network_pointer, order, solution, collect_dynamic);
        
        number_neighbors = 3;
        current_number_clusters = numpy.Inf;
        
        dyn_phase = [];
        dyn_time = [];
        
        radius = average_neighbor_distance(self._osc_loc, number_neighbors);
        
        while(current_number_clusters > self._number_clusters):                
            self._create_connections(radius);
        
            (t, dyn) = self.simulate_dynamic(order, solution, collect_dynamic);
            if (collect_dynamic == True):
                dyn_phase += dyn;
                
                if (len(dyn_time) > 0):
                    point_time_last = dyn_time[len(dyn_time) - 1];
                    dyn_time += [time_point + point_time_last for time_point in t];
                else:
                    dyn_time += t;
            
            clusters = self.get_clusters(0.05);
            
            # Get current number of allocated clusters
            current_number_clusters = len(clusters);
            
            # Increase number of neighbors that should be used
            number_neighbors += 1;
            
            # Update connectivity radius and check if average function can be used anymore
            if (number_neighbors >= len(self._osc_loc)):
                radius = radius * 0.1 + radius;
            else:
                radius = average_neighbor_distance(self._osc_loc, number_neighbors);
        
        
        return (dyn_time, dyn_phase);
    
    
    def get_clusters(self, eps = 0.1):
        "Return list of clusters in line with state of ocillators (phases)."
        
        "(in) eps     - tolerance level that define maximal difference between phases of oscillators in one cluster."
        
        "Return list of clusters, for example [ [cluster1], [cluster2], ... ]."
        
        if (self.__ccore_network_pointer is not None):
            return core.get_clusters_syncnet(self.__ccore_network_pointer, eps);
        else:
            return self.allocate_sync_ensembles(eps);
