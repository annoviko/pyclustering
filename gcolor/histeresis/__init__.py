from nnet.hysteresis import hysteresis_network;

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
    