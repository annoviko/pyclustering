'''

Examples how to use OPTICS algorithm and clustering result demonstration.
Just run it for obtaining results.

'''

from clustering.optics import optics;

from support import read_sample, draw_clusters;

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

import matplotlib.pyplot as plt;

def template_clustering(path_sample, eps, minpts):
    sample = read_sample(path_sample);
    
    optics_instance = optics(sample, eps, minpts);
    optics_instance.process();
    
    clusters = optics_instance.get_clusters();
    noise = optics_instance.get_noise();
    
    draw_clusters(sample, clusters, [], '.');
    
    ordering = optics_instance.get_cluster_ordering();
    indexes = [i for i in range(0, len(ordering))];
    
    # visualization of cluster ordering in line with reachability distance.
    plt.bar(indexes, ordering);
    plt.show();
    
    
def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 3);
    
def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2.0, 3);
    
def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3);
    
def cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3);

def cluster_sample5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3);
    
def cluster_sample6():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, 1.0, 3);
 
def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 0.5, 3);
    
def cluster_lsun():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 0.5, 3);    
    
def cluster_target():
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 0.5, 2);    
    
def cluster_two_diamonds():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 0.15, 7);   
    
def cluster_wing_nut():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 0.25, 2);
    
def cluster_chainlink():
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 0.5, 3); 
    
def cluster_hepta():
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3); 
    
def cluster_golf_ball():
    template_clustering(FCPS_SAMPLES.SAMPLE_GOLF_BALL, 0.5, 3); 
    
def cluster_atom():
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, 15, 3); 

def cluster_tetra():
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 0.4, 3);
     
def cluster_engy_time():
    template_clustering(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 0.2, 20);    
    
    
cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_sample4();
cluster_sample5();
cluster_sample6();
cluster_elongate();
cluster_lsun();
cluster_target();
cluster_two_diamonds();
cluster_wing_nut();
cluster_chainlink();
cluster_hepta();
cluster_golf_ball();
cluster_atom();
cluster_tetra();
cluster_engy_time();