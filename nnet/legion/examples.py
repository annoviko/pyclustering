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
    
    template_dynamic_legion(1, 2000, 500, params = parameters);

def one_oscillator_stimulated():
    parameters = legion_parameters();
    parameters.teta = 0;    # because no neighbors at all
    
    template_dynamic_legion(1, 2000, 500, stimulus = [1], params = parameters);
    
def three_oscillator_unstimulated_list():
    parameters = legion_parameters();
    parameters.teta = 0;    # because no stmulated neighbors
    
    template_dynamic_legion(3, 2000, 200, conn_type = conn_type.LIST_BIDIR, params = parameters);
    
def three_oscillator_stimulated_list():
    template_dynamic_legion(3, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1]);
    
def three_oscillator_mix_stimulated_list():
    parameters = legion_parameters();
    parameters.Wt = 4.0;
    template_dynamic_legion(3, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 0, 1], params = parameters);
    
def ten_oscillator_stimulated_list():
    template_dynamic_legion(10, 1000, 750, conn_type = conn_type.LIST_BIDIR, stimulus = [1] * 10);
    
def ten_oscillator_mix_stimulated_list():
    template_dynamic_legion(10, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1, 0, 0, 0, 1, 1, 0, 0]);
    
def thirteen_oscillator_three_stimulated_ensembles_list():
    "Good example of three synchronous ensembels"
    parameters = legion_parameters();
    parameters.teta_x = -1.05;
    parameters.Wt = 4.0;
    parameters.teta_p = 3.0;
    parameters.Wz = 3.0;
    template_dynamic_legion(13, 2000, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1], params = parameters);
    
def sixteen_oscillator_two_stimulated_ensembles_grid():
    parameters = legion_parameters();
    parameters.teta_x = -1.1;
    template_dynamic_legion(16, 2000, 1500, conn_type = conn_type.GRID_FOUR, params = parameters, stimulus = [1, 1, 1, 0, 
                                                                                                              1, 1, 1, 0, 
                                                                                                              0, 0, 0, 1, 
                                                                                                              0, 0, 1, 1]);

    
one_oscillator_unstimulated();
one_oscillator_stimulated();
three_oscillator_unstimulated_list();
three_oscillator_stimulated_list();
three_oscillator_mix_stimulated_list();
ten_oscillator_stimulated_list();
ten_oscillator_mix_stimulated_list();
thirteen_oscillator_three_stimulated_ensembles_list();
sixteen_oscillator_two_stimulated_ensembles_grid();