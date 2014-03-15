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
    template_clustering(2, '../samples/SampleSimple1.txt');
    
def cluster_sample2():
    template_clustering(3, '../samples/SampleSimple2.txt');
    
def cluster_sample3():
    template_clustering(4, '../samples/SampleSimple3.txt');
    
def cluster_sample4():
    template_clustering(5, '../samples/SampleSimple4.txt');
    
def cluster_sample5():
    template_clustering(4, '../samples/SampleSimple5.txt');    
    
def cluster_elongate():
    "NOTE: Not applicable for this sample"
    template_clustering(2, '../samples/SampleElongate.txt');

def cluster_lsun():
    "NOTE: Not applicable for this sample"
    template_clustering(3, '../samples/SampleLsun.txt');  
    
def cluster_target():
    "NOTE: Not applicable for this sample"
    template_clustering(6, '../samples/SampleTarget.txt');     

def cluster_two_diamonds():
    template_clustering(2, '../samples/SampleTwoDiamonds.txt');  

def cluster_wing_nut():
    template_clustering(2, '../samples/SampleWingNut.txt'); 
    
def cluster_chainlink():
    "NOTE: Not applicable for this sample"
    template_clustering(2, '../samples/SampleChainlink.txt');     
    
def cluster_hepta():
    template_clustering(7, '../samples/SampleHepta.txt'); 
    
def cluster_tetra():
    template_clustering(4, '../samples/SampleTetra.txt');    
    
def cluster_engy_time():
    template_clustering(2, '../samples/SampleEngyTime.txt');
    
    
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
