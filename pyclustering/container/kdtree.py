"""!

@brief Data Structure: KD-Tree
@details Based on book description:
         - M.Samet. The Design And Analysis Of Spatial Data Structures. 1994.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2015
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

import numpy;

from pyclustering.utils import euclidean_distance_sqrt;

class node:
    """!
    @brief Represents node of KD-Tree.
    
    """
    
    def __init__(self, data = None, payload = None, left = None, right = None, disc = None, parent = None):
        """!
        @brief 
        
        @param[in] data (list): Data point that is presented as list of coodinates.
        @param[in] payload (*): Payload of node (pointer to essense that is attached to this node).
        @param[in] left (node): Node of KD-Tree that is represented left successor.
        @param[in] right (node): Node of KD-Tree that is represented right successor.
        @param[in] disc (uint): Index of dimension of that node.
        @param[in] parent (node): Node of KD-Tree that is represented parent.
        
        """
        
        ## Data point that is presented as list of coodinates.
        self.data = data;
        
        ## Payload of node that can be used by user for storing specific information in the node.
        self.payload = payload;
        
        ## Left node successor of the node.
        self.left = left;
        
        ## Right node successor of the node.
        self.right = right;
        
        ## Index of dimension.
        self.disc = disc;
        
        ## Parent node of the node.
        self.parent = parent;
    
    def __repr__(self):
        """!
        @return (string) Default representation of the node.
        
        """
        left = None; 
        right = None; 
        
        if (self.left is not None):
            left = self.left.data;
            
        if (self.right is not None):
            right = self.right.data;
        
        return 'Node (%s, [%s %s])' % (self.data, left, right);
    
    def __str__(self):
        """!
        @return (string) String representation of the node.
        
        """
        return self.__repr__();


class kdtree:
    """!
    @brief Represents KD Tree.
    
    """
    
    __root = None;
    __dimension = None;
    
    def __init__(self, data_list = None, payload_list = None):
        """!
        @brief Create kd-tree from list of points and from according list of payloads.
        @details If lists were not specified then empty kd-tree will be created.
        
        @param[in] data_list (list): Insert points from the list to created KD tree.
        @param[in] payload_list (list): Insert payload from the list to created KD tree, length should be equal to length of data_list if it is specified.
        
        """
        
        if (data_list is None):
            return; # Just return from here, tree can be filled by insert method later
        
        if (payload_list is None):
            # Case when payload is not specified.
            for index in range(0, len(data_list)):
                self.insert(data_list[index], None);
        else:
            # Case when payload is specified.
            for index in range(0, len(data_list)):
                self.insert(data_list[index], payload_list[index]);
            
                    
    def insert(self, point, payload):
        """!
        @brief Insert new point with payload to kd-tree.
        
        @param[in] point (list): Coordinates of the point of inserted node.
        @param[in] payload (*): Payload of inserted node.
        
        """
        
        if (self.__root is None):
            self.__dimension = len(point);
            self.__root = node(point, payload, None, None, 0);
            return self.__root;
        
        cur_node = self.__root;
        
        while True:
            if (cur_node.data[cur_node.disc] <= point[cur_node.disc]):
                # If new node is greater or equal than current node then check right leaf
                if (cur_node.right is None):
                    discriminator = cur_node.disc + 1;
                    if (discriminator >= self.__dimension):
                        discriminator = 0;
                        
                    cur_node.right = node(point, payload, None, None, discriminator, cur_node);
                    return cur_node.right;
                else: 
                    cur_node = cur_node.right;
            
            else:
                # If new node is less than current then check left leaf
                if (cur_node.left is None):
                    discriminator = cur_node.disc + 1;
                    if (discriminator >= self.__dimension):
                        discriminator = 0;
                        
                    cur_node.left = node(point, payload, None, None, discriminator, cur_node);
                    return cur_node.left;
                else:
                    cur_node = cur_node.left;
    
    
    def remove(self, point):
        """!
        @brief Remove specified point from kd-tree.
        
        @param[in] point (list): Coordinates of the point of removed node.
        
        @return (node) Root if node has been successfully removed, otherwise None.
        
        """
        
        # Get required node
        node_for_remove = self.find_node(point);
        if (node_for_remove is None):
            return None;
        
        parent = node_for_remove.parent;
        node = self.__recursive_remove(node_for_remove);
        if (parent is None):
            self.__root = node;
            
            # If all k-d tree was destroyed
            if (node is not None):
                node.parent = None;
        else:
            if (parent.left is node_for_remove):
                parent.left = node;
            elif (parent.right is node_for_remove):
                parent.right = node;
            else:
                assert 0;   # FATAL ERROR
        
        return self.__root;
    
    
    def __recursive_remove(self, node):
        """!
        @brief Delete node and return root of subtree.
        
        @param[in] node (node): Node that should be removed.
        
        @return (node) Minimal node in line with coordinate that is defined by descriminator.
        
        """
                
        # Check if it is leaf
        if ( (node.right is None) and (node.left is None) ):
            return None;
        
        discriminator = node.disc;
        
        # Check if only left branch exist
        if (node.right is None):
            node.right = node.left;
            node.left = None;
        
        # Find minimal node in line with coordinate that is defined by discriminator
        minimal_node = self.find_minimal_node(node.right, discriminator);
        parent = minimal_node.parent;
        
        if (parent.left is minimal_node):
            parent.left = self.__recursive_remove(minimal_node);
        elif (parent.right is minimal_node):
            parent.right = self.__recursive_remove(minimal_node);
        else:
            assert 0;
        
        minimal_node.parent = node.parent;
        minimal_node.disc = node.disc;
        minimal_node.right = node.right;
        minimal_node.left = node.left;
        
        # Update parent for successors of previous parent.
        if (minimal_node.right is not None):
            minimal_node.right.parent = minimal_node;
             
        if (minimal_node.left is not None):
            minimal_node.left.parent = minimal_node;
        
        return minimal_node;
        
    
    def find_minimal_node(self, node, discriminator):
        """!
        @brief Find minimal node in line with coordinate that is defined by discriminator.
        
        @param[in] node (node): Node of KD tree from that search should be started.
        @param[in] discriminator (uint): Coordinate number that is used for comparison.
        
        @return (node) Minimal node in line with descriminator from the specified node.
        
        """
        
        min_key = lambda cur_node: cur_node.data[discriminator];
        stack = [];
        candidates = [];
        isFinished = False;
        while isFinished is False:
            if node is not None:
                stack.append(node);
                node = node.left;
            else:
                if len(stack) != 0:
                    node = stack.pop();
                    candidates.append(node);
                    node = node.right;
                else:
                    isFinished = True;

        return min(candidates, key = min_key);
    
    
    def find_node(self, point, cur_node = None):
        """!
        @brief Find node with coordinates that are defined by specified point.
        @details If node does not exist then None will be returned. Otherwise required node will be returned.
        
        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] cur_node (node): Node from which search should be started.
        
        @return (node) Node in case of existance of node with specified coordinates, otherwise it return None.
        
        """
        
        req_node = None;
        
        if (cur_node is None):
            cur_node = self.__root;
        
        while True:
            if (cur_node.data[cur_node.disc] <= point[cur_node.disc]):
                # Check if it's required node
                if (cur_node.data == point):
                    req_node = cur_node;
                    break;
                
                if (cur_node.right is not None):
                    cur_node = cur_node.right;
                else:
                    assert 0
            
            else:
                if (cur_node.left is not None):
                    cur_node = cur_node.left;
                else:
                    assert 0
                
        return req_node;
    
    
    
    def find_nearest_dist_node(self, point, distance, retdistance = False):
        """!
        @brief Find nearest neighbor in area with radius = distance.
        
        @param[in] point (list): Maximum distance where neighbors are searched.
        @param[in] distance (double): Maximum distance where neighbors are searched.
        @param[in] retdistance (bool): If True - returns neighbors with distances to them, otherwise only neighbors is returned.
        
        @return (list) Neighbors, if redistance is True then neighbors with distances to them will be returned.
        
        """
        
        best_nodes = self.find_nearest_dist_nodes(point, distance);
            
        if (best_nodes == []): 
            return None;
        
        nearest = min(best_nodes, key = lambda item: item[0]);
        
        if (retdistance == True):
            return nearest;
        else:
            return nearest[1];
    
    
    def find_nearest_dist_nodes(self, point, distance):
        """!
        @brief Find neighbors that are located in area that is covered by specified distance.
        
        @param[in] point (list): Coordinates that is considered as centroind for searching.
        @param[in] distance (double): Distance from the center where seaching is performed.
        
        @return (list) Neighbors in area that is specified by point (center) and distance (radius).
        
        """
        
        best_nodes = [];
        self.__recursive_nearest_nodes(point, distance, distance ** 2, self.__root, best_nodes);
        
        return best_nodes;
    
    
    def __recursive_nearest_nodes(self, point, distance, sqrt_distance, node, best_nodes):
        """!
        @brief Returns list of neighbors such as tuple (distance, node) that is located in area that is covered by distance.
        
        @param[in] point (list): Coordinates that is considered as centroind for searching
        @param[in] distance (double): Distance from the center where seaching is performed.
        @param[in] sqrt_distance (double): Square distance from the center where searching is performed.
        @param[in] node (node): Node from that searching is performed.
        @param[in|out] best_nodes (list): List of founded nodes.
        
        """
        
        minimum = node.data[node.disc] - distance;
        maximum = node.data[node.disc] + distance;
        
        if (node.right is not None):
            if (point[node.disc] >= minimum):
                self.__recursive_nearest_nodes(point, distance, sqrt_distance, node.right, best_nodes);
        
        if (node.left is not None):
            if (point[node.disc] < maximum):
                self.__recursive_nearest_nodes(point, distance, sqrt_distance, node.left, best_nodes);
        
        candidate_distance = euclidean_distance_sqrt(point, node.data);
        if (candidate_distance <= sqrt_distance):
            best_nodes.append( (candidate_distance, node) );
    
    
    def children(self, node):
        """!
        @brief Returns list of children of node.
        
        @param[in] node (node): Node whose children are required. 
        
        @return (list) Children of node. If node haven't got any child then None is returned.
        
        """
        
        if (node.left is not None):
            yield node.left;
        if (node.right is not None):
            yield node.right;
            
    
    def traverse(self, start_node = None, level = None):
        """!
        @brief Traverses all nodes of subtree that is defined by node specified in input parameter.
        
        @param[in] start_node (node): Node from that travering of subtree is performed.
        @param[in, out] level (uint): Should be ignored by application.
        
        @return (list) All nodes of the subtree.
        
        """
        
        if (start_node is None):
            start_node  = self.__root;
            level = 0;
        
        if (start_node is None):
            return [];
        
        items = [ (level, start_node) ];        
        for child in self.children(start_node):
            if child is not None:
                items += self.traverse(child, level + 1);
        
        return items;
            
    
    def show(self):
        """!
        @brief Display tree on the console.
        
        """
        
        nodes = self.traverse();
        if (nodes == []):
            return;
        
        nodes.sort(key = lambda item: item[0]);
        
        level = nodes[0];
        string = "";
        for item in nodes:
            if (level == item[0]):
                string += str(item[1]) + "\t";
                
            else:
                print(string);
                level = item[0];
                string = str(item[1]) + "\t";
                
        print(string);
    