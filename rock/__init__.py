from support import euclidean_distance;
from support import read_sample;
from support import draw_clusters;


def rock(data, eps, number_clusters, threshold = 0.5):
    # TODO: First iteration should be fixed. Euclidean distance should be used for clustering between two points and rock algorithm between clusters 
    # because we consider non-categorical samples.
    degree_normalization = 1 + 2 * ( (1 - threshold) / (1 + threshold) );
    adjacency_matrix = create_adjacency_matrix(data, eps);
    clusters = [[index] for index in range(len(data))];
    
    while (len(clusters) > number_clusters):
        indexes = find_pair_clusters(clusters, adjacency_matrix, degree_normalization);
        clusters[indexes[0]] += clusters[indexes[1]];
        clusters.pop(indexes[1]);   # remove merged cluster.
    
    return clusters;


def find_pair_clusters(clusters, adjacency_matrix, degree_normalization):
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
    number_links = 0;
    
    for index1 in cluster1:
        for index2 in cluster2:
            number_links += adjacency_matrix[index1][index2];
            
    return number_links;
            

def create_adjacency_matrix(data, eps):
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
    number_links = calculate_links(cluster1, cluster2, adjacency_matrix);
    devider = (len(cluster1) + len(cluster2)) ** degree_normalization - len(cluster1) ** degree_normalization - len(cluster2) ** degree_normalization;
    
    return (number_links / devider);


# sample = read_sample('../samples/SampleTarget.txt');
# clusters = rock(sample, 1.2, 6, 0.2);
# #print("Total time: ", ticks);
# draw_clusters(sample, clusters);