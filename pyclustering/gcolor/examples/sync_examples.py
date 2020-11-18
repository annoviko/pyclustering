"""!

@brief Examples of usage and demonstration of abilities of algorithm (based on modified Sync) in graph coloring.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from pyclustering.gcolor.sync import syncgcolor;

from pyclustering.nnet import *;

from pyclustering.utils import draw_dynamics;
from pyclustering.utils.graph import read_graph, draw_graph;

from pyclustering.samples.definitions import GRAPH_SIMPLE_SAMPLES;


def template_graph_coloring(positive_weight, negative_weight, filename, reduction = None, title = None):
    if (title is None): title = filename;
    print("\nGraph Coloring: ", title);
    
    graph = read_graph(filename);
    network = syncgcolor(graph.data, positive_weight, negative_weight, reduction);
    
    analyser = network.process(order = 0.999, solution = solve_type.FAST, collect_dynamic = True);
    sync.sync_visualizer.show_output_dynamic(analyser);

    clusters = analyser.allocate_color_clusters();
    
    for index in range(0, len(clusters)):
        print("Color #", index, ": ", clusters[index]);
        
    coloring_map = analyser.allocate_map_coloring();
    print("Number colors: ", max(coloring_map));
    
    draw_graph(graph, coloring_map);
    
    # Check validity of colors
    for index_node in range(len(graph.data)):
        color_neighbors = [ coloring_map[index] for index in range(len(graph.data[index_node])) if graph.data[index_node][index] != 0 and index_node != index];
        #print(index_node, map_coloring[index_node], color_neighbors, assigned_colors, map_coloring, "\n\n");
        
        if (coloring_map[index_node] in color_neighbors):
            print("Warining: Incorrect coloring");
            return;


def run_all_graph_simple_samples():
    template_graph_coloring(1, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE1, None, "Circle 1");    
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE2, None, "Circle 2");   
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE3, None, "Circle 3");   
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE1, None, "Broken Circle 1");   
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE2, None, "Broken Circle 2");  
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CROSSROAD, None, "One Crossroad");
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_STAR, None, "Five Pointed Star");   
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_LINE, None, "One Line");      
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_TWO_CROSSROADS, None, "Two Interconnected Stars");
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_FRAME_STAR, None, "Five Pointed Star With Frame");    
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_FULL1, None, "Full interconneted graph 1 (all-to-all)");      
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_FULL2, None, "Full interconneted graph 2 (all-to-all)"); 
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE1, None, "Simple 1"); 
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE2, None, "Simple 2");
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE3, None, "Simple 3");  


run_all_graph_simple_samples();