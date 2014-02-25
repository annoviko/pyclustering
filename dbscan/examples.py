from dbscan import dbscan;
from support import read_sample;
from support import timedcall;

def template_clustering(radius, neighb, path, draw = True):
    sample = read_sample(path);
    
    (ticks, clusters) = timedcall(dbscan, sample, radius, neighb, draw);
    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");
    

def cluster_sample1():
    template_clustering(0.5, 3, '../Samples/SampleSimple1.txt');
    
def cluster_sample2():
    template_clustering(1, 2, '../Samples/SampleSimple2.txt');
    
def cluster_sample3():
    template_clustering(0.5, 3, '../Samples/SampleSimple3.txt');
    
def cluster_elongate():
    template_clustering(0.5, 3, '../Samples/SampleElongate.txt');
    
def cluster_lsun():
    template_clustering(0.5, 3, '../Samples/SampleLsun.txt');    
    
def cluster_target():
    template_clustering(0.5, 2, '../Samples/SampleTarget.txt');    
    
def cluster_two_diamonds():
    "It's hard to choose properly parameters, but it's OK"
    template_clustering(0.15, 7, '../Samples/SampleTwoDiamonds.txt');   
    
def cluster_wing_nut():
    "It's hard to choose properly parameters, but it's OK"
    template_clustering(0.25, 2, '../Samples/SampleWingNut.txt'); 
    
def cluster_chainlink():
    template_clustering(0.5, 3, '../Samples/SampleChainlink.txt'); 
    
def cluster_hepta():
    template_clustering(1, 3, '../Samples/SampleHepta.txt'); 
    
def cluster_golf_ball():
    "Toooooooooooo looooong"
    template_clustering(0.5, 3, '../Samples/SampleGolfBall.txt'); 
    
def cluster_atom():
    template_clustering(15, 3, '../Samples/SampleAtom.txt'); 

def cluster_tetra():
    template_clustering(0.4, 3, '../Samples/SampleTetra.txt');
     
def cluster_engy_time():
    template_clustering(0.4, 3, '../Samples/SampleEngyTime.txt');

def experiment_execution_time():
    template_clustering(0.5, 3, '../Samples/SampleSimple1.txt', False);
    template_clustering(1, 2, '../Samples/SampleSimple2.txt', False);
    template_clustering(0.5, 3, '../Samples/SampleSimple3.txt', False);
    template_clustering(0.5, 3, '../Samples/SampleElongate.txt', False);
    template_clustering(0.5, 3, '../Samples/SampleLsun.txt', False);
    template_clustering(0.5, 2, '../Samples/SampleTarget.txt', False);
    template_clustering(0.15, 7, '../Samples/SampleTwoDiamonds.txt', False);
    template_clustering(0.25, 2, '../Samples/SampleWingNut.txt', False);
    template_clustering(0.5, 3, '../Samples/SampleChainlink.txt', False);
    template_clustering(1, 3, '../Samples/SampleHepta.txt', False);
    template_clustering(0.4, 3, '../Samples/SampleTetra.txt', False);


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
#cluster_golf_ball();            # it is commented due to long time of processing - it's working absolutely correct!
cluster_atom();
cluster_tetra();
cluster_engy_time();


# experiment_execution_time();