from nnet.sync import sync_network, conn_type, solve_type;
from support import draw_dynamics;
import math;


class syncgcolor(sync_network):
    _positive_weight = None;
    _negative_weight = None;
    _reduction = None;
    
    def __init__(self, graph_matrix, positive_weight, negative_weight, reduction = None):
        number_oscillators = len(graph_matrix);
        super().__init__(number_oscillators, type_conn = conn_type.NONE);
        
        if (reduction == None):
            self._reduction = self._num_osc;
        else:
            self._reduction = reduction;
        
        self._positive_weight = positive_weight;
        self._negative_weight = negative_weight;
        
        self._create_connections(graph_matrix);
        
    
    def _create_connections(self, graph_matrix):
        "Create connection in the network in line with graph."

        "(in) graph_matrix     - matrix representation of the graph"
        
        for row in range(0, len(graph_matrix)):
            for column in range (0, len(graph_matrix[row])):
                self._osc_conn[row][column] = graph_matrix[row][column];
                
    
    def phase_kuramoto(self, teta, t, argv):
        "Return result of phase calculation for oscillator in the network"
        "Solvers as ODEINT or ODE may pass only one value if their extra argument has length equals to one"
        
        "(in) teta     - value of phase of the oscillator with index argv in the network"
        "(in) t        - unused"
        "(in) argv     - index of the oscillator in the network"
        
        "Return new value of phase for oscillator with index argv"
        
        index = argv;
        phase = 0;
        
        for k in range(0, self.num_osc):
            if (self.has_connection(index, k) == True):
                phase += self._negative_weight * math.sin(self._phases[k] - teta);
            else:
                phase += self._positive_weight * math.sin(self._phases[k] - teta);
            
        return ( phase / self._reduction );        
    
    
    def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False):
        "Perform simulation of the network (perform solving of graph coloring problem"
        
        "(in) order            - defines when process of synchronization in the network is over. Range from 0 to 1."
        "(in) solution         - defines type (method) of solving diff. equation"
        "(in) collect_dynamic  - if True - return full dynamic of the network, otherwise - last state of phases"
        
        "Return dynamic of the network (time, phases)"
        
        return self.simulate_dynamic(order, solution, collect_dynamic);
    
    
    def get_clusters(self, tolerance = 0.1):
        "Return allocated clusters, when one cluster defines only one color"
        
        "(in) tolerance        - defines maximum deviation between phases"
        
        "Return allocated clusters [vertices with color 1], [vertices with color 2], ..., [vertices with color n]"
        
        return self.allocate_sync_ensembles(tolerance);
    