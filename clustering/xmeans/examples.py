from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from clustering.xmeans import xmeans;

from support import draw_clusters, read_sample, timedcall;

def template_clustering(start_centers, path, tolerance = 0.25, ccore = True):
    sample = read_sample(path);
    
    (ticks, clusters) = timedcall(xmeans, sample, start_centers);
    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");

    draw_clusters(sample, clusters);
    

def cluster_sample1():
    "Start with wrong number of clusters."
    start_centers = [[3.7, 5.5]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
    
def cluster_sample2():
    "Start with wrong number of clusters."
    start_centers = [[3.5, 4.8], [2.6, 2.5]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
    
def cluster_sample3():
    "Start with wrong number of clusters."
    start_centers = [[0.2, 0.1], [4.0, 1.0]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
    
def cluster_sample4():
    "Start with right number of clusters."
    start_centers = [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE4);    
    
def cluster_sample5():
    "Start with wrong number of clusters."
    start_centers = [[0.0, 1.0], [0.0, 0.0]];
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE5);   
    
cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_sample4();
cluster_sample5();