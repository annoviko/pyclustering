from gcolor.sync import syncgcolor;

from nnet.sync import solve_type;

from support import draw_dynamics;
from support.graph import read_graph;

from samples.definitions import GRAPH_SIMPLE_SAMPLES;


def template_graph_coloring(positive_weight, negative_weight, filename, reduction = None, title = None):
    if (title is None): title = filename;
    print("\nGraph Coloring: ", title);
    
    graph = read_graph(filename);
    network = syncgcolor(graph.data, positive_weight, negative_weight, reduction);
    
    (t, dyn) = network.process(order = 0.999, solution = solve_type.FAST, collect_dynamic = True);
    draw_dynamics(t, dyn, x_title = "Time", y_title = "Phase", y_lim = [0, 2 * 3.14]);

    clusters = network.get_clusters();
    
    for index in range(0, len(clusters)):
        print("Color #", index, ": ", clusters[index]);


def one_circle1():
    template_graph_coloring(1, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE1, None, "Circle 1");    


def one_circle2():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE2, None, "Circle 2");   
    
    
def one_circle3():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE3, None, "Circle 3");   


def broken_circle1():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE1, None, "Broken Circle 1");   
    

def broken_circle2():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_BROKEN_CIRCLE2, None, "Broken Circle 2");  


def one_crossroad():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CROSSROAD, None, "One Crossroad");


def five_pointed_star():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_STAR, None, "Five Pointed Star");   


def one_line():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_LINE, None, "One Line");      


def two_crossroads():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_TWO_CROSSROADS, None, "Two Interconnected Stars");
    
    
def five_pointed_frame_star():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_FIVE_POINTED_FRAME_STAR, None, "Five Pointed Star With Frame");    
    
    
def full_interconnected1():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_FULL1, None, "Full interconneted graph 1 (all-to-all)");      


def full_interconnected2():
    template_graph_coloring(0, -1, GRAPH_SIMPLE_SAMPLES.GRAPH_FULL2, None, "Full interconneted graph 2 (all-to-all)"); 
        
        
one_line();
one_circle1();
one_circle2();
one_circle3();
broken_circle1();
broken_circle2();
one_crossroad();
two_crossroads();
five_pointed_star();
five_pointed_frame_star();
full_interconnected1();
full_interconnected2();