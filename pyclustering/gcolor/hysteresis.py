"""!

@brief Graph coloring algorithm: Algorithm based on Hysteresis Oscillatory Network
@details Implementation based on paper @cite article::gcolor::hysteresis::1.

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


from pyclustering.nnet.hysteresis import hysteresis_network, hysteresis_dynamic


class hysteresis_analyser(hysteresis_dynamic):
    """!
    @brief Performs analysis of output dynamic of the hysteresis oscillatory network to extract information about clusters or color allocation.
    
    """
    
    def __init__(self, amplitudes, time):
        """!
        @brief Constructor of the analyser.
        
        @param[in] amplitudes (list): Output dynamic of the hysteresis oscillatory network, where one iteration consists of all amplitudes of oscillators.
        @param[in] time (list): Simulation time (timestamps of simulation steps) when amplitudes are stored.
        
        """
        super().__init__(amplitudes, time)


    def allocate_clusters(self, tolerance=0.1, threshold_steps=10):
        """!
        @brief Returns list of clusters in line with state of ocillators (phases).
        
        @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
        @param[in] threshold_steps (uint): Number of steps from the end of simulation that should be analysed for ensemble allocation.
                    If amount of simulation steps has been less than threshold steps than amount of steps will be reduced to amount
                    of simulation steps.
        
        @remark Results can be obtained only after network simulation (graph processing by the network).
        
        @return (list) List of clusters, for example [ [cluster1], [cluster2], ... ].
        
        @see allocate_map_coloring()
        
        """
        return self.allocate_sync_ensembles(tolerance, threshold_steps=threshold_steps)


    def allocate_map_coloring(self, tolerance, threshold_steps = 10):
        """!
        @brief Returns list of color indexes that are assigned to each object from input data space accordingly.
        
        @param[in] tolerance (double): Tolerance level that define maximal difference between outputs of oscillators in one synchronous ensemble.
        @param[in] threshold_steps (uint): Number of steps from the end of simulation that should be analysed for ensemble allocation.
                    If amount of simulation steps has been less than threshold steps than amount of steps will be reduced to amount
                    of simulation steps.
        
        @remark Results can be obtained only after network simulation (graph processing by the network).
        
        @return (list) Color indexes that are assigned to each object from input data space accordingly.
        
        @see allocate_clusters()
        
        """
        clusters = self.allocate_clusters(tolerance, threshold_steps)
        
        coloring_map = [0] * len(self._dynamic[0])
        
        for color_index in range(len(clusters)):
            for node_index in clusters[color_index]:
                coloring_map[node_index] = color_index
                
        return coloring_map


class hysteresisgcolor(hysteresis_network):
    """!
    @brief Class represents graph coloring algorithm based on hysteresis oscillatory network. 
           This is bio-inspired algorithm where the network uses relaxation oscillators that is
           regarded as a multi-vibrator. Each ensemble of synchronous oscillators corresponds to
           only one color.
    
    Example
    @code
        # import required modules
        from pyclustering.nnet.hysteresis import hysteresis_visualizer;
        
        from pyclustering.gcolor.hysteresis import hysteresisgcolor;
        
        from pyclustering.utils.graph import read_graph, draw_graph;
        
        # load graph from a file
        graph = read_graph(filename);
        
        # create oscillatory network for solving graph coloring problem
        network = hysteresisgcolor(graph.data, alpha, eps);
        
        # perform simulation of the network
        output_dynamic = network.simulate(2000, 20);
        
        # show dynamic of the network
        hysteresis_visualizer.show_output_dynamic(output_dynamic);
        
        # obtain results of graph coloring and display results
        coloring_map = hysteresis_visualizer.allocate_map_coloring();
        draw_graph(graph, coloring_map);
    @endcode
    
    """
    
    def __init__(self, graph_matrix, alpha, eps):
        """!
        @brief Constructor of hysteresis oscillatory network for graph coloring.
        
        @param[in] graph_matrix (list): Matrix representation of a graph.
        @param[in] alpha (double): Positive constant (affect weight between two oscillators w[i][j]).
        @param[in] eps (double): Positive constant (affect feedback to itself (i = j) of each oscillator w[i][j] = -alpha - eps).
                
        """
        number_oscillators = len(graph_matrix)
        
        super().__init__(number_oscillators)
        
        self._states = [0] * self._num_osc
        for i in range(0, self._num_osc):
            self._states[i] = 1 - (2 / self._num_osc) * i
        
        self._outputs = [-1] * self._num_osc
        self._outputs_buffer = [-1] * self._num_osc
        self._time_contant = 1
        
        # Create connections
        self._weight = []
        for row in range(0, self._num_osc):
            self._weight.append([0] * self._num_osc)
            for col in range(0, self._num_osc):
                if (row != col):
                    self._weight[row][col] = -alpha * (graph_matrix[row][col]) / sum(graph_matrix[row])
                else:
                    self._weight[row][col] = -alpha - eps
    
    
    def process(self, steps, time, collect_dynamic=True):
        """!
        @brief Peforms graph coloring analysis using simulation of the oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] collect_dynamic (bool): Specified requirement to collect whole dynamic of the network.
        
        @return (hysteresis_analyser) Returns analyser of results of clustering.
        
        """
        
        output_dynamic = super().simulate(steps, time, collect_dynamic=collect_dynamic)
        return hysteresis_analyser(output_dynamic.output, output_dynamic.time)
