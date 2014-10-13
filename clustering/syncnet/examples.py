from clustering.syncnet import syncnet;

from nnet import solve_type;

from samples.definitions import SIMPLE_SAMPLES;
from samples.definitions import FCPS_SAMPLES;

from support import draw_clusters;
from support import read_sample;
from support import timedcall;
from support import draw_dynamics;

def template_clustering(file, radius, order, show_dyn = False, show_conn = False, show_clusters = True, ena_conn_weight = False, ccore_flag = False):
    sample = read_sample(file);
    network = syncnet(sample, radius, enable_conn_weight = ena_conn_weight, ccore = ccore_flag);
    
    (ticks, (dyn_time, dyn_phase)) = timedcall(network.process, order, solve_type.FAST, show_dyn);
    print("Sample: ", file, "\t\tExecution time: ", ticks, "\n");
    
    if (show_dyn == True):
        draw_dynamics(dyn_time, dyn_phase, x_title = "Time", y_title = "Phase", y_lim = [0, 2 * 3.14]);
    
    if (show_conn == True):
        network.show_network();
    
    if (show_clusters == True):
        clusters = network.get_clusters(0.1);
        draw_clusters(sample, clusters);
    
    
def cluster_simple1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, show_dyn = True, show_conn = True);
    
def cluster_simple2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, show_dyn = True, show_conn = True);
    
def cluster_simple3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, show_dyn = True, show_conn = True);

def cluster_simple4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0.999, show_dyn = True, show_conn = True);
    
def cluster_simple5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0.999, show_dyn = True, show_conn = True);

def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 0.5, 0.999, show_dyn = True, show_conn = True);

def cluster_lsun():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 0.3, 0.999, show_dyn = True, show_conn = True);

def cluster_hepta():
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 0.999, show_dyn = True, show_conn = True);
    
def cluster_chainlink():
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 0.5, 0.999, show_dyn = True, show_conn = True);

def cluster_two_diamonds():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 0.03, 0.999, show_dyn = False, show_conn = False);  

def cluster_atom():
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, 20, 0.999, show_dyn = False, show_conn = False); 
    
def cluster_wing_nut():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 0.08, 0.999, show_dyn = False, show_conn = False); 

def experiment_execution_time(show_dyn = False, ccore = False):
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 0.5, 0.999, show_dyn, False, True, False, ccore);
    
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 0.3, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 0.4, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 0.03, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 0.08, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 0.5, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 0.3, 0.999, show_dyn, False, True, False, ccore);

def cluster_simple1_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True); 
    
def cluster_simple2_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True);   

def cluster_simple3_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True);

def cluster_simple4_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True);

def cluster_simple5_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 10, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True);


cluster_simple1();
cluster_simple2();
cluster_simple3();
cluster_simple4();
cluster_simple5();
cluster_elongate();
cluster_lsun();
cluster_hepta();
cluster_chainlink();
cluster_two_diamonds();
cluster_atom();
cluster_wing_nut();
      
cluster_simple1_conn_weight();
cluster_simple2_conn_weight();
cluster_simple3_conn_weight();
cluster_simple4_conn_weight();
cluster_simple5_conn_weight();
 
experiment_execution_time(False, False);
experiment_execution_time(True, True);