from support import draw_dynamics;

from nnet.hhn import hhn_network;

def template_dynamic_sync(num_osc):
    network = hhn_network(num_osc);

    (t, dyn) = network.simulate();

    draw_dynamics(t, dyn, x_title = "Time", y_title = "V");
    return network;