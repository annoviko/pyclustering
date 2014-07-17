from support import draw_dynamics;

from nnet.pcnn import pcnn_network, pcnn_parameters;
from nnet import *;

def template_dynamic_pcnn(num_osc, steps, stimulus = None, params = None, conn_type = conn_type.NONE, separate_representation = True):
    net = pcnn_network(num_osc, stimulus, params, conn_type);
    (t, y) = net.simulate(steps, None, None, True);
    # (t, y, thr, f, l) = net.simulate(steps, None, None, True);
    
    print(net.allocate_sync_ensembles());
    
    draw_dynamics(t, y, x_title = "Time", y_title = "y(t)", separate = separate_representation);
    #draw_dynamics(t, thr, x_title = "Time", y_title = "threshold");
    #draw_dynamics(t, f, x_title = "Time", y_title = "feeding");
    #draw_dynamics(t, l, x_title = "Time", y_title = "linking");
    
def one_neuron_unstimulated():
    template_dynamic_pcnn(1, 100, [0]);
    
def one_neuron_stimulated():
    template_dynamic_pcnn(1, 100, [1]);
    
def nine_neurons_stimulated_one_sync():
    "Just dynamic demonstration"
    params = pcnn_parameters();
    template_dynamic_pcnn(9, 100, [1.0] * 9, params, conn_type.GRID_FOUR);
    
    
def nine_neurons_mix_stimulated():
    "Just dynamic demonstration"
    template_dynamic_pcnn(9, 100, [1, 1, 1, 
                                   0, 0, 0, 
                                   1, 1, 1], None, conn_type.GRID_FOUR);
    
def twenty_five_neurons_mix_stimulated():
    "Object allocation"
    "If M = 0 then only object will be allocated"
    params = pcnn_parameters();
    
    params.AF = 0.1;
    params.AL = 0.0;
    params.AT = 0.7;
    params.VF = 1.0;
    params.VL = 1.0;
    params.VT = 10.0;
    params.M = 0.0;
    
    template_dynamic_pcnn(25, 100, [0, 0, 0, 0, 0, 
                                    0, 0, 0, 0, 0,
                                    0, 1, 1, 0, 0,
                                    0, 1, 1, 0, 0,
                                    0, 0, 0, 0, 0], params, conn_type.GRID_FOUR, False);

def hundred_neurons_mix_stimulated():
    "Allocate several clusters: the first contains borders (indexes of oscillators) and the second objects (indexes of oscillators)"
    params = pcnn_parameters();
    
    params.AF = 0.1;
    params.AL = 0.1;
    params.AT = 0.8;
    params.VF = 1.0;
    params.VL = 1.0;
    params.VT = 20.0;
    params.W = 1.0;
    params.M = 1.0;
    
    template_dynamic_pcnn(100, 50,  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                                     0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                                     0, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                                     0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                                     0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
                                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0], params, conn_type.GRID_EIGHT, False);


one_neuron_unstimulated();
one_neuron_stimulated();
nine_neurons_stimulated_one_sync();
nine_neurons_mix_stimulated();
twenty_five_neurons_mix_stimulated();
hundred_neurons_mix_stimulated();