from support import euclidean_distance;

class optics_descriptor:
    reachability_distance = None;
    core_distance = None;
    

def optics(sample, eps, minpts):
    processed = [False] * len(sample);
    optics_objects = [optics_descriptor()] * len(sample);
    clusters = [];
    
    for index_object in range(0, len(sample), 1):
        if (processed[index_object] is False):
            expand_cluster_order(sample, index_object, eps, minpts, optics_objects, processed);
    
    return clusters;


def expand_cluster_order(data, index_object, eps, minpts, optics_objects, processed):
    processed[index_object] = True;
    
    neighbors_descriptor = neighbor_indexes(data, index_object, eps);
    optics_objects[index_object].reachability_distance = None;
    
    # Check core distance
    if (len(neighbors_descriptor) >= minpts):
        optics_objects[index_object].core_distance = min(neighbors_descriptor, key = lambda obj: obj[1]);
        
        # Continue processing        
    else:
        optics_objects[index_object].core_distance = None;


def neighbor_indexes(data, index_object, eps):
    "Private function that is used by optics. Return list of indexes of neighbors of specified point for the data."
    
    "(in) data         - input data for clustering."
    "(in) index_object - index of point for which potential neighbors should be returned for the data in line with connectivity radius."
    "(in) eps          - connectivity radius between points, points may be connected if distance between them less then the radius."
    
    "Return list of tuples with indexes of neighbors and distance to them (index, distance) in line the connectivity radius."
    
    neighbor_description = [];
    
    for index in range(0, len(data), 1):
        if (index == index_object):
            continue;
        
        distance = euclidean_distance(data[index_object], data[index]);
        if (distance <= eps):
            neighbor_description.append((index, distance));
        
    return neighbor_description;