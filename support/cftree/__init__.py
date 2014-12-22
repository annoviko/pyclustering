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
        return 'CF (N: %s, LS: %s, SS: %s)' % (self.number_points, self.__linear_sum, self.__square_sum);    
    
    
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
            print("diameter_part:", diameter_part);
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
    
    def __init__(self, feature, parent, successors, entities):
        self.feature = copy(feature);
        self.successors = successors;   # pointers to CF nodes
        self.parent = parent;
        
        self.entities = entities;       # pointer to entities (clustering features) - used only in case of leaf
    
    
    def __repr__(self):
        return 'Node (%s, %s, [%s, %s])' % (self.feature, len(self.successors));


    def __str__(self):
        return self.__repr__();
    
    
    def append_entity(self, entity):
        self.feature = self.feature.merge(entity);
        self.entities.append(entity);
    
    
    def append_successor(self, successor):
        self.feature = self.feature.merge(successor.feature);
        self.successors.append(successor);
    
    
    def get_distance(self, node, type_measurement):
        if (type(node) == cfnode):
            return self.feature.get_distance(node.feature, type_measurement);
        elif (type(node) == cfentry):
            return self.feature.get_distance(node, type_measurement);
        else:
            assert 0;

    
    def get_farthest_entities(self):
        farthest_entity1 = None;
        farthest_entity2 = None;
        farthest_distance = float("Inf");
        
        for i in range(0, len(self.entities)):
            candidate1 = self.entities[i];
            
            for j in range(i, len(self.entities)):
                candidate2 = self.entities[j];
                candidate_distance = candidate1.get_distance(candidate2, self.__type_measurement);
                
                if (candidate_distance < farthest_distance):
                    farthest_distance = candidate_distance;
                    farthest_entity1 = candidate1;
                    farthest_entity2 = candidate2;        
        
        return [farthest_entity1, farthest_entity2];
    
    
    def get_farthest_nodes(self, essences):
        farthest_node1 = None;
        farthest_node2 = None;
        farthest_distance = float("Inf");
        
        for i in range(0, len(self.successors)):
            candidate1 = self.successors[i];
            
            for j in range(i, len(self.successors)):
                candidate2 = self.successors[j];
                candidate_distance = candidate1.get_distance(candidate2, self.__type_measurement);
                
                if (candidate_distance < farthest_distance):
                    farthest_distance = candidate_distance;
                    farthest_node1 = candidate1;
                    farthest_node2 = candidate2;        
        
        return [farthest_node1, farthest_node2];
    
    
    def get_nearest_entity(self, entity): 
        min_key = lambda cur_entity: cur_entity.get_distance(entity, self.__type_measurement);
        return min(self.entities, key = min_key);



class cftree:
    __root = None;
    __leafes = None;
    
    __branch_factor = 0;
    __threshold = 0.0;
    __max_entities = None;
    
    __type_measurement = None;
    
    
    def __init__(self, branch_factor, threshold, max_entities, type_measurement = measurement_type.CENTROID_EUCLIDIAN_DISTANCE):
        self.__branch_factor = branch_factor; # maximum number of children
        self.__threshold = threshold;         # maximum diameter of sub-clusters stored at the leaf nodes
        self.__max_entities = max_entities;
        
        self.__leafes = [];
        
        self.__type_measurement = type_measurement;
    
    
    def insert(self, cluster):
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster));
        node = cfnode(copy(entry), None, None, None);
        
        if (self.__root is None):
            self.__root = cfnode(copy(entry), None, [ node ], None);
            
            node.parent = self.__root;
            node.entries = [ copy(node.feature) ];
            
            self.__leafes.append(node);
        else:
            self.__recursive_insert(node, self.__root);
    
    
    def find_nearest_leaf(self, node, search_node = None):
        nearest_node = self.__root;
        
        if (search_node is not None):
            nearest_node = search_node;
        
        if (search_node.successors is not None):
            min_key = lambda child_node: child_node.get_distance(node, self.__type_measurement);
            nearest_child_node = min(node.successors, key = min_key);
            
            nearest_node = self.__find_nearest_leaf(node, nearest_child_node);
        
        return nearest_node;
    
    
    def __recursive_insert(self, new_node, search_node):
        # None-leaf node
        if (search_node.successors is not None):
            min_key = lambda child_node: child_node.get_distance(search_node, self.__type_measurement);
            nearest_child_node = min(search_node.successors, key = min_key);
            
            self.__recursive_insert(new_node, nearest_child_node);
            
            # Update clustering feature of none-leaf node.
            search_node.feature.merge(new_node.feature);
                
            # Check branch factor, probably some leaf has been splitted and threshold has been exceeded.
            if (len(search_node.successors) > self.__branch_factor):
                
                # Check if it's aleady root then new root should be created (height is increased in this case).
                if (search_node is self.__root):
                    self.__root = cfnode(copy(search_node.feature), None, [ search_node ], None);
                    search_node.parent = self.__root;
                    
                [new_node1, new_node2] = self.__split_nonleaf_node(self, search_node);
                
                # Update parent list of successors
                parent = search_node.parent;
                parent.successors.remove(search_node);
                parent.successors.append(new_node1);
                parent.successors.append(new_node2);
        
        # Leaf is reached 
        else:
            # Try to absorb by the entity
            search_entity = search_node.get_nearest_entity();
            merged_entity = search_entity.merge(new_node.feature, self.__threshold);
            
            # Otherwise try to add new entry
            if (merged_entity is None):
                # If it's not exceeded append entity and update feature of the leaf node.
                if (len(search_node.successors) < self.__max_entities):
                    search_node.append_entity(new_node.feature);
                
                # otherwise current node should be splitted
                else:
                    [new_node1, new_node2] = self.__split_leaf_node(search_node);        
                    
                    self.__leafes.append(new_node1);
                    self.__leafes.append(new_node2);
                    
                    # Update parent list of successors
                    parent = search_node.parent;
                    if (parent is not None):
                        if (parent is not self.__root):
                            parent.successors.remove(search_node);
                            parent.successors.append(new_node1);
                            parent.successors.append(new_node2);
    
    
    def __split_nonleaf_node(self, node):
        [farthest_node1, farthest_node2] = node.get_farthest_nodes();
        
        # create new non-leaf nodes
        new_node1 = cfnode(farthest_node1.feature, node.parent, [ farthest_node1 ], None);
        new_node2 = cfnode(farthest_node2.feature, node.parent, [ farthest_node2 ], None);
                    
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
        # search farthest pair of entities
        [farthest_entity1, farthest_entity2] = node.get_farthest_entities();
                    
        # create new nodes
        new_node1 = cfnode(farthest_entity1, node.parent, None, [ farthest_entity1 ]);
        new_node2 = cfnode(farthest_entity2, node.parent, None, [ farthest_entity2 ]);
        
        # re-insert other entities
        for entity in node.entities:
            if ( (entity is not farthest_entity1) and (entity is not farthest_entity2) ):
                distance1 = new_node1.get_distance(entity, self.__type_measurement);
                distance2 = new_node2.get_distance(entity, self.__type_measurement);
                
                if (distance1 < distance2):
                    new_node1.append_entity(entity);
                else:
                    new_node2.append_entity(entity);
        
        return [new_node1, new_node2];

    
    