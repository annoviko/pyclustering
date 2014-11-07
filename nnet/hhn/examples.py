from support import draw_dynamics;

from nnet.hhn import hhn_network;

def template_dynamic_hhn(num_osc, steps, time, stimulus = None, separate_representation = False):
    network = hhn_network(num_osc, stimulus);

    (t, dyn) = network.simulate(steps, time);

    draw_dynamics(t, dyn, x_title = "Time", y_title = "V", separate = separate_representation);


def one_oscillator_unstimulated():
    template_dynamic_hhn(1, 750, 100, separate_representation = True);

def one_oscillator_stimulated():
    template_dynamic_hhn(1, 750, 100, [25], separate_representation = True);
    
def three_oscillators_stimulated():
    template_dynamic_hhn(3, 750, 100, [25] * 3, separate_representation = True);
    
def four_oscillators_mix_stimulated():
    template_dynamic_hhn(4, 600, 200, [20, 20, 40, 40], separate_representation = True);

    
one_oscillator_unstimulated();
one_oscillator_stimulated();
three_oscillators_stimulated();
four_oscillators_mix_stimulated();