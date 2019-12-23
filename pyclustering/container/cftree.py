"""!

@brief Data Structure: CF-Tree
@details Implementation based on paper @cite article::birch::1.

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

from copy import copy

from pyclustering.utils import euclidean_distance_square
from pyclustering.utils import manhattan_distance
from pyclustering.utils import linear_sum, square_sum

from enum import IntEnum


class measurement_type(IntEnum):
    """!
    @brief Enumeration of measurement types for CF-Tree.
    
    @see cftree
    
    """
    
    ## Euclidian distance between centroids of clustering features.
    CENTROID_EUCLIDEAN_DISTANCE = 0
    
    ## Manhattan distance between centroids of clustering features.
    CENTROID_MANHATTAN_DISTANCE = 1
    
    ## Average distance between all objects from clustering features.
    AVERAGE_INTER_CLUSTER_DISTANCE = 2
    
    ## Average distance between all objects within clustering features and between them.
    AVERAGE_INTRA_CLUSTER_DISTANCE = 3
    
    ## Variance based distance between clustering features.
    VARIANCE_INCREASE_DISTANCE = 4


class cfnode_type(IntEnum):
    """!
    @brief Enumeration of CF-Node types that are used by CF-Tree.
    
    @see cfnode
    @see cftree
    
    """
    
    ## Undefined node.
    CFNODE_DUMMY = 0
    
    ## Leaf node hasn't got successors, only entries.
    CFNODE_LEAF = 1
    
    ## Non-leaf node has got successors and hasn't got entries.
    CFNODE_NONLEAF = 2


class cfentry:
    """!
    @brief Clustering feature representation.
    
    @see cfnode
    @see cftree
    
    """

    @property
    def number_points(self):
        """!
        @brief Returns number of points that are encoded.
        
        @return (uint) Number of encoded points.
        
        """
        return self.__number_points

    @property
    def linear_sum(self):
        """!
        @brief Returns linear sum.
        
        @return (list) Linear sum.
        
        """
        
        return self.__linear_sum

    @property
    def square_sum(self):
        """!
        @brief Returns square sum.
        
        @return (double) Square sum.
        
        """
        return self.__square_sum


    def __init__(self, number_points, linear_sum, square_sum):
        """!
        @brief CF-entry constructor.
        
        @param[in] number_points (uint): Number of objects that is represented by the entry.
        @param[in] linear_sum (list): Linear sum of values that represent objects in each dimension.
        @param[in] square_sum (double): Square sum of values that represent objects.
        
        """
        
        self.__number_points = number_points
        self.__linear_sum = numpy.array(linear_sum)
        self.__square_sum = square_sum
        
        self.__centroid = None
        self.__radius = None
        self.__diameter = None


    def __copy__(self):
        """!
        @returns (cfentry) Makes copy of the CF-entry instance.
        
        """
        return cfentry(self.__number_points, self.__linear_sum, self.__square_sum)


    def __repr__(self):
        """!
        @return (string) Returns CF-entry representation.
        
        """
        return "CF-Entry (N: '%s', LS: '%s', D: '%s')" % \
               (self.number_points, self.linear_sum, str(self.get_diameter()))


    def __str__(self):
        """!
        @brief Default cfentry string representation.
        
        """
        return self.__repr__()


    def __add__(self, entry):
        """!
        @brief Overloaded operator add. Performs addition of two clustering features.
        
        @param[in] entry (cfentry): Entry that is added to the current.
        
        @return (cfentry) Result of addition of two clustering features.
        
        """
        
        number_points = self.number_points + entry.number_points
        result_linear_sum = numpy.add(self.linear_sum, entry.linear_sum)
        result_square_sum = self.square_sum + entry.square_sum
        
        return cfentry(number_points, result_linear_sum, result_square_sum)


    def __eq__(self, entry):
        """!
        @brief Overloaded operator eq. 
        @details Performs comparison of two clustering features.
        
        @param[in] entry (cfentry): Entry that is used for comparison with current.
        
        @return (bool) True is both clustering features are equals in line with tolerance, otherwise False.
        
        """
                
        tolerance = 0.00001
        
        result = (self.__number_points == entry.number_points)
        result &= ((self.square_sum + tolerance > entry.square_sum) and (self.square_sum - tolerance < entry.square_sum))
        
        for index_dimension in range(0, len(self.linear_sum)):
            result &= ((self.linear_sum[index_dimension] + tolerance > entry.linear_sum[index_dimension]) and (self.linear_sum[index_dimension] - tolerance < entry.linear_sum[index_dimension]))
        
        return result


    def get_distance(self, entry, type_measurement):
        """!
        @brief Calculates distance between two clusters in line with measurement type.
        
        @details In case of usage CENTROID_EUCLIDIAN_DISTANCE square euclidian distance will be returned.
                 Square root should be taken from the result for obtaining real euclidian distance between
                 entries. 
        
        @param[in] entry (cfentry): Clustering feature to which distance should be obtained.
        @param[in] type_measurement (measurement_type): Distance measurement algorithm between two clusters.
        
        @return (double) Distance between two clusters.
        
        """
        
        if type_measurement is measurement_type.CENTROID_EUCLIDEAN_DISTANCE:
            return euclidean_distance_square(entry.get_centroid(), self.get_centroid())
        
        elif type_measurement is measurement_type.CENTROID_MANHATTAN_DISTANCE:
            return manhattan_distance(entry.get_centroid(), self.get_centroid())
        
        elif type_measurement is measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE:
            return self.__get_average_inter_cluster_distance(entry)
            
        elif type_measurement is measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE:
            return self.__get_average_intra_cluster_distance(entry)
        
        elif type_measurement is measurement_type.VARIANCE_INCREASE_DISTANCE:
            return self.__get_variance_increase_distance(entry)

        else:
            raise ValueError("Unsupported type of measurement '%s' is specified." % type_measurement)


    def get_centroid(self):
        """!
        @brief Calculates centroid of cluster that is represented by the entry. 
        @details It's calculated once when it's requested after the last changes.
        
        @return (array_like) Centroid of cluster that is represented by the entry.
        
        """
        
        if self.__centroid is not None:
            return self.__centroid

        self.__centroid = numpy.divide(self.linear_sum, self.number_points)
        return self.__centroid
    
    
    def get_radius(self):
        """!
        @brief Calculates radius of cluster that is represented by the entry.
        @details It's calculated once when it's requested after the last changes.
        
        @return (double) Radius of cluster that is represented by the entry.
        
        """
        
        if self.__radius is not None:
            return self.__radius

        N = self.number_points
        centroid = self.get_centroid()
        
        radius_part_1 = self.square_sum
        radius_part_2 = 2.0 * numpy.dot(self.linear_sum, centroid)
        radius_part_3 = N * numpy.dot(centroid, centroid)
        
        self.__radius = ((1.0 / N) * (radius_part_1 - radius_part_2 + radius_part_3)) ** 0.5
        return self.__radius


    def get_diameter(self):
        """!
        @brief Calculates diameter of cluster that is represented by the entry.
        @details It's calculated once when it's requested after the last changes.
        
        @return (double) Diameter of cluster that is represented by the entry.
        
        """
        
        if self.__diameter is not None:
            return self.__diameter

        diameter_part = self.square_sum * self.number_points - 2.0 * numpy.dot(self.linear_sum, self.linear_sum) + self.square_sum * self.number_points

        if diameter_part < 0.000000001:
            self.__diameter = 0.0
        else:
            self.__diameter = (diameter_part / (self.number_points * (self.number_points - 1))) ** 0.5

        return self.__diameter


    def __get_average_inter_cluster_distance(self, entry):
        """!
        @brief Calculates average inter cluster distance between current and specified clusters.
        
        @param[in] entry (cfentry): Clustering feature to which distance should be obtained.
        
        @return (double) Average inter cluster distance.
        
        """
        
        linear_part_distance = numpy.dot(self.linear_sum, entry.linear_sum)

        return ((entry.number_points * self.square_sum - 2.0 * linear_part_distance + self.number_points * entry.square_sum) / (self.number_points * entry.number_points)) ** 0.5


    def __get_average_intra_cluster_distance(self, entry):
        """!
        @brief Calculates average intra cluster distance between current and specified clusters.
        
        @param[in] entry (cfentry): Clustering feature to which distance should be obtained.
        
        @return (double) Average intra cluster distance.
        
        """
        
        linear_part_first = numpy.add(self.linear_sum, entry.linear_sum)
        linear_part_second = linear_part_first
        
        linear_part_distance = numpy.dot(linear_part_first, linear_part_second)
        
        general_part_distance = 2.0 * (self.number_points + entry.number_points) * (self.square_sum + entry.square_sum) - 2.0 * linear_part_distance
        
        return (general_part_distance / ((self.number_points + entry.number_points) * (self.number_points + entry.number_points - 1.0))) ** 0.5
    
    
    def __get_variance_increase_distance(self, entry):
        """!
        @brief Calculates variance increase distance between current and specified clusters.
        
        @param[in] entry (cfentry): Clustering feature to which distance should be obtained.
        
        @return (double) Variance increase distance.
        
        """
                
        linear_part_12 = numpy.add(self.linear_sum, entry.linear_sum)
        variance_part_first = (self.square_sum + entry.square_sum) - \
            2.0 * numpy.dot(linear_part_12, linear_part_12) / (self.number_points + entry.number_points) + \
            (self.number_points + entry.number_points) * numpy.dot(linear_part_12, linear_part_12) / (self.number_points + entry.number_points)**2.0
        
        linear_part_11 = numpy.dot(self.linear_sum, self.linear_sum)
        variance_part_second = -(self.square_sum - (2.0 * linear_part_11 / self.number_points) + (linear_part_11 / self.number_points))
        
        linear_part_22 = numpy.dot(entry.linear_sum, entry.linear_sum)
        variance_part_third = -(entry.square_sum - (2.0 / entry.number_points) * linear_part_22 + entry.number_points * (1.0 / entry.number_points ** 2.0) * linear_part_22)

        return variance_part_first + variance_part_second + variance_part_third
        

class cfnode:
    """!
    @brief Representation of node of CF-Tree.
    
    """
    
    def __init__(self, feature, parent):
        """!
        @brief Constructor of abstract CF node.
        
        @param[in] feature (cfentry): Clustering feature of the created node.
        @param[in] parent (cfnode): Parent of the created node.
        
        """
        
        ## Clustering feature of the node.
        self.feature = copy(feature)

        ## Pointer to the parent node (None for root).
        self.parent = parent
        
        ## Type node (leaf or non-leaf).
        self.type = cfnode_type.CFNODE_DUMMY
    
    
    def __repr__(self):
        """!
        @return (string) Default representation of CF node.
        
        """
        
        return 'CF node %s, parent %s, feature %s' % (hex(id(self)), self.parent, self.feature)


    def __str__(self):
        """!
        @return (string) String representation of CF node.
        
        """
        return self.__repr__()
    
    
    def get_distance(self, node, type_measurement):
        """!
        @brief Calculates distance between nodes in line with specified type measurement.
        
        @param[in] node (cfnode): CF-node that is used for calculation distance to the current node.
        @param[in] type_measurement (measurement_type): Measurement type that is used for calculation distance.
        
        @return (double) Distance between two nodes.
        
        """
        
        return self.feature.get_distance(node.feature, type_measurement)
    

class non_leaf_node(cfnode):
    """!
    @brief Representation of clustering feature non-leaf node.
    
    """ 
    
    @property
    def successors(self):
        """!
        @return (list) List of successors of the node.
        
        """
        return self.__successors
    
    
    def __init__(self, feature, parent, successors):
        """!
        @brief Create CF Non-leaf node.
        
        @param[in] feature (cfentry): Clustering feature of the created node.
        @param[in] parent (non_leaf_node): Parent of the created node.
        @param[in] successors (list): List of successors of the node.
        
        """
                
        super().__init__(feature, parent)
        
        ## Node type in CF tree that is CFNODE_NONLEAF for non leaf node.
        self.type = cfnode_type.CFNODE_NONLEAF
        
        self.__successors = successors
    
    
    def __repr__(self):
        """!
        @return (string) Representation of non-leaf node representation.
        
        """   
        return 'Non-leaf node %s, parent %s, feature %s, successors: %d' % (hex(id(self)), self.parent, self.feature, len(self.successors))
    
    
    def __str__(self):
        """!
        @return (string) String non-leaf representation.
        
        """
        return self.__repr__()
    
    
    def insert_successor(self, successor):
        """!
        @brief Insert successor to the node.
        
        @param[in] successor (cfnode): Successor for adding.
        
        """
        
        self.feature += successor.feature
        self.successors.append(successor)
        
        successor.parent = self


    def merge(self, node):
        """!
        @brief Merge non-leaf node to the current.
        
        @param[in] node (non_leaf_node): Non-leaf node that should be merged with current.
        
        """
                
        self.feature += node.feature
        
        for child in node.successors:
            child.parent = self
            self.successors.append(child)
    
    
    def get_farthest_successors(self, type_measurement):
        """!
        @brief Find pair of farthest successors of the node in line with measurement type.
        
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining farthest successors.
        
        @return (list) Pair of farthest successors represented by list [cfnode1, cfnode2].
        
        """
        
        farthest_node1 = None
        farthest_node2 = None
        farthest_distance = 0.0
        
        for i in range(0, len(self.successors)):
            candidate1 = self.successors[i]
            
            for j in range(i + 1, len(self.successors)):
                candidate2 = self.successors[j]
                candidate_distance = candidate1.get_distance(candidate2, type_measurement)
                
                if candidate_distance > farthest_distance:
                    farthest_distance = candidate_distance
                    farthest_node1 = candidate1
                    farthest_node2 = candidate2
        
        return [farthest_node1, farthest_node2]
    
    
    def get_nearest_successors(self, type_measurement):
        """!
        @brief Find pair of nearest successors of the node in line with measurement type.
        
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining nearest successors.
        
        @return (list) Pair of nearest successors represented by list.
        
        """
                
        nearest_node1 = None
        nearest_node2 = None
        nearest_distance = float("Inf")
        
        for i in range(0, len(self.successors)):
            candidate1 = self.successors[i]
            
            for j in range(i + 1, len(self.successors)):
                candidate2 = self.successors[j]
                candidate_distance = candidate1.get_distance(candidate2, type_measurement)
                
                if candidate_distance < nearest_distance:
                    nearest_distance = candidate_distance
                    nearest_node1 = candidate1
                    nearest_node2 = candidate2
        
                return [nearest_node1, nearest_node2]


class leaf_node(cfnode):
    """!
    @brief Represents clustering feature leaf node.
    
    """
    
    @property
    def entries(self):
        """!
        @return (list) List of leaf nodes.
        
        """
        return self.__entries
    
    
    def __init__(self, feature, parent, entries):
        """!
        @brief Create CF Leaf node.
        
        @param[in] feature (cfentry): Clustering feature of the created node.
        @param[in] parent (non_leaf_node): Parent of the created node.
        @param[in] entries (list): List of entries of the node.
        
        """
        
        super().__init__(feature, parent)
        
        ## Node type in CF tree that is CFNODE_LEAF for leaf node.
        self.type = cfnode_type.CFNODE_LEAF
        
        self.__entries = entries   # list of clustering features
        
    
    def __repr__(self):
        """!
        @return (string) Default leaf node represenation.
        
        """
        text_entries = "\n"
        for entry in self.entries:
            text_entries += "\t" + str(entry) + "\n"
        
        return "Leaf-node: '%s', parent: '%s', feature: '%s', entries: '%d'" % \
               (str(hex(id(self))), self.parent, self.feature, len(self.entries))
    
    
    def __str__(self):
        """!
        @return (string) String leaf node representation.
        
        """
        return self.__repr__()
    
    
    def insert_entry(self, entry):
        """!
        @brief Insert new clustering feature to the leaf node.
        
        @param[in] entry (cfentry): Clustering feature.
        
        """

        self.feature += entry
        self.entries.append(entry)


    def merge(self, node):
        """!
        @brief Merge leaf node to the current.
        
        @param[in] node (leaf_node): Leaf node that should be merged with current.
        
        """
        
        self.feature += node.feature
        
        # Move entries from merged node
        for entry in node.entries:
            self.entries.append(entry)


    def get_farthest_entries(self, type_measurement):
        """!
        @brief Find pair of farthest entries of the node.
        
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining farthest entries.
        
        @return (list) Pair of farthest entries of the node that are represented by list.
        
        """
        
        farthest_entity1 = None
        farthest_entity2 = None
        farthest_distance = 0
        
        for i in range(0, len(self.entries)):
            candidate1 = self.entries[i]
            
            for j in range(i + 1, len(self.entries)):
                candidate2 = self.entries[j]
                candidate_distance = candidate1.get_distance(candidate2, type_measurement)
                
                if candidate_distance > farthest_distance:
                    farthest_distance = candidate_distance
                    farthest_entity1 = candidate1
                    farthest_entity2 = candidate2
        
        return [farthest_entity1, farthest_entity2]


    def get_nearest_index_entry(self, entry, type_measurement):
        """!
        @brief Find nearest index of nearest entry of node for the specified entry.
        
        @param[in] entry (cfentry): Entry that is used for calculation distance.
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining nearest entry to the specified.
        
        @return (uint) Index of nearest entry of node for the specified entry.
        
        """
        
        minimum_distance = float('Inf')
        nearest_index = -1
        
        for candidate_index in range(0, len(self.entries)):
            candidate_distance = self.entries[candidate_index].get_distance(entry, type_measurement)
            if candidate_distance < minimum_distance:
                minimum_distance = candidate_distance
                nearest_index = candidate_index
        
        return nearest_index


    def get_nearest_entry(self, entry, type_measurement):
        """!
        @brief Find nearest entry of node for the specified entry.
        
        @param[in] entry (cfentry): Entry that is used for calculation distance.
        @param[in] type_measurement (measurement_type): Measurement type that is used for obtaining nearest entry to the specified.
        
        @return (cfentry) Nearest entry of node for the specified entry.
        
        """
        
        min_key = lambda cur_entity: cur_entity.get_distance(entry, type_measurement)
        return min(self.entries, key=min_key)


class cftree:
    """!
    @brief CF-Tree representation.
    @details A CF-tree is a height-balanced tree with two parameters: branching factor and threshold.
    
    """

    @property
    def root(self):
        """!
        @return (cfnode) Root of the tree.
        
        """
        return self.__root


    @property
    def leafes(self):
        """!
        @return (list) List of all leaf nodes in the tree.
        
        """
        return self.__leafes


    @property
    def amount_nodes(self):
        """!
        @return (unit) Number of nodes (leaf and non-leaf) in the tree.
        
        """
        return self.__amount_nodes


    @property
    def amount_entries(self):
        """!
        @return (uint) Number of entries in the tree.
        
        """
        return self.__amount_entries


    @property
    def height(self):
        """!
        @return (uint) Height of the tree.
        
        """
        return self.__height


    @property
    def branch_factor(self):
        """!
        @return (uint) Branching factor of the tree.
        @details Branching factor defines maximum number of successors in each non-leaf node.
        
        """
        return self.__branch_factor


    @property
    def threshold(self):
        """!
        @return (double) Threshold of the tree that represents maximum diameter of sub-clusters that is formed by leaf node entries.
        
        """
        return self.__threshold


    @property
    def max_entries(self):
        """!
        @return (uint) Maximum number of entries in each leaf node.
        
        """
        return self.__max_entries


    @property
    def type_measurement(self):
        """!
        @return (measurement_type) Type that is used for measuring.
        
        """
        return self.__type_measurement


    def __init__(self, branch_factor, max_entries, threshold, type_measurement = measurement_type.CENTROID_EUCLIDEAN_DISTANCE):
        """!
        @brief Create CF-tree.
        
        @param[in] branch_factor (uint): Maximum number of children for non-leaf nodes.
        @param[in] max_entries (uint): Maximum number of entries for leaf nodes.
        @param[in] threshold (double): Maximum diameter of feature clustering for each leaf node.
        @param[in] type_measurement (measurement_type): Measurement type that is used for calculation distance metrics.
        
        """

        self.__root = None

        self.__branch_factor = branch_factor  # maximum number of children
        if self.__branch_factor < 2:
            self.__branch_factor = 2
        
        self.__threshold = threshold  # maximum diameter of sub-clusters stored at the leaf nodes
        self.__max_entries = max_entries
        
        self.__leafes = []
        
        self.__type_measurement = type_measurement
        
        # statistics
        self.__amount_nodes = 0    # root, despite it can be None.
        self.__amount_entries = 0
        self.__height = 0          # tree size with root.


    def get_level_nodes(self, level):
        """!
        @brief Traverses CF-tree to obtain nodes at the specified level.
        
        @param[in] level (uint): CF-tree level from that nodes should be returned.
        
        @return (list) List of CF-nodes that are located on the specified level of the CF-tree.
        
        """
        
        level_nodes = []
        if level < self.__height:
            level_nodes = self.__recursive_get_level_nodes(level, self.__root)
        
        return level_nodes


    def __recursive_get_level_nodes(self, level, node):
        """!
        @brief Traverses CF-tree to obtain nodes at the specified level recursively.
        
        @param[in] level (uint): Current CF-tree level.
        @param[in] node (cfnode): CF-node from that traversing is performed.
        
        @return (list) List of CF-nodes that are located on the specified level of the CF-tree.
        
        """
        
        level_nodes = []
        if level is 0:
            level_nodes.append(node)
        
        else:
            for sucessor in node.successors:
                level_nodes += self.__recursive_get_level_nodes(level - 1, sucessor)
        
        return level_nodes


    def insert_point(self, point):
        """!
        @brief Insert point that is represented by list of coordinates.

        @param[in] point (list): Point represented by list of coordinates that should be inserted to CF tree.

        """

        entry = cfentry(len([point]), linear_sum([point]), square_sum([point]))
        self.insert(entry)
    
    
    def insert(self, entry):
        """!
        @brief Insert clustering feature to the tree.
        
        @param[in] entry (cfentry): Clustering feature that should be inserted.
        
        """
                
        if self.__root is None:
            node = leaf_node(entry, None, [entry])
            
            self.__root = node
            self.__leafes.append(node)
            
            # Update statistics
            self.__amount_entries += 1
            self.__amount_nodes += 1
            self.__height += 1             # root has successor now
        else:
            child_node_updation = self.__recursive_insert(entry, self.__root)
            if child_node_updation is True:
                # Splitting has been finished, check for possibility to merge (at least we have already two children).
                if self.__merge_nearest_successors(self.__root) is True:
                    self.__amount_nodes -= 1


    def find_nearest_leaf(self, entry, search_node = None):
        """!
        @brief Search nearest leaf to the specified clustering feature.
        
        @param[in] entry (cfentry): Clustering feature.
        @param[in] search_node (cfnode): Node from that searching should be started, if None then search process will be started for the root.
        
        @return (leaf_node) Nearest node to the specified clustering feature.
        
        """
        
        if search_node is None:
            search_node = self.__root
        
        nearest_node = search_node
        
        if search_node.type == cfnode_type.CFNODE_NONLEAF:
            min_key = lambda child_node: child_node.feature.get_distance(entry, self.__type_measurement)
            nearest_child_node = min(search_node.successors, key = min_key)
            
            nearest_node = self.find_nearest_leaf(entry, nearest_child_node)
        
        return nearest_node


    def __recursive_insert(self, entry, search_node):
        """!
        @brief Recursive insert of the entry to the tree.
        @details It performs all required procedures during insertion such as splitting, merging.
        
        @param[in] entry (cfentry): Clustering feature.
        @param[in] search_node (cfnode): Node from that insertion should be started.
        
        @return (bool) True if number of nodes at the below level is changed, otherwise False.
        
        """
        
        # None-leaf node
        if search_node.type == cfnode_type.CFNODE_NONLEAF:
            return self.__insert_for_noneleaf_node(entry, search_node)
        
        # Leaf is reached 
        else:
            return self.__insert_for_leaf_node(entry, search_node)


    def __insert_for_leaf_node(self, entry, search_node):
        """!
        @brief Recursive insert entry from leaf node to the tree.
        
        @param[in] entry (cfentry): Clustering feature.
        @param[in] search_node (cfnode): None-leaf node from that insertion should be started.
        
        @return (bool) True if number of nodes at the below level is changed, otherwise False.
        
        """
        
        node_amount_updation = False
        
        # Try to absorb by the entity
        index_nearest_entry = search_node.get_nearest_index_entry(entry, self.__type_measurement)
        nearest_entry = search_node.entries[index_nearest_entry]    # get nearest entry
        merged_entry = nearest_entry + entry
        
        # Otherwise try to add new entry
        if merged_entry.get_diameter() > self.__threshold:
            # If it's not exceeded append entity and update feature of the leaf node.
            search_node.insert_entry(entry)
            
            # Otherwise current node should be splitted
            if len(search_node.entries) > self.__max_entries:
                self.__split_procedure(search_node)
                node_amount_updation = True
            
            # Update statistics
            self.__amount_entries += 1
            
        else:
            search_node.entries[index_nearest_entry] = merged_entry
            search_node.feature += entry
        
        return node_amount_updation


    def __insert_for_noneleaf_node(self, entry, search_node):
        """!
        @brief Recursive insert entry from none-leaf node to the tree.
        
        @param[in] entry (cfentry): Clustering feature.
        @param[in] search_node (cfnode): None-leaf node from that insertion should be started.
        
        @return (bool) True if number of nodes at the below level is changed, otherwise False.
        
        """
        
        node_amount_updation = False
        
        min_key = lambda child_node: child_node.get_distance(search_node, self.__type_measurement)
        nearest_child_node = min(search_node.successors, key=min_key)
        
        child_node_updation = self.__recursive_insert(entry, nearest_child_node)
        
        # Update clustering feature of none-leaf node.
        search_node.feature += entry
            
        # Check branch factor, probably some leaf has been splitted and threshold has been exceeded.
        if (len(search_node.successors) > self.__branch_factor):
            
            # Check if it's aleady root then new root should be created (height is increased in this case).
            if search_node is self.__root:
                self.__root = non_leaf_node(search_node.feature, None, [search_node])
                search_node.parent = self.__root
                
                # Update statistics
                self.__amount_nodes += 1
                self.__height += 1
                
            [new_node1, new_node2] = self.__split_nonleaf_node(search_node)
            
            # Update parent list of successors
            parent = search_node.parent
            parent.successors.remove(search_node)
            parent.successors.append(new_node1)
            parent.successors.append(new_node2)
            
            # Update statistics
            self.__amount_nodes += 1
            node_amount_updation = True
            
        elif child_node_updation is True:
            # Splitting has been finished, check for possibility to merge (at least we have already two children).
            if self.__merge_nearest_successors(search_node) is True:
                self.__amount_nodes -= 1
        
        return node_amount_updation


    def __merge_nearest_successors(self, node):
        """!
        @brief Find nearest sucessors and merge them.
        
        @param[in] node (non_leaf_node): Node whose two nearest successors should be merged.
        
        @return (bool): True if merging has been successfully performed, otherwise False.
        
        """
        
        merging_result = False
        
        if node.successors[0].type == cfnode_type.CFNODE_NONLEAF:
            [nearest_child_node1, nearest_child_node2] = node.get_nearest_successors(self.__type_measurement)
            
            if len(nearest_child_node1.successors) + len(nearest_child_node2.successors) <= self.__branch_factor:
                node.successors.remove(nearest_child_node2)
                if nearest_child_node2.type == cfnode_type.CFNODE_LEAF:
                    self.__leafes.remove(nearest_child_node2)
                
                nearest_child_node1.merge(nearest_child_node2)
                
                merging_result = True
        
        return merging_result


    def __split_procedure(self, split_node):
        """!
        @brief Starts node splitting procedure in the CF-tree from the specify node.
        
        @param[in] split_node (cfnode): CF-tree node that should be splitted.
        
        """
        if split_node is self.__root:
            self.__root = non_leaf_node(split_node.feature, None, [ split_node ])
            split_node.parent = self.__root
            
            # Update statistics
            self.__amount_nodes += 1
            self.__height += 1
        
        [new_node1, new_node2] = self.__split_leaf_node(split_node)
        
        self.__leafes.remove(split_node)
        self.__leafes.append(new_node1)
        self.__leafes.append(new_node2)
        
        # Update parent list of successors
        parent = split_node.parent
        parent.successors.remove(split_node)
        parent.successors.append(new_node1)
        parent.successors.append(new_node2)
        
        # Update statistics
        self.__amount_nodes += 1


    def __split_nonleaf_node(self, node):
        """!
        @brief Performs splitting of the specified non-leaf node.
        
        @param[in] node (non_leaf_node): Non-leaf node that should be splitted.
        
        @return (list) New pair of non-leaf nodes [non_leaf_node1, non_leaf_node2].
        
        """
        
        [farthest_node1, farthest_node2] = node.get_farthest_successors(self.__type_measurement)
        
        # create new non-leaf nodes
        new_node1 = non_leaf_node(farthest_node1.feature, node.parent, [farthest_node1])
        new_node2 = non_leaf_node(farthest_node2.feature, node.parent, [farthest_node2])
        
        farthest_node1.parent = new_node1
        farthest_node2.parent = new_node2
        
        # re-insert other successors
        for successor in node.successors:
            if (successor is not farthest_node1) and (successor is not farthest_node2):
                distance1 = new_node1.get_distance(successor, self.__type_measurement)
                distance2 = new_node2.get_distance(successor, self.__type_measurement)
                
                if distance1 < distance2:
                    new_node1.insert_successor(successor)
                else:
                    new_node2.insert_successor(successor)
        
        return [new_node1, new_node2]


    def __split_leaf_node(self, node):
        """!
        @brief Performs splitting of the specified leaf node.
        
        @param[in] node (leaf_node): Leaf node that should be splitted.
        
        @return (list) New pair of leaf nodes [leaf_node1, leaf_node2].
        
        @warning Splitted node is transformed to non_leaf.
        
        """
        
        # search farthest pair of entries
        [farthest_entity1, farthest_entity2] = node.get_farthest_entries(self.__type_measurement)
                    
        # create new nodes
        new_node1 = leaf_node(farthest_entity1, node.parent, [farthest_entity1])
        new_node2 = leaf_node(farthest_entity2, node.parent, [farthest_entity2])
        
        # re-insert other entries
        for entity in node.entries:
            if (entity is not farthest_entity1) and (entity is not farthest_entity2):
                distance1 = new_node1.feature.get_distance(entity, self.__type_measurement)
                distance2 = new_node2.feature.get_distance(entity, self.__type_measurement)
                
                if distance1 < distance2:
                    new_node1.insert_entry(entity)
                else:
                    new_node2.insert_entry(entity)
        
        return [new_node1, new_node2]
