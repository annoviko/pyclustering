from support import euclidean_distance;
from support import read_sample;
from support import draw_clusters;


def rock(data, eps, number_clusters, threshold = 0.5):
    "Clustering algorithm ROCK returns allocated clusters and noise that are consisted from input data."
    
    "(in) data                - input data - list of points where each point is represented by list of coordinates."
    "(in) eps                 - connectivity radius (similarity threshold), points are neighbors if distance between them is less than connectivity radius."
    "(in) number_clusters     - defines number of clusters that should be allocated from the input data set."
    "(in) threshold           - value that defines degree of normalization that influences on choice of clusters for merging during processing."
    
    "Returns list of allocated clusters, each cluster contains indexes of objects in list of data."
    
    # TODO: First iteration should be investigated. Euclidean distance should be used for clustering between two points and rock algorithm between clusters 
    # because we consider non-categorical samples. But it is required more investigations.
    degree_normalization = 1 + 2 * ( (1 - threshold) / (1 + threshold) );
    adjacency_matrix = create_adjacency_matrix(data, eps);
    clusters = [[index] for index in range(len(data))];
    
    while (len(clusters) > number_clusters):
        indexes = find_pair_clusters(clusters, adjacency_matrix, degree_normalization);
        clusters[indexes[0]] += clusters[indexes[1]];
        clusters.pop(indexes[1]);   # remove merged cluster.
    
    return clusters;


def find_pair_clusters(clusters, adjacency_matrix, degree_normalization):
    "Private function that is used by rock. Returns pair of clusters that are best candidates for merging in line with goodness measure."
    "The pair of clusters for which the above goodness measure is maximum is the best pair of clusters to be merged."
    
    "(in) clusters                 - list of cluster that have been allocated during processing, each cluster is represented by list of indexes of points from the input data set."
    "(in) adjacency_matrix         - adjacency matrix that represents distances between objects (points) from the input data set."
    "(in) degree_normalization     - degree of normalization that is used by goodness measurement for obtaining most suitable clusters for merging."
    
    "Returns list that contains two indexes of clusters (from list 'clusters') that should be merged on this step."
    
    maximum_goodness = 0;
    cluster_indexes = [-1, -1];
    
    for i in range(0, len(clusters)):
        for j in range(i + 1, len(clusters)):
            goodness = calculate_goodness(clusters[i], clusters[j], adjacency_matrix, degree_normalization);
            if (goodness > maximum_goodness):
                maximum_goodness = goodness;
                cluster_indexes = [i, j];
    
    return cluster_indexes;


def calculate_links(cluster1, cluster2, adjacency_matrix):
    "Private function that is used by calculate_goodness. Returns number of link between two clusters."
    "Link between objects (points) exists only if distance between them less than connectivity radius."
    
    "(in) cluster1                - cluster that is represented by list contains indexes of objects (points) from input data set."
    "(in) cluster2                - cluster that is represented by list contains indexes of objects (points) from input data set."
    "(in) adjacency_matrix        - adjacency matrix that represents distances between objects (points) from the input data set."
    
    "Returns number of links between two clusters."
    
    number_links = 0;
    
    for index1 in cluster1:
        for index2 in cluster2:
            number_links += adjacency_matrix[index1][index2];
            
    return number_links;
            

def create_adjacency_matrix(data, eps):
    "Private function that is used by rock. Returns 2D matrix (list of lists) where each element described existence of link between points (marks them as neighbors)."
    
    "(in) data                - input data - list of points where each point is represented by list of coordinates."
    "(in) eps                 - connectivity radius (similarity threshold), points are neighbors if distance between them is less than connectivity radius."
    
    "Returns adjacency matrix for the input data set in line with connectivity radius."
    
    size_data = len(data);
    
    adjacency_matrix = [ [ 0 for i in range(size_data) ] for j in range(size_data) ];
    for i in range(0, size_data):
        for j in range(i + 1, size_data):
            distance = euclidean_distance(data[i], data[j]);
            if (distance <= eps):
                adjacency_matrix[i][j] = 1;
                adjacency_matrix[j][i] = 1;
    
    return adjacency_matrix;
    

def calculate_goodness(cluster1, cluster2, adjacency_matrix, degree_normalization):
    "Private function that is used by find_pair_clusters. Calculates coefficient 'goodness measurement' between two clusters."
    "The coefficient defines level of suitability of clusters for merging."
    
    "(in) cluster1                - cluster that is represented by list contains indexes of objects (points) from input data set."
    "(in) cluster2                - cluster that is represented by list contains indexes of objects (points) from input data set."
    "(in) adjacency_matrix        - adjacency matrix that represents distances between objects (points) from the input data set."
    "(in) degree_normalization    - degree of normalization that is used by goodness measurement for obtaining most suitable clusters for merging."
    
    "Returns goodness measure between two clusters."
    
    number_links = calculate_links(cluster1, cluster2, adjacency_matrix);
    devider = (len(cluster1) + len(cluster2)) ** degree_normalization - len(cluster1) ** degree_normalization - len(cluster2) ** degree_normalization;
    
    return (number_links / devider);
