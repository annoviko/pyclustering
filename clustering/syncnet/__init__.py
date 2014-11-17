'''

Cluster analysis algorithm: Sync

Based on article description:
 - T.Miyano, T.Tsutsui. Data Synchronization as a Method of Data Mining. 2007.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

import core;

from nnet.sync import *;

from support import draw_clusters;
from support import read_sample;

class syncnet(sync_network):
    _osc_loc = None;            # Location (coordinates) of oscillators in the feature space.
    
    _ena_conn_weight = False;   # Enable mode: when strength of connection depends on distance between two oscillators.
    _conn_weight = None;        # Stength of connection between oscillators.
    
    __ccore_network_pointer = None;      # Pointer to CCORE SyncNet implementation of the network.
    
    def __init__(self, sample, radius, conn_repr = conn_represent.MATRIX, initial_phases = initial_type.RANDOM_GAUSSIAN, enable_conn_weight = False, ccore = False):
        "Contructor of the oscillatory network SYNC for cluster analysis."
        
        "(in) sample             - input data that is presented as list of points (objects), each point should be represented by list or tuple."
        "(in) radius             - connectivity radius between points, points should be connected if distance between them less then the radius."
        "(in) conn_repr          - internal representation of connection in the network: matrix or list."
        "(in) initial_phases     - type of initialization of initial phases of oscillators (random, uniformly distributed, etc.)."
        "(in) enable_conn_weight - if True - enable mode when strength between oscillators depends on distance between two oscillators."
        "                          if False - all connection between oscillators have the same strength that equals to 1 (True)."
        "(in) ccore              - defines should be CCORE C++ library used instead of Python code or not."
        
        if (ccore is True):
            self.__ccore_network_pointer = core.create_syncnet_network(sample, radius, initial_phases, enable_conn_weight);
        else:
            super().__init__(len(sample), 1, 0, 1, conn_type.NONE, initial_phases);
            
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
        "Destructor of oscillatory network is based on Kuramoto model."
        if (self.__ccore_network_pointer is not None):
            core.destroy_syncnet_network(self.__ccore_network_pointer);
            self.__ccore_network_pointer = None;
        else:
            self._osc_loc = None;   # pointer to external object


    def _create_connections(self, radius):
        "Create connections between oscillators in line with input radius of connectivity."
        
        "(in) radius    - connectivity radius between oscillators."
        
        if (self._ena_conn_weight is True):
            self._conn_weight = [[0] * self._num_osc for index in range(0, self._num_osc, 1)];
        
        maximum_distance = 0;
        minimum_distance = numpy.Inf;
        
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
        "Network is trained via achievement sync state between the oscillators using the radius of coupling."
        
        "(in) order             - order of synchronization that is used as indication for stopping processing."
        "(in) solution          - specified type of solving diff. equation."
        "(in) collect_dynamic   - specified requirement to collect whole dynamic of the network."
        
        "Return last values of simulation time and phases of oscillators as a tuple if collect_dynamic is False, and whole dynamic"
        "if collect_dynamic is True. Format of returned value: (simulation_time, oscillator_phases)."
        
        if (self.__ccore_network_pointer is not None):
            return core.process_syncnet(self.__ccore_network_pointer, order, solution, collect_dynamic);
        else:
            return self.simulate_dynamic(order, solution, collect_dynamic);
    
    
    def phase_kuramoto(self, teta, t, argv):
        "Overrided method for calculation of oscillator phase."
        
        "(in) teta     - current value of phase."
        "(in) t        - time (can be ignored)."
        "(in) argv     - index of oscillator whose phase represented by argument teta."
        
        "Return new value of phase of oscillator with index 'argv'."
        
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
        "Return list of clusters in line with state of ocillators (phases)."
        
        "(in) eps     - tolerance level that define maximal difference between phases of oscillators in one cluster."
        
        "Return list of clusters, for example [ [cluster1], [cluster2], ... ]."
        
        if (self.__ccore_network_pointer is not None):
            return core.get_clusters_syncnet(self.__ccore_network_pointer, eps);
        else:
            return self.allocate_sync_ensembles(eps);
    
    
    def show_network(self):
        "Shows connections in the network. It supports only 2-d and 3-d representation."
        
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
    
