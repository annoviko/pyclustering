from nnet.som import som;
from nnet.som import type_conn;
from nnet.som import type_init;

from support import read_sample;

def template_self_organization(file, rows, cols, time, structure, init_type = type_init.uniform_grid):
    sample = read_sample(file);
    network = som(rows, cols, sample, time, structure, init_type);
    network.train();
    network.show_network(False, dataset = False);

def som_sample1():
    template_self_organization('../../Samples/SampleSimple1.txt', 1, 2, 100, type_conn.grid_four);
    
def som_sample2():
    template_self_organization('../../Samples/SampleSimple2.txt', 1, 3, 100, type_conn.grid_four);
    
def som_sample3():
    template_self_organization('../../Samples/SampleSimple3.txt', 2, 2, 100, type_conn.grid_four);
    
def som_sample4():
    template_self_organization('../../Samples/SampleSimple4.txt', 1, 5, 100, type_conn.grid_four);
    
def som_sample5():
    template_self_organization('../../Samples/SampleSimple5.txt', 2, 2, 100, type_conn.grid_four);
    
def som_lsun():
    template_self_organization('../../Samples/SampleLsun.txt', 5, 5, 100, type_conn.grid_four);
    
def som_target():
    template_self_organization('../../Samples/SampleTarget.txt', 5, 5, 100, type_conn.grid_four);
    
def som_tetra():
    template_self_organization('../../Samples/SampleTetra.txt', 1, 4, 100, type_conn.grid_four);
    
def som_two_diamonds():
    template_self_organization('../../Samples/SampleTwoDiamonds.txt', 5, 5, 100, type_conn.grid_four);
    
def som_elongate():
    template_self_organization('../../Samples/SampleElongate.txt', 5, 5, 100, type_conn.grid_four);
    
def som_wing_nut():
    template_self_organization('../../Samples/SampleWingNut.txt', 5, 5, 100, type_conn.grid_four);
    
def som_chainlink():
    template_self_organization('../../Samples/SampleChainlink.txt', 5, 5, 100, type_conn.grid_four);
    
def som_atom():
    template_self_organization('../../Samples/SampleAtom.txt', 5, 5, 100, type_conn.grid_four);
    
def som_golf_ball():
    template_self_organization('../../Samples/SampleGolfBall.txt', 5, 5, 100, type_conn.grid_four);
    
def som_hepta():
    template_self_organization('../../Samples/SampleHepta.txt', 1, 7, 100, type_conn.grid_four);
    
def som_engy_time():
    template_self_organization('../../Samples/SampleEngyTime.txt', 5, 5, 100, type_conn.grid_four);
    
def som_target_diffence_intialization():
    template_self_organization('../../Samples/SampleTarget.txt', 9, 9, 150, type_conn.grid_four, type_init.random_centroid);
    template_self_organization('../../Samples/SampleTarget.txt', 9, 9, 150, type_conn.grid_four, type_init.random_surface);
    template_self_organization('../../Samples/SampleTarget.txt', 9, 9, 150, type_conn.grid_four, type_init.uniform_grid);
    
def som_two_diamonds_diffence_intialization():
    template_self_organization('../../Samples/SampleTwoDiamonds.txt', 5, 5, 150, type_conn.grid_four, type_init.random_centroid);
    template_self_organization('../../Samples/SampleTwoDiamonds.txt', 5, 5, 150, type_conn.grid_four, type_init.random_surface);
    template_self_organization('../../Samples/SampleTwoDiamonds.txt', 5, 5, 150, type_conn.grid_four, type_init.uniform_grid);    


som_sample1();
som_sample2();
som_sample3();
som_sample4();
som_sample5();
som_lsun();
som_target();
som_tetra();
som_two_diamonds();
som_elongate();
som_wing_nut();
som_chainlink();
som_atom();
som_golf_ball();
som_hepta();
som_engy_time();

#som_target_diffence_intialization();
#som_two_diamonds_diffence_intialization();