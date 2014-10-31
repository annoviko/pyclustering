from support import euclidean_distance;

class optics_descriptor:
    reachability_distance = None;
    core_distance = None;
    index_object = None;
    
    def __init__(self, index, core_distance = None, reachability_distance = None):
        self.index_object = index;
        self.core_distance = core_distance;
        self.reachability_distance = reachability_distance;
        
    def __repr__(self):
        return '(%s, [core: %s, reach: %s])' % (self.index_object, self.core_distance, self.reachability_distance);
    

def optics(sample, eps, minpts):
    processed = [False] * len(sample);
    optics_objects = [optics_descriptor(i) for i in range(len(sample))];
    ordered_database = [];
    
    for index_object in range(0, len(sample), 1):
        if (processed[index_object] is False):
            expand_cluster_order(sample, index_object, eps, minpts, optics_objects, processed, ordered_database);
    
    # print(optics_objects);
    
    clusters = extract_clusters(ordered_database, eps, minpts);
    return clusters;


def extract_clusters(ordered_database, eps, minpts):
    clusters = [];
    noise = [];
    
    current_cluster = [];
    for optics_object in ordered_database:
        if ((optics_object.reachability_distance is None) or (optics_object.reachability_distance > eps)):
            if ((optics_object.core_distance is not None) and (optics_object.core_distance <= eps)):
                if (len(current_cluster) > 0):
                    clusters.append(current_cluster);
                    current_cluster = [];
                    
                current_cluster.append(optics_object.index_object);
            else:
                noise.append(optics_object.index_object);
        else:
            current_cluster.append(optics_object.index_object);
    
    if (len(current_cluster) > 0):
        clusters.append(current_cluster);
        
    return clusters;    


def expand_cluster_order(data, index_object, eps, minpts, optics_objects, processed, ordered_database):
    processed[index_object] = True;
    
    neighbors_descriptor = neighbor_indexes(data, index_object, eps);
    optics_objects[index_object].reachability_distance = None;
    
    ordered_database.append(optics_objects[index_object]);
    
    # Check core distance
    if (len(neighbors_descriptor) >= minpts):
        neighbors_descriptor = sorted(neighbors_descriptor, key = lambda obj: obj[1]); # TODO: Find three smallest distances much faster than sorting
        optics_objects[index_object].core_distance = neighbors_descriptor[minpts - 1][1];
        
        # Continue processing
        order_seed = []; # sorted by their reachability-distance        
        update_order_seed(index_object, optics_objects, order_seed, neighbors_descriptor, processed);
        
        for optic_descriptor in order_seed:
            neighbors_descriptor = neighbor_indexes(data, optic_descriptor.index_object, eps);
            processed[optic_descriptor.index_object] = True;
            
            ordered_database.append(optic_descriptor);
            
            if (len(neighbors_descriptor) >= minpts):
                neighbors_descriptor = sorted(neighbors_descriptor, key = lambda obj: obj[1]); # TODO: Find three smallest distances much faster than sorting
                optic_descriptor.core_distance = neighbors_descriptor[minpts - 1][1];
                
                update_order_seed(optic_descriptor.index_object, optics_objects, order_seed, neighbors_descriptor, processed);
            else:
                optic_descriptor.core_distance = None;
                
    else:
        optics_objects[index_object].core_distance = None;


def update_order_seed(index_object, optics_objects, order_seed, neighbors_descriptor, processed):
    for neighbor_descriptor in neighbors_descriptor:
        index_neighbor = neighbor_descriptor[0];
        current_reachable_distance = neighbor_descriptor[1];
        
        if (processed[index_neighbor] != True):
            reachable_distance = max(current_reachable_distance, optics_objects[index_object].core_distance);
            if (optics_objects[index_neighbor].reachability_distance is None):
                optics_objects[index_neighbor].reachability_distance = reachable_distance;
                
                order_seed.append(optics_objects[index_neighbor]);
            else:
                if (reachable_distance < optics_objects[index_neighbor].reachability_distance):
                    optics_objects[index_neighbor].reachability_distance = reachable_distance;
                    
                    sorted(order_seed, key = lambda obj: obj.reachability_distance); # TODO: Rellocation is less complexity than sorting


def neighbor_indexes(data, index_object, eps):
    "Private function that is used by optics. Return list of indexes of neighbors of specified point for the data."
    
    "(in) data         - input data for clustering."
    "(in) index_object - index of point for which potential neighbors should be returned for the data in line with connectivity radius."
    "(in) eps          - connectivity radius between points, points may be connected if distance between them less then the radius."
    
    "Return list of lists with indexes of neighbors and distance to them [index, distance] in line the connectivity radius."
    
    neighbor_description = [];
    
    for index in range(0, len(data), 1):
        if (index == index_object):
            continue;
        
        distance = euclidean_distance(data[index_object], data[index]);
        if (distance <= eps):
            neighbor_description.append( [index, distance] );
        
    return neighbor_description;