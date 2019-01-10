"""!

@brief Data Structure: KD-Tree
@details Implementation based on paper @cite book::the_design_and_analysis.

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


import numpy

from pyclustering.utils import euclidean_distance_square


class kdtree_text_visualizer:
    """!
    @brief KD-tree text visualizer that provides service to diplay tree structure using text representation.
    
    """

    def __init__(self, kdtree_instance):
        """!
        @brief Initialize KD-tree text visualizer.
        
        @param[in] kdtree_instance (kdtree): Instance of KD-Tree that should be visualized.
        
        """
        self.__kdtree_instance = kdtree_instance
        
        self.__tree_level_text  = ""
        self.__tree_text        = ""


    def visualize(self, display=True):
        """!
        @brief Display KD-tree to console.
        
        @param[in] display (bool): If 'True' then tree will be shown in console.
        
        @return (string) Text representation of the KD-tree.
        
        """

        kdnodes = self.__get_nodes()
        level = kdnodes[0]
        
        for kdnode in kdnodes:
            self.__print_node(level, kdnode)

        self.__tree_text += self.__tree_level_text
        if display is True:
            print(self.__tree_text)
        
        return self.__tree_text


    def __print_node(self, level, kdnode):
        if level == kdnode[0]:
            self.__tree_level_text += str(kdnode[1]) + "\t"

        else:
            self.__tree_text += self.__tree_level_text + "\n"
            level = kdnode[0]
            self.__tree_level_text = str(kdnode[1]) + "\t"


    def __get_nodes(self):
        kdnodes = self.__kdtree_instance.traverse()
        if kdnodes == []:
            return

        kdnodes.sort(key = lambda item: item[0])
        return kdnodes



class node:
    """!
    @brief Represents node of KD-Tree.
    
    """
    
    def __init__(self, data=None, payload=None, left=None, right=None, disc=None, parent=None):
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
        self.data = data
        
        ## Payload of node that can be used by user for storing specific information in the node.
        self.payload = payload
        
        ## Left node successor of the node.
        self.left = left
        
        ## Right node successor of the node.
        self.right = right
        
        ## Index of dimension.
        self.disc = disc
        
        ## Parent node of the node.
        self.parent = parent


    def __repr__(self):
        """!
        @return (string) Default representation of the node.
        
        """
        left = None
        right = None
        
        if self.left is not None:
            left = self.left.data
            
        if self.right is not None:
            right = self.right.data
        
        return "(%s: [L:'%s', R:'%s'])" % (self.data, left, right)
    
    def __str__(self):
        """!
        @return (string) String representation of the node.
        
        """
        return self.__repr__()


class kdtree:
    """!
    @brief Represents KD Tree that is a space-partitioning data structure for organizing points in a k-dimensional space.
    @details In the term k-d tree, k denotes the dimensionality of the space being represented. Each data point is represented 
              as a node in the k-d tree in the form of a record of type node.
    
    Examples:
    @code
        # Import required modules
        from pyclustering.samples.definitions import SIMPLE_SAMPLES;
        from pyclustering.container.kdtree import kdtree;
        from pyclustering.utils import read_sample;
        
        # Read data from text file
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
        
        # Create instance of KD-tree and initialize (fill) it by read data.
        tree_instance = kdtree(sample);
        
        # Search for nearest point
        search_distance = 0.3;
        nearest_node = tree_instance.find_nearest_dist_node([1.12, 4.31], search_distance);
        
        # Search for nearest point in radius 0.3
        nearest_nodes = tree_instance.find_nearest_dist_nodes([1.12, 4.31], search_distance);
        print("Nearest nodes:", nearest_nodes);
    @endcode
    
    """
    
    def __init__(self, data_list = None, payload_list = None):
        """!
        @brief Create kd-tree from list of points and from according list of payloads.
        @details If lists were not specified then empty kd-tree will be created.
        
        @param[in] data_list (list): Insert points from the list to created KD tree.
        @param[in] payload_list (list): Insert payload from the list to created KD tree, length should be equal to length of data_list if it is specified.
        
        """
        
        self.__root = None
        self.__dimension = None
        self.__point_comparator = None

        self.__fill_tree(data_list, payload_list)


    def insert(self, point, payload):
        """!
        @brief Insert new point with payload to kd-tree.
        
        @param[in] point (list): Coordinates of the point of inserted node.
        @param[in] payload (any-type): Payload of inserted node. It can be identificator of the node or
                    some useful payload that belongs to the point.
        
        @return (node) Inserted node to the kd-tree.
        
        """
        
        if self.__root is None:
            self.__dimension = len(point)
            self.__root = node(point, payload, None, None, 0)
            self.__point_comparator = self.__create_point_comparator(type(point))
            return self.__root
        
        cur_node = self.__root
        
        while True:
            if cur_node.data[cur_node.disc] <= point[cur_node.disc]:
                # If new node is greater or equal than current node then check right leaf
                if cur_node.right is None:
                    discriminator = cur_node.disc + 1
                    if discriminator >= self.__dimension:
                        discriminator = 0
                        
                    cur_node.right = node(point, payload, None, None, discriminator, cur_node)
                    return cur_node.right
                else: 
                    cur_node = cur_node.right
            
            else:
                # If new node is less than current then check left leaf
                if cur_node.left is None:
                    discriminator = cur_node.disc + 1
                    if discriminator >= self.__dimension:
                        discriminator = 0
                        
                    cur_node.left = node(point, payload, None, None, discriminator, cur_node)
                    return cur_node.left
                else:
                    cur_node = cur_node.left
    
    
    def remove(self, point, **kwargs):
        """!
        @brief Remove specified point from kd-tree.
        @details It removes the first found node that satisfy to the input parameters. Make sure that
                  pair (point, payload) is unique for each node, othewise the first found is removed.
        
        @param[in] point (list): Coordinates of the point of removed node.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'payload').
        
        <b>Keyword Args:</b><br>
            - payload (any): Payload of the node that should be removed.
        
        @return (node) Root if node has been successfully removed, otherwise None.
        
        """
        
        # Get required node
        node_for_remove = None
        if 'payload' in kwargs:
            node_for_remove = self.find_node_with_payload(point, kwargs['payload'], None)
        else:
            node_for_remove = self.find_node(point, None)
        
        if node_for_remove is None:
            return None
        
        parent = node_for_remove.parent
        minimal_node = self.__recursive_remove(node_for_remove)
        if parent is None:
            self.__root = minimal_node
            
            # If all k-d tree was destroyed
            if minimal_node is not None:
                minimal_node.parent = None
        else:
            if parent.left is node_for_remove:
                parent.left = minimal_node
            elif parent.right is node_for_remove:
                parent.right = minimal_node
        
        return self.__root
    
    
    def __recursive_remove(self, node_removed):
        """!
        @brief Delete node and return root of subtree.
        
        @param[in] node_removed (node): Node that should be removed.
        
        @return (node) Minimal node in line with coordinate that is defined by descriminator.
        
        """
                
        # Check if it is leaf
        if (node_removed.right is None) and (node_removed.left is None):
            return None
        
        discriminator = node_removed.disc
        
        # Check if only left branch exist
        if node_removed.right is None:
            node_removed.right = node_removed.left
            node_removed.left = None
        
        # Find minimal node in line with coordinate that is defined by discriminator
        minimal_node = self.find_minimal_node(node_removed.right, discriminator)
        parent = minimal_node.parent
        
        if parent.left is minimal_node:
            parent.left = self.__recursive_remove(minimal_node)
        elif parent.right is minimal_node:
            parent.right = self.__recursive_remove(minimal_node)
        
        minimal_node.parent = node_removed.parent
        minimal_node.disc = node_removed.disc
        minimal_node.right = node_removed.right
        minimal_node.left = node_removed.left
        
        # Update parent for successors of previous parent.
        if minimal_node.right is not None:
            minimal_node.right.parent = minimal_node
             
        if minimal_node.left is not None:
            minimal_node.left.parent = minimal_node
        
        return minimal_node


    def find_minimal_node(self, node_head, discriminator):
        """!
        @brief Find minimal node in line with coordinate that is defined by discriminator.
        
        @param[in] node_head (node): Node of KD tree from that search should be started.
        @param[in] discriminator (uint): Coordinate number that is used for comparison.
        
        @return (node) Minimal node in line with descriminator from the specified node.
        
        """
        
        min_key = lambda cur_node: cur_node.data[discriminator]
        stack = []
        candidates = []
        isFinished = False
        while isFinished is False:
            if node_head is not None:
                stack.append(node_head)
                node_head = node_head.left
            else:
                if len(stack) != 0:
                    node_head = stack.pop()
                    candidates.append(node_head)
                    node_head = node_head.right
                else:
                    isFinished = True

        return min(candidates, key = min_key)


    def __fill_tree(self, data_list, payload_list):
        """!
        @brief Fill KD-tree by specified data and create point comparator in line with data type.

        @param[in] data_list (array_like): Data points that should be inserted to the tree.
        @param[in] payload_list (array_like): Data point payloads that follows data points inserted to the tree.

        """
        if data_list is None or len(data_list) == 0:
            return # Just return from here, tree can be filled by insert method later

        if payload_list is None:
            # Case when payload is not specified.
            for index in range(0, len(data_list)):
                self.insert(data_list[index], None)
        else:
            # Case when payload is specified.
            for index in range(0, len(data_list)):
                self.insert(data_list[index], payload_list[index])

        self.__point_comparator = self.__create_point_comparator(type(self.__root.data))


    def __create_point_comparator(self, type_point):
        """!
        @brief Create point comparator.
        @details In case of numpy.array specific comparator is required.

        @param[in] type_point (data_type): Type of point that is stored in KD-node.

        @return (callable) Callable point comparator to compare to points.

        """
        if type_point == numpy.ndarray:
            return lambda obj1, obj2: numpy.array_equal(obj1, obj2)

        return lambda obj1, obj2: obj1 == obj2


    def __find_node_by_rule(self, point, search_rule, cur_node):
        """!
        @brief Search node that satisfy to parameters in search rule.
        @details If node with specified parameters does not exist then None will be returned, 
                  otherwise required node will be returned.
        
        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] search_rule (lambda): Rule that is called to check whether node satisfies to search parameter.
        @param[in] cur_node (node): Node from which search should be started.
        
        @return (node) Node if it satisfies to input parameters, otherwise it return None.
        
        """
        
        req_node = None
        
        if cur_node is None:
            cur_node = self.__root
        
        while cur_node:
            if cur_node.data[cur_node.disc] <= point[cur_node.disc]:
                # Check if it's required node
                if search_rule(cur_node):
                    req_node = cur_node
                    break
                
                cur_node = cur_node.right
            
            else:
                cur_node = cur_node.left
        
        return req_node


    def find_node_with_payload(self, point, point_payload, cur_node = None):
        """!
        @brief Find node with specified coordinates and payload.
        @details If node with specified parameters does not exist then None will be returned, 
                  otherwise required node will be returned.
        
        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] point_payload (any): Payload of the node that is searched in the tree.
        @param[in] cur_node (node): Node from which search should be started.
        
        @return (node) Node if it satisfies to input parameters, otherwise it return None.
        
        """
        
        rule_search = lambda node, point=point, payload=point_payload: self.__point_comparator(node.data, point) and node.payload == payload
        return self.__find_node_by_rule(point, rule_search, cur_node)


    def find_node(self, point, cur_node = None):
        """!
        @brief Find node with coordinates that are defined by specified point.
        @details If node with specified parameters does not exist then None will be returned, 
                  otherwise required node will be returned.
        
        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] cur_node (node): Node from which search should be started.
        
        @return (node) Node if it satisfies to input parameters, otherwise it return None.
        
        """
        
        rule_search = lambda node, point=point: self.__point_comparator(node.data, point)
        return self.__find_node_by_rule(point, rule_search, cur_node)
    
    
    def find_nearest_dist_node(self, point, distance, retdistance = False):
        """!
        @brief Find nearest neighbor in area with radius = distance.
        
        @param[in] point (list): Maximum distance where neighbors are searched.
        @param[in] distance (double): Maximum distance where neighbors are searched.
        @param[in] retdistance (bool): If True - returns neighbors with distances to them, otherwise only neighbors is returned.
        
        @return (node|list) Nearest neighbor if 'retdistance' is False and list with two elements [node, distance] if 'retdistance' is True,
                 where the first element is pointer to node and the second element is distance to it.
        
        """
        
        best_nodes = self.find_nearest_dist_nodes(point, distance)
            
        if best_nodes == []:
            return None
        
        nearest = min(best_nodes, key = lambda item: item[0])
        
        if retdistance is True:
            return nearest
        else:
            return nearest[1]
    
    
    def find_nearest_dist_nodes(self, point, distance):
        """!
        @brief Find neighbors that are located in area that is covered by specified distance.
        
        @param[in] point (list): Coordinates that is considered as centroind for searching.
        @param[in] distance (double): Distance from the center where seaching is performed.
        
        @return (list) Neighbors in area that is specified by point (center) and distance (radius).
        
        """

        best_nodes = []
        if self.__root is not None:
            self.__recursive_nearest_nodes(point, distance, distance * distance, self.__root, best_nodes)

        return best_nodes


    def __recursive_nearest_nodes(self, point, distance, sqrt_distance, node_head, best_nodes):
        """!
        @brief Returns list of neighbors such as tuple (distance, node) that is located in area that is covered by distance.
        
        @param[in] point (list): Coordinates that is considered as centroind for searching
        @param[in] distance (double): Distance from the center where seaching is performed.
        @param[in] sqrt_distance (double): Square distance from the center where searching is performed.
        @param[in] node_head (node): Node from that searching is performed.
        @param[in|out] best_nodes (list): List of founded nodes.
        
        """

        if node_head.right is not None:
            minimum = node_head.data[node_head.disc] - distance
            if point[node_head.disc] >= minimum:
                self.__recursive_nearest_nodes(point, distance, sqrt_distance, node_head.right, best_nodes)
        
        if node_head.left is not None:
            maximum = node_head.data[node_head.disc] + distance
            if point[node_head.disc] < maximum:
                self.__recursive_nearest_nodes(point, distance, sqrt_distance, node_head.left, best_nodes)
        
        candidate_distance = euclidean_distance_square(point, node_head.data)
        if candidate_distance <= sqrt_distance:
            best_nodes.append( (candidate_distance, node_head) )


    def children(self, node_parent):
        """!
        @brief Returns list of children of node.
        
        @param[in] node_parent (node): Node whose children are required. 
        
        @return (list) Children of node. If node haven't got any child then None is returned.
        
        """
        
        if node_parent.left is not None:
            yield node_parent.left
        if node_parent.right is not None:
            yield node_parent.right


    def traverse(self, start_node = None, level = None):
        """!
        @brief Traverses all nodes of subtree that is defined by node specified in input parameter.
        
        @param[in] start_node (node): Node from that travering of subtree is performed.
        @param[in, out] level (uint): Should be ignored by application.
        
        @return (list) All nodes of the subtree.
        
        """
        
        if start_node is None:
            start_node  = self.__root
            level = 0
        
        if start_node is None:
            return []
        
        items = [ (level, start_node) ]
        for child in self.children(start_node):
            if child is not None:
                items += self.traverse(child, level + 1)
        
        return items
