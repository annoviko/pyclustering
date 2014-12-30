from pyclustering.support import draw_dynamics;

from pyclustering.nnet.hhn import hhn_network, hhn_parameters;

def template_dynamic_hhn(num_osc, steps, time, stimulus = None, params = None, separate_representation = False):
    net = hhn_network(num_osc, stimulus, params);

    (t, dyn) = net.simulate(steps, time);

    draw_dynamics(t, dyn, x_title = "Time", y_title = "V", separate = separate_representation);


def one_oscillator_unstimulated():
    template_dynamic_hhn(1, 750, 100, separate_representation = True);

def one_oscillator_stimulated():
    template_dynamic_hhn(1, 750, 100, [25], separate_representation = True);
    
def three_oscillators_stimulated():
    template_dynamic_hhn(3, 750, 100, [25] * 3, separate_representation = True);
    
def ten_oscillators_stimulated_desync():
    params = hhn_parameters();
    params.w1 = 0;
    params.w2 = 0;
    params.w3 = 0;
    
    template_dynamic_hhn(10, 750, 100, [25, 25, 25, 25, 25, 11, 11, 11, 11, 11], params, separate_representation = True);
    
def ten_oscillators_stimulated_sync():
    params = hhn_parameters();
    params.w1 = 0.1;
    params.w2 = 0.0;
    params.w3 = 0;
    
    template_dynamic_hhn(10, 750, 100, [25, 25, 25, 25, 25, 27, 27, 27, 27, 27], params, separate_representation = True);    
    
def ten_oscillators_stimulated_partial_sync():
    params = hhn_parameters();
    params.w1 = 0.1;
    params.w2 = 5.0;
    params.w3 = 0;
    
    template_dynamic_hhn(10, 750, 200, [25, 25, 25, 25, 25, 11, 11, 11, 11, 11], params, separate_representation = True);     
    
def ten_oscillators_mix_stimulated():
    params = hhn_parameters();
    params.deltah = 400;
    
    template_dynamic_hhn(6, 1200, 600, [0, 0, 25, 25, 47, 47], params, separate_representation = True);

    
one_oscillator_unstimulated();
one_oscillator_stimulated();
three_oscillators_stimulated();
ten_oscillators_stimulated_desync();
ten_oscillators_stimulated_sync();
ten_oscillators_stimulated_partial_sync();
ten_oscillators_mix_stimulated();