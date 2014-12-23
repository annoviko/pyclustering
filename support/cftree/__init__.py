'''

Data Structure: CF-Tree

Based on book description:
 - M.Zhang, R.Ramakrishnan, M.Livny. BIRCH: An Efficient Data Clustering Method for Very Large Databases. 1996.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from copy import copy;

from support import euclidean_distance, euclidean_distance_sqrt;
from support import manhattan_distance;
from support import list_math_addition, list_math_multiplication,list_math_division_number;
from support import linear_sum, square_sum;

class measurement_type:
    CENTROID_EUCLIDIAN_DISTANCE = 0;
    CENTROID_MANHATTAN_DISTANCE = 1;
    AVERAGE_INTER_CLUSTER_DISTANCE = 2;
    AVERAGE_INTRA_CLUSTER_DISTANCE = 3;
    VARIANCE_INCREASE_DISTANCE = 4;

class cfentry:
    "Clustering feature representation."
    
    __centroid = None;
    __radius = None;
    __diameter = None;
    
    __number_points = 0;
    __linear_sum = None;
    __square_sum = None;
    
    @property
    def number_points(self):
        return self.__number_points;
    
    @property
    def linear_sum(self):
        return self.__linear_sum;
    
    @property
    def square_sum(self):
        return self.__square_sum;
    
    
    def __init__(self, number_points, linear_sum, square_sum):
        self.__number_points = number_points;
        self.__linear_sum = linear_sum;
        self.__square_sum = square_sum;
        
        self.__centroid = None;
        self.__radius = None;
        self.__diameter = None;
    
    
    def __copy__(self):
        return cfentry(self.__number_points, self.__linear_sum, self.__square_sum);
    
    
    def __repr__(self):
        return 'CF (%s, %0.4f, %0.4f) [%s]' % ( self.number_points, self.__linear_sum, self.__square_sum, hex(id(self)) );    
    
    
    def __str__(self):
        return self.__repr__();
    
    
    def merge(self, entry, threshold_diameter):
        "Try to merge current clustering feature with another. Return result of merging cluster features."
        
        "(in) entry                 - pointer to clustering feature that should be merged with current."
        "(in) threshold_diameter    - if specified then cluster feature is merged if new diameter is less than threshold."
        "                             if None then cluster feature is merged certainly."
        
        "Return merged cluster feature in case of successful merging (less than specified diameter). Otherwise return None."
        
        number_points = self.number_points + entry.number_points;
        linear_sum = list_math_addition(self.linear_sum, entry.linear_sum);        
        square_sum = self.square_sum + entry.square_sum;
        
        merged_entry = cfentry(number_points, linear_sum, square_sum);
        if ( (threshold_diameter is not None) and (merged_entry.get_diameter() > threshold_diameter) ):
            return None;
        
        return merged_entry;
    
    
    def get_distance(self, entry, type_measurement):
        "Return distance between two clusters in line with measurement type."
        
        "(in) entry               - pointer of clustering feature to which distance should be obtained."
        "(in) type_measurement    - distance measurement algorithm between two clusters."
        
        "Return distance between two clusters."
        
        if (type_measurement is measurement_type.CENTROID_EUCLIDIAN_DISTANCE):
            return euclidean_distance_sqrt(entry.get_centroid(), self.get_centroid());
        
        elif (type_measurement is measurement_type.CENTROID_MANHATTAN_DISTANCE):
            return manhattan_distance(entry.get_centroid(), self.get_centroid());
        
        elif (type_measurement is measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE):
            return self.__get_average_inter_cluster_distance(entry);
            
        elif (type_measurement is measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE):
            return self.__get_average_intra_cluster_distance(entry);
        
        elif (type_measurement is measurement_type.VARIANCE_INCREASE_DISTANCE):
            return self.__get_variance_increase_distance(entry);
        
        else:
            assert 0;
    
        
    def get_centroid(self):
        "Return centroid of cluster that is represented by the entry. It's calculated once when it's requested after the last changes."
        
        if (self.__centroid is not None):
            return self.__centroid;
        
        if (type(self.linear_sum) == list):
            self.__centroid = [0] * len(self.linear_sum);
            for index_dimension in range(0, len(self.linear_sum)):
                self.__centroid[index_dimension] = self.linear_sum[index_dimension] / self.number_points;
        else:
            self.__centroid = self.linear_sum / self.number_points;
        
        return self.__centroid;
    
    
    def get_radius(self):
        "Return radius of cluster that is represented by the entry. It's calculated once when it's requested after the last changes."
        
        if (self.__radius is not None):
            return self.__radius;
        
        centroid = self.get_centroid();
        
        radius_part_1 = self.square_sum;
        
        radius_part_2 = 0.0;
        radius_part_3 = 0.0;
        
        if (type(centroid) == list):
            radius_part_2 = 2.0 * sum(list_math_multiplication(self.linear_sum, centroid));
            radius_part_3 = self.number_points * sum(list_math_multiplication(centroid, centroid));
        else:
            radius_part_2 = 2.0 * self.linear_sum * centroid;
            radius_part_3 = self.number_points * centroid * centroid;
        
        self.__radius = ( (1.0 / self.number_points) * (radius_part_1 - radius_part_2 + radius_part_3) ) ** 0.5;
        return self.__radius;
        
    
    def get_diameter(self):
        "Return diameter of cluster that is represented by the entry. It's calculated once when it's requested after the last changes."
        
        if (self.__diameter is not None):
            return self.__diameter;
        
        diameter_part = 0.0;
        if (type(self.linear_sum) == list):
            diameter_part = self.square_sum * self.number_points - 2.0 * sum(list_math_multiplication(self.linear_sum, self.linear_sum)) + self.square_sum * self.number_points;
        else:
            diameter_part = self.square_sum * self.number_points - 2.0 * self.linear_sum * self.linear_sum + self.square_sum * self.number_points;
            
        self.__diameter = ( diameter_part / (self.number_points * (self.number_points - 1)) ) ** 0.5;
        return self.__diameter;
    
        
    def __get_average_inter_cluster_distance(self, entry):
        "Return average inter cluster distance between current and specified clusters."
        
        "(in) entry    - pointer to clustering feature to which distance should be obtained."
        
        "Return average inter cluster distance."
        
        linear_part_distance = sum(list_math_multiplication(self.linear_sum, entry.linear_sum));
        
        return ( (entry.number_points * self.square_sum - 2.0 * linear_part_distance + self.number_points * entry.square_sum) / (self.number_points * entry.number_points) ) ** 0.5;
    
    
    def __get_average_intra_cluster_distance(self, entry):
        "Return average intra cluster distance between current and specified clusters."
        
        "(in) entry    - pointer to clustering feature to which distance should be obtained."
        
        "Return average intra cluster distance."
        
        linear_part_first = list_math_addition(self.linear_sum, entry.linear_sum);
        linear_part_second = linear_part_first;
        
        linear_part_distance = sum(list_math_multiplication(linear_part_first, linear_part_second));
        
        general_part_distance = 2.0 * (self.number_points + entry.number_points) * (self.square_sum + entry.square_sum) - 2.0 * linear_part_distance;
        
        return (general_part_distance / ( (self.number_points + entry.number_points) * (self.number_points + entry.number_points - 1.0) )) ** 0.5;
    
    
    def __get_variance_increase_distance(self, entry):
        "Return variance increase distance between current and specified clusters."
        
        "(in) entry    - pointer to clustering feature to which distance should be obtained."
        
        "Return variance increase distance."
                
        linear_part_12 = list_math_addition(self.linear_sum, entry.linear_sum);
        variance_part_first = (self.square_sum + entry.square_sum) - \
            2.0 * sum(list_math_multiplication(linear_part_12, linear_part_12)) / (self.number_points + entry.number_points) + \
            (self.number_points + entry.number_points) * sum(list_math_multiplication(linear_part_12, linear_part_12)) / (self.number_points + entry.number_points)**2.0;

        
        linear_part_11 = sum(list_math_multiplication(self.linear_sum, self.linear_sum));
        variance_part_second = -( self.square_sum - (2.0 * linear_part_11 / self.number_points) + (linear_part_11 / self.number_points) );
        
        linear_part_22 = sum(list_math_multiplication(entry.linear_sum, entry.linear_sum));
        variance_part_third = -( entry.square_sum - (2.0 / entry.number_points) * linear_part_22 + entry.number_points * (1.0 / entry.number_points ** 2.0) * linear_part_22 );

        return (variance_part_first + variance_part_second + variance_part_third);
        

class cfnode:
    "Representation of node of CF-Tree."
    
    feature     = None;     # clustering feature of the node
    successors  = None;     # successors of the node (None for leaf nodes)
    parent      = None;     # pointer to parent node (None for root)
    entries     = None;     # entries of leaf-node (None for non-leaf nodes)
    
    def __init__(self, feature, parent, successors, entries):
        self.feature = copy(feature);
        self.successors = successors;   # pointers to CF nodes
        self.parent = parent;
        
        self.entries = entries;       # pointer to entries (clustering features) - used only in case of leaf
    
    
    def __repr__(self):
        type_node = "unknown";
        if (self.successors is not None):
            type_node = 'non leaf (childs %s)' % len(self.successors);
        else:
            type_node = 'leaf (entries %s)' % len(self.entries);
            
        return 'CF %s node [%s], parent [%s]' % ( type_node, hex(id(self)), hex(id(self.parent)) );


    def __str__(self):
        return self.__repr__();
    
    
    def append_entity(self, entity):
        self.feature = self.feature.merge(entity, None);
        self.entries.append(entity);
    
    
    def append_successor(self, successor):
        self.feature = self.feature.merge(successor.feature, None);
        self.successors.append(successor);
        
        successor.parent = self;
    
    
    def get_distance(self, node, type_measurement):
        if (type(node) == cfnode):
            return self.feature.get_distance(node.feature, type_measurement);
        elif (type(node) == cfentry):
            return self.feature.get_distance(node, type_measurement);
        else:
            assert 0;

    
    def get_farthest_entries(self, type_measurement):
        farthest_entity1 = None;
        farthest_entity2 = None;
        farthest_distance = float("Inf");
        
        for i in range(0, len(self.entries)):
            candidate1 = self.entries[i];
            
            for j in range(i + 1, len(self.entries)):
                candidate2 = self.entries[j];
                candidate_distance = candidate1.get_distance(candidate2, type_measurement);
                
                if (candidate_distance < farthest_distance):
                    farthest_distance = candidate_distance;
                    farthest_entity1 = candidate1;
                    farthest_entity2 = candidate2;        
        
        return [farthest_entity1, farthest_entity2];
    
    
    def get_farthest_successors(self, type_measurement):
        farthest_node1 = None;
        farthest_node2 = None;
        farthest_distance = float("Inf");
        
        for i in range(0, len(self.successors)):
            candidate1 = self.successors[i];
            
            for j in range(i + 1, len(self.successors)):
                candidate2 = self.successors[j];
                candidate_distance = candidate1.get_distance(candidate2, type_measurement);
                
                if (candidate_distance < farthest_distance):
                    farthest_distance = candidate_distance;
                    farthest_node1 = candidate1;
                    farthest_node2 = candidate2;        
        
        return [farthest_node1, farthest_node2];
    
    
    def get_nearest_entity(self, entity, type_measurement): 
        min_key = lambda cur_entity: cur_entity.get_distance(entity, type_measurement);
        return min(self.entries, key = min_key);



class cftree:
    __root = None;
    __leafes = None;
    
    __branch_factor = 0;
    __threshold = 0.0;
    __max_entries = None;
    
    __type_measurement = None;
    
    #statistics
    __amount_nodes = 0;     # amount of nodes.
    __amount_entries = 0;   # amount of entries.
    __height = 0;           # height of tree.
    
    
    @property
    def root(self):
        return self.__root;
    
    @property
    def leafes(self):
        return self.__leafes;
    
    @property
    def amount_nodes(self):
        return self.__amount_nodes;
    
    @property
    def amount_entries(self):
        return self.__amount_entries;
    
    @property
    def height(self):
        return self.__height;
    
    
    def __init__(self, branch_factor, max_entries, threshold, type_measurement = measurement_type.CENTROID_EUCLIDIAN_DISTANCE):
        if (branch_factor < 2):
            branch_factor = 2;
        
        self.__branch_factor = branch_factor; # maximum number of children
        self.__threshold = threshold;         # maximum diameter of sub-clusters stored at the leaf nodes
        self.__max_entries = max_entries;
        
        self.__leafes = [];
        
        self.__type_measurement = type_measurement;
        
        # statistics
        self.__amount_nodes = 0;    # root, despite it can be None.
        self.__amount_entries = 0;
        self.__height = 0;          # tree size with root.
    
    
    def insert(self, cluster):
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster));
        node = cfnode(entry, None, None, [ entry ]);
        
        if (self.__root is None):
            self.__root = node;            
            self.__leafes.append(node);
            
            # Update statistics
            self.__amount_entries += 1;
            self.__amount_nodes += 1;       
            self.__height += 1;             # root has successor now
        else:
            self.__recursive_insert(node, self.__root);
    
    
    def find_nearest_leaf(self, node, search_node = None):
        if (search_node is None):
            search_node = self.__root;
        
        nearest_node = search_node;
        
        if (search_node.successors is not None):
            min_key = lambda child_node: child_node.get_distance(node, self.__type_measurement);
            nearest_child_node = min(search_node.successors, key = min_key);
            
            nearest_node = self.find_nearest_leaf(nearest_node, nearest_child_node);
        
        return nearest_node;
    
    
    def __recursive_insert(self, new_node, search_node):
        # None-leaf node
        if (search_node.successors is not None):
            min_key = lambda child_node: child_node.get_distance(search_node, self.__type_measurement);
            nearest_child_node = min(search_node.successors, key = min_key);
            
            self.__recursive_insert(new_node, nearest_child_node);
            
            # Update clustering feature of none-leaf node.
            search_node.feature.merge(new_node.feature, None);
                
            # Check branch factor, probably some leaf has been splitted and threshold has been exceeded.
            if (len(search_node.successors) > self.__branch_factor):
                
                # Check if it's aleady root then new root should be created (height is increased in this case).
                if (search_node is self.__root):
                    self.__root = cfnode(search_node.feature, None, [ search_node ], None);
                    search_node.parent = self.__root;
                    
                    # Update statistics
                    self.__amount_nodes += 1;
                    self.__height += 1;
                    
                [new_node1, new_node2] = self.__split_nonleaf_node(search_node);
                
                # Update parent list of successors
                parent = search_node.parent;
                parent.successors.remove(search_node);
                parent.successors.append(new_node1);
                parent.successors.append(new_node2);
                
                # Update statistics
                self.__amount_nodes += 1;
        
        # Leaf is reached 
        else:
            # Try to absorb by the entity
            search_entity = search_node.get_nearest_entity(new_node.feature, self.__type_measurement);
            merged_entity = search_entity.merge(new_node.feature, self.__threshold);
            
            # Otherwise try to add new entry
            if (merged_entity is None):
                # If it's not exceeded append entity and update feature of the leaf node.
                search_node.append_entity(new_node.feature);
                
                # Otherwise current node should be splitted
                if (len(search_node.entries) > self.__max_entries):
                    if (search_node is self.__root):
                        self.__root = cfnode(search_node.feature, None, [ search_node ], None);
                        search_node.parent = self.__root;
                        
                        # Update statistics
                        self.__amount_nodes += 1;
                        self.__height += 1;
                    
                    [new_node1, new_node2] = self.__split_leaf_node(search_node);        
                    
                    self.__leafes.remove(search_node);
                    self.__leafes.append(new_node1);
                    self.__leafes.append(new_node2);
                    
                    # Update parent list of successors
                    parent = search_node.parent;
                    parent.successors.remove(search_node);
                    parent.successors.append(new_node1);
                    parent.successors.append(new_node2);
                            
                    # Update statistics
                    self.__amount_nodes += 1;
                
                # Update statistics
                self.__amount_entries += 1;
    
    
    def __split_nonleaf_node(self, node):
        [farthest_node1, farthest_node2] = node.get_farthest_successors(self.__type_measurement);
        
        # create new non-leaf nodes
        new_node1 = cfnode(farthest_node1.feature, node.parent, [ farthest_node1 ], None);
        new_node2 = cfnode(farthest_node2.feature, node.parent, [ farthest_node2 ], None);
        
        farthest_node1.parent = new_node1;
        farthest_node2.parent = new_node2;
        
        # re-insert other successors
        for successor in node.successors:
            if ( (successor is not farthest_node1) and (successor is not farthest_node2) ):
                distance1 = new_node1.get_distance(successor, self.__type_measurement);
                distance2 = new_node2.get_distance(successor, self.__type_measurement);
                
                if (distance1 < distance2):
                    new_node1.append_successor(successor);
                else:
                    new_node2.append_successor(successor);
        
        return [new_node1, new_node2];
    
    
    def __split_leaf_node(self, node):
        # search farthest pair of entries
        [farthest_entity1, farthest_entity2] = node.get_farthest_entries(self.__type_measurement);
                    
        # create new nodes
        new_node1 = cfnode(farthest_entity1, node.parent, None, [ farthest_entity1 ]);
        new_node2 = cfnode(farthest_entity2, node.parent, None, [ farthest_entity2 ]);
        
        # re-insert other entries
        for entity in node.entries:
            if ( (entity is not farthest_entity1) and (entity is not farthest_entity2) ):
                distance1 = new_node1.get_distance(entity, self.__type_measurement);
                distance2 = new_node2.get_distance(entity, self.__type_measurement);
                
                if (distance1 < distance2):
                    new_node1.append_entity(entity);
                else:
                    new_node2.append_entity(entity);
        
        return [new_node1, new_node2];
    
    