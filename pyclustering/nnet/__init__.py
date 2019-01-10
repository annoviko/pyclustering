"""!

@brief Neural and oscillatory network module. Consists of models of bio-inspired networks.

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

import math;

from enum import IntEnum;

class initial_type(IntEnum):
    """!
    @brief Enumerator of types of oscillator output initialization.
    
    """
    
    ## Output of oscillators are random in line with gaussian distribution.
    RANDOM_GAUSSIAN = 0;
    
    ## Output of oscillators are equidistant from each other (uniformly distributed, not randomly).
    EQUIPARTITION = 1;


class solve_type(IntEnum):
    """!
    @brief Enumerator of solver types that are used for network simulation.
    
    """
    
    ## Forward Euler first-order method.
    FAST = 0;                   # Usual calculation: x(k + 1) = x(k) + f(x(k)).
    
    ## Classic fourth-order Runge-Kutta method (fixed step).
    RK4 = 1;
    
    ## Runge-Kutta-Fehlberg method with order 4 and 5 (float step)."
    RKF45 = 2;


class conn_type(IntEnum):
    """!
    @brief Enumerator of connection types between oscillators.
    
    """
    
    ## No connection between oscillators.
    NONE = 0;
    
    ## All oscillators have connection with each other.
    ALL_TO_ALL = 1;
    
    ## Connections between oscillators represent grid where one oscillator can be connected with four neighbor oscillators: right, upper, left, lower.
    GRID_FOUR = 2;
    
    ## Connections between oscillators represent grid where one oscillator can be connected with eight neighbor oscillators: right, right-upper, upper, upper-left, left, left-lower, lower, lower-right.
    GRID_EIGHT = 3;
    
    ## Connections between oscillators represent bidirectional list.
    LIST_BIDIR = 4; 
    
    ## Connections are defined by user or by network during simulation.
    DYNAMIC = 5;


class conn_represent(IntEnum):
    """!
    @brief Enumerator of internal network connection representation between oscillators.
    
    """
    
    ## Each oscillator has list of his neighbors.
    LIST = 0;
    
    ## Connections are represented my matrix connection NxN, where N is number of oscillators.
    MATRIX = 1;    


class network:
    """!
    @brief Common network description that consists of information about oscillators and connection between them.
    
    """
    
    _num_osc = 0;
    
    _osc_conn = None;
    _conn_represent = None;
    __conn_type = None;
    
    __height = 0;
    __width = 0;
    
    
    @property
    def height(self):
        """!
        @brief Height of the network grid (that is defined by amout of oscillators in each column), this value is zero in case of non-grid structure.
        
        @note This property returns valid value only for network with grid structure.
        
        """
        return self.__height;
    

    @property
    def width(self):
        """!
        @brief Width of the network grid, this value is zero in case of non-grid structure.
        
        @note This property returns valid value only for network with grid structure.
        
        """
        return self.__width;


    @property
    def structure(self):
        """!
        @brief Type of network structure that is used for connecting oscillators.
        
        """        
        return self.__conn_type;
   
   
    def __init__(self, num_osc, type_conn = conn_type.ALL_TO_ALL, conn_repr = conn_represent.MATRIX, height = None, width = None):
        """!
        @brief Constructor of the network.
        
        @param[in] num_osc (uint): Number of oscillators in the network that defines size of the network.
        @param[in] type_conn (conn_type): Type of connections that are used in the network between oscillators.
        @param[in] conn_repr (conn_represent): Type of representation of connections.
        @param[in] height (uint): Number of oscillators in column of the network, this argument is used 
                    only for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types this argument is ignored.
        @param[in] width (uint): Number of oscillotors in row of the network, this argument is used only 
                    for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types this argument is ignored.
        
        """
        
        self._num_osc = num_osc;
        self._conn_represent = conn_repr;
        self.__conn_type = type_conn;
        
        if (conn_repr is None):
            self._conn_represent = conn_represent.MATRIX;
        
        if ( (type_conn == conn_type.GRID_EIGHT) or (type_conn == conn_type.GRID_FOUR) ):
            if ( (height is not None) and (width is not None) ):
                self.__height = height;
                self.__width = width;
            else:
                side_size = self._num_osc ** (0.5);
                if (side_size - math.floor(side_size) > 0):
                    raise NameError("Invalid number of oscillators '" + str(num_osc) + "' in the network in case of grid structure (root square should be extractable for the number of oscillators).");
                
                self.__height = int(side_size);
                self.__width = self.__height;
        
            if (self.__height * self.__width != self._num_osc):
                raise NameError('Width (' + str(self.__width) + ') x Height (' + str(self.__height) + ') must be equal to Size (' + str(self._num_osc) + ') in case of grid structure');
        
        self._create_structure(type_conn);
    
    
    def __len__(self):
        """!
        @brief Returns size of the network that is defined by amount of oscillators.
        
        """
        return self._num_osc;


    def __create_connection(self, index1, index2):
        if (self._conn_represent == conn_represent.MATRIX):
            self._osc_conn[index1][index2] = True;
        else:
            self._osc_conn[index1].append(index2);


    def __create_all_to_all_connections(self):
        """!
        @brief Creates connections between all oscillators.
        
        """
        
        if (self._conn_represent == conn_represent.MATRIX):
            for index in range(0, self._num_osc, 1):
                self._osc_conn.append([True] * self._num_osc);
                self._osc_conn[index][index] = False;
        
        elif (self._conn_represent == conn_represent.LIST):
            for index in range(0, self._num_osc, 1):
                self._osc_conn.append([neigh for neigh in range(0, self._num_osc, 1) if index != neigh]); 


    def __create_grid_four_connections(self):
        """!
        @brief Creates network with connections that make up four grid structure.
        @details Each oscillator may be connected with four neighbors in line with 'grid' structure: right, upper, left, lower.
        
        """
        
        side_size = self.__width;
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
                self.__create_connection(index, upper_index);
            
            if (lower_index < self._num_osc):
                self.__create_connection(index, lower_index);
            
            if ( (left_index >= 0) and (math.ceil(left_index / side_size) == node_row_index) ):
                self.__create_connection(index, left_index);
            
            if ( (right_index < self._num_osc) and (math.ceil(right_index / side_size) == node_row_index) ):
                self.__create_connection(index, right_index);
    
    
    def __create_grid_eight_connections(self):
        """!
        @brief Creates network with connections that make up eight grid structure.
        @details Each oscillator may be connected with eight neighbors in line with grid structure: right, right-upper, upper, upper-left, left, left-lower, lower, lower-right.
        
        """
        
        self.__create_grid_four_connections();     # create connection with right, upper, left, lower.
        side_size = self.__width;
        
        for index in range(0, self._num_osc, 1):
            upper_left_index = index - side_size - 1;
            upper_right_index = index - side_size + 1;
            
            lower_left_index = index + side_size - 1;
            lower_right_index = index + side_size + 1;
            
            node_row_index = math.floor(index / side_size);
            upper_row_index = node_row_index - 1;
            lower_row_index = node_row_index + 1;
            
            if ( (upper_left_index >= 0) and (math.floor(upper_left_index / side_size) == upper_row_index) ):
                self.__create_connection(index, upper_left_index);
            
            if ( (upper_right_index >= 0) and (math.floor(upper_right_index / side_size) == upper_row_index) ):
                self.__create_connection(index, upper_right_index);
                
            if ( (lower_left_index < self._num_osc) and (math.floor(lower_left_index / side_size) == lower_row_index) ):
                self.__create_connection(index, lower_left_index);
                
            if ( (lower_right_index < self._num_osc) and (math.floor(lower_right_index / side_size) == lower_row_index) ):
                self.__create_connection(index, lower_right_index);
    
    
    def __create_list_bidir_connections(self):
        """!
        @brief Creates network as bidirectional list.
        @details Each oscillator may be conneted with two neighbors in line with classical list structure: right, left.
        
        """
        
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
        """!
        @brief Creates network without connections.
        
        """
        if (self._conn_represent == conn_represent.MATRIX):
            for _ in range(0, self._num_osc, 1):
                self._osc_conn.append([False] * self._num_osc);
        elif (self._conn_represent == conn_represent.LIST):
            self._osc_conn = [[] for _ in range(0, self._num_osc, 1)];

    
    def __create_dynamic_connection(self):
        """!
        @brief Prepare storage for dynamic connections.
        
        """   
        if (self._conn_represent == conn_represent.MATRIX):
            for _ in range(0, self._num_osc, 1):
                self._osc_conn.append([False] * self._num_osc);   
        elif (self._conn_represent == conn_represent.LIST):
            self._osc_conn = [[] for _ in range(0, self._num_osc, 1)];
        
    
    def _create_structure(self, type_conn = conn_type.ALL_TO_ALL):
        """!
        @brief Creates connection in line with representation of matrix connections [NunOsc x NumOsc].
        
        @param[in] type_conn (conn_type): Connection type (all-to-all, bidirectional list, grid structure, etc.) that is used by the network.
        
        """
        
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
        
        elif (type_conn == conn_type.DYNAMIC):
            self.__create_dynamic_connection();
        
        else:
            raise NameError('The unknown type of connections');
         
         
    def has_connection(self, i, j):
        """!
        @brief Returns True if there is connection between i and j oscillators and False - if connection doesn't exist.
        
        @param[in] i (uint): index of an oscillator in the network.
        @param[in] j (uint): index of an oscillator in the network.
        
        """
        if (self._conn_represent == conn_represent.MATRIX):
            return (self._osc_conn[i][j]);
        
        elif (self._conn_represent == conn_represent.LIST):
            for neigh_index in range(0, len(self._osc_conn[i]), 1):
                if (self._osc_conn[i][neigh_index] == j):
                    return True;
            return False;
        
        else:
            raise NameError("Unknown type of representation of coupling");
    
    
    def set_connection(self, i, j):
        """!
        @brief Couples two specified oscillators in the network with dynamic connections.
        
        @param[in] i (uint): index of an oscillator that should be coupled with oscillator 'j' in the network.
        @param[in] j (uint): index of an oscillator that should be coupled with oscillator 'i' in the network.
        
        @note This method can be used only in case of DYNAMIC connections, otherwise it throws expection.
        
        """
        
        if (self.structure != conn_type.DYNAMIC):
            raise NameError("Connection between oscillators can be changed only in case of dynamic type.");
        
        if (self._conn_represent == conn_represent.MATRIX):
            self._osc_conn[i][j] = True;
            self._osc_conn[j][i] = True;
        else:
            self._osc_conn[i].append(j);
            self._osc_conn[j].append(i); 
    
    
    def get_neighbors(self, index):
        """!
        @brief Finds neighbors of the oscillator with specified index.
        
        @param[in] index (uint): index of oscillator for which neighbors should be found in the network.
        
        @return (list) Indexes of neighbors of the specified oscillator.
        
        """
        
        if (self._conn_represent == conn_represent.LIST):
            return self._osc_conn[index];      # connections are represented by list.
        elif (self._conn_represent == conn_represent.MATRIX):
            return [neigh_index for neigh_index in range(self._num_osc) if self._osc_conn[index][neigh_index] == True];
        else:
            raise NameError("Unknown type of representation of connections");
