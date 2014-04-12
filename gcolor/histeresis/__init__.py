from nnet.hysteresis import hysteresis_network;

from support import read_sample;
from support import draw_dynamics;

from samples.definitions import GRAPH_SIMPLE_SAMPLES;

class hysteresisgcolor(hysteresis_network):
    def __init__(self, graph_matrix, alpha, eps):
        self._num_osc = len(graph_matrix);
        
        self._states = [0] * self._num_osc;
        for i in range(0, self._num_osc):
            self._states[i] = 1 - (2 / self._num_osc) * i;
        
        self._outputs = [-1] * self._num_osc;
        self._outputs_buffer = [-1] * self._num_osc;
        self._time_contant = 1;
        
        # Create connections
        self._weight = [];
        for row in range(0, self._num_osc):
            self._weight.append([0] * self._num_osc);
            for col in range(0, self._num_osc):
                if (row != col):
                    self._weight[row][col] = -alpha * (graph_matrix[row][col]) / sum(graph_matrix[row]);
                else:
                    self._weight[row][col] = -alpha - eps;
        
    def get_clusters(self, tolerance = 0.1):
        return self.allocate_sync_ensembles(tolerance);
    
    
# graph_matrix_repr = read_sample(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE1);
# network = hysteresisgcolor(graph_matrix_repr, 1.2, 3.8);
# 
# (t, dyn) = network.simulate(10000, 20);
# draw_dynamics(t, dyn);
# print(network.get_clusters());