from hierarchical import hierarchical
from support import read_sample;
from support import draw_clusters;
from support import timedcall;

def template_clustering(number_clusters, path):
    sample = read_sample(path);
    
    (ticks, clusters) = timedcall(hierarchical, sample, number_clusters);
    print("Execution time: ", ticks);
    
    draw_clusters(sample, clusters);
    
def cluster_sample1():
    template_clustering(2, '../Samples/SampleSimple1.txt');
    
def cluster_sample2():
    template_clustering(3, '../Samples/SampleSimple2.txt');
    
def cluster_sample3():
    template_clustering(4, '../Samples/SampleSimple3.txt');
    
def cluster_elongate():
    "Not so applicable for this sample"
    template_clustering(2, '../Samples/SampleElongate.txt');

def cluster_lsun():
    "Not so applicable for this sample"
    template_clustering(3, '../Samples/SampleLsun.txt');  
    
def cluster_target():
    "Not so applicable for this sample"
    template_clustering(6, '../Samples/SampleTarget.txt');     

def cluster_two_diamonds():
    template_clustering(2, '../Samples/SampleTwoDiamonds.txt');  

def cluster_wing_nut():
    "Almost good!"
    template_clustering(2, '../Samples/SampleWingNut.txt'); 
    
def cluster_chainlink():
    template_clustering(2, '../Samples/SampleChainlink.txt');     
    
def cluster_hepta():
    template_clustering(7, '../Samples/SampleHepta.txt'); 
    
def cluster_tetra():
    template_clustering(4, '../Samples/SampleTetra.txt');    
    
def cluster_engy_time():
    template_clustering(2, '../Samples/SampleEngyTime.txt');
    
    
cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_elongate();
cluster_lsun();
cluster_target();
cluster_two_diamonds();
cluster_wing_nut();
cluster_chainlink();
cluster_hepta();
cluster_tetra();
cluster_engy_time();