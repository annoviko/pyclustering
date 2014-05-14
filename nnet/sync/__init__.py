import numpy;
import random;
import math;
import scipy.spatial;
import support;

import matplotlib.pyplot as plt;

from scipy import pi;
from scipy.integrate import odeint;
from scipy.integrate import ode;

from support import euclidean_distance;
from hierarchical import hierarchical;
from nnet import *;


class sync_network(network, network_interface):    
    # Protected members:
    _name = 'Phase Sync Network'
    _phases = None;                    # Current phases of oscillators.
    _freq = None;                      # Own frequencies of oscillators.
    _weight = 0;                       # Strength of connections between oscillators.
    _cluster = 1;                      # Parameter of artificial clustering during synchronization of phases of oscillators.
    
    # Properties of class that represents oscillatory neural network
    @property
    def name(self):
        return self._name;
    
    @property
    def phases(self):
        return self._phases;
    
    @property
    def cluster(self):
        return self._cluster;
    
    @cluster.setter
    def cluster(self, value):
        self._cluster = value;


    def __init__(self, num_osc, weight = 1, frequency = False, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.MATRIX, initial_phases = initial_type.RANDOM_GAUSSIAN):
        super().__init__(num_osc, type_conn, conn_represent);
        
        self._weight = weight;
        
        self._phases = list();
        self._freq = list();
        
        for index in range(0, num_osc, 1):    
            if (initial_phases == initial_type.RANDOM_GAUSSIAN):
                self._phases.append(random.random() * 2 * pi);
            elif (initial_phases == initial_type.EQUIPARTITION):
                self._phases.append( (2 * pi) / (num_osc - 1) * index);
            
            if (frequency == True):
                self._freq.append(random.random());
            else:
                self._freq.append(0);        
    
    
    def sync_order(self):
        "Return level of global synchorization"
        exp_amount = 0;
        average_phase = 0;
        
        for index in range(0, self.num_osc, 1):
            exp_amount += math.expm1( abs(1j * self._phases[index]) );
            average_phase += self._phases[index];
        
        exp_amount /= self.num_osc;
        average_phase = math.expm1( abs(1j * (average_phase / self.num_osc)) );
        
        return abs(average_phase) / abs(exp_amount);    
    
    
    def sync_local_order(self):
        exp_amount = 0;
        num_neigh = 0;
        
        for i in range(0, self.num_osc, 1):
            for j in range(0, self.num_osc, 1):
                if (self.has_connection(i, j) == True):
                    exp_amount += math.exp(-abs(self._phases[j] - self._phases[i]));
                    num_neigh += 1;
        
        if (num_neigh == 0):
            num_neigh = 1;
        
        return exp_amount / num_neigh;        
    
    
    def phase_kuramoto(self, teta, t, argv):
        "Return result of phase calculation for oscillator in the network"
        "Solvers as ODEINT or ODE may pass only one value if their extra argument has length equals to one"
        index = argv;
        phase = 0;
        for k in range(0, self.num_osc):
            if (self.has_connection(index, k) == True):
                phase += math.sin(self._cluster * (self._phases[k] - teta));
            
        return ( self._freq[index] + (phase * self._weight / self.num_osc) );             
    
    
    def allocate_sync_ensembles(self, tolerance = 0.01):
        "Allocate clusters in line with ensembles of synchronous oscillators where each" 
        "synchronous ensemble corresponds to only one cluster"
        clusters = [ [0] ];
        
        for i in range(1, self._num_osc, 1):
            cluster_allocated = False;
            for cluster in clusters:
                for neuron_index in cluster:
                    if ( (self._phases[i] < (self._phases[neuron_index] + tolerance)) and (self._phases[i] > (self._phases[neuron_index] - tolerance)) ):
                        cluster_allocated = True;
                        cluster.append(i);
                        break;
                
                if (cluster_allocated == True):
                    break;
            
            if (cluster_allocated == False):
                clusters.append([i]);
        
        return clusters;
    
    
    def simulate(self, steps, time, solution = solve_type.FAST, collect_dynamic = True):
        "Simulate phase dynamics of network and return simulated dynamic"
        return self.simulate_static(steps, time, solution, collect_dynamic);


    def simulate_dynamic(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False, step = 0.1, int_step = 0.01, threshold_changes = 0.000001):
        "Simulate network until level synchronization level (order) is not reached"
        # For statistics and integration
        time_counter = 0;
        
        # Prevent infinite loop. It's possible when required state cannot be reached.
        previous_order = 0;
        current_order = self.sync_local_order();
        
        # If requested input dynamics
        dyn_phase = [];
        dyn_time = [];
        if (collect_dynamic == True):
            dyn_phase.append(self._phases);
            dyn_time.append(0);
        
        # Execute until sync state will be reached
        while (current_order < order):                
            # update states of oscillators
            self._phases = self._calculate_phases(solution, time_counter, step, int_step);
            
            # update time
            time_counter += step;
            
            # if requested input dynamic
            if (collect_dynamic == True):
                dyn_phase.append(self._phases);
                dyn_time.append(time_counter);
            else:
                dyn_phase = self._phases;
                dyn_time = time_counter;
                
            # update orders
            previous_order = current_order;
            current_order = self.sync_local_order();
            
            # hang prevention
            if (abs(current_order - previous_order) < threshold_changes):
                break;
                
        return (dyn_time, dyn_phase);


    def simulate_static(self, steps, time, solution = solve_type.FAST, collect_dynamic = False):
        "Simulate network during specified time and return dynamic of the network if it's required"
        dyn_phase = None;
        dyn_time = None;
        
        if (collect_dynamic == True):
            dyn_phase = [];
            dyn_time = [];
            
            dyn_phase.append(self._phases);
            dyn_time.append(0);
        
        step = time / steps;
        int_step = step / 10;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._phases = self._calculate_phases(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_phase.append(self._phases);
                dyn_time.append(t);
            else:
                dyn_phase = self._phases;
                dyn_time = t;
        
        return (dyn_time, dyn_phase);        


    def _calculate_phases(self, solution, t, step, int_step):
        "Calculate new states of oscillator in the network"
        next_phases = [0] * self.num_osc;    # new oscillator _phases
        
        for index in range (0, self.num_osc, 1):
            if (solution == solve_type.FAST):
                result = self._phases[index] + self.phase_kuramoto(self._phases[index], 0, index);
                next_phases[index] = phase_normalization(result);
                
            elif (solution == solve_type.ODEINT):
                result = odeint(self.phase_kuramoto, self._phases[index], numpy.arange(t - step, t, int_step), (index , ));
                next_phases[index] = phase_normalization(result[len(result) - 1][0]);
                
            else:
                assert 0;
        
        return next_phases;
        

def phase_normalization(teta):
    "Normalization of phase of oscillator that should be placed between [0; 2 * pi]"
    norm_teta = teta;
    while (norm_teta > (2 * pi)) or (norm_teta < 0):
        if (norm_teta > (2 * pi)):
            norm_teta -= 2 * pi;
        else:
            norm_teta += 2 * pi;
    
    return norm_teta;
