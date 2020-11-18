"""!

@brief Data Structure: KD-Tree
@details Implementation based on paper @cite book::the_design_and_analysis.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import numpy
import matplotlib.pyplot as plt

from pyclustering.utils import euclidean_distance_square, find_left_element


class kdtree_visualizer:
    """!
    @brief KD-tree visualizer that provides service to display graphical representation of the tree using
            `matplotlib` library.
    @details The visualizer is able to visualize 2D KD-trees only.

    There is an example how to visualize balanced KD-tree for `TwoDiamonds` sample using `kdtree_visualizer`:
    @code
        from pyclustering.container.kdtree import kdtree_balanced, kdtree_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)
        tree_instance = kdtree_balanced(sample)

        kdtree_visualizer(tree_instance).visualize()
    @endcode

    Output result of the example above (balanced tree) - figure 1:
    @image html kd_tree_unbalanced_two_diamonds.png "Fig. 1. Balanced KD-tree for sample 'TwoDiamonds'."

    There is one more example to demonstrate unbalanced KD-tree. `kdtree` class is child class of `kdtree_balanced`
    that allows to add points step by step and thus an unbalanced KD-tree can be built.
    @code
        from pyclustering.container.kdtree import kdtree, kdtree_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)
        tree_instance = kdtree()    # Do not use sample in constructor to avoid building of balanced tree.

        # Fill KD-tree step by step to obtain unbalanced tree.
        for point in sample:
            tree_instance.insert(point)

        kdtree_visualizer(tree_instance).visualize()
    @endcode

    Output result of the example above (unbalanced tree) - figure 2:
    @image html kd_tree_unbalanced_two_diamonds.png "Fig. 2. Unbalanced KD-tree for sample 'TwoDiamonds'."

    """

    def __init__(self, kdtree_instance):
        """!
        @brief Initialize KD-tree visualizer.

        @param[in] kdtree_instance (kdtree): Instance of a KD-tree that should be visualized.

        """
        self.__tree = kdtree_instance
        self.__colors = ['blue', 'red', 'green']
        self.__verify()

    def visualize(self):
        """!
        @brief Visualize KD-tree using plot in 2-dimensional data-space.

        """
        node = self.__tree.get_root()
        min, max = self.__get_limits()

        figure = plt.figure(111)
        ax = figure.add_subplot(111)

        self.__draw_node(ax, node, min, max)

        ax.set_xlim(min[0], max[0])
        ax.set_ylim(min[1], max[1])
        plt.show()

    def __draw_node(self, ax, node, min, max):
        self.__draw_split_line(ax, node, min, max)

        if node.left is not None:
            rborder = max[:]
            rborder[node.disc] = node.data[node.disc]
            self.__draw_node(ax, node.left, min, rborder)

        if node.right is not None:
            lborder = min[:]
            lborder[node.disc] = node.data[node.disc]
            self.__draw_node(ax, node.right, lborder, max)

    def __draw_split_line(self, ax, node, min, max):
        max_coord = max[:]
        min_coord = min[:]

        dimension = len(min)
        for d in range(dimension):
            if d == node.disc:
                max_coord[d] = node.data[d]
                min_coord[d] = node.data[d]

        if dimension == 2:
            ax.plot(node.data[0], node.data[1], color='black', marker='.', markersize=6)
            ax.plot([min_coord[0], max_coord[0]], [min_coord[1], max_coord[1]], color=self.__colors[node.disc],
                    linestyle='-', linewidth=1)

    def __get_limits(self):
        dimension = len(self.__tree.get_root().data)
        nodes = self.__get_all_nodes()

        max, min = [float('-inf')] * dimension, [float('+inf')] * dimension

        for node in nodes:
            for d in range(dimension):
                if max[d] < node.data[d]:
                    max[d] = node.data[d]

                if min[d] > node.data[d]:
                    min[d] = node.data[d]

        return min, max

    def __get_all_nodes(self):
        nodes = []

        next_level = [self.__tree.get_root()]

        while len(next_level) != 0:
            cur_level = next_level
            nodes += next_level
            next_level = []

            for cur_node in cur_level:
                children = cur_node.get_children()
                if children is not None:
                    next_level += children

        return nodes

    def __verify(self):
        root = self.__tree.get_root()
        if root is None:
            raise ValueError("KD-Tree is empty - nothing to visualize.")

        dimension = len(root.data)
        if dimension != 2:
            raise NotImplementedError("KD-Tree data has '%d' dimension - only KD-tree with 2D data can be visualized."
                                      % dimension)



class node:
    """!
    @brief Represents a node in a KD-Tree.
    @details The KD-Tree node contains point's coordinates, discriminator, payload and pointers to parent and children.

    @see kdtree_balanced
    @see kdtree

    """

    def __init__(self, data=None, payload=None, left=None, right=None, disc=None, parent=None):
        """!
        @brief Creates KD-tree node.

        @param[in] data (list): Data point that is presented as list of coordinates.
        @param[in] payload (any): Payload of node (pointer to essence that is attached to this node).
        @param[in] left (node): Node of KD-Tree that represents left successor.
        @param[in] right (node): Node of KD-Tree that represents right successor.
        @param[in] disc (uint): Index of dimension of that node.
        @param[in] parent (node): Node of KD-Tree that represents parent.

        """

        ## Data point that is presented as list of coordinates.
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

    def get_children(self):
        """!
        @brief Returns list of not `None` children of the node.

        @return (list) list of not `None` children of the node; if the node does not have children
                        then `None` is returned.

        """

        if self.left is not None:
            yield self.left
        if self.right is not None:
            yield self.right



class kdtree_balanced:
    """!
    @brief Represents balanced static KD-tree that does not provide services to add and remove nodes after
            initialization.
    @details In the term KD tree, k denotes the dimensionality of the space being represented. Each data point is
              represented as a node in the k-d tree in the form of a record of type node.

    There is an example how to create KD-tree:
    @code
        from pyclustering.container.kdtree import kdtree_balanced, kdtree_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        sample = read_sample(FCPS_SAMPLES.SAMPLE_LSUN)
        tree_instance = kdtree_balanced(sample)

        kdtree_visualizer(tree_instance).visualize()
    @endcode

    Output result of the example above - figure 1.
    @image html kd_tree_balanced_lsun.png "Fig. 1. Balanced KD-tree for sample 'Lsun'."

    @see kdtree

    """

    def __init__(self, points, payloads=None):
        """!
        @brief Initializes balanced static KD-tree.

        @param[in] points (array_like): Points that should be used to build KD-tree.
        @param[in] payloads (array_like): Payload of each point in `points`.

        """

        if points is None:
            self._length = 0
            self._dimension = 0
            self._point_comparator = None
            self._root = None
            return

        self._dimension = len(points[0])
        self._point_comparator = self._create_point_comparator(type(points[0]))
        self._length = 0

        nodes = []
        for i in range(len(points)):
            payload = None
            if payloads is not None:
                payload = payloads[i]

            nodes.append(node(points[i], payload, None, None, -1, None))

        self._root = self.__create_tree(nodes, None, 0)

    def __len__(self):
        """!
        @brief Returns amount of nodes in the KD-tree.

        @return (uint) Amount of nodes in the KD-tree.

        """
        return self._length

    def get_root(self):
        """!
        @brief Returns root of the tree.

        @return (node) The root of the tree.

        """
        return self._root

    def __create_tree(self, nodes, parent, depth):
        """!
        @brief Creates balanced sub-tree using elements from list `nodes`.

        @param[in] nodes (list): List of KD-tree nodes.
        @param[in] parent (node): Parent node that is used as a root to build the sub-tree.
        @param[in] depth (uint): Depth of the tree that where children of the `parent` should be placed.

        @return (node) Returns a node that is a root of the built sub-tree.

        """
        if len(nodes) == 0:
            return None

        discriminator = depth % self._dimension

        nodes.sort(key=lambda n: n.data[discriminator])
        median = len(nodes) // 2

        # Elements could be the same around the median, but all elements that are >= to the current should
        # be at the right side.
        # TODO: optimize by binary search - no need to use O(n)
        median = find_left_element(nodes, median, lambda n1, n2: n1.data[discriminator] < n2.data[discriminator])
        # while median - 1 >= 0 and \
        #         nodes[median].data[discriminator] == nodes[median - 1].data[discriminator]:
        #     median -= 1

        new_node = nodes[median]
        new_node.disc = discriminator
        new_node.parent = parent
        new_node.left = self.__create_tree(nodes[:median], new_node, depth + 1)
        new_node.right = self.__create_tree(nodes[median + 1:], new_node, depth + 1)

        self._length += 1
        return new_node

    def _create_point_comparator(self, type_point):
        """!
        @brief Create point comparator.
        @details In case of numpy.array specific comparator is required.

        @param[in] type_point (data_type): Type of point that is stored in KD-node.

        @return (callable) Callable point comparator to compare to points.

        """
        if type_point == numpy.ndarray:
            return lambda obj1, obj2: numpy.array_equal(obj1, obj2)

        return lambda obj1, obj2: obj1 == obj2

    def _find_node_by_rule(self, point, search_rule, cur_node):
        """!
        @brief Search node that satisfy to parameters in search rule.
        @details If node with specified parameters does not exist then None will be returned,
                  otherwise required node will be returned.

        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] search_rule (lambda): Rule that is called to check whether node satisfies to search parameter.
        @param[in] cur_node (node): Node from which search should be started.

        @return (node) Node if it satisfies to input parameters, otherwise it return None.

        """

        if cur_node is None:
            cur_node = self._root

        while cur_node:
            if cur_node.data[cur_node.disc] <= point[cur_node.disc]:
                # no need to check each node, only when it may satisfy the condition
                if search_rule(cur_node):  # compare point with point in the current node
                    return cur_node

                cur_node = cur_node.right
            else:
                cur_node = cur_node.left

        return None

    def find_node_with_payload(self, point, point_payload, cur_node=None):
        """!
        @brief Find node with specified coordinates and payload.
        @details If node with specified parameters does not exist then None will be returned,
                  otherwise required node will be returned.

        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] point_payload (any): Payload of the node that is searched in the tree.
        @param[in] cur_node (node): Node from which search should be started.

        @return (node) Node if it satisfies to input parameters, otherwise it return None.

        """

        rule_search = lambda node, point=point, payload=point_payload: self._point_comparator(node.data, point) and \
                                                                       node.payload == payload
        return self._find_node_by_rule(point, rule_search, cur_node)

    def find_node(self, point, cur_node=None):
        """!
        @brief Find node with coordinates that are defined by specified point.
        @details If node with specified parameters does not exist then None will be returned,
                  otherwise required node will be returned.

        @param[in] point (list): Coordinates of the point whose node should be found.
        @param[in] cur_node (node): Node from which search should be started.

        @return (node) Node if it satisfies to input parameters, otherwise it return None.

        """

        rule_search = lambda node, point=point: self._point_comparator(node.data, point)
        return self._find_node_by_rule(point, rule_search, cur_node)

    def find_nearest_dist_node(self, point, distance, retdistance=False):
        """!
        @brief Find nearest neighbor in area with radius = distance.

        @param[in] point (list): Maximum distance where neighbors are searched.
        @param[in] distance (double): Maximum distance where neighbors are searched.
        @param[in] retdistance (bool): If True - returns neighbors with distances to them, otherwise only neighbors
                    is returned.

        @return (node|list) Nearest neighbor if 'retdistance' is False and list with two elements [node, distance]
                 if 'retdistance' is True, where the first element is pointer to node and the second element is
                 distance to it.

        """

        best_nodes = self.find_nearest_dist_nodes(point, distance)

        if len(best_nodes) == 0:
            return None

        nearest = min(best_nodes, key=lambda item: item[0])

        if retdistance is True:
            return nearest
        else:
            return nearest[1]

    def find_nearest_dist_nodes(self, point, distance):
        """!
        @brief Find neighbors that are located in area that is covered by specified distance.

        @param[in] point (list): Coordinates that is considered as centroid for searching.
        @param[in] distance (double): Distance from the center where searching is performed.

        @return (list) Neighbors in area that is specified by point (center) and distance (radius).

        """

        best_nodes = []
        if self._root is not None:
            self.__recursive_nearest_nodes(point, distance, distance * distance, self._root, best_nodes)

        return best_nodes

    def __recursive_nearest_nodes(self, point, distance, sqrt_distance, node_head, best_nodes):
        """!
        @brief Returns list of neighbors such as tuple (distance, node) that is located in area that is covered by distance.

        @param[in] point (list): Coordinates that is considered as centroid for searching
        @param[in] distance (double): Distance from the center where searching is performed.
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
            best_nodes.append((candidate_distance, node_head))



