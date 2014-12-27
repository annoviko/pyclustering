from clustering.birch import birch;

from support.cftree import measurement_type;

from support import read_sample;
from support import draw_clusters;
from support import timedcall;

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

def template_clustering(number_clusters, path, branching_factor = 5, max_node_entries = 5, initial_diameter = 0.5, type_measurement = measurement_type.CENTROID_EUCLIDIAN_DISTANCE, entry_size_limit = 200, ccore = True):
    sample = read_sample(path);
    
    birch_instance = birch(sample, number_clusters, branching_factor, max_node_entries, initial_diameter, type_measurement, entry_size_limit, ccore)
    (ticks, result) = timedcall(birch_instance.process);
    
    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");
    
    clusters = birch_instance.get_clusters();
    draw_clusters(sample, clusters);
    
    
def cluster_sample1():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 5, 0.1, measurement_type.CENTROID_EUCLIDIAN_DISTANCE, 2);      # only two entries available

def cluster_sample2():
    template_clustering(3, SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
    
def cluster_sample3():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
    
def cluster_sample4():
    # template_clustering(5, SIMPLE_SAMPLES.SAMPLE_SIMPLE4);
    template_clustering(5, SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 100, 1, 0, measurement_type.CENTROID_EUCLIDIAN_DISTANCE, 200);
    
def cluster_sample5():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE5);
    
def cluster_elongate():
    # something like typical k-means algorithm
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_ELONGATE);
    
    # almost good, but two points are clustered in wrong way
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_ELONGATE, 10, 10, 0.5, measurement_type.VARIANCE_INCREASE_DISTANCE, 20);

def cluster_lsun():
    # almost good result, but not best
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN, 10, 10, 0.2, measurement_type.CENTROID_EUCLIDIAN_DISTANCE, 75);
    
    # no encoding - worth result, like hierarchical with centroids
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN, 5, 5, 0.1, measurement_type.CENTROID_EUCLIDIAN_DISTANCE, 400);
    
def cluster_target():
    #template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET);
    
    template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET, 5, 5, 0.1, measurement_type.VARIANCE_INCREASE_DISTANCE, 200);

def cluster_two_diamonds():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS);  

def cluster_wing_nut():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT); 
    
def cluster_chainlink():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_CHAINLINK);     
    
def cluster_hepta():
    template_clustering(7, FCPS_SAMPLES.SAMPLE_HEPTA); 
    
def cluster_tetra():
    template_clustering(4, FCPS_SAMPLES.SAMPLE_TETRA);    
    
def cluster_engy_time():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_ENGY_TIME); 
    
    
cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_sample4();
cluster_sample5();
cluster_elongate();
cluster_lsun();
cluster_target();
cluster_two_diamonds();
cluster_wing_nut();
cluster_chainlink();
cluster_hepta();
cluster_tetra();
cluster_engy_time();
