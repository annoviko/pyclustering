'''

Graph coloring algorithm: Algorithm based on Hysteresis Oscillatory Network

Based on article description:
 - K.Jinno, H.Taguchi, T.Yamamoto, H.Hirose. Dynamical Hysteresis Neural Network for Graph Coloring Problem. 2003.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

from pyclustering.nnet.hysteresis import hysteresis_network;

class hysteresisgcolor(hysteresis_network):
    def __init__(self, graph_matrix, alpha, eps):
        number_oscillators = len(graph_matrix);
        
        super().__init__(number_oscillators);
        
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
    
    def get_map_coloring(self, tolerance = 0.1):
        clusters = self.get_clusters(tolerance);
        
        coloring_map = [0] * self._num_osc;
        
        for color_index in range(len(clusters)):
            for node_index in clusters[color_index]:
                coloring_map[node_index] = color_index;
                
        return coloring_map;
    