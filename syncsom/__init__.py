from nnet.som import som, type_conn;
from nnet.sync import sync_network;
from nnet import initial_type;

from syncnet import syncnet;

from support import average_neighbor_distance, read_sample, draw_clusters;

class syncsom:
    _som = None;        # The first (input) later - SOM layer.
    _data = None;       # Pointer to input data.
    _sync = None;       # The second (output) layer - Sync layer.
    _struct = None;     # Structure of connections between oscillators in the second layer - Sync layer.
    
    # For convenience
    _som_osc_table = None;
    
    @property
    def som_layer(self):
        return self._som;
    
    @property
    def sync_layer(self):
        return self._sync;
    
    def __init__(self, data, rows, cols):
        "Constructor of the double layer oscillatory network SYNC-SOM."
        
        "(in) data    - input data that is presented as list of points (objects), each point should be represented by list or tuple."
        "(in) rows    - rows of neurons (number of neurons in column) in the input layer (self-organized feature map)."
        "(in) cols    - columns of neurons (number of neurons in row) in the input later (self-organized feature map)."
        
        self._data = data;
        self._som = som(rows, cols, data, 100, conn_type = type_conn.grid_four);
        self._som_osc_table = list();        
    
    def process(self, number_neighbours, collect_dynamic = False, order = 0.999):
        "Performs simulation of the oscillatory network. Returns results of simulation."
        
        "(in) number_neighbours   - number of neighbours that should be used for calculation average distance and creation connections between oscillators."
        "(in) collect_dynamic     - if True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics."
        "(in) order               - order of process synchronization, destributed 0..1."
        
        "Returns dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,"
        "otherwise returns only last values (last step of simulation) of dynamic."
        
        # train self-organization map.
        self._som.train();
        
        # prepare to build list.
        weights = list();
        self._som_osc_table.clear();        # must be cleared, if it's used before.
        for i in range(self._som.size):
            if (self._som.awards[i] > 0):
                weights.append(self._som.weights[i]);
                self._som_osc_table.append(i);
        
        # calculate trusted distance between objects.
        radius = 0;
        if (len(weights) >= number_neighbours):
            radius = average_neighbor_distance(weights, number_neighbours);
        else:
            radius = 0;
        
        # create oscillatory neural network.
        self._sync = syncnet(weights, initial_phases = initial_type.EQUIPARTITION);
        (dyn_time, dyn_phase) = self._sync.process(radius, order, collect_dynamic = collect_dynamic);
        
        # Draw SOM clusters.
        #clusters = self._sync.get_clusters();
        #draw_clusters(weights, clusters);
        #self._som.show_network(awards = False, belongs = True);
        
        # return dynamic if it was requested.
        return (dyn_time, dyn_phase);   
    
    def get_som_clusters(self, eps = 0.1):
        "Returns clusters with SOM neurons that encode input features in line with result of synchronization in the second (Sync) layer."
        
        "(in) eps    - maximum error for allocation of synchronous ensemble oscillators."
        
        "Returns list of clusters that are represented by lists of indexes of neurons that encode input data."
        
        sync_clusters = self._sync.get_clusters();
        
        # Decode it to indexes of SOM neurons
        som_clusters = list();
        for oscillators in sync_clusters:
            cluster = list();
            for index_oscillator in oscillators:
                index_neuron = self._som_osc_table[index_oscillator];
                cluster.append(index_neuron);
                
            som_clusters.append(cluster);
            
        return som_clusters;
            
    
    def get_clusters(self, eps = 0.1):
        "Returns clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster."
        
        "(in) eps    - maximum error for allocation of synchronous ensemble oscillators."
        
        "Returns list of grours (lists) of indexes of synchronous oscillators."
        "For example [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ]."
        
        sync_clusters = self._sync.get_clusters(eps);       # NOTE: it isn't indexes of SOM neurons
        
        clusters = list();
        total_winners = 0;
        total_number_points = 0;
        for oscillators in sync_clusters:
            cluster = list();
            for index_oscillator in oscillators:
                index_neuron = self._som_osc_table[index_oscillator];
                assert self._som.awards[index_neuron] == len(self._som.capture_objects[index_neuron]);      # TODO: Should be moved to unit-test
                assert self._som.awards[index_neuron] > 0;              # TODO: Should be moved to unit-test
                
                cluster += self._som.capture_objects[index_neuron];
                total_number_points += len(self._som.capture_objects[index_neuron]);
                total_winners += 1;
                
            clusters.append(cluster);
        
        assert self._som.get_winner_number() == total_winners;      # TODO: Should be moved to unit-test
        assert len(self._data) == total_number_points;              # TODO: Should be moved to unit-test
        
        # TODO: Should be moved to unit-test
        capture_points = 0;
        for points in clusters:
            capture_points += len(points);
        # print("[POINTS] Capture: ", capture_points, ", Real: ", len(self._data));
        assert capture_points == len(self._data);
        
        return clusters;


    def show_som_layer(self):
        "Shows visual representation of the first (SOM) layer."
        
        self._som.show_network();
    
    
    def show_sync_layer(self):
        "Shows visual representation of the second (Sync) layer."
        
        self._sync.show_network();
        