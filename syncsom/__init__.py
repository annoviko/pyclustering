from nnet.som import som, type_conn;
from nnet.sync import sync_network;
from syncnet import syncnet;
from support import average_neighbor_distance, read_sample, draw_clusters;

class syncsom:
    _som = None;
    _data = None;       # Pointer to input data
    _sync = None;
    _struct = None;
    
    # For convenience
    _som_osc_table = None;
    
    @property
    def weights(self):
        return self._som.weights;
    
    def __init__(self, data, rows, cols):
        self._data = data;
        self._som = som(rows, cols, data, 100, conn_type = type_conn.grid_four);
        self._som_osc_table = list();
    
    def assert_capture_points(self):
        # TODO: Should be moved to unit-test
        capture_points = 0;
        hiper_cluster = list();
        for index in range(len(self._som.capture_objects)):
            assert self._som.awards[index] == len(self._som.capture_objects[index]);
            if (self._som.awards[index] > 0):
                capture_points += len(self._som.capture_objects[index]);
                hiper_cluster += self._som.capture_objects[index];
            
        print("[POINTS] Capture: ", capture_points, ", Real: ", len(self._data));
        assert capture_points == len(self._data);
        assert len(hiper_cluster) == len(self._data);
        
    
    def process(self, number_neighbors, collect_dynamic = False, order = 0.999):
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
        radius = average_neighbor_distance(weights, number_neighbors);
        
        # create oscillatory neural network.
        self._sync = syncnet(weights);
        (dyn_time, dyn_phase) = self._sync.process(radius, order, collect_dynamic = collect_dynamic);
        
        # Draw SOM clusters.
        #clusters = self._sync.get_clusters();
        #draw_clusters(weights, clusters);
        #self._som.show_network(awards = False, belongs = True);
        
        # return dynamic if it was requested.
        return (dyn_time, dyn_phase);
    
    def get_som_clusters(self, eps = 0.1):
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
        print("[POINTS] Capture: ", capture_points, ", Real: ", len(self._data));
        assert capture_points == len(self._data);
        
        return clusters;
        
    def show_som_layer(self):
        self._som.show_network();
    
    def show_sync_layer(self):
        self._sync.show_network();
        
        

# sample = read_sample('../samples/SampleChainlink.txt');
# 
# # Create network
# network = syncsom(sample, 9, 9);
# 
# # Run processing
# (dyn_time, dyn_phase) = network.process(20, collect_dynamic = False);
# 
# from support import draw_dynamics;
# # Show dynamic of the last layer.
# draw_dynamics(dyn_time, dyn_phase);
# 
# clusters = network.get_som_clusters(0.1);
# draw_clusters(network.weights, clusters);
# 
# 
# clusters = network.get_clusters(0.1);
# draw_clusters(sample, clusters);
    