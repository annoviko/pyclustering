'''

Graph coloring algorithm: DSATUR

Based on article description:
 - D.Brelaz. New Methods to color the vertices of a graph. 1979.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

def dsatur(data):
    "DSATUR algorithm implementation. Performs graph coloring problem."
    
    "(in) data        - matrix graph representation."
    
    "Returns vector with assigned colors where each element corresponds to node in the graph, for example (1, 2, 2, 1, 3, 4, 1)."
    if (len(data[0]) != len(data)):
        raise NameError('Only matrix graph representation is available.');
    
    color_counter = 1;
    
    degrees = list();
    saturation_degrees = [0] * len(data);
    
    coloring = [0] * len(data);
    uncolored_vertices = set(range(len(data)));
    
    index_maximum_degree = 0;
    maximum_degree = 0;
    for index_node in range(len(data)):
        # Fill degree of nodes in the input graph
        degrees.append( ( sum(data[index_node]), index_node ) );
        
        # And find node with maximal degree at the same time.
        if (degrees[index_node][0] > maximum_degree):
            (maximum_degree, node_index) = degrees[index_node];
            index_maximum_degree = index_node;
        
    # Update saturation
    neighbors = get_neighbors(index_maximum_degree, data);
    for index_neighbor in neighbors:
        saturation_degrees[index_neighbor] += 1;
    
    # Coloring the first node
    coloring[index_maximum_degree] = color_counter;
    uncolored_vertices.remove(index_maximum_degree);
    
    while(len(uncolored_vertices) > 0):
        # Get maximum saturation degree
        maximum_satur_degree = -1;
        for index in uncolored_vertices:
            if (saturation_degrees[index] > maximum_satur_degree):
                maximum_satur_degree = saturation_degrees[index];
        
        # Get list of indexes with maximum saturation degree
        indexes_maximum_satur_degree = [index for index in uncolored_vertices if saturation_degrees[index] == maximum_satur_degree];           

        coloring_index = indexes_maximum_satur_degree[0];
        if (len(indexes_maximum_satur_degree) > 1): # There are more then one node with maximum saturation
            # Find node with maximum degree
            maximum_degree = -1;
            for index in indexes_maximum_satur_degree:
                (degree, node_index) = degrees[index];
                if (degree > maximum_degree):
                    coloring_index = node_index;
                    maximum_degree = degree;
        
        # Coloring
        node_index_neighbors = get_neighbors(coloring_index, data);
        for number_color in range(1, color_counter + 1, 1):
            if (get_amount_color(node_index_neighbors, coloring, number_color) == 0):
                coloring[coloring_index] = number_color;
                break;
                
        # If it has not been colored then
        if (coloring[coloring_index] == 0):
            color_counter += 1;     # Add new color
            coloring[coloring_index] = color_counter;
        
        # Remove node from uncolored set
        uncolored_vertices.remove(coloring_index);
        
        
        # Update degree of saturation
        for index_neighbor in node_index_neighbors:
            subneighbors = get_neighbors(index_neighbor, data);
            
            if (get_amount_color(subneighbors, coloring, coloring[coloring_index]) == 1):
                saturation_degrees[index_neighbor] += 1;
        
    return coloring;


def get_amount_color(node_indexes, coloring, color_number):
    "Private function that is used by 'dsatur'. Countes how many nodes has color 'color_number'."
    
    "(in) node_indexes    - indexes of graph nodes for checking."
    "(in) coloring        - map where colors are stored."
    "(in) color_number    - number of color that is searched in nodes."
    
    "Returns number found nodes with the specified color 'color_number'."
    color_counter = 0;  
    for index in node_indexes:
        if (coloring[index] == color_number):
            color_counter += 1;
    
    return color_counter;


def get_neighbors(node_index, data):
    "Private function that is used by 'dsatur'. Returns indexes of neighbors of the specified node."
    
    "(in) node_index    - index of node for which neighbours should be found."
    "(in) data          - matrix graph representation."
    
    "Returns list of neighbors of the specified node."
    return [ index for index in range(len(data[node_index])) if data[node_index][index] != 0 ]; 