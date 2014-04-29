import matplotlib.pyplot as plt;
from matplotlib import colors;

import numpy;


class type_graph_descr:
    GRAPH_UNKNOWN = 0;
    GRAPH_MATRIX_DESCR = 1;
    GRAPH_VECTOR_DESCR = 2;

class graph:
    __type_graph = None;
    __data = None;
    __space_description = None;
    __comments = None;
    
    def __init__(self, data, type_graph = None, space_descr = None, comments = None):
        self.__data = data;
        self.__space_descr = space_descr;
        self.__comments = comments;
        
        if (type_graph is not None):
            self.__type_graph = type_graph;
        else:
            self.__type_graph = type_graph_descr.GRAPH_MATRIX_DESCR;
            for row in self.__data:
                if (len(row) != len(self.__data)):
                    self.__type_graph = type_graph_descr.GRAPH_VECTOR_DESCR;
                    break;
                
                for element in row:
                    if ( (element != 0) or (element != 1) ):
                        self.__type_graph = type_graph_descr.GRAPH_VECTOR_DESCR;
        
    @property
    def data(self): return self.__data;
    
    @property
    def space_description(self): return self.__space_descr;
    
    @property
    def comments(self): return self.__comments;
    
    @property
    def type_graph_descr(self): return self.__type_graph;
    
    
def read_graph(filename):
    "Read graph from file in GRPR format"
    file = open(filename, 'r');
    
    comments = "";
    space_descr = [];
    data = [];
    data_type = None;
    
    for line in file:
        if (line[0] == 'c'): 
            comments += line[1:]; 
        
        elif (line[0] == 'r'): 
            node_coordinates = [float(val) for val in line[1:].split()];
            if (len(node_coordinates) != 2):
                raise NameError('Invalid format of space description for node (only 2-dimension space is supported');
                
            space_descr.append( [float(val) for val in line[1:].split()] );
            
        
        elif (line[0] == 'm'):
            data_type = type_graph_descr.GRAPH_MATRIX_DESCR;
            data.append( [float(val) for val in line[1:].split()] );
        
        elif (line[0] == 'v'):
            data_type = type_graph_descr.GRAPH_VECTOR_DESCR;
            data.append( [float(val) for val in line[1:].split()] );
            
        elif (len(line.strip()) == 0): continue;
        
        else: 
            print(line);
            raise NameError('Invalid format of file with graph description');
    
    file.close();
    
    if (len(data) != len(space_descr)):
        raise NameError("Invalid format of file with graph - number of nodes is different in space representation and graph description");
    
    return graph(data, data_type, space_descr, comments);



def draw_graph(graph_instance, map_coloring = None):
    fig = plt.figure();
    axes = fig.add_subplot(111);
    
    available_colors = ['#00a2e8', '#22b14c', '#ed1c24',
                        '#fff200', '#000000', '#a349a4',
                        '#ffaec9', '#7f7f7f', '#b97a57',
                        '#c8bfe7', '#880015', '#ff7f27',
                        '#3f48cc', '#c3c3c3', '#ffc90e',
                        '#efe4b0', '#b5e61d', '#99d9ea',
                        '#7092b4', '#ffffff'];
              
    if (map_coloring is not None):
        if (len(map_coloring) > len(available_colors)):
            raise NameError('Impossible to represent colored graph due to number of specified colors.');
    
    x_maximum = -numpy.Inf;
    x_minimum = numpy.Inf;
    y_maximum = -numpy.Inf;
    y_minimum = numpy.Inf;
    
    for i in range(0, len(graph_instance.space_description), 1):
        if (graph_instance.type_graph_descr == type_graph_descr.GRAPH_MATRIX_DESCR):
            for j in range(i, len(graph_instance.space_description), 1):    # draw connection between two points only one time
                if (graph_instance.data[i][j] == 1):
                    axes.plot([graph_instance.space_description[i][0], graph_instance.space_description[j][0]], [graph_instance.space_description[i][1], graph_instance.space_description[j][1]], 'k-', linewidth = 1.5);
                    
        elif (graph_instance.type_graph_descr == type_graph_descr.GRAPH_VECTOR_DESCR):
            for j in graph_instance.data[i]:
                if (i > j):     # draw connection between two points only one time
                    axes.plot([graph_instance.space_description[i][0], graph_instance.space_description[j][0]], [graph_instance.space_description[i][1], graph_instance.space_description[j][1]], 'k-', linewidth = 1.5);   
            
        color_node = 'b';
        if (map_coloring is not None):
            color_node = colors.hex2color(available_colors[map_coloring[i]]);
        
        axes.plot(graph_instance.space_description[i][0], graph_instance.space_description[i][1], color = color_node, marker = 'o', markersize = 20);
    
        if (x_maximum < graph_instance.space_description[i][0]): x_maximum = graph_instance.space_description[i][0];
        if (x_minimum > graph_instance.space_description[i][0]): x_minimum = graph_instance.space_description[i][0];  
        if (y_maximum < graph_instance.space_description[i][1]): y_maximum = graph_instance.space_description[i][1]; 
        if (y_minimum > graph_instance.space_description[i][1]): y_minimum = graph_instance.space_description[i][1];
    
    plt.xlim(x_minimum - 0.5, x_maximum + 0.5);
    plt.ylim(y_minimum - 0.5, y_maximum + 0.5);
    
    plt.show();