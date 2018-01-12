"""!

@brief Examples of usage and demonstration of abilities of oscillatory network
       based on Hodgkin-Huxley model of neuron.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""


from pyclustering.nnet.dynamic_visualizer import dynamic_visualizer;

from pyclustering.nnet.hhn import hhn_network, hhn_parameters;


def template_dynamic_hhn(num_osc, steps, time, stimulus = None, params = None, separate_representation = False, ccore_flag = False):
    net = hhn_network(num_osc, stimulus, params, ccore = ccore_flag);

    (t, dyn_peripheral, dyn_central) = net.simulate(steps, time);

    amount_canvases = 1;
    if (isinstance(separate_representation, list)):
        amount_canvases = len(separate_representation) + 2;
    elif (separate_representation is True):
        amount_canvases = len(dyn_peripheral[0]) + 2;
    
    print(len(dyn_peripheral));
    print(len(dyn_central));
    
    visualizer = dynamic_visualizer(amount_canvases, x_title = "Time", y_title = "V", y_labels = False);
    visualizer.append_dynamics(t, dyn_peripheral, 0, separate_representation);
    visualizer.append_dynamics(t, dyn_central, amount_canvases - 2, separate_representation);
    visualizer.show();


def one_oscillator_unstimulated():
    template_dynamic_hhn(1, 750, 100, separate_representation = True, ccore_flag = False);
    template_dynamic_hhn(1, 750, 100, separate_representation = True, ccore_flag = True);

def one_oscillator_stimulated():
    template_dynamic_hhn(1, 750, 100, [25], separate_representation = True, ccore_flag = False);
    template_dynamic_hhn(1, 750, 100, [25], separate_representation = True, ccore_flag = True);

def three_oscillators_stimulated():
    template_dynamic_hhn(3, 750, 100, [25] * 3, separate_representation = True, ccore_flag = False);
    template_dynamic_hhn(3, 750, 100, [25] * 3, separate_representation = True, ccore_flag = True);

def two_sync_ensembles():
    template_dynamic_hhn(4, 400, 200, [25, 25, 50, 50], separate_representation = True, ccore_flag = False);
    template_dynamic_hhn(4, 400, 200, [25, 25, 50, 50], separate_representation = True, ccore_flag = True);

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
    

def six_oscillators_mix_2_stimulated():
    params = hhn_parameters();
    params.deltah = 400;
    
    template_dynamic_hhn(6, 1200, 600, [25, 25, 25, 47, 47, 47], params, separate_representation = True);


def six_oscillators_mix_3_stimulated():
    params = hhn_parameters();
    params.deltah = 400;
    
    template_dynamic_hhn(6, 1200, 600, [0, 0, 25, 25, 47, 47], params, separate_representation = True);


# one_oscillator_unstimulated();
# one_oscillator_stimulated();
# three_oscillators_stimulated();
two_sync_ensembles();
ten_oscillators_stimulated_desync();
ten_oscillators_stimulated_sync();
ten_oscillators_stimulated_partial_sync();
six_oscillators_mix_2_stimulated();
six_oscillators_mix_3_stimulated();