from hierarchical import hierarchical

from support import read_sample;
from support import draw_clusters;
from support import timedcall;

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

def template_clustering(number_clusters, path):
    sample = read_sample(path);
    
    (ticks, clusters) = timedcall(hierarchical, sample, number_clusters);
    print("Execution time: ", ticks);
    
    draw_clusters(sample, clusters);
    
def cluster_sample1():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
    
def cluster_sample2():
    template_clustering(3, SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
    
def cluster_sample3():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
    
def cluster_sample4():
    template_clustering(5, SIMPLE_SAMPLES.SAMPLE_SIMPLE4);
    
def cluster_sample5():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE5);    
    
def cluster_elongate():
    "NOTE: Not applicable for this sample"
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_ELONGATE);

def cluster_lsun():
    "NOTE: Not applicable for this sample"
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN);  
    
def cluster_target():
    "NOTE: Not applicable for this sample"
    template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET);     

def cluster_two_diamonds():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS);  

def cluster_wing_nut():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT); 
    
def cluster_chainlink():
    "NOTE: Not applicable for this sample"
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
