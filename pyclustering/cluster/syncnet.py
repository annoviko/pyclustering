"""!

@brief Cluster analysis algorithm: Sync
@details Based on article description:
         - T.Miyano, T.Tsutsui. Data Synchronization as a Method of Data Mining. 2007.

@authors Andrei Novikov (pyclustering@yandex.ru)
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

import matplotlib.pyplot as plt;

from pyclustering.core.syncnet_wrapper import *;

from pyclustering.nnet import *;
from pyclustering.nnet.sync import *;

from pyclustering.utils import euclidean_distance;


class syncnet_analyser(sync_dynamic):
    """!
    @brief Performs analysis of output dynamic of the oscillatory network syncnet to extract information about cluster allocation.
    
    """
    
    def __init__(self, phase, time, pointer_sync_analyser):
        """!
        @brief Constructor of the analyser.
        
        @param[in] phase (list): Output dynamic of the oscillatory network, where one iteration consists of all phases of oscillators.
        @param[in] time (list): Simulation time.
        @param[in] pointer_sync_analyser (POINTER): Pointer to CCORE analyser, if specified then other arguments can be omitted.
        
        """
        super().__init__(phase, time, pointer_sync_analyser);
    
    def __del__(self):
        """!
        @brief Desctructor of the analyser.
        
        """
        
        if (self._ccore_sync_dynamic_pointer is not None):
            syncnet_analyser_destroy(self._ccore_sync_dynamic_pointer);
            self._ccore_sync_dynamic_pointer = None;
    
    def allocate_clusters(self, eps = 0.01):
        """!
        @brief Returns list of clusters in line with state of ocillators (phases).
        
        @param[in] eps (double): Tolerance level that define maximal difference between phases of oscillators in one cluster.
        
        @return (list) List of clusters, for example [ [cluster1], [cluster2], ... ].
        
        @see allocate_noise()
        
        """        
        return self.allocate_sync_ensembles(eps);
    
    def allocate_noise(self):
        """!
        @brief Returns allocated noise.
        
        @remark Allocated noise can be returned only after data processing (use method process() before). Otherwise empty list is returned.
        
        @return (list) List of indexes that are marked as a noise.
        
        @see allocate_clusters()
        
        """         
        return [];


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
            self.__ccore_network_pointer = syncnet_create_network(sample, radius, initial_phases, enable_conn_weight);
        else:
            super().__init__(len(sample), 1, 0, conn_type.DYNAMIC, initial_phases);
            
            self._ena_conn_weight = enable_conn_weight;
            self._osc_loc = sample;
            self._conn_represent = conn_repr;
            
            # Create connections.
            if (radius is not None):
                self._create_connections(radius);
    

    def __del__(self):
        """!
        @brief Destructor of oscillatory network is based on Kuramoto model.
        
        """
        
        if (self.__ccore_network_pointer is not None):
            syncnet_destroy_network(self.__ccore_network_pointer);
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
                        self.set_connection(i, j);
        
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
        
        @return (syncnet_analyser) Returns analyser of results of clustering.
        
        """
        
        if (self.__ccore_network_pointer is not None):
            pointer_output_dynamic = syncnet_process(self.__ccore_network_pointer, order, solution, collect_dynamic);
            return syncnet_analyser(None, None, pointer_output_dynamic);
        else:
            output_sync_dynamic = self.simulate_dynamic(order, solution, collect_dynamic);
            return syncnet_analyser(output_sync_dynamic.output, output_sync_dynamic.time, None);
    
    
    def _phase_kuramoto(self, teta, t, argv):
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
        
        for i in range(0, self._num_osc, 1):
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
    
