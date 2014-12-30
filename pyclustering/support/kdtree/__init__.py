'''

Data Structure: KD-Tree

Based on book description:
 - M.Samet. The Design And Analysis Of Spatial Data Structures. 1994.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

import numpy;

from pyclustering.support import euclidean_distance_sqrt;

class node:
    def __init__(self, data = None, payload = None, left = None, right = None, disc = None, parent = None):
        "Constructor of node of KD Tree."
        
        "(in) data           - data point that is presented as list of coodinates."
        "(in) payload        - payload of node (pointer to essense that is attached to this node)."
        "(in) left           - pointer to the node of KD-Tree that is represented left successor."
        "(in) right          - pointer to the node of KD-Tree that is represented right successor."
        "(in) disc           - index of dimention of that node."
        "(in) parent         - pointer to the node of KD-Tree that is represented parent."
        
        self.data = data;
        self.payload = payload;
        self.left = left;
        self.right = right;
        self.disc = disc;
        self.parent = parent;
    
    def __repr__(self):
        #return 'Node (%s, %s)' % (self.data, hex(id(self.payload)));
        
        left = None; right = None; parent = None;
        if (self.left is not None):
            left = self.left.data;
            
        if (self.right is not None):
            right = self.right.data;
        
        return 'Node (%s, [%s %s])' % (self.data, left, right);
    
    def __str__(self):
        #return 'Node (%s, %s)' % (self.data, hex(id(self.payload)));
        return self.__repr__();


class kdtree:
    __root = None;
    __dimension = None;
    
    def __init__(self, data_list = None, payload_list = None):
        "Create kd-tree from list of points and from according list of payloads."
        "If lists were not specified then empty kd-tree will be created."
        
        "(in) data_list       - insert points from the list to created KD tree."
        "(in) payload_list    - insert payload from the list to created KD tree, length should be equal to length of data_list if it is specified."
        
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
        "Insert new point with payload to kd-tree."
        
        "(in) point      - coordinates of the point of inserted node."
        "(in) payload    - payload of inserted node."
        
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
        "Remove specified point from kd-tree."
        
        "(in) point      - coordinates of the point of removed node."
        
        "Return root if node has been successfully removed, otherwise None."
        
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
        "Delete node and return root of subtree."
        
        "(in) node    - pointer to the node that should be removed."
        
        "Return minimal node in line with coordinate that is defined by descriminator."
                
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
        "Return node minimal coordinate that is defined by discriminator."
        
        "(in) node            - node of KD tree from that search should be started."
        "(in) discriminator   - coordinate number that is used for comparison."
        
        "Return minimal node in line with descriminator from the specified node."
        
        assert node is not None;
        candidates = [self.find_minimal_node(child, discriminator) for child in self.children(node) if child is not None];
        candidates = candidates + [ node ];
        
        min_key = lambda cur_node: cur_node.data[discriminator];
        return min(candidates, key = min_key);    
    
    
    def find_node(self, point, cur_node = None):
        "Return node with coordinates that are defined by specified point."
        "If node does not exist then None will be returned."
        "Otherwise required node will be returned."
        
        "(in) point    - list of coordinates of the point whose node should be found."
        "(in) cure_node    - pointer to node of tree from that search should be started."
        
        "Return founded node in case of existance of node with specified coordinates, otherwise it return None."
        
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
        "Return nearest neighbor in area with radius = distance."
        
        "(in) point        - list of coordinates (point) for which searching is performed."
        "(in) distance     - maximum distance where neighbors are searched."
        "(in) retdistance  - if True - returns neighbors with distances to them, otherwise only neighbors is returned."
        
        "Return neighbors, of redistance is True then neighbors with distances to them will be returned."
        
        best_nodes = self.find_nearest_dist_nodes(point, distance);
            
        if (best_nodes == []): 
            return None;
        
        nearest = min(best_nodes, key = lambda item: item[0]);
        
        if (retdistance == True):
            return nearest;
        else:
            return nearest[1];
    
    
    def find_nearest_dist_nodes(self, point, distance):
        "Return list of neighbors such as tuple (distance, node) that is located in area that is covered by distance."
        
        "(in) point       - list of coordinates that is considered as centroind for searching."
        "(in) distance    - distance from the center where seaching is performed."
        
        "Return list of neighbors in area that is specified by point (center) and distance (radius)."
        
        best_nodes = [];
        self.__recursive_nearest_nodes(point, distance, distance ** 2, self.__root, best_nodes);
        
        return best_nodes;
    
    
    def __recursive_nearest_nodes(self, point, distance, sqrt_distance, node, best_nodes):
        "Return list of neighbors such as tuple (distance, node) that is located in area that is covered by distance."
        
        "(in) point           - list of coordinates that is considered as centroind for searching."
        "(in) distance        - distance from the center where seaching is performed."
        "(in) sqrt_distance   - square distance from the center where searching is performed."
        "(in) node            - node from that searching is performed."
        "(out) best_nodes     - list of founded nodes."
        
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
    
    
    # TODO: This method is not ready yet
    def find_nearest_node(self, point):
        "Search the nearest node of the given point"
        "Note: Does not work properly"
        cur_node = self.__root;
        
        best_node = None;
        best_distance = numpy.Inf;
        
        while True:
            # Check if it's best candidate and maybe it's owner of the coordinates.
            candidate_distance = euclidean_distance_sqrt(cur_node.data, point);
            if ((candidate_distance < best_distance) and (candidate_distance != 0)):
                best_node = cur_node;
                best_distance = candidate_distance;

            # Sort the children, nearer one first
            children = iter( sorted(self.children(cur_node), key = lambda node: euclidean_distance_sqrt(node.data[cur_node.disc], point[cur_node.disc])) );

            c1 = next(children, None);
            if c1:
                cur_node = c1;
                continue;

            c2 = next(children, None);
            if c2 and ( euclidean_distance_sqrt(cur_node.data[cur_node.disc], point[cur_node.disc]) < best_distance ):
                cur_node = c2;
                continue;

            return best_node;
    
    
    def children(self, node):
        "Return list of children of node."
        
        "(in) node    - node whose children are required."
        
        "Return list of children of node. If node haven't got any child then None is returned."
        
        if (node.left is not None):
            yield node.left;
        if (node.right is not None):
            yield node.right;
            
    
    def traverse(self, node = None, level = None):
        "Return all nodes of subtree that is defined by node specified in input parameter."
        
        "(in) node        - node from that travering of subtree is performed."
        "(in) level       - should be ignored by application."
        
        "Return all nodes of subtree."
        
        if (node is None):
            node  = self.__root;
            level = 0;
        
        if (node is None):
            return [];
        
        items = [ (level, node) ];        
        for child in self.children(node):
            if child is not None:
                items += self.traverse(child, level + 1);
        
        return items;
            
    
    def show(self):
        "Display tree on the console."
        
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
    