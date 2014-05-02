import math;

class initial_type:
    RANDOM_GAUSSIAN = 0;
    EQUIPARTITION = 1;

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


class network:
    _num_osc = 0;
    _osc_conn = None;
    _conn_represent = None;
    
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