class kdtree(kdtree_balanced):
    """!
    @brief   Represents KD Tree that is a space-partitioning data structure for organizing points
              in a k-dimensional space.
    @details In the term k-d tree, k denotes the dimensionality of the space being represented. Each data point is
              represented as a node in the k-d tree in the form of a record of type node. The tree supports
              dynamic construction when nodes can be dynamically added and removed. As a result KD-tree might not be
              balanced if methods `insert` and `remove` are used to built the tree. If the tree is built using
              constructor where all points are passed to the tree then balanced tree is built. Single point search and
              range-search procedures have complexity is `O(n)` in worse case in case of unbalanced tree.
              If there is no need to build dynamic KD-tree, then it is much better to use static KD-tree
              `kdtree_balanced`.
    
    There is an example how to use KD-tree to search nodes (points from input data) that are nearest to some point:
    @code
        # Import required modules
        from pyclustering.samples.definitions import SIMPLE_SAMPLES;
        from pyclustering.container.kdtree import kdtree;
        from pyclustering.utils import read_sample;
        
        # Read data from text file
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
        
        # Create instance of KD-tree and initialize (fill) it by read data.
        # In this case the tree is balanced.
        tree_instance = kdtree(sample);
        
        # Search for nearest point
        search_distance = 0.3;
        nearest_node = tree_instance.find_nearest_dist_node([1.12, 4.31], search_distance);
        
        # Search for nearest point in radius 0.3
        nearest_nodes = tree_instance.find_nearest_dist_nodes([1.12, 4.31], search_distance);
        print("Nearest nodes:", nearest_nodes);
    @endcode

    In case of building KD-tree using `insert` and `remove` method, the output KD-tree might be unbalanced - here
    is an example that demonstrates this:
    @code
        from pyclustering.container.kdtree import kdtree, kdtree_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

        # Build tree using constructor - balanced will be built because tree will know about all points.
        tree_instance = kdtree(sample)
        kdtree_visualizer(tree_instance).visualize()

        # Build tree using `insert` only - unbalanced tree will be built.
        tree_instance = kdtree()
        for point in sample:
            tree_instance.insert(point)

        kdtree_visualizer(tree_instance).visualize()
    @endcode

    There are two figures where difference between balanced and unbalanced KD-trees is demonstrated.

    @image html kd_tree_unbalanced_two_diamonds.png "Fig. 1. Balanced KD-tree for sample 'TwoDiamonds'."
    @image html kd_tree_unbalanced_two_diamonds.png "Fig. 2. Unbalanced KD-tree for sample 'TwoDiamonds'."

    @see kdtree_balanced

    """
    
    def __init__(self, data_list=None, payload_list=None):
        """!
        @brief Create kd-tree from list of points and from according list of payloads.
        @details If lists were not specified then empty kd-tree will be created.
        
        @param[in] data_list (list): Insert points from the list to created KD tree.
        @param[in] payload_list (list): Insert payload from the list to created KD tree, length should be equal to
                    length of data_list if it is specified.
        
        """

        super().__init__(data_list, payload_list)

    def insert(self, point, payload=None):
        """!
        @brief Insert new point with payload to kd-tree.
        
        @param[in] point (list): Coordinates of the point of inserted node.
        @param[in] payload (any-type): Payload of inserted node. It can be ID of the node or
                    some useful payload that belongs to the point.
        
        @return (node) Inserted node to the kd-tree.
        
        """
        
        if self._root is None:
            self._dimension = len(point)
            self._root = node(point, payload, None, None, 0)
            self._point_comparator = self._create_point_comparator(type(point))

            self._length += 1
            return self._root

        cur_node = self._root

        while True:
            discriminator = (cur_node.disc + 1) % self._dimension

            if cur_node.data[cur_node.disc] <= point[cur_node.disc]:
                if cur_node.right is None:
                    cur_node.right = node(point, payload, None, None, discriminator, cur_node)

                    self._length += 1
                    return cur_node.right
                else: 
                    cur_node = cur_node.right
            
            else:
                if cur_node.left is None:
                    cur_node.left = node(point, payload, None, None, discriminator, cur_node)

                    self._length += 1
                    return cur_node.left
                else:
                    cur_node = cur_node.left

    def remove(self, point, **kwargs):
        """!
        @brief Remove specified point from kd-tree.
        @details It removes the first found node that satisfy to the input parameters. Make sure that
                  pair (point, payload) is unique for each node, otherwise the first found is removed.
        
        @param[in] point (list): Coordinates of the point of removed node.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'payload').
        
        <b>Keyword Args:</b><br>
            - payload (any): Payload of the node that should be removed.
        
        @return (node) Root if node has been successfully removed, otherwise None.
        
        """

        if 'payload' in kwargs:
            node_for_remove = self.find_node_with_payload(point, kwargs['payload'], None)
        else:
            node_for_remove = self.find_node(point, None)
        
        if node_for_remove is None:
            return None

        self._length -= 1

        parent = node_for_remove.parent
        minimal_node = self.__recursive_remove(node_for_remove)
        if parent is None:
            self._root = minimal_node
            
            # If all k-d tree was destroyed
            if minimal_node is not None:
                minimal_node.parent = None
        else:
            if parent.left is node_for_remove:
                parent.left = minimal_node
            elif parent.right is node_for_remove:
                parent.right = minimal_node
        
        return self._root

    def __recursive_remove(self, node_removed):
        """!
        @brief Delete node and return root of subtree.
        
        @param[in] node_removed (node): Node that should be removed.
        
        @return (node) Minimal node in line with coordinate that is defined by discriminator.
        
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
        minimal_node = self.__find_minimal_node(node_removed.right, discriminator)
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

    def __find_minimal_node(self, node_head, discriminator):
        """!
        @brief Find minimal node in line with coordinate that is defined by discriminator.
        
        @param[in] node_head (node): Node of KD tree from that search should be started.
        @param[in] discriminator (uint): Coordinate number that is used for comparison.
        
        @return (node) Minimal node in line with discriminator from the specified node.
        
        """
        
        min_key = lambda cur_node: cur_node.data[discriminator]

        stack, candidates = [], []
        is_finished = False

        while is_finished is False:
            if node_head is not None:
                stack.append(node_head)
                node_head = node_head.left
            else:
                if len(stack) != 0:
                    node_head = stack.pop()
                    candidates.append(node_head)
                    node_head = node_head.right
                else:
                    is_finished = True

        return min(candidates, key=min_key)
