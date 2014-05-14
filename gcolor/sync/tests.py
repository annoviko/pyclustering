import unittest;

from gcolor.sync import syncgcolor;

from support.graph import read_graph;

from samples.definitions import GRAPH_SIMPLE_SAMPLES;

class Test(unittest.TestCase):
    def templateTestColoringNegativeConnections(self, filename):
        graph = read_graph(filename);
        syncgcolor_network = syncgcolor(graph.data, 0, -1);
        
        syncgcolor_network.process();
        map_coloring = syncgcolor_network.get_map_coloring(0.05);
        
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

if __name__ == "__main__":
    unittest.main();