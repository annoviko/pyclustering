from pyclustering.support import draw_dynamics;

from pyclustering.nnet.legion import legion_network, legion_parameters;
from pyclustering.nnet import *;

def template_dynamic_legion(num_osc, steps, time, conn_type = conn_type.NONE, stimulus = None, params = None, separate_repr = True):
    net = legion_network(num_osc, stimulus, type_conn = conn_type, parameters = params);
    (t, x, z) = net.simulate(steps, time, solution = solve_type.RK4);
    
    draw_dynamics(t, x, x_title = "Time", y_title = "x(t)", separate = separate_repr);
    draw_dynamics(t, z, x_title = "Time", y_title = "z(t)");
    
    ensembles = net.allocate_sync_ensembles(0.1);
    print(ensembles);
    
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
    template_dynamic_legion(10, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1, 0, 0, 0, 1, 1, 0, 0], separate_repr = [ [0, 1, 2], [3, 4, 5, 8, 9], [6, 7] ]);
    
def thirteen_oscillator_three_stimulated_ensembles_list():
    "Good example of three synchronous ensembels"
    "Not accurate due to false skipes are observed"
    parameters = legion_parameters();
    parameters.Wt = 4.0;
    parameters.fi = 0.8;
    template_dynamic_legion(15, 1000, 1000, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1], params = parameters, separate_repr = [ [0, 1, 2], [3, 4, 5, 9, 10], [6, 7, 8], [11, 12, 13, 14] ]);
    
def sixteen_oscillator_two_stimulated_ensembles_grid():
    "Not accurate false due to spikes are observed"
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