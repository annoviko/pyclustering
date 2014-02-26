import numpy;
import random;
import math;
import scipy.spatial;

import matplotlib.pyplot as plt;

from scipy import pi;
from scipy.integrate import odeint;
from scipy.integrate import ode;
from scipy.spatial import distance;
from support import euclidean_distance;


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


    def __init__(self, num_osc, weight, frequency = False, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.MATRIX, initial_phases = initial_type.RANDOM_GAUSSIAN):
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
        self.__create_connections(type_conn);
        
    
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

    
    def __create_connections(self, type_conn = conn_type.ALL_TO_ALL):
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
        "Return lists of synchonized ensembles of oscillators"     
        "BUG: When we have high disorder and high tolerance then we can allocate several clusters that can have shared oscillators"   
        clusters = list();
        if (self.num_osc > 0):
            clusters.append( (self._phases[0], [0]) );
        
        for index in range(1, self.num_osc, 1):
            allocated = False;
            for cluster in clusters:
                if ( abs(cluster[0] - self._phases[index]) < tolerance ):
                    allocated = True;
                    cluster[1].append(index);
            
            if (allocated != True):
                clusters.append( (self._phases[index], [index]) );
        
        return clusters;
    
    
    def simulate(self, steps, time, solution = solve_type.FAST, collect_dynamic = True):
        "Simulate phase dynamics of network and return simulated dynamic"
        return self.simulate_static(steps, time, solution, collect_dynamic);


    def simulate_dynamic(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False):
        "Simulate network until level synchronization level (order) is not reached"
        # For statistics
        iter_counter = 0;
        
        # If requested input dynamics
        dyn_phase = None;
        dyn_time = None;
        if (collect_dynamic == True):
            dyn_phase = list();
            dyn_time = list();
            
            dyn_phase.append(self._phases);
            dyn_time.append(0);
        
        # Execute until sync state will be reached
        while (self.sync_local_order() < order):
            iter_counter += 1;
            
            # update states of oscillators
            self._phases = self._calculate_phases(solution, 0, 0.1, 1);
            
            # If requested input dynamic
            if (collect_dynamic == True):
                dyn_phase.append(self._phases);
                dyn_time.append(iter_counter);
            else:
                dyn_phase = self._phases;
                dyn_time = iter_counter;
        
#             print("Local order: ", self.sync_local_order());
#             print("Order: ", self.sync_order());
#             if (iter_counter % 10):
#                 draw_dynamics(dyn_time, dyn_phase);
                
        
        #print("Number of iteration: ", iter_counter);
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
        


