"""!

@brief Neural and oscillatory network module. Consists of models of bio-inspired networks.

@authors Andrei Novikov (spb.andr@yandex.ru)
@date 2014-2015
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

import math;

from abc import ABCMeta, abstractmethod;


class initial_type:
    """!
    @brief Enumerator of types of oscillator output initialization.
    
    """
    
    """!
    @brief Output of oscillators are random in line with gaussian distribution.
    
    """
    RANDOM_GAUSSIAN = 0;
    
    """!
    @brief Output of oscillators are equidistant from each other (uniformly distributed, not randomly).
    
    """
    EQUIPARTITION = 1;


class solve_type:
    """!
    @brief Enumerator of solver types that are used for network simulation.
    
    """
    
    """!
    @brief Forward Euler first-order method.
    
    """
    FAST = 0;                   # Usual calculation: x(k + 1) = x(k) + f(x(k)).
    
    """!
    @brief Classic fourth-order Runge-Kutta method (fixed step).
    
    """
    RK4 = 1;
    
    """!
    @brief Runge-Kutta-Fehlberg method with order 4 and 5 (float step).
    
    """
    RKF45 = 2;


class conn_type:
    """!
    @brief Enumerator of connection types between oscillators.
    
    """
    
    """!
    @brief No connection between oscillators.
    
    """
    NONE = 0;
    
    """!
    @brief All oscillators have connection with each other.
    
    """
    ALL_TO_ALL = 1;
    
    """!
    @brief Connections between oscillators represent grid where one oscillator can be connected with four neighbor oscillators: right, upper, left, lower.
    
    """
    GRID_FOUR = 2;
    
    """!
    @brief Connections between oscillators represent grid where one oscillator can be connected with eight neighbor 
           oscillators: right, right-upper, upper, upper-left, left, left-lower, lower, lower-right.
           
    """
    GRID_EIGHT = 3;
    
    """!
    @brief Connections between oscillators represent bidirectional list.
    
    """
    LIST_BIDIR = 4; 
    
    """!
    @brief Connections are defined by user or by network during simulation.
    
    """
    DYNAMIC = 5;


class conn_represent:
    """!
    @brief Enumerator of internal network connection representation between oscillators.
    
    """
    
    """!
    @brief Each oscillator has list of his neighbors.
    
    """
    LIST = 0;
    
    """!
    @brief Connections are represented my matrix connection NxN, where N is number of oscillators.
    
    """
    MATRIX = 1;    


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
    
    
    def __len__(self):
        return self._num_osc;
    
    
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
            upper_left_index = index - side_size - 1;
            upper_right_index = index - side_size + 1;
            
            lower_left_index = index + side_size - 1;
            lower_right_index = index + side_size + 1;
            
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