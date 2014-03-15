from support import read_sample;
from support import draw_clusters;
from support import timedcall;

from cure import cure;

def template_clustering(number_clusters, path, number_represent_points = 5, compression = 0.5, draw = True):
    sample = read_sample(path);
    (ticks, cure_clusters) = timedcall(cure, sample, number_clusters, number_represent_points, compression);

    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");

    clusters = [ cure_cluster.points for cure_cluster in cure_clusters ];

    if (draw is True):
        draw_clusters(None, clusters);


def cluster_sample1():
    template_clustering(2, '../samples/SampleSimple1.txt');
    
def cluster_sample2():
    template_clustering(3, '../samples/SampleSimple2.txt');
    
def cluster_sample3():
    template_clustering(4, '../samples/SampleSimple3.txt');
    
def cluster_elongate():
    template_clustering(2, '../samples/SampleElongate.txt');

def cluster_lsun():
    template_clustering(3, '../samples/SampleLsun.txt');  
    
def cluster_target():
    template_clustering(6, '../samples/SampleTarget.txt', 10, 0.3);     

def cluster_two_diamonds():
    template_clustering(2, '../samples/SampleTwoDiamonds.txt');  

def cluster_wing_nut():
    template_clustering(2, '../samples/SampleWingNut.txt', 1, 1); 
    
def cluster_chainlink():
    template_clustering(2, '../samples/SampleChainlink.txt');     
    
def cluster_hepta():
    template_clustering(7, '../samples/SampleHepta.txt'); 
    
def cluster_tetra():
    template_clustering(4, '../samples/SampleTetra.txt');    
    
def cluster_engy_time():
    template_clustering(2, '../samples/SampleEngyTime.txt', 50, 0.5);

def cluster_golf_ball():
    template_clustering(1, '../samples/SampleGolfBall.txt'); 
    
def cluster_atom():
    "Impossible to obtain parameters that satisfy us, it seems to me that compression = 0.2 is key parameter here, because results of clustering doesn't depend on number of represented points, except 0."
    "Thus the best parameters is following: number of points for representation: [5, 400]; compression: [0.2, 0.204]"
    "Results of clustering is not so dramatically, but clusters are not allocated properly"
    template_clustering(2, '../samples/SampleAtom.txt', 20, 0.2);

def find_best_atom():
    for represent in range(5, 20, 100):
        for compression in range(0, 10, 1):
            print("number of represent points: ", represent, ", compression: ", float(compression) / 10);
            template_clustering(2, '../samples/SampleAtom.txt', represent, float(compression) / 10);

# find_best_atom();


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
cluster_atom();
cluster_engy_time();
cluster_golf_ball();