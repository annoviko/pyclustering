'''

Cluster analysis algorithm: Sync

Based on article description:
 - T.Miyano, T.Tsutsui. Data Synchronization as a Method of Data Mining. 2007.

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

import pyclustering.core.wrapper as wrapper;

from pyclustering.nnet import *;
from pyclustering.nnet.sync import *;


class syncnet(sync_network):
    """!
    @brief Class represents clustering algorithm SyncNet. SyncNet is bio-inspired algorithm that is based on oscillatory network that uses modified Kuramoto model.
    
    Example:
    @code
        # read sample for clustering from some file
        sample = read_sample(path_to_file);
        
        # create oscillatory network with connectivity radius 0.5 using CCORE (C++ implementation of pyclustering)
        network = syncnet(sample, 0.5, ccore = True);
        
        # run cluster analysis and collect output dynamic of the oscillatory network, 
        # network simulation is performed by Runge Kutta Fehlberg 45.
        (dyn_time, dyn_phase) = network.process(0.998, solve_type.RFK45, True);
        
        # show oscillatory network
        network.show_network();
        
        # obtain clustering results
        clusters = network.get_clusters();
        
        # show clusters
        draw_clusters(sample, clusters);
    @endcode
    
    """
    _osc_loc = None;            # Location (coordinates) of oscillators in the feature space.
    
    _ena_conn_weight = False;   # Enable mode: when strength of connection depends on distance between two oscillators.
    _conn_weight = None;        # Stength of connection between oscillators.
    
    __ccore_network_pointer = None;      # Pointer to CCORE SyncNet implementation of the network.
    
    def __init__(self, sample, radius, conn_repr = conn_represent.MATRIX, initial_phases = initial_type.RANDOM_GAUSSIAN, enable_conn_weight = False, ccore = False):
        """!
        @brief Contructor of the oscillatory network SYNC for cluster analysis.
        
        @param[in] sample (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] radius (double): Connectivity radius between points, points should be connected if distance between them less then the radius.
        @param[in] conn_repr (conn_represent): Internal representation of connection in the network: matrix or list. Ignored in case of usage of CCORE library.
        @param[in] initial_phases (initial_type): Type of initialization of initial phases of oscillators (random, uniformly distributed, etc.).
        @param[in] enable_conn_weight (bool): If True - enable mode when strength between oscillators depends on distance between two oscillators.
              If False - all connection between oscillators have the same strength that equals to 1 (True).
        @param[in] ccore (bool): Defines should be CCORE C++ library used instead of Python code or not.
        
        """
        
        if (ccore is True):
            self.__ccore_network_pointer = wrapper.create_syncnet_network(sample, radius, initial_phases, enable_conn_weight);
        else:
            super().__init__(len(sample), 1, 0, conn_type.NONE, initial_phases);
            
            self._ena_conn_weight = enable_conn_weight;
            self._osc_loc = sample;
            self._conn_represent = conn_repr;
    
            # Connections will be represent by lists.
            if (conn_repr == conn_represent.MATRIX):
                self._osc_conn = [[0] * self._num_osc for index in range(0, self._num_osc, 1)];
                
            elif (conn_repr == conn_represent.LIST):
                self._osc_conn = [[] for index in range(0, self._num_osc, 1)];
                
            else:
                raise NameError("Unknown type of representation of coupling between oscillators");
            
            # Create connections.
            if (radius is not None):
                self._create_connections(radius);
    

    def __del__(self):
        """!
        @brief Destructor of oscillatory network is based on Kuramoto model.
        
        """
        
        if (self.__ccore_network_pointer is not None):
            wrapper.destroy_syncnet_network(self.__ccore_network_pointer);
            self.__ccore_network_pointer = None;
        else:
            self._osc_loc = None;   # pointer to external object


    def _create_connections(self, radius):
        """!
        @brief Create connections between oscillators in line with input radius of connectivity.
        
        @param[in] radius (double): Connectivity radius between oscillators.
        
        """
        
        if (self._ena_conn_weight is True):
            self._conn_weight = [[0] * self._num_osc for index in range(0, self._num_osc, 1)];
        
        maximum_distance = 0;
        minimum_distance = float('inf');
        
        # Create connections
        for i in range(0, self._num_osc, 1):
            for j in range(i + 1, self._num_osc, 1):                 
                    dist = euclidean_distance(self._osc_loc[i], self._osc_loc[j]);
                    
                    if (self._ena_conn_weight is True):
                        self._conn_weight[i][j] = dist;
                        self._conn_weight[j][i] = dist;
                        
                        if (dist > maximum_distance): maximum_distance = dist;
                        if (dist < minimum_distance): minimum_distance = dist;
                    
                    if (dist <= radius):
                        if (self._conn_represent == conn_represent.LIST):
                            self._osc_conn[i].append(j);
                            self._osc_conn[j].append(i);
                        else:
                            self._osc_conn[i][j] = True;
                            self._osc_conn[j][i] = True;
        
        if (self._ena_conn_weight is True):
            multiplier = 1; 
            subtractor = 0;
            
            if (maximum_distance != minimum_distance):
                multiplier = (maximum_distance - minimum_distance);
                subtractor = minimum_distance;
            
            for i in range(0, self._num_osc, 1):
                for j in range(i + 1, self._num_osc, 1):
                    value_conn_weight = (self._conn_weight[i][j] - subtractor) / multiplier;
                    
                    self._conn_weight[i][j] = value_conn_weight;
                    self._conn_weight[j][i] = value_conn_weight;


    def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = True):
        """!
        @brief Peforms cluster analysis using simulation of the oscillatory network.
        
        @param[in] order (double): Order of synchronization that is used as indication for stopping processing.
        @param[in] solution (solve_type): Specified type of solving diff. equation.
        @param[in] collect_dynamic (bool): Specified requirement to collect whole dynamic of the network.
        
        @return (tuple) Last values of simulation time and phases of oscillators as a tuple if collect_dynamic is False, and whole dynamic
                if collect_dynamic is True. Format of returned value: (simulation_time, oscillator_phases).
        
        @see get_clusters()
        
        """
        
        if (self.__ccore_network_pointer is not None):
            return wrapper.process_syncnet(self.__ccore_network_pointer, order, solution, collect_dynamic);
        else:
            return self.simulate_dynamic(order, solution, collect_dynamic);
    
    
    def phase_kuramoto(self, teta, t, argv):
        """!
        @brief Overrided method for calculation of oscillator phase.
        
        @param[in] teta (double): Current value of phase.
        @param[in] t (double): Time (can be ignored).
        @param[in] argv (uint): Index of oscillator whose phase represented by argument teta.
        
        @return (double) New value of phase of oscillator with index 'argv'.
        
        """
        
        index = argv;   # index of oscillator
        phase = 0;      # phase of a specified oscillator that will calculated in line with current env. states.
        
        neighbors = self.get_neighbors(index);
        for k in neighbors:
            conn_weight = 1;
            if (self._ena_conn_weight is True):
                conn_weight = self._conn_weight[index][k];
                
            phase += conn_weight * self._weight * math.sin(self._phases[k] - teta);
        
        divider = len(neighbors);
        if (divider == 0): 
            divider = 1;
            
        return ( self._freq[index] + (phase / divider) );   


    def get_clusters(self, eps = 0.1):
        """!
        @brief Returns list of clusters in line with state of ocillators (phases).
        
        @param[in] eps (double): Tolerance level that define maximal difference between phases of oscillators in one cluster.
        
        @return (list) List of clusters, for example [ [cluster1], [cluster2], ... ].
        
        @see process()
        
        """
        
        if (self.__ccore_network_pointer is not None):
            return wrapper.get_clusters_syncnet(self.__ccore_network_pointer, eps);
        else:
            return self.allocate_sync_ensembles(eps);
    
    
    def show_network(self):
        """!
        @brief Shows connections in the network. It supports only 2-d and 3-d representation.
        
        """
        
        if (self.__ccore_network_pointer is not None):
            raise NameError("Not supported for CCORE");
        
        dimension = len(self._osc_loc[0]);
        if ( (dimension != 3) and (dimension != 2) ):
            raise NameError('Network that is located in different from 2-d and 3-d dimensions can not be represented');
        
        from matplotlib.font_manager import FontProperties;
        from matplotlib import rcParams;
    
        rcParams['font.sans-serif'] = ['Arial'];
        rcParams['font.size'] = 12;

        fig = plt.figure();
        axes = None;
        if (dimension == 2):
            axes = fig.add_subplot(111);
        elif (dimension == 3):
            axes = fig.gca(projection='3d');
        
        surface_font = FontProperties();
        surface_font.set_name('Arial');
        surface_font.set_size('12');
        
        for i in range(0, self.num_osc, 1):
            if (dimension == 2):
                axes.plot(self._osc_loc[i][0], self._osc_loc[i][1], 'bo');  
                if (self._conn_represent == conn_represent.MATRIX):
                    for j in range(i, self._num_osc, 1):    # draw connection between two points only one time
                        if (self.has_connection(i, j) == True):
                            axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], 'b-', linewidth = 0.5);    
                            
                else:
                    for j in self.get_neighbors(i):
                        if ( (self.has_connection(i, j) == True) and (i > j) ):     # draw connection between two points only one time
                            axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], 'b-', linewidth = 0.5);    
            
            elif (dimension == 3):
                axes.scatter(self._osc_loc[i][0], self._osc_loc[i][1], self._osc_loc[i][2], c = 'b', marker = 'o');
                
                if (self._conn_represent == conn_represent.MATRIX):
                    for j in range(i, self._num_osc, 1):    # draw connection between two points only one time
                        if (self.has_connection(i, j) == True):
                            axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], [self._osc_loc[i][2], self._osc_loc[j][2]], 'b-', linewidth = 0.5);
                        
                else:
                    for j in self.get_neighbors(i):
                        if ( (self.has_connection(i, j) == True) and (i > j) ):     # draw connection between two points only one time
                            axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], [self._osc_loc[i][2], self._osc_loc[j][2]], 'b-', linewidth = 0.5);
                               
        plt.grid();
        plt.show();
    
