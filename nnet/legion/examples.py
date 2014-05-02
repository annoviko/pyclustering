from support import draw_dynamics;

from nnet.legion import legion_network;
from nnet import *;

def template_dynamic_legion(num_osc, steps, time, conn_type = conn_type.NONE, stimulus = None, params = None):
    net = legion_network(num_osc, stimulus, type_conn = conn_type);
    (t, x) = net.simulate(steps, time);
    
    draw_dynamics(t, x, x_title = "Time", y_title = "x(t)");
    
def one_oscillator_unstimulated():
    template_dynamic_legion(1, 2000, 200);

def one_oscillator_stimulated():
    template_dynamic_legion(1, 2000, 200, stimulus = [1]);
    
def three_oscillator_unstimulated_list():
    template_dynamic_legion(3, 2000, 200, conn_type = conn_type.LIST_BIDIR);
    
def three_oscillator_stimulated_list():
    template_dynamic_legion(3, 1000, 500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1]);
    
def three_oscillator_mix_stimulated_list():
    template_dynamic_legion(3, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 0, 1]);
    
def ten_oscillator_stimulated_list():
    template_dynamic_legion(10, 1000, 750, conn_type = conn_type.LIST_BIDIR, stimulus = [1] * 10);
    
def ten_oscillator_mix_stimulated_list():
    template_dynamic_legion(10, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1, 0, 0, 0, 0, 1, 1, 1]);
    
one_oscillator_unstimulated();
one_oscillator_stimulated();
three_oscillator_unstimulated_list();
three_oscillator_stimulated_list();
three_oscillator_mix_stimulated_list();
ten_oscillator_stimulated_list();
ten_oscillator_mix_stimulated_list();
