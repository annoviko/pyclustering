from gcolor.hysteresis import hysteresisgcolor;

from support.graph import read_graph, draw_graph;
from support import draw_dynamics;

from samples.definitions import GRAPH_SIMPLE_SAMPLES;

def template_graph_coloring(filename, alpha, eps, steps, time, title = None):
    if (title is None): title = filename;
    
    graph = read_graph(filename);
    network = hysteresisgcolor(graph.data, alpha, eps);
    
    (t, dyn) = network.simulate(steps, time);
    draw_dynamics(t, dyn, x_title = "Time", y_title = "State");
    
    clusters = network.get_clusters(0.1);
    for index in range(0, len(clusters)):
        print("Color #", index, ": ", clusters[index]);
    
    coloring_map = network.get_map_coloring();
    draw_graph(graph, coloring_map);


def graph_simple1():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_SIMPLE1, 1.2, 1.8, 2000, 20);

def graph_one_circle1():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE1, 1.1, 1.1, 2000, 20);

def graph_one_circle2():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE2, 1.1, 1.1, 2000, 20);

def graph_one_circle3():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE3, 1.1, 1.1, 2000, 20);

def graph_five_pointed_frame_star():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_FRAME_STAR, 1, 1, 3000, 30);


graph_simple1();
graph_one_circle1();
graph_one_circle2();
graph_one_circle3();
graph_five_pointed_frame_star();