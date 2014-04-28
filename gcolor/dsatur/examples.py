from support.graph import read_graph, draw_graph;

from samples.definitions import GRAPH_SIMPLE_SAMPLES;

from gcolor.dsatur import dsatur;

def template_graph_coloring(filename):
    graph = read_graph(filename);
    coloring = dsatur(graph.data);
    
    draw_graph(graph, coloring);
    
    
def run_all_graph_samples():
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
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE1);
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_TWO_CROSSROADS);

run_all_graph_samples();    