'''

Data Structure: CF-Tree

Based on book description:
 - M.Zhang, R.Ramakrishnan, M.Livny. BIRCH: An Efficient Data Clustering Method for Very Large Databases. 1996.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from copy import copy;

from support import euclidean_distance, euclidean_distance_sqrt;
from support import manhattan_distance;
from support import list_math_addition, list_math_subtraction, list_math_multiplication,list_math_division_number;
from support import linear_sum, square_sum;


class measurement_type:
    CENTROID_EUCLIDIAN_DISTANCE     = 0;
    CENTROID_MANHATTAN_DISTANCE     = 1;
    AVERAGE_INTER_CLUSTER_DISTANCE  = 2;
    AVERAGE_INTRA_CLUSTER_DISTANCE  = 3;
    VARIANCE_INCREASE_DISTANCE      = 4;
    

class cfnode_type:
    CFNODE_DUMMY    = 0;
    CFNODE_LEAF     = 1;
    CFNODE_NONLEAF  = 2;
    

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
        return 'CF (%s, %s, %0.2f) [%s]' % ( self.number_points, self.linear_sum, self.__square_sum, hex(id(self)) );    
    
    
    def __str__(self):
        return self.__repr__();
    
    
    def __add__(self, entry):
        "Overloaded operator add. Performs addition of two clustering features."
        
        "(in) entry    - entry that is added to the current."
        
        "Returns result of addition of two clustering features."
        
        number_points = self.number_points + entry.number_points;
        linear_sum = list_math_addition(self.linear_sum, entry.linear_sum);        
        square_sum = self.square_sum + entry.square_sum;  
        
        return cfentry(number_points, linear_sum, square_sum);
    
    
    def __sub__(self, entry):
        "Overloaded operator sub. Performs substraction of two clustering features."
        "Substraction can't be performed with clustering feature whose description is less then substractor."
        
        "(in) entry    - entry that is substracted from the current."
        
        "Returns result of substraction of two clustering features."
                
        number_points = self.number_points - entry.number_points;
        linear_sum = list_math_subtraction(self.linear_sum, entry.linear_sum);        
        square_sum = self.square_sum - entry.square_sum;
        
        if ( (number_points < 0) or (square_sum < 0) ):
            raise NameError("Substruction with negative result is not possible for clustering features.");
        
        return cfentry(number_points, linear_sum, square_sum);        
    
    
    def __eq__(self, entry):
        "Overloaded operator eq. Performs comparison of two clustering features."
        
        "(in) entry    - entry that is used for comparison with current."
        
        "Returns True is both clustering features are equals in line with tolerance, otherwise False."
                
        tolerance = 0.00001;
        
        result = (self.number_points == entry.number_points);
        result &= ( (self.square_sum + tolerance > entry.square_sum) and (self.square_sum - tolerance < entry.square_sum) );
        
        for index_dimension in range(0, len(self.linear_sum)):
            result &= ( (self.linear_sum[index_dimension] + tolerance > entry.linear_sum[index_dimension]) and (self.linear_sum[index_dimension] - tolerance < entry.linear_sum[index_dimension]) );
        
        return result;
    
    
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
        
        self.__centroid = [0] * len(self.linear_sum);
        for index_dimension in range(0, len(self.linear_sum)):
            self.__centroid[index_dimension] = self.linear_sum[index_dimension] / self.number_points;
        
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
    parent      = None;     # pointer to parent node (None for root)
    type        = None;     # type node
    
    def __init__(self, feature, parent, type = cfnode_type.CFNODE_DUMMY):
        self.feature = copy(feature);
        self.parent = parent;
        self.type = type;
        
    
    def __repr__(self):
        parent = None;
        if (self.parent is not None):
            parent = hex(id(self.parent));
            
        return 'CF node %s, parent %s' % ( hex(id(self)), parent );


    def __str__(self):
        return self.__repr__();
    
    
    def get_distance(self, node, type_measurement):
        "Returns distance between nodes in line with specified type measurement."
        
        "(in) node                - cf node that is used for calculation distance to the current node."
        "(in) type_measurement    - measurement type that is used for calculation distance."
        
        "Return distance between two nodes."
        
        return self.feature.get_distance(node.feature, type_measurement);
    

class non_leaf_node(cfnode):    
    "Representation of clustering feature non-leaf node."
    
    __successors = None;
    
    @property
    def successors(self):
        return self.__successors;
    
    
    def __init__(self, feature, parent, successors):
        "Create CF Non-leaf node."
        
        "(in) feature    - clustering feature of the created node."
        "(in) parent     - parent of the created node."
        "(in) successors - list of successors of the node."
                
        super().__init__(feature, parent, cfnode_type.CFNODE_NONLEAF);
        
        self.__successors = successors;
    
    
    def insert_successor(self, successor):
        "Insert successor to the node."
        
        "(in) successor    - pointer to the successor."
        
        self.feature += successor.feature;
        self.successors.append(successor);
        
        successor.parent = self;
    
    
    def remove_successor(self, successor):
        "Remove successor from the node."
        
        "(in) successor    - pointer to the successor."
        
        self.feature -= successor.feature;
        self.successors.append(successor);
        
        successor.parent = self;
    
    
    def merge(self, node):
        "Merge non-leaf node to the current."
        
        "(in) node    - pointer to non-leaf node that should be merged with current."
                
        self.feature += node.feature;
        
        for child in node.successors:
            child.parent = self;      
    
    
    def get_farthest_successors(self, type_measurement):
        "Return pair of farthest successors of the node in line with measurement type."
        
        "(in) type_measurement    - measurement type that is used for obtaining farthest successors."
        
        "Return pair of farthest successors represented by list."
        
        farthest_node1 = None;
        farthest_node2 = None;
        farthest_distance = 0;
        
        for i in range(0, len(self.successors)):
            candidate1 = self.successors[i];
            
            for j in range(i + 1, len(self.successors)):
                candidate2 = self.successors[j];
                candidate_distance = candidate1.get_distance(candidate2, type_measurement);
                
                if (candidate_distance > farthest_distance):
                    farthest_distance = candidate_distance;
                    farthest_node1 = candidate1;
                    farthest_node2 = candidate2;        
        
                    return [farthest_node1, farthest_node2];
    
    
    def get_nearest_successors(self, type_measurement):
        "Return pair of nearest successors of the node in line with measurement type."
        
        "(in) type_measurement    - measurement type that is used for obtaining nearest successors."
        
        "Return pair of nearest successors represented by list."
                
        nearest_node1 = None;
        nearest_node2 = None;
        nearest_distance = float("Inf");
        
        for i in range(0, len(self.successors)):
            candidate1 = self.successors[i];
            
            for j in range(i + 1, len(self.successors)):
                candidate2 = self.successors[j];
                candidate_distance = candidate1.get_distance(candidate2, type_measurement);
                
                if (candidate_distance < nearest_distance):
                    nearest_distance = candidate_distance;
                    nearest_node1 = candidate1;
                    nearest_node2 = candidate2;        
        
        return [nearest_node1, nearest_node2];    


class leaf_node(cfnode):
    "Representation of clustering feature leaf node."
    
    __entries = None;   # list of clustering features
    
    @property
    def entries(self):
        return self.__entries;
    
    
    def __init__(self, feature, parent, entries):
        "Create CF Leaf node."
        
        "(in) feature    - clustering feature of the created node."
        "(in) parent     - parent of the created node."
        "(in) entries    - list of entries of the node."
        
        super().__init__(feature, parent, cfnode_type.CFNODE_LEAF);
        
        self.__entries = entries;
    
    
    def insert_entry(self, entry):  
        "Insert new clustering feature to the leaf node."
        
        "(in) entry    - pointer to the clustering feature."
                              
        self.feature += entry;
        self.entries.append(entry);
        
    
    def remove_entry(self, entry):
        "Remove clustering feature from the leaf node."
        
        "(in) entry    - pointer to the clustering feature."
                
        self.feature -= entry;
        self.entries.remove(entry);
    
    
    def merge(self, node):
        "Merge leaf node to the current."
        
        "(in) node    - pointer to leaf node that should be merged with current."
        
        self.feature += node.feature;
        
        # Move entries from merged node
        for entry in node.entries:
            self.entries.append(entry);
            
    
    def get_farthest_entries(self, type_measurement):
        "Return pair of farthest entries of the node."
        
        "(in) type_measurement    - measurement type that is used for obtaining farthest entries."
        
        "Return pair of farthest entries of the node that are represented by list."
        
        farthest_entity1 = None;
        farthest_entity2 = None;
        farthest_distance = 0;
        
        for i in range(0, len(self.entries)):
            candidate1 = self.entries[i];
            
            for j in range(i + 1, len(self.entries)):
                candidate2 = self.entries[j];
                candidate_distance = candidate1.get_distance(candidate2, type_measurement);
                
                if (candidate_distance > farthest_distance):
                    farthest_distance = candidate_distance;
                    farthest_entity1 = candidate1;
                    farthest_entity2 = candidate2;        
        
        return [farthest_entity1, farthest_entity2];
    
    
    def get_nearest_index_entry(self, entry, type_measurement):
        "Return index of nearest entry of node for the specified entry."
        
        "(in) entry               - entry that is used for calculation distance."
        "(in) type_measurement    - measurement type that is used for obtaining nearest entry to the specified."
        
        "Return index of nearest entry of node for the specified entry."  
        
        minimum_distance = float('Inf');
        nearest_index = 0;
        
        for candidate_index in range(0, len(self.entries)):
            candidate_distance = self.entries[candidate_index].get_distance(entry, type_measurement)    ;
            if (candidate_distance < minimum_distance):
                nearest_index = candidate_index;
                
        return candidate_index;
    
    
    def get_nearest_entry(self, entry, type_measurement):
        "Return nearest entry of node for the specified entry."
        
        "(in) entry               - entry that is used for calculation distance."
        "(in) type_measurement    - measurement type that is used for obtaining nearest entry to the specified."
        
        "Return nearest entry of node for the specified entry."
        
        min_key = lambda cur_entity: cur_entity.get_distance(entry, type_measurement);
        return min(self.__entries, key = min_key);


class cftree:
    "CF-Tree representation."
    
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
        "Create CF-tree."
        
        "(in) branch_factor        - maximum number of children for non-leaf nodes."
        "(in) max_entries          - maximum number of entries for leaf nodes."
        "(in) threshold            - maximum diameter of feature clustering for each leaf node."
        "(in) type_measurement     - measurement type that is used for calculation distance metrics."
        
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
    
    
    def insert_cluster(self, cluster):
        "Insert cluster that is represented as list of points where each point is represented by list of coordinates."
        "Clustering feature is created for that cluster and inserted to the tree."
        
        "(in) cluster    - cluster that is represented by list of points that should be inserted to the tree."
        
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster));
        self.insert(entry);
        
        
    def insert(self, entry):
        "Insert clustering feature to the tree."
        
        "(in) entry    - clustering feature that should be inserted."
                
        if (self.__root is None):
            node = leaf_node(entry, None, [ entry ]);
            
            self.__root = node;            
            self.__leafes.append(node);
            
            # Update statistics
            self.__amount_entries += 1;
            self.__amount_nodes += 1;       
            self.__height += 1;             # root has successor now
        else:
            child_node_updation = self.__recursive_insert(entry, self.__root);
            if (child_node_updation is True):
                # Splitting has been finished, check for possibility to merge (at least we have already two children).
                if (self.__merge_nearest_successors(self.__root) is True):
                    self.__amount_nodes -= 1;
    
    
    def find_nearest_leaf(self, entry, search_node = None):
        "Search nearest leaf to the specified clustering feature."
        
        "(in) entry          - pointer to clustering feature."
        "(in) search_node    - node from that searching should be started."
        
        "Return nearest node to the specified clustering feature."
        
        if (search_node is None):
            search_node = self.__root;
        
        nearest_node = search_node;
        
        if (search_node.type == cfnode_type.CFNODE_NONLEAF):
            min_key = lambda child_node: child_node.feature.get_distance(entry, self.__type_measurement);
            nearest_child_node = min(search_node.successors, key = min_key);
            
            nearest_node = self.find_nearest_leaf(entry, nearest_child_node);
        
        return nearest_node;
    
    
    def __recursive_insert(self, entry, search_node):
        "Recursive insert of the entry to the tree. It performs all required procedures during insertion such as splitting, merging."
        
        "(in) entry          - pointer to clustering feature."
        "(in) search_node    - node from that insertion should be started."
        
        "Return True is number of nodes at the below level is changed, otherwise False."
        
        node_amount_updation = False;
        
        # None-leaf node
        if (search_node.type == cfnode_type.CFNODE_NONLEAF):
            min_key = lambda child_node: child_node.get_distance(search_node, self.__type_measurement);
            nearest_child_node = min(search_node.successors, key = min_key);
            
            child_node_updation = self.__recursive_insert(entry, nearest_child_node);
            
            # Update clustering feature of none-leaf node.
            search_node.feature += entry;
                
            # Check branch factor, probably some leaf has been splitted and threshold has been exceeded.
            if (len(search_node.successors) > self.__branch_factor):
                
                # Check if it's aleady root then new root should be created (height is increased in this case).
                if (search_node is self.__root):
                    self.__root = non_leaf_node(search_node.feature, None, [ search_node ]);
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
                node_amount_updation = True;
                
            elif (child_node_updation is True):
                # Splitting has been finished, check for possibility to merge (at least we have already two children).
                if (self.__merge_nearest_successors(search_node) is True):
                    self.__amount_nodes -= 1;
        
        # Leaf is reached 
        else:
            # Try to absorb by the entity
            index_nearest_entry= search_node.get_nearest_index_entry(entry, self.__type_measurement);
            merged_entry = search_node.entries[index_nearest_entry] + entry;
            
            # Otherwise try to add new entry
            if (merged_entry.get_diameter() > self.__threshold):
                # If it's not exceeded append entity and update feature of the leaf node.
                search_node.insert_entry(entry);
                
                # Otherwise current node should be splitted
                if (len(search_node.entries) > self.__max_entries):
                    if (search_node is self.__root):
                        self.__root = non_leaf_node(search_node.feature, None, [ search_node ]);
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
                    node_amount_updation = True;
                
                # Update statistics
                self.__amount_entries += 1;
                
            else:
                search_node.entries[index_nearest_entry] = merged_entry;
                search_node.feature = copy(merged_entry);
                
        return node_amount_updation;
    
    
    def __merge_nearest_successors(self, node):
        "Find pair of nearest successors and try to merge taking into account branch factor."
        
        "(in) node    - node whose two nearest successors should be merged."
        
        "Return True if merging has been successfully performed, otherwise False."
        
        merging_result = False;
        
        if (len(node.successors) < self.__branch_factor):
            [nearest_child_node1, nearest_child_node2] = node.get_nearest_successors(self.__type_measurement);
                    
            node.successors.remove(nearest_child_node2);
            nearest_child_node1.merge(nearest_child_node2);
            
            merging_result = True;
        
        return merging_result;
            
    
    def __split_nonleaf_node(self, node):
        "Performs splitting of the specified non-leaf node."
        
        "(in) node    - non-leaf node that should be splitted."
        
        "Return new pair of non-leaf nodes."
        
        [farthest_node1, farthest_node2] = node.get_farthest_successors(self.__type_measurement);
        
        # create new non-leaf nodes
        new_node1 = non_leaf_node(farthest_node1.feature, node.parent, [ farthest_node1 ]);
        new_node2 = non_leaf_node(farthest_node2.feature, node.parent, [ farthest_node2 ]);
        
        farthest_node1.parent = new_node1;
        farthest_node2.parent = new_node2;
        
        # re-insert other successors
        for successor in node.successors:
            if ( (successor is not farthest_node1) and (successor is not farthest_node2) ):
                distance1 = new_node1.get_distance(successor, self.__type_measurement);
                distance2 = new_node2.get_distance(successor, self.__type_measurement);
                
                if (distance1 < distance2):
                    new_node1.insert_successor(successor);
                else:
                    new_node2.insert_successor(successor);
        
        return [new_node1, new_node2];
    
    
    def __split_leaf_node(self, node):
        "Performs splitting of the specified leaf node."
        
        "(in) node    - leaf node that should be splitted."
        
        "Return new pair of leaf nodes."
        
        # search farthest pair of entries
        [farthest_entity1, farthest_entity2] = node.get_farthest_entries(self.__type_measurement);
                    
        # create new nodes
        new_node1 = leaf_node(farthest_entity1, node.parent, [ farthest_entity1 ]);
        new_node2 = leaf_node(farthest_entity2, node.parent, [ farthest_entity2 ]);
        
        # re-insert other entries
        for entity in node.entries:
            if ( (entity is not farthest_entity1) and (entity is not farthest_entity2) ):
                distance1 = new_node1.feature.get_distance(entity, self.__type_measurement);
                distance2 = new_node2.feature.get_distance(entity, self.__type_measurement);
                
                if (distance1 < distance2):
                    new_node1.insert_entry(entity);
                else:
                    new_node2.insert_entry(entity);
        
        return [new_node1, new_node2];
    
    