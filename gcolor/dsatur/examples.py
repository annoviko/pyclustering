from support import read_sample;

from samples.definitions import GRAPH_SIMPLE_SAMPLES;

from gcolor.dsatur import dsatur;

def template_graph_coloring(filename):
    graph_matrix_repr = read_sample(filename);
    coloring = dsatur(graph_matrix_repr);
    print("\nGraph: ", filename);
    print(coloring); 
    
    
def graph_one_line():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_LINE);
    
def graph_full_1():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL1);
    
def graph_full_2():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_FULL2);
    
def graph_one_circle():
    template_graph_coloring(GRAPH_SIMPLE_SAMPLES.GRAPH_ONE_CIRCLE1);
    

graph_one_line();
graph_full_1();
graph_full_2();
graph_one_circle();
