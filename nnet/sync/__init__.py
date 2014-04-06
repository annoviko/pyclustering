import numpy;
import random;
import math;
import scipy.spatial;
import support;

import matplotlib.pyplot as plt;

from scipy import pi;
from scipy.integrate import odeint;
from scipy.integrate import ode;
from scipy.spatial import distance;

from support import euclidean_distance;
from hierarchical import hierarchical;


class solve_type:
    FAST = 1;                   # Usual calculation: x(k + 1) = x(k) + f(x(k)).
    ODEINT = 2;                 # Runge-Kutte method with fixed step.
    ODE = 3;


class conn_type:
    NONE = 0;                   # No connection between oscillators.
    ALL_TO_ALL = 1;             # All oscillators have counnection with each other.
    GRID_FOUR = 2;              # Connections between oscillators represents grid where one oscillator can be connected with four oscillators: right, upper, left, lower.
    GRID_EIGHT = 3;             # Similar to previous, but neighbors are: right, right-upper, upper, upper-left, left, left-lower, lower, lower-right.
    LIST_BIDIR = 4;             # Connections between oscillators represents bidirectional list (chain).


class conn_represent:
    LIST = 0;
    MATRIX = 1;    


class initial_type:
    RANDOM_GAUSSIAN = 0;
    EQUIPARTITION = 1;


class order_type:
    GLOBAL_SYNC = 0;
    LOCAL_SYNC = 1;


class net:    
    # Protected members:
    _name = 'Phase Sync Network'
    _num_osc = 0;                      # Number of oscillators in the network
    _osc_conn = None;                  # Connection bertween oscillators. Can be represented by matrix or list.
    _phases = None;                    # Current phases of oscillators.
    _freq = None;                      # Own frequencies of oscillators.
    _weight = 0;                       # Strength of connections between oscillators.
    _cluster = 1;                      # Parameter of artificial clustering during synchronization of phases of oscillators.
    
    _conn_represent = conn_represent.MATRIX;
    
    # Properties of class that represents oscillatory neural network
    @property
    def name(self):
        return self._name;
    
    @property
    def num_osc(self):
        return self._num_osc;
    
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
        self._num_osc = num_osc;
        self._weight = weight;
        
        self._phases = list();
        self._freq = list();
        self._osc_conn = list();
        
        for index in range(0, num_osc, 1):    
            if (initial_phases == initial_type.RANDOM_GAUSSIAN):
                self._phases.append(random.random() * 2 * pi);
            elif (initial_phases == initial_type.EQUIPARTITION):
                self._phases.append( (2 * pi) / (num_osc - 1) * index);
            
            if (frequency == True):
                self._freq.append(random.random());
            else:
                self._freq.append(0);
                
        self._conn_represent = conn_represent;
        self._create_structure(type_conn);
        
    
    def __create_all_to_all_connections(self):
        "Create connections between all oscillators"
        if (self._conn_represent == conn_represent.MATRIX):
            for index in range(0, self.num_osc, 1):
                self._osc_conn.append([True] * self.num_osc);
                self._osc_conn[index][index] = False;    
        
        elif (self._conn_represent == conn_represent.LIST):
            for index in range(0, self.num_osc, 1):
                self._osc_conn.append([neigh for neigh in range(0, self.num_osc, 1) if index != neigh]); 
          
            
    def __create_grid_four_connections(self):
        "Each oscillator may be connected with four neighbors in line with 'grid' structure: right, upper, left, lower"
        side_size = self.num_osc ** (0.5);
        if (side_size - math.floor(side_size) > 0):
            raise NameError('Invalid number of oscillators in the network');
        
        side_size = int(side_size);
        if (self._conn_represent == conn_represent.MATRIX):
            self._osc_conn = [[0] * self.num_osc for index in range(0, self.num_osc, 1)];
        elif (self._conn_represent == conn_represent.LIST):
            self._osc_conn = [[] for index in range(0, self.num_osc, 1)];
        else:
            raise NameError("Unknown type of representation of connections");
        
        for index in range(0, self.num_osc, 1):
            upper_index = index - side_size;
            lower_index = index + side_size;
            left_index = index - 1;
            right_index = index + 1;
            
            node_row_index = math.ceil(index / side_size);
            if (upper_index >= 0):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][upper_index] = True;
                else:
                    self._osc_conn[index].append(upper_index);
            
            if (lower_index < self.num_osc):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][lower_index] = True;
                else:
                    self._osc_conn[index].append(lower_index);
            
            if ( (left_index >= 0) and (math.ceil(left_index / side_size) == node_row_index) ):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][left_index] = True;
                else:
                    self._osc_conn[index].append(left_index);
            
            if ( (right_index < self.num_osc) and (math.ceil(right_index / side_size) == node_row_index) ):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][right_index] = True;
                else:
                    self._osc_conn[index].append(right_index);  
    
    
    def __create_list_bidir_connections(self):
        "Each oscillator may be conneted with two neighbors in line with 'list' structure: right, left"
        if (self._conn_represent == conn_represent.MATRIX):
            for index in range(0, self.num_osc, 1):
                self._osc_conn.append([0] * self.num_osc);
                self._osc_conn[index][index] = False;
                if (index > 0):
                    self._osc_conn[index][index - 1] = True;
                    
                if (index < (self.num_osc - 1)):
                    self._osc_conn[index][index + 1] = True;   
                    
        elif (self._conn_represent == conn_represent.LIST):
            for index in range(self.num_osc):
                self._osc_conn.append([]);
                if (index > 0):
                    self._osc_conn[index].append(index - 1);
                
                if (index < (self.num_osc - 1)):
                    self._osc_conn[index].append(index + 1);
    
    
    def __create_none_connections(self):
        "Create non-exited connections"
        if (self._conn_represent == conn_represent.MATRIX):
            for index in range(0, self.num_osc, 1):
                self._osc_conn.append([False] * self.num_osc);   
        elif (self._conn_represent == conn_represent.LIST):
            self._osc_conn = [[] for index in range(0, self.num_osc, 1)];

    
    def _create_structure(self, type_conn = conn_type.ALL_TO_ALL):
        "Create connection in line with representation of matrix connections [NunOsc x NumOsc]"
        if (type_conn == conn_type.NONE):
            self.__create_none_connections();
        
        elif (type_conn == conn_type.ALL_TO_ALL):
            self.__create_all_to_all_connections();
        
        elif (type_conn == conn_type.GRID_FOUR):
            self.__create_grid_four_connections();
            
        elif (type_conn == conn_type.LIST_BIDIR):
            self.__create_list_bidir_connections();
            
        else:
            raise NameError('The unknown type of connections');
         
         
    def has_connection(self, i, j):
        "Return strength of connection between i and j oscillators. Return 0 - if connection doesn't exist."
        if (self._conn_represent == conn_represent.MATRIX):
            return (self._osc_conn[i][j]);
        
        elif (self._conn_represent == conn_represent.LIST):
            for neigh_index in range(0, len(self._osc_conn[i]), 1):
                if (self._osc_conn[i][neigh_index] == j):
                    return True;
            return False;
        
        else:
            raise NameError("Unknown type of representation of coupling");                
    
    
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
