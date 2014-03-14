from nnet.sync import *;

from syncnet import syncnet;
from support import average_neighbor_distance, read_sample, draw_clusters;

class hsyncnet(syncnet):
    def __init__(self, source_data):
        super().__init__(source_data);
    
    def process(self, number_clusters, order = 0.998, solution = solve_type.FAST, collect_dynamic = False):
        number_neighbors = 3;
        current_number_clusters = numpy.Inf;
        
        while(current_number_clusters > number_clusters):
            radius = average_neighbor_distance(self._osc_loc, number_neighbors);
            self._create_connections(radius);
        
            self.simulate_dynamic(order, solution, collect_dynamic);
            clusters = self.get_clusters();
            
            current_number_clusters = len(clusters);
            number_neighbors += 1;
        

sample = read_sample('../Samples/SampleSimple1.txt');
network = hsyncnet(sample);

network.process(2);

# draw_dynamics(dyn_time, dyn_phase);

clusters = network.get_clusters();
draw_clusters(sample, clusters);
