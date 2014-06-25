from clustering.dbscan import dbscan;

from support import read_sample;
from support import timedcall;
from support import draw_clusters;

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

def template_clustering(radius, neighb, path, invisible_axes = False, ccore = True):
    sample = read_sample(path);
    
    (ticks, result) = timedcall(dbscan, sample, radius, neighb, True, ccore);
    clusters = result[0];
    noise = result[1];
    
    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");
    
    draw_clusters(sample, clusters, [], 'o', hide_axes = invisible_axes);
    


def cluster_sample1():
    template_clustering(0.4, 2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
    
def cluster_sample2():
    template_clustering(1, 2, SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
    
def cluster_sample3():
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
    
def cluster_sample4():
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE4);

def cluster_sample5():
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE5);
 
def cluster_elongate():
    template_clustering(0.5, 3, SIMPLE_SAMPLES.SAMPLE_ELONGATE);
    
def cluster_lsun():
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_LSUN);    
    
def cluster_target():
    template_clustering(0.5, 2, FCPS_SAMPLES.SAMPLE_TARGET);    
    
def cluster_two_diamonds():
    "It's hard to choose properly parameters, but it's OK"
    template_clustering(0.15, 7, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS);   
    
def cluster_wing_nut():
    "It's hard to choose properly parameters, but it's OK"
    template_clustering(0.25, 2, FCPS_SAMPLES.SAMPLE_WING_NUT); 
    
def cluster_chainlink():
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_CHAINLINK); 
    
def cluster_hepta():
    template_clustering(1, 3, FCPS_SAMPLES.SAMPLE_HEPTA); 
    
def cluster_golf_ball():
    "Toooooooooooo looooong"
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_GOLF_BALL); 
    
def cluster_atom():
    template_clustering(15, 3, FCPS_SAMPLES.SAMPLE_ATOM); 

def cluster_tetra():
    template_clustering(0.4, 3, FCPS_SAMPLES.SAMPLE_TETRA);
     
def cluster_engy_time():
    template_clustering(0.2, 20, FCPS_SAMPLES.SAMPLE_ENGY_TIME);

def experiment_execution_time(ccore = False):
    "Performance measurement"
    template_clustering(0.5, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, False, ccore);
    template_clustering(1, 2, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, False, ccore);
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE3, False, ccore);
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE4, False, ccore);
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE5, False, ccore);
    template_clustering(0.5, 3, SIMPLE_SAMPLES.SAMPLE_ELONGATE, False, ccore);
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_LSUN, False, ccore);
    template_clustering(0.5, 2, FCPS_SAMPLES.SAMPLE_TARGET, False, ccore);
    template_clustering(0.15, 7, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, ccore);
    template_clustering(0.25, 2, FCPS_SAMPLES.SAMPLE_WING_NUT, False, ccore);
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_CHAINLINK, False, ccore);
    template_clustering(1, 3, FCPS_SAMPLES.SAMPLE_HEPTA, False, ccore);
    template_clustering(0.4, 3, FCPS_SAMPLES.SAMPLE_TETRA, False, ccore);


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
cluster_golf_ball();            # it is commented due to long time of processing - it's working absolutely correct!
cluster_atom();
cluster_tetra();
cluster_engy_time();

experiment_execution_time(False);   # Python code
experiment_execution_time(True);    # C++ code + Python env.