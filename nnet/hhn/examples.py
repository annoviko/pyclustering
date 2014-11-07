from support import draw_dynamics;

from nnet.hhn import hhn_network;

def template_dynamic_hhn(num_osc, steps, time):
    network = hhn_network(num_osc);

    (t, dyn) = network.simulate(steps, time);
    print(dyn);

    draw_dynamics(t, dyn, x_title = "Time", y_title = "V");
    return network;


def one_oscillator_unstimulated():
    template_dynamic_hhn(1, 500, 100);

def one_oscillator_stimulated():
    template_dynamic_hhn(1, 1000, 100);
    
    
    
one_oscillator_unstimulated();