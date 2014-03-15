from nnet.sync import draw_dynamics;

from support import read_sample, draw_clusters;
from hsyncnet import hsyncnet;

def template_clustering(file, number_clusters, arg_collect_dynamic = True, show_network_structure = False, arg_order = 0.999, arg_eps = 0.1):
        sample = read_sample(file);
        network = hsyncnet(sample);
        
        (time, dynamic) = network.process(number_clusters, order = arg_order, collect_dynamic = arg_collect_dynamic);
        clusters = network.get_clusters();
        
        if (show_network_structure == True):
            network.show_network();
            
        if (arg_collect_dynamic == True):
            draw_dynamics(time, dynamic);
        
        draw_clusters(sample, clusters);
        

def cluster_sample1():
    template_clustering('../Samples/SampleSimple1.txt', 2);
    
def cluster_sample2():
    template_clustering('../Samples/SampleSimple2.txt', 3);
    
def cluster_sample3():
    template_clustering('../Samples/SampleSimple3.txt', 4);
    
def cluster_simple4():
    template_clustering('../Samples/SampleSimple4.txt', 5);
    
def cluster_simple5():
    template_clustering('../Samples/SampleSimple5.txt', 4);
    
def cluster_elongate():
    template_clustering('../Samples/SampleElongate.txt', 2, arg_collect_dynamic = False);

def cluster_lsun():
    "NOTE: Too slow"
    template_clustering('../Samples/SampleLsun.txt', 3, arg_collect_dynamic = False);
    
def cluster_hepta():
    template_clustering('../Samples/SampleHepta.txt', 7, arg_collect_dynamic = False);
    
def cluster_tetra():
    "NOTE: Too slow"
    template_clustering('../Samples/SampleTetra.txt', 4, arg_collect_dynamic = False);

def cluster_target():
    "NOTE: Too slow"
    template_clustering('../Samples/SampleTarget.txt', 6, arg_collect_dynamic = False);
    
def cluster_chainlink():
    "NOTE: Too slow"
    template_clustering('../Samples/SampleChainlink.txt', 2, arg_collect_dynamic = False);
    
def cluster_wing_nut():
    "NOTE: Too slow"
    template_clustering('../Samples/SampleWingNut.txt', 2, arg_collect_dynamic = False);
    
def cluster_two_diamonds():
    "NOTE: Too slow"
    template_clustering('../Samples/SampleTwoDiamonds.txt', 2, arg_collect_dynamic = False);    

# cluster_sample1();
# cluster_sample2();
# cluster_sample3();
# cluster_simple4();
# cluster_elongate();
# cluster_lsun();
# cluster_hepta();
# cluster_tetra();
# cluster_target();
# cluster_chainlink();
# cluster_wing_nut();
# cluster_two_diamonds();
