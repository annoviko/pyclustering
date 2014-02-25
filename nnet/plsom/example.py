from nnet.plsom import plsom;
from nnet.som import type_conn;

from support import read_sample;

def template_self_organization(file, rows, cols, structure):
    sample = read_sample(file);
    network = plsom(rows, cols, sample, structure);
    network.train();
    network.show_network();

def plsom_sample1():
    template_self_organization('../../Samples/SampleSimple1.txt', 1, 2, type_conn.grid_four);
    
def plsom_sample2():
    template_self_organization('../../Samples/SampleSimple2.txt', 1, 3, type_conn.grid_four);
    
def plsom_sample3():
    template_self_organization('../../Samples/SampleSimple3.txt', 2, 2, type_conn.grid_four);
    
def plsom_sample4():
    template_self_organization('../../Samples/SampleSimple4.txt', 1, 5, type_conn.grid_four);
    
def plsom_sample5():
    template_self_organization('../../Samples/SampleSimple5.txt', 2, 2, type_conn.grid_four);
    
def plsom_lsun():
    template_self_organization('../../Samples/SampleLsun.txt', 5, 5, type_conn.grid_four);
    
def plsom_target():
    template_self_organization('../../Samples/SampleTarget.txt', 5, 5, type_conn.grid_four);
    
def plsom_tetra():
    template_self_organization('../../Samples/SampleTetra.txt', 5, 5, type_conn.grid_four);
    
def plsom_two_diamonds():
    template_self_organization('../../Samples/SampleTwoDiamonds.txt', 5, 5, type_conn.grid_four);
    
def plsom_elongate():
    template_self_organization('../../Samples/SampleElongate.txt', 5, 5, type_conn.grid_four);
    
def plsom_wing_nut():
    "Tooooo looooong"
    template_self_organization('../../Samples/SampleWingNut.txt', 5, 5, type_conn.grid_four);
    
def plsom_chainlink():
    template_self_organization('../../Samples/SampleChainlink.txt', 5, 5, type_conn.grid_four);
    
def plsom_atom():
    template_self_organization('../../Samples/SampleAtom.txt', 5, 5, type_conn.grid_four);
    
def plsom_golf_ball():
    template_self_organization('../../Samples/SampleGolfBall.txt', 5, 5, type_conn.grid_four);
    
def plsom_hepta():
    template_self_organization('../../Samples/SampleHepta.txt', 1, 7, type_conn.grid_four);
    
def plsom_engy_time():
    template_self_organization('../../Samples/SampleEngyTime.txt', 5, 5, type_conn.grid_four);


plsom_sample1();
plsom_sample2();
plsom_sample3();
plsom_sample4();
plsom_sample5();
plsom_lsun();
plsom_target();
plsom_tetra();
plsom_two_diamonds();
plsom_elongate();
# plsom_wing_nut(); # Too long
plsom_chainlink();
plsom_atom();
plsom_golf_ball();
plsom_hepta();
plsom_engy_time();