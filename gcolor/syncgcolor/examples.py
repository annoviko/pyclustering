from gcolor.syncgcolor import syncgcolor;
from nnet.sync import net, conn_type, solve_type, draw_dynamics;

def template_graph_coloring(strength, graph_matrix_repr, title = "Sample"):
    print("\nGraph Coloring: ", title);
    network = syncgcolor(graph_matrix_repr, strength);
    
    (t, dyn) = network.process(collect_dynamic = True);
    draw_dynamics(t, dyn);

    clusters = network.get_clusters();
    
    for index in range(0, len(clusters)):
        print("Color #", index, ": ", clusters[index]);


def one_circle1():
    graph_matrix_repr = [ [0, 1, 0, 0, 1],
                          [1, 0, 1, 0, 0],
                          [0, 1, 0, 1, 0],
                          [0, 0, 1, 0, 1],
                          [1, 0, 0, 1, 0] ];
                          
    template_graph_coloring(1, graph_matrix_repr, "Circle 1");    


def one_circle2():
    graph_matrix_repr = [ [0, 1, 0, 0, 0, 1],
                          [1, 0, 1, 0, 0, 0],
                          [0, 1, 0, 1, 0, 0],
                          [0, 0, 1, 0, 1, 0],
                          [0, 0, 0, 1, 0, 1],
                          [1, 0, 0, 0, 1, 0] ];
                          
    template_graph_coloring(1, graph_matrix_repr, "Circle 2");   
    
    
def one_circle3():
    graph_matrix_repr = [ [0, 1, 0, 0, 0, 0, 1],
                          [1, 0, 1, 0, 0, 0, 0],
                          [0, 1, 0, 1, 0, 0, 0],
                          [0, 0, 1, 0, 1, 0, 0],
                          [0, 0, 0, 1, 0, 1, 0],
                          [0, 0, 0, 0, 1, 0, 1],
                          [1, 0, 0, 0, 0, 1, 0] ];
                          
    template_graph_coloring(1, graph_matrix_repr, "Circle 3");   


def one_star():
    graph_matrix_repr = [ [0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 1],
                          [1, 1, 1, 1, 0] ];
                          
    template_graph_coloring(1, graph_matrix_repr, "One Star");


def one_line():
    graph_matrix_repr = [ [0, 1, 0, 0, 0],
                          [1, 0, 1, 0, 0],
                          [0, 1, 0, 1, 0],
                          [0, 0, 1, 0, 1],
                          [0, 0, 0, 1, 0] ];
                          
    template_graph_coloring(1, graph_matrix_repr, "One Line");      


def two_interconnected_stars():
    graph_matrix_repr = [ [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                          [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 1, 1, 1, 1, 1, 0] ];
                      
    template_graph_coloring(2, graph_matrix_repr, "Two Interconnected Stars");
    
    
one_line();
one_circle1();
one_circle2();
one_circle3();
one_star();
two_interconnected_stars();