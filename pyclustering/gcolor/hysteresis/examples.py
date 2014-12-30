from pyclustering.gcolor.hysteresis import hysteresisgcolor;

from pyclustering.support.graph import read_graph, draw_graph;
from pyclustering.support import draw_dynamics;

from pyclustering.samples.definitions import GRAPH_SIMPLE_SAMPLES;

def template_graph_coloring(filename, alpha, eps, steps, time, title = None, tolerance = 0.1):
    if (title is None): title = filename;
    
    graph = read_graph(filename);
    network = hysteresisgcolor(graph.data, alpha, eps);
    
    (t, dyn) = network.simulate(steps, time);
    draw_dynamics(t, dyn, x_title = "Time", y_title = "State");
    
    clusters = network.get_clusters(tolerance);
    for index in range(0, len(clusters)):
        print("Color #", index, ": ", clusters[index]);
    
    coloring_map = network.get_map_coloring(tolerance);
    draw_graph(graph, coloring_map);


def graph_simple1():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE1, 1.2, 1.8, 2000, 20);
    
def graph_one_line():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_LINE, 1.2, 1.8, 2000, 20);
    
def graph_one_crossroad():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CROSSROAD, 1.2, 1.8, 2000, 20);
    
def graph_two_crossroads():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_TWO_CROSSROADS, 1.2, 1.8, 2000, 20);
    
def graph_full_interconnected1():
    "Bad result - two vertices colored by the same color"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL1, 1.2, 1.8, 2000, 20, tolerance = 0.05);
    
def graph_full_interconnected2():
    "Good result - optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL2, 1.2, 1.8, 2000, 20, tolerance = 0.05);

def graph_one_circle1():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE1, 1.1, 1.1, 2000, 20);

def graph_one_circle2():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE2, 1.1, 1.1, 2000, 20);

def graph_one_circle3():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE3, 1.1, 1.1, 2000, 20);

def graph_five_pointed_frame_star():
    "Good result - not optimal"
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_FRAME_STAR, 1.1, 1.4, 3000, 30);



graph_simple1();
graph_one_line();
graph_one_crossroad();
graph_two_crossroads();
graph_full_interconnected1();
graph_full_interconnected2();
graph_one_circle1();
graph_one_circle2();
graph_one_circle3();
graph_five_pointed_frame_star();