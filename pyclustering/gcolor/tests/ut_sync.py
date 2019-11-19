"""!

@brief Unit-tests for algorithm based on modified Sync.

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

from pyclustering.nnet import solve_type;

from pyclustering.gcolor.sync import syncgcolor;

from pyclustering.utils.graph import read_graph;

from pyclustering.samples.definitions import GRAPH_SIMPLE_SAMPLES;

class Test(unittest.TestCase):
    def templateTestColoringNegativeConnections(self, filename, solver_type = solve_type.FAST):
        result_testing = False;
        
        # If phases crosses each other because of random part of the network then we should try again.
        for attempt in range(0, 3, 1):        
            graph = read_graph(filename);
            syncgcolor_network = syncgcolor(graph.data, 0, -1);
            
            analyser = syncgcolor_network.process(solution = solver_type);
            
            map_coloring = analyser.allocate_map_coloring(0.05);
            
            # Check number of colors
            assigned_colors = set(map_coloring);
            
            # Check validity of color numbers
            for color_number in range(0, len(assigned_colors), 1):
                if (color_number not in assigned_colors):
                    continue;
                
            # Check validity of colors
            for index_node in range(len(graph.data)):
                color_neighbors = [ map_coloring[index] for index in range(len(graph.data[index_node])) if graph.data[index_node][index] != 0 and index_node != index];
                #print(index_node, map_coloring[index_node], color_neighbors, assigned_colors, map_coloring, "\n\n");
                if (map_coloring[index_node] in color_neighbors):
                    continue;
            
            result_testing = True;
                
        assert result_testing;

    def testColoringFull1(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL1);
         
    def testColoringFull2(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL2);
         
    def testColoringBrokenCircle1(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE1);
         
    def testColoringBrokenCircle2(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE2);
         
    def testColoringCircle1(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE1);
 
    def testColoringCircle2(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE2);     
         
    def testColoringFivePointedStar(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_STAR); 
         
    def testColoringFivePointedFrameStar(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_FRAME_STAR);
         
    def testColoringVerification(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE1);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE2);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_FRAME_STAR);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_STAR);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL1);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL2);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE1);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE2);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE3);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CROSSROAD);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_LINE);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE1);
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_TWO_CROSSROADS);

    
    def testOdeIntSolutionGraphFull1(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL1, solve_type.RK4);
        
    def testOdeIntSolutionGraphFull2(self):
        self.templateTestColoringNegativeConnections(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL2, solve_type.RK4);
