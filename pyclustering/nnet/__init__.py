'''

Abstract network representation that is used as a basic class.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import math;

from abc import ABCMeta, abstractmethod;

class initial_type:
    RANDOM_GAUSSIAN = 0;
    EQUIPARTITION = 1;

class solve_type:
    FAST = 0;                   # Usual calculation: x(k + 1) = x(k) + f(x(k)).
    RK4 = 1;                    # Runge-Kutte 4 method with fixed step.
    RKF45 = 2;                  # Runge-Kutte-Fehlberg 45 method float step.

class conn_type:
    NONE = 0;                   # No connection between oscillators.
    ALL_TO_ALL = 1;             # All oscillators have counnection with each other.
    GRID_FOUR = 2;              # Connections between oscillators represents grid where one oscillator can be connected with four oscillators: right, upper, left, lower.
    GRID_EIGHT = 3;             # Similar to previous, but neighbors are: right, right-upper, upper, upper-left, left, left-lower, lower, lower-right.
    LIST_BIDIR = 4;             # Connections between oscillators represents bidirectional list (chain).

class conn_represent:
    LIST = 0;
    MATRIX = 1;    


class network_interface(metaclass = ABCMeta):
    @abstractmethod
    def simulate(self, steps, time, solution, collect_dynamic):
        "Performs static simulation of oscillatory network"
        
        "(in) steps            - number steps of simulations during simulation"
        "(in) time             - time of simulation"
        "(in) solution         - type of solution (solving)"
        "(in) collect_dynamic  - if True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics"
        
        "Returns dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,"
        "otherwise returns only last values (last step of simulation) of dynamic"        
        
        pass;
    
    
    @abstractmethod
    def simulate_static(self, steps, time, solution, collect_dynamic):
        "Performs static simulation of oscillatory network"
        
        "(in) steps            - number steps of simulations during simulation"
        "(in) time             - time of simulation"
        "(in) solution         - type of solution (solving)"
        "(in) collect_dynamic  - if True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics"
        
        "Returns dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,"
        "otherwise returns only last values (last step of simulation) of dynamic"        
                
        pass;
    
    
    @abstractmethod
    def simulate_dynamic(self, order, solution, collect_dynamic, step, int_step, threshold_changes):
        "Performs dynamic simulation of the network until stop condition is not reached. Stop condition is defined by"
        "input argument 'order'."
        
        "(in) order              - order of process synchronization, destributed 0..1"
        "(in) solution           - type of solution (solving)"
        "(in) collect_dynamic    - if True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics"
        "(in) step               - time step of one iteration of simulation"
        "(in) int_step           - integration step, should be less than step"
        "(in) threshold_changes  - additional stop condition that helps prevent infinite simulation, defines limit of changes of oscillators between current and previous steps"
        
        "Returns dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,"
        "otherwise returns only last values (last step of simulation) of dynamic"
                
        pass;
    
    
    @abstractmethod
    def allocate_sync_ensembles(self, tolerance):
        "Allocate clusters in line with ensembles of synchronous oscillators where each" 
        "synchronous ensemble corresponds to only one cluster"
        
        "(in) tolerance        - maximum error for allocation of synchronous ensemble oscillators"
        
        "Returns list of grours (lists) of indexes of synchronous oscillators"
        "For example [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ]"
        
        pass;
    

class network:
    _num_osc = 0;
    _osc_conn = None;
    _conn_represent = None;
    
    
    @property
    def num_osc(self):
        return self._num_osc;
    
    
    def __init__(self, num_osc, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.MATRIX):
        self._num_osc = num_osc;
        self._conn_represent = conn_represent;
        
        self._create_structure(type_conn);
        
    
    def __create_all_to_all_connections(self):
        "Create connections between all oscillators"
        if (self._conn_represent == conn_represent.MATRIX):
            for index in range(0, self._num_osc, 1):
                self._osc_conn.append([True] * self._num_osc);
                self._osc_conn[index][index] = False;    
        
        elif (self._conn_represent == conn_represent.LIST):
            for index in range(0, self._num_osc, 1):
                self._osc_conn.append([neigh for neigh in range(0, self._num_osc, 1) if index != neigh]); 
          
            
    def __create_grid_four_connections(self):
        "Each oscillator may be connected with four neighbors in line with 'grid' structure: right, upper, left, lower"
        side_size = self._num_osc ** (0.5);
        if (side_size - math.floor(side_size) > 0):
            raise NameError('Invalid number of oscillators in the network');
        
        side_size = int(side_size);
        if (self._conn_represent == conn_represent.MATRIX):
            self._osc_conn = [[0] * self._num_osc for index in range(0, self._num_osc, 1)];
        elif (self._conn_represent == conn_represent.LIST):
            self._osc_conn = [[] for index in range(0, self._num_osc, 1)];
        else:
            raise NameError("Unknown type of representation of connections");
        
        for index in range(0, self._num_osc, 1):
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
            
            if (lower_index < self._num_osc):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][lower_index] = True;
                else:
                    self._osc_conn[index].append(lower_index);
            
            if ( (left_index >= 0) and (math.ceil(left_index / side_size) == node_row_index) ):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][left_index] = True;
                else:
                    self._osc_conn[index].append(left_index);
            
            if ( (right_index < self._num_osc) and (math.ceil(right_index / side_size) == node_row_index) ):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][right_index] = True;
                else:
                    self._osc_conn[index].append(right_index);  
    
    
    def __create_grid_eight_connections(self):
        "Each oscillator may be connected with eight neighbors in line with 'grid' structure: right, right-upper, upper, upper-left, left, left-lower, lower, lower-right"
        self.__create_grid_four_connections();     # create connection with right, upper, left, lower.
        side_size = int(self._num_osc ** (0.5));
        
        for index in range(0, self._num_osc, 1):
            upper_index = index - side_size;
            upper_left_index = index - side_size - 1;
            upper_right_index = index - side_size + 1;
            
            lower_index = index + side_size;
            lower_left_index = index + side_size - 1;
            lower_right_index = index + side_size + 1;
            
            left_index = index - 1;
            right_index = index + 1;
            
            node_row_index = math.floor(index / side_size);
            upper_row_index = node_row_index - 1;
            lower_row_index = node_row_index + 1;
            
            if ( (upper_left_index >= 0) and (math.floor(upper_left_index / side_size) == upper_row_index) ):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][upper_left_index] = True;
                else:
                    self._osc_conn[index].append(upper_left_index);
            
            if ( (upper_right_index >= 0) and (math.floor(upper_right_index / side_size) == upper_row_index) ):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][upper_right_index] = True;
                else:
                    self._osc_conn[index].append(upper_right_index);
                
            if ( (lower_left_index < self._num_osc) and (math.floor(lower_left_index / side_size) == lower_row_index) ):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][lower_left_index] = True;
                else:
                    self._osc_conn[index].append(lower_left_index);
                
            if ( (lower_right_index < self._num_osc) and (math.floor(lower_right_index / side_size) == lower_row_index) ):
                if (self._conn_represent == conn_represent.MATRIX):
                    self._osc_conn[index][lower_right_index] = True;
                else:
                    self._osc_conn[index].append(lower_right_index);     
    
    
    def __create_list_bidir_connections(self):
        "Each oscillator may be conneted with two neighbors in line with 'list' structure: right, left"
        if (self._conn_represent == conn_represent.MATRIX):
            for index in range(0, self._num_osc, 1):
                self._osc_conn.append([0] * self._num_osc);
                self._osc_conn[index][index] = False;
                if (index > 0):
                    self._osc_conn[index][index - 1] = True;
                    
                if (index < (self._num_osc - 1)):
                    self._osc_conn[index][index + 1] = True;   
                    
        elif (self._conn_represent == conn_represent.LIST):
            for index in range(self._num_osc):
                self._osc_conn.append([]);
                if (index > 0):
                    self._osc_conn[index].append(index - 1);
                
                if (index < (self._num_osc - 1)):
                    self._osc_conn[index].append(index + 1);
    
    
    def __create_none_connections(self):
        "Create non-exited connections"
        if (self._conn_represent == conn_represent.MATRIX):
            for index in range(0, self._num_osc, 1):
                self._osc_conn.append([False] * self._num_osc);   
        elif (self._conn_represent == conn_represent.LIST):
            self._osc_conn = [[] for index in range(0, self._num_osc, 1)];

    
    def _create_structure(self, type_conn = conn_type.ALL_TO_ALL):
        "Create connection in line with representation of matrix connections [NunOsc x NumOsc]"
        self._osc_conn = list();
        
        if (type_conn == conn_type.NONE):
            self.__create_none_connections();
        
        elif (type_conn == conn_type.ALL_TO_ALL):
            self.__create_all_to_all_connections();
        
        elif (type_conn == conn_type.GRID_FOUR):
            self.__create_grid_four_connections();
            
        elif (type_conn == conn_type.GRID_EIGHT):
            self.__create_grid_eight_connections();
            
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
        
        
    def get_neighbors(self, index):
        "Return list of neighbors of a oscillator with sequence number 'index'"
        
        "(in) index    - index of oscillator in the network"
        
        "Return list of neighbors"
        if (self._conn_represent == conn_represent.LIST):
            return self._osc_conn[index];      # connections are represented by list.
        elif (self._conn_represent == conn_represent.MATRIX):
            return [neigh_index for neigh_index in range(self._num_osc) if self._osc_conn[index][neigh_index] == True];
        else:
            raise NameError("Unknown type of representation of connections");