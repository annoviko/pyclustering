"""!

@brief Unit-tests for Hysteresis Oscillatory Network for graph coloring.

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

import unittest;

from pyclustering.gcolor.hysteresis import hysteresisgcolor;

from pyclustering.utils.graph import read_graph;

from pyclustering.samples.definitions import GRAPH_SIMPLE_SAMPLES;

class Test(unittest.TestCase):
    def templateTestColoring(self, filename, alpha, eps, steps, time):
        graph = read_graph(filename);
        network = hysteresisgcolor(graph.data, alpha, eps);
        
        output_analyser = network.process(steps, time);
        map_coloring = output_analyser.allocate_map_coloring(0.05, 20);
        
        # Check number of colors
        assigned_colors = set(map_coloring);
        
        # Check validity of color numbers
        for color_number in range(0, len(assigned_colors), 1):
            assert color_number in assigned_colors;
            
        # Check validity of colors
        for index_node in range(len(graph.data)):
            color_neighbors = [ map_coloring[index] for index in range(len(graph.data[index_node])) if graph.data[index_node][index] != 0 and index_node != index];
            #print(index_node, map_coloring[index_node], color_neighbors, assigned_colors, map_coloring, "\n\n");
            assert map_coloring[index_node] not in color_neighbors;


    def testColoringSimple1(self):
        self.templateTestColoring(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE1, 1.2, 1.8, 1500, 15);
        
    def testColoringCircle2(self):
        self.templateTestColoring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE2, 1.1, 1.1, 1500, 15);
        
    def testColoringFivePointedFrameStar(self):
        self.templateTestColoring(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_FRAME_STAR, 1, 1, 2500, 25);
        
    def testColoringOneLine(self):
        self.templateTestColoring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_LINE, 1.2, 1.8, 1500, 15);
        
    def testColoringOneCrossroad(self):
        self.templateTestColoring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CROSSROAD, 1.2, 1.8, 1500, 15);
    
    def testColoringTwoCrossroads(self):
        self.templateTestColoring(GRAPH_SIMPLE_SAMPLES.GRAPH_TWO_CROSSROADS, 1.2, 1.8, 1500, 15);
