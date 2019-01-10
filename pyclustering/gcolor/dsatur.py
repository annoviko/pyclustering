"""!

@brief Graph coloring algorithm: DSATUR
@details Implementation based on paper @cite article::gcolor::dsatur::1.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""

class dsatur:
    """!
    @brief Represents DSATUR algorithm for graph coloring problem that uses greedy strategy.
    
    """
    
    def __init__(self, data):
        """!
        @brief Constructor of DSATUR algorithm.
        
        @param[in] data (list): Matrix graph representation.
        
        """
        if (len(data[0]) != len(data)):
            raise NameError('Only matrix graph representation is available.');
    
        self.__data_pointer = data;
        self.__colors = [];
        self.__coloring = None;
        
    def process(self):
        """!
        @brief Perform graph coloring using DSATUR algorithm.
        
        @see get_colors()
        
        """        
        color_counter = 1;
        
        degrees = list();
        saturation_degrees = [0] * len(self.__data_pointer);
        
        self.__coloring = [0] * len(self.__data_pointer);
        uncolored_vertices = set(range(len(self.__data_pointer)));
        
        index_maximum_degree = 0;
        maximum_degree = 0;
        for index_node in range(len(self.__data_pointer)):
            # Fill degree of nodes in the input graph
            degrees.append( ( sum(self.__data_pointer[index_node]), index_node ) );
            
            # And find node with maximal degree at the same time.
            if (degrees[index_node][0] > maximum_degree):
                (maximum_degree, node_index) = degrees[index_node];
                index_maximum_degree = index_node;
            
        # Update saturation
        neighbors = self.__get_neighbors(index_maximum_degree);
        for index_neighbor in neighbors:
            saturation_degrees[index_neighbor] += 1;
        
        # Coloring the first node
        self.__coloring[index_maximum_degree] = color_counter;
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
            node_index_neighbors = self.__get_neighbors(coloring_index);
            for number_color in range(1, color_counter + 1, 1):
                if (self.__get_amount_color(node_index_neighbors, number_color) == 0):
                    self.__coloring[coloring_index] = number_color;
                    break;
                    
            # If it has not been colored then
            if (self.__coloring[coloring_index] == 0):
                color_counter += 1;     # Add new color
                self.__coloring[coloring_index] = color_counter;
            
            # Remove node from uncolored set
            uncolored_vertices.remove(coloring_index);
            
            
            # Update degree of saturation
            for index_neighbor in node_index_neighbors:
                subneighbors = self.__get_neighbors(index_neighbor);
                
                if (self.__get_amount_color(subneighbors, self.__coloring[coloring_index]) == 1):
                    saturation_degrees[index_neighbor] += 1;     
    
    def get_colors(self):
        """!
        @brief Returns results of graph coloring.
        
        @return (list) list with assigned colors where each element corresponds 
                to node in the graph, for example [1, 2, 2, 1, 3, 4, 1].
                
        @see process()
        
        """
    
        return self.__coloring;
    
    def __get_amount_color(self, node_indexes, color_number):
        """!
        @brief Countes how many nodes has color 'color_number'.
        
        @param[in] node_indexes (list): Indexes of graph nodes for checking.
        @param[in] color_number (uint): Number of color that is searched in nodes.
        
        @return (uint) Number found nodes with the specified color 'color_number'.
        
        """
        
        color_counter = 0;  
        for index in node_indexes:
            if (self.__coloring[index] == color_number):
                color_counter += 1;
        
        return color_counter;
    
    
    def __get_neighbors(self, node_index):
        """!
        @brief Returns indexes of neighbors of the specified node.
        
        @param[in] node_index (uint):
        
        @return (list) Neighbors of the specified node.
        
        """
        
        return [ index for index in range(len(self.__data_pointer[node_index])) if self.__data_pointer[node_index][index] != 0 ]; 
    