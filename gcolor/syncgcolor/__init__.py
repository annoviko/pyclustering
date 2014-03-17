from nnet.sync import net, conn_type, solve_type, draw_dynamics;

class syncgcolor(net):
    _network = None;
    _graph = None;
    
    def __init__(self, graph_matrix, connection_strength = 1):
        number_oscillators = len(graph_matrix);
        super().__init__(number_oscillators, -connection_strength, type_conn = conn_type.NONE);
        
        self._create_connections(graph_matrix);
        
    
    def _create_connections(self, graph_matrix):
        for row in range(0, len(graph_matrix)):
            for column in range (0, len(graph_matrix[row])):
                self._osc_conn[row][column] = graph_matrix[row][column];
                
    
    def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False, ):
        return self.simulate_dynamic(order, solution, collect_dynamic);
    
    
    def get_clusters(self, tolerance = 0.1):
        return self.allocate_sync_ensembles(tolerance);