from syncnet import syncnet;
from syncnet import solve_type;

from nnet.sync import draw_dynamics;

from support import draw_clusters;
from support import read_sample;
from support import timedcall;

def template_clustering(file, radius, order, show_dyn = False, show_conn = False, show_clusters = True):
    sample = read_sample(file);
    network = syncnet(sample);
    
    (ticks, (dyn_time, dyn_phase)) = timedcall(network.process, radius, order, solve_type.FAST, show_dyn);
    print("Sample: ", file, "\t\tExecution time: ", ticks, "\n");
    
    if (show_dyn == True):
        draw_dynamics(dyn_time, dyn_phase);
    
    if (show_conn == True):
        network.show_network();
    
    if (show_clusters == True):
        clusters = network.get_clusters(0.05);
        draw_clusters(sample, clusters);
    
    
def cluster_simple1():
    template_clustering('../samples/SampleSimple1.txt', 1, 0.998, show_dyn = True, show_conn = True);
    
def cluster_simple2():
    template_clustering('../samples/SampleSimple2.txt', 1, 0.998, show_dyn = True, show_conn = True);
    
def cluster_simple3():
    template_clustering('../samples/SampleSimple3.txt', 1, 0.998, show_dyn = True, show_conn = True);

def cluster_simple4():
    template_clustering('../samples/SampleSimple4.txt', 1, 0.998, show_dyn = True, show_conn = True);
    
def cluster_simple5():
    template_clustering('../samples/SampleSimple5.txt', 1, 0.998, show_dyn = True, show_conn = True);

def cluster_elongate():
    template_clustering('../samples/SampleElongate.txt', 0.5, 0.999, show_dyn = True, show_conn = True);

def cluster_lsun():
    template_clustering('../samples/SampleLsun.txt', 0.5, 0.999, show_dyn = True, show_conn = True);

def cluster_hepta():
    template_clustering('../samples/SampleHepta.txt', 1, 0.999, show_dyn = True, show_conn = False);

def cluster_two_diamonds():
    "Toooo long and wrong"
    template_clustering('../samples/SampleTwoDiamonds.txt', 0.25, 0.998, show_dyn = False, show_conn = False);  

def cluster_atom():
    template_clustering('../samples/SampleAtom.txt', 20, 0.998, show_dyn = False, show_conn = False); 
    
def cluster_wing_nut():
    "It's hard to choose properly parameters"
    template_clustering('../samples/SampleWingNut.txt', 0.2, 0.99, show_dyn = False, show_conn = False); 

def experiment_execution_time():
    template_clustering('../samples/SampleLsun.txt', 0.5, 0.998, False, False, False);
    template_clustering('../samples/SampleTarget.txt', 0.2, 0.998, False, False, False);
    template_clustering('../samples/SampleTwoDiamonds.txt', 0.5, 0.998, False, False, False);
    template_clustering('../samples/SampleWingNut.txt', 0.4, 0.995, False, False, True);
    template_clustering('../samples/SampleChainlink.txt', 0.6, 0.998, False, False, False);
    template_clustering('../samples/SampleHepta.txt', 1, 0.998, False, False, False);
    template_clustering('../samples/SampleTetra.txt', 0.5, 0.998, False, False, False);
    

cluster_simple1();
cluster_simple2();
cluster_simple3();
cluster_simple4();
cluster_simple5();
cluster_elongate();
cluster_lsun();
cluster_hepta();
cluster_two_diamonds();
cluster_atom();
cluster_wing_nut();

#experiment_execution_time();