"""!

@brief Graph coloring algorithm based on Sync Oscillatory Network
@details Implementation based on paper @cite article::gcolor::sync::1.
         
@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
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

from pyclustering.nnet import *
from pyclustering.nnet.sync import sync_network
from pyclustering.nnet.sync import sync_dynamic


class syncgcolor_analyser(sync_dynamic):
    """!
    @brief Analyser of output dynamic of the oscillatory network syncgcolor.
    
    """
        
    def __init__(self, phase, time, pointer_sync_analyser):
        """!
        @brief Constructor of the analyser.
        
        @param[in] phase (list): Output dynamic of the oscillatory network, where one iteration consists of all phases of oscillators.
        @param[in] time (list): Simulation time.
        @param[in] pointer_sync_analyser (POINTER): Pointer to CCORE analyser, if specified then other arguments can be omitted.
        
        """
        
        super().__init__(phase, time, pointer_sync_analyser);
    
    
    def allocate_color_clusters(self, tolerance = 0.1):
        """!
        @brief Allocates clusters, when one cluster defines only one color.
        
        @param[in] tolerance (double): Defines maximum deviation between phases.
        
        @return (list) Clusters [vertices with color 1], [vertices with color 2], ..., [vertices with color n].
        
        """
        
        return self.allocate_sync_ensembles(tolerance);
    
    
    def allocate_map_coloring(self, tolerance = 0.1):
        """!
        @brief Allocates coloring map for graph that has been processed.
        
        @param[in] tolerance (double): Defines maximum deviation between phases.
        
        @return (list) Colors for each node (index of node in graph), for example [color1, color2, color2, ...].
        
        """
        
        clusters = self.allocate_color_clusters(tolerance);
        number_oscillators = len(self._dynamic[0]);
        
        coloring_map = [0] * number_oscillators;
        
        for color_index in range(len(clusters)):
            for node_index in clusters[color_index]:
                coloring_map[node_index] = color_index;
                
        return coloring_map;
    

class syncgcolor(sync_network):
    """!
    @brief Oscillatory network based on Kuramoto model with negative and positive connections for graph coloring problem.
    
    """
    
    def __init__(self, graph_matrix, positive_weight, negative_weight, reduction = None):
        """!
        @brief Constructor of the oscillatory network syncgcolor for graph coloring problem.
        
        @param[in] graph_matrix (list): Graph represented by matrix.
        @param[in] positive_weight (double): Value of weight of positive connections.
        @param[in] negative_weight (double): Value of weight of negative connections.
        @param[in] reduction (bool): Inverse degree of the processed graph.
        
        """
        number_oscillators = len(graph_matrix);
        super().__init__(number_oscillators, type_conn = conn_type.DYNAMIC, ccore = False);
        
        if (reduction == None):
            self._reduction = self._num_osc;
        else:
            self._reduction = reduction;

        self._positive_weight = positive_weight;
        self._negative_weight = negative_weight;
        
        self._create_connections(graph_matrix);
        
    
    def _create_connections(self, graph_matrix):
        """!
        @brief Creates connection in the network in line with graph.
        
        @param[in] graph_matrix (list): Matrix representation of the graph.
        
        """
        
        for row in range(0, len(graph_matrix)):
            for column in range (0, len(graph_matrix[row])):
                if (graph_matrix[row][column] > 0):
                    self.set_connection(row, column);
                
    
    def _phase_kuramoto(self, teta, t, argv):
        """!
        @brief Returns result of phase calculation for oscillator in the network.
        
        @param[in] teta (double): Value of phase of the oscillator with index argv in the network.
        @param[in] t (double): Unused, can be ignored.
        @param[in] argv (uint): Index of the oscillator in the network.
        
        @return (double) New value of phase for oscillator with index argv.
        
        """
        
        index = argv;
        phase = 0;
        
        for k in range(0, self._num_osc):
            if (self.has_connection(index, k) == True):
                phase += self._negative_weight * math.sin(self._phases[k] - teta);
            else:
                phase += self._positive_weight * math.sin(self._phases[k] - teta);
            
        return ( phase / self._reduction );
    
    
    def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False):
        """!
        @brief Performs simulation of the network (performs solving of graph coloring problem).
        
        @param[in] order (double): Defines when process of synchronization in the network is over, range from 0 to 1.
        @param[in] solution (solve_type): defines type (method) of solving diff. equation.
        @param[in] collect_dynamic (bool): If True - return full dynamic of the network, otherwise - last state of phases.
        
        @return (syncnet_analyser) Returns analyser of results of coloring.
        
        """
        
        analyser = self.simulate_dynamic(order, solution, collect_dynamic);
        return syncgcolor_analyser(analyser.output, analyser.time, None);
    
    