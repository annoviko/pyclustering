"""!

@brief Examples of usage and demonstration of abilities of DSATUR algorithm in graph coloring.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from pyclustering.utils.graph import read_graph, draw_graph;

from pyclustering.samples.definitions import GRAPH_SIMPLE_SAMPLES;

from pyclustering.gcolor.dsatur import dsatur;

def template_graph_coloring(filename):
    graph = read_graph(filename);
    
    dsatur_instance = dsatur(graph.data);
    dsatur_instance.process();
    coloring = dsatur_instance.get_colors();
    
    print("Number colors: ", max(coloring));
    
    draw_graph(graph, coloring);
    
    
def run_all_graph_simple_samples():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE1);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE2);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_FRAME_STAR);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_STAR);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL1);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL2);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE1);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE2);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE3);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CROSSROAD);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_LINE);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_TWO_CROSSROADS);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE1);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE2);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE3);


run_all_graph_simple_samples();