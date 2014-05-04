from support import draw_dynamics;

from nnet.legion import legion_network, legion_parameters;
from nnet import *;

def template_dynamic_legion(num_osc, steps, time, conn_type = conn_type.NONE, stimulus = None, params = None):
    net = legion_network(num_osc, stimulus, type_conn = conn_type, parameters = params);
    (t, x, z) = net.simulate(steps, time);
    
    draw_dynamics(t, x, x_title = "Time", y_title = "x(t)", separate = True);
    draw_dynamics(t, z, x_title = "Time", y_title = "z(t)", separate = True);
    
def one_oscillator_unstimulated():
    parameters = legion_parameters();
    parameters.teta = 0;    # because no neighbors at all
    
    template_dynamic_legion(1, 2000, 200, params = parameters);

def one_oscillator_stimulated():
    parameters = legion_parameters();
    parameters.teta = 0;    # because no neighbors at all
    
    template_dynamic_legion(1, 2000, 200, stimulus = [1], params = parameters);
    
def three_oscillator_unstimulated_list():
    parameters = legion_parameters();
    parameters.teta = 0;    # because no stmulated neighbors
    
    template_dynamic_legion(3, 2000, 200, conn_type = conn_type.LIST_BIDIR, params = parameters);
    
def three_oscillator_stimulated_list():
    template_dynamic_legion(3, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1]);
    
def three_oscillator_mix_stimulated_list():
    template_dynamic_legion(3, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 0, 1]);
    
def ten_oscillator_stimulated_list():
    template_dynamic_legion(10, 1000, 750, conn_type = conn_type.LIST_BIDIR, stimulus = [1] * 10);
    
def ten_oscillator_mix_stimulated_list():
    template_dynamic_legion(10, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]);
    
def ten_oscillator_three_stimulated_ensembles_list():
    parameters = legion_parameters();
    parameters.betta = 0.2;
    parameters.Wz = 2.5;
    template_dynamic_legion(10, 2000, 2000, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1], params = parameters);
    
def sixteen_oscillator_two_stimulated_ensembles_grid():
    parameters = legion_parameters();
    template_dynamic_legion(16, 1500, 1500, conn_type = conn_type.GRID_FOUR, params = parameters, stimulus = [1, 1, 0, 0, 
                                                                                                              1, 1, 0, 0, 
                                                                                                              0, 0, 1, 1, 
                                                                                                              0, 0, 1, 1]);

def sixteen_oscillator_three_stimulated_ensembles_grid(): 
    parameters = legion_parameters();
    parameters.betta = 0.2;
    parameters.Wz = 8;
    template_dynamic_legion(16, 3000, 2000, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1 ]);
    
one_oscillator_unstimulated();
one_oscillator_stimulated();
three_oscillator_unstimulated_list();
three_oscillator_stimulated_list();
three_oscillator_mix_stimulated_list();
ten_oscillator_stimulated_list();
ten_oscillator_mix_stimulated_list();
ten_oscillator_three_stimulated_ensembles_list();
sixteen_oscillator_two_stimulated_ensembles_grid();
sixteen_oscillator_three_stimulated_ensembles_grid();