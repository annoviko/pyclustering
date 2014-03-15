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
    template_clustering('../samples/SampleSimple1.txt', 2);
    
def cluster_sample2():
    template_clustering('../samples/SampleSimple2.txt', 3);
    
def cluster_sample3():
    template_clustering('../samples/SampleSimple3.txt', 4);
    
def cluster_simple4():
    template_clustering('../samples/SampleSimple4.txt', 5);
    
def cluster_simple5():
    template_clustering('../samples/SampleSimple5.txt', 4);
    
def cluster_elongate():
    template_clustering('../samples/SampleElongate.txt', 2, arg_collect_dynamic = False);

def cluster_lsun():
    "NOTE: Too slow"
    template_clustering('../samples/SampleLsun.txt', 3, arg_collect_dynamic = False);
    
def cluster_hepta():
    template_clustering('../samples/SampleHepta.txt', 7, arg_collect_dynamic = False);
    
def cluster_tetra():
    "NOTE: Too slow"
    template_clustering('../samples/SampleTetra.txt', 4, arg_collect_dynamic = False);

def cluster_target():
    "NOTE: Too slow"
    template_clustering('../samples/SampleTarget.txt', 6, arg_collect_dynamic = False);
    
def cluster_chainlink():
    "NOTE: Too slow"
    template_clustering('../samples/SampleChainlink.txt', 2, arg_collect_dynamic = False);
    
def cluster_wing_nut():
    "NOTE: Too slow"
    template_clustering('../samples/SampleWingNut.txt', 2, arg_collect_dynamic = False);
    
def cluster_two_diamonds():
    "NOTE: Too slow"
    template_clustering('../samples/SampleTwoDiamonds.txt', 2, arg_collect_dynamic = False);    

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
