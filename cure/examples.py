from support import read_sample;
from support import draw_clusters;
from support import timedcall;

from samples.definitions import SIMPLE_SAMPLES;
from samples.definitions import FCPS_SAMPLES;

from cure import cure;

def template_clustering(number_clusters, path, number_represent_points = 5, compression = 0.5, draw = True):
    sample = read_sample(path);
    (ticks, clusters) = timedcall(cure, sample, number_clusters, number_represent_points, compression);

    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");

    if (draw is True):
        draw_clusters(None, clusters);


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
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_ELONGATE);

def cluster_lsun():
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN);  
    
def cluster_target():
    template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET, 10, 0.3);     

def cluster_two_diamonds():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS);  

def cluster_wing_nut():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT, 1, 1); 
    
def cluster_chainlink():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_CHAINLINK);     
    
def cluster_hepta():
    template_clustering(7, FCPS_SAMPLES.SAMPLE_HEPTA); 
    
def cluster_tetra():
    template_clustering(4, FCPS_SAMPLES.SAMPLE_TETRA);    
    
def cluster_engy_time():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_ENGY_TIME, 50, 0.5);

def cluster_golf_ball():
    template_clustering(1, FCPS_SAMPLES.SAMPLE_GOLF_BALL); 
    
def cluster_atom():
    "Impossible to obtain parameters that satisfy us, it seems to me that compression = 0.2 is key parameter here, because results of clustering doesn't depend on number of represented points, except 0."
    "Thus the best parameters is following: number of points for representation: [5, 400]; compression: [0.2, 0.204]"
    "Results of clustering is not so dramatically, but clusters are not allocated properly"
    template_clustering(2, FCPS_SAMPLES.SAMPLE_ATOM, 20, 0.2);

def find_best_atom():
    for represent in range(5, 20, 100):
        for compression in range(0, 10, 1):
            print("number of represent points: ", represent, ", compression: ", float(compression) / 10);
            template_clustering(2, FCPS_SAMPLES.SAMPLE_ATOM, represent, float(compression) / 10);

def experiment_execution_time():
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN, draw = False);
    template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET, 10, 0.3, draw = False);
    template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, draw = False); 
    template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT, 1, 1, draw = False);
    template_clustering(2, FCPS_SAMPLES.SAMPLE_CHAINLINK, draw = False);
    template_clustering(4, FCPS_SAMPLES.SAMPLE_TETRA, draw = False);
    template_clustering(7, FCPS_SAMPLES.SAMPLE_HEPTA, draw = False);

# find_best_atom();

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
cluster_atom();
cluster_engy_time();
cluster_golf_ball();

experiment_execution_time();