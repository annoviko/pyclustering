from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from kmeans import kmeans, draw_clusters
from support import read_sample;
from support import timedcall;

def template_clustering(start_centers, path):
    sample = read_sample(path);
    
    (ticks, (clusters, centers)) = timedcall(kmeans, sample, start_centers);
    print("Execution time: ", ticks);

    draw_clusters(sample, clusters, centers, start_centers);
    
def cluster_sample1():
    start_centers = [[3.7, 5.5], [6.7, 7.5]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
    
def cluster_sample2():
    start_centers = [[3.5, 4.8], [6.9, 7], [7.5, 0.5]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
    
def cluster_sample3():
    start_centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
    
def cluster_sample4():
    start_centers = [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE4);    
    
def cluster_sample5():
    start_centers = [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE5);    
        
def cluster_elongate():
    "Not so applicable for this sample"
    start_centers = [[1.0, 4.5], [3.1, 2.7]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_ELONGATE);

def cluster_lsun():
    "Not so applicable for this sample"
    start_centers = [[1.0, 3.5], [2.0, 0.5], [3.0, 3.0]];
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_LSUN);  
    
def cluster_target():
    "Not so applicable for this sample"
    start_centers = [[0.2, 0.2], [0.0, -2.0], [3.0, -3.0], [3.0, 3.0], [-3.0, 3.0], [-3.0, -3.0]];
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TARGET);     

def cluster_two_diamonds():
    start_centers = [[0.8, 0.2], [3.0, 0.0]];
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS);  

def cluster_wing_nut():
    "Almost good!"
    start_centers = [[-1.5, 1.5], [1.5, 1.5]];
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_WING_NUT); 
    
def cluster_chainlink():
    start_centers = [[1.1, -1.7, 1.1], [-1.4, 2.5, -1.2]];
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_CHAINLINK);     
    
def cluster_hepta():
    start_centers = [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [-2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, -3.0, 0.0], [0.0, 0.0, 2.5], [0.0, 0.0, -2.5]];
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_HEPTA); 
    
def cluster_tetra():
    start_centers = [[1, 0, 0], [0, 1, 0], [0, -1, 0], [-1, 0, 0]];
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TETRA);    
    
def cluster_engy_time():
    start_centers = [[0.5, 0.5], [2.3, 2.9]];
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_ENGY_TIME);
    
    
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