class trainnet(net):
    "This oscillatory neural network can be trained by input data and after can be used for classification problem"
    _osc_loc = None;     # Location of each oscillator in a N-dimensional space.
    
    def __init__(self, source_data, conn_repr = conn_represent.MATRIX):
        file = open(source_data, 'r');
        sample = [[float(val) for val in line.split()] for line in file];
        file.close();
        
        super().__init__(len(sample), 1, False, conn_type.NONE);
        
        self._osc_loc = sample;
        self._conn_represent = conn_repr;

        # Connections will be represent by lists.
        if (conn_repr == conn_represent.MATRIX):
            self._osc_conn = [[0] * self._num_osc for index in range(0, self._num_osc, 1)];
            
        elif (conn_repr == conn_represent.LIST):
            self._osc_conn = [[] for index in range(0, self._num_osc, 1)];
            
        else:
            raise NameError("Unknown type of representation of coupling between oscillators");
    
    
    def train(self, radius, order = 0.995, solution = solve_type.FAST):
        "Network is trained via achievement sync state between the oscillators using the radius of coupling"
        # Create connections
        for i in range(0, self._num_osc, 1):
            for j in range(0, self._num_osc, 1):
                dist = euclidean_distance(self._osc_loc[i], self._osc_loc[j]);
                if (dist <= radius):
                    if (self._conn_represent == conn_represent.LIST):
                        self._osc_conn[i].append(j);
                    else:
                        self._osc_conn[i][j] = True;
        
        # Execute until sync state will be reached
        while (self.sync_local_order() < order):
            next_phases = [0] * self.num_osc;    # new oscillator _phases
            
            for index in range (0, self.num_osc, 1):
                if (solution == solve_type.FAST):
                    result = self._phases[index] + self.phase_kuramoto(self._phases[index], 0, index);
                    next_phases[index] = phase_normalization(result);
                    
                elif (solution == solve_type.ODEINT):
                    result = odeint(self.phase_kuramoto, self._phases[index], numpy.arange(0, 0.1, 1), (index , ));
                    next_phases[index] = phase_normalization(result[len(result) - 1][0]);
                    
                else:
                    "Nothing"
            
            # update states of oscillators
            self._phases = next_phases;
        
        # Reconnect
        self._osc_conn.clear();
        if (self._conn_represent == conn_represent.LIST):
            self._osc_conn = [[] for index in range(0, self._num_osc, 1)]; 
        else:
            self._osc_conn = [[False] * self._num_osc for index in range(self._num_osc)];
        
        for i in range(0, self._num_osc, 1):
            for j in range(0, self._num_osc, 1):
                if (abs(self._phases[i] - self._phases[j]) < 0.1):
                    if (self._conn_represent == conn_represent.LIST):
                        self._osc_conn[i].append(j);
                    else:
                        self._osc_conn[i][j] = True;
    
    
    def get_neighbors(self, index):
        "Return list of neighbors of a oscillator with sequence number 'index'"
        if (self._conn_represent == conn_represent.LIST):
            return self._osc_conn[index];      # connections are represented by list.
        elif (self._conn_represent == conn_represent.MATRIX):
            return [neigh_index for neigh_index in range(self._num_osc) if self._osc_conn[index][neigh_index] == True];
        else:
            raise NameError("Unknown type of representation of connections");
    
    
    def phase_kuramoto(self, teta, t, argv):
        "Overrided method for calculation of oscillator phase"
        index = argv;   # index of oscillator
        phase = 0;      # phase of a specified oscillator that will calculated in line with current env. states.
        
        neighbors = self.get_neighbors(index);
        for k in neighbors:
            phase += math.sin(self._cluster * (self._phases[k] - teta));
            
        return ( self._freq[index] + (phase * self._weight / len(neighbors)) );    
    
    
    def classify(self, data):
        "Classify input data by trained network"
        "In this case we no need to recalculate sync states of oscillators which compose trained network - it's locked states!"
        pass;
    
    
    def classify_and_learn(self, data):
        "Classify input data and learn changes that occur during classification"
        pass;
    
    
    def show(self):
        "Show connections in the network. It supports only 2-d and 3-d representation."
        if (len(self._osc_loc) > 3 and len(self._osc_loc) < 2):
            raise NameError('Network that is located in different from 2-d and 3-d dimensions can not be represented');
        
        from matplotlib.font_manager import FontProperties;
        from matplotlib import rcParams;
    
        rcParams['font.sans-serif'] = ['Arial'];
        rcParams['font.size'] = 12;

        fig = plt.figure();
        axes = fig.add_subplot(111);

        surface_font = FontProperties();
        surface_font.set_name('Arial');
        surface_font.set_size('12');
        
        for i in range(0, self.num_osc, 1):
            axes.plot(self._osc_loc[i][0], self._osc_loc[i][1], 'bo');  
            if (self._conn_represent == conn_represent.MATRIX):
                for j in range(self._num_osc):
                    if (self.has_connection(i, j) == True):
                        axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], 'b-', linewidth=0.5);    
                        
            else:
                for j in self.get_neighbors(i):
                    if (self.has_connection(i, j) == True):
                        axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], 'b-', linewidth=0.5);    
                                            
        plt.grid();
        plt.show();



def phase_normalization(teta):
    "Normalization of phase of oscillator that should be placed between [0; 2 * pi]"
    norm_teta = teta;
    while (norm_teta > (2 * pi)) or (norm_teta < 0):
        if (norm_teta > (2 * pi)):
            norm_teta -= 2 * pi;
        else:
            norm_teta += 2 * pi;
    
    return norm_teta;



def draw_dynamics(t, dyn_phase):
    "Draw dynamics of ocillators in the network"
    from matplotlib.font_manager import FontProperties;
    from matplotlib import rcParams;
    
    rcParams['font.sans-serif'] = ['Arial'];
    rcParams['font.size'] = 12;
    
    fig = plt.figure();
    axes = fig.add_subplot(111);
    
    surface_font = FontProperties();
    surface_font.set_name('Arial');
    surface_font.set_size('12');
    
    num_items = len(dyn_phase[0]);
    
    for index in range(0, num_items, 1):       
        y = [item[index] for item in dyn_phase];
        axes.plot(t, y, 'b-', linewidth=0.5);    

    plt.ylabel('Phase', fontproperties=surface_font);
    plt.xlabel('Time', fontproperties=surface_font);
    plt.ylim(0, 2 * math.pi);

    plt.grid();
    plt.show();



#network = trainnet('D:\\userdata\\annoviko\\workspace\\Clastering\\Samples\\SampleSimple1.txt');
#network.train(0.5);
#network.show();


# network = net(10, 1, False, conn_type.ALL_TO_ALL);   
# network.cluster = 2;
# 
# network.simulate_dynamic(collect_dynamic = True);
# clusters = network.allocate_sync_ensembles(0.1);
# 
# assert len(clusters) == 2;
