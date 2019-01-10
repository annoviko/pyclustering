"""!

@brief Examples of usage and demonstration of abilities of Hysteresis Oscillatory Network.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
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

from pyclustering.nnet.hysteresis import hysteresis_network, hysteresis_visualizer;
from pyclustering.nnet import *;


def template_dynamic(num_osc, own_weight = -3, neigh_weight = -1, initial_states = None, initial_outputs = None, steps = 1000, time = 10):
    network = hysteresis_network(num_osc, own_weight, neigh_weight);
    
    if (initial_states is not None):
        network.states = initial_states;
        
    if (initial_outputs is not None):
        network.outputs = initial_outputs;
    
    output_dynamic = network.simulate(steps, time);
    hysteresis_visualizer.show_output_dynamic(output_dynamic);
    
    ensembles = output_dynamic.allocate_sync_ensembles(tolerance = 0.5, threshold_steps = 5);
    print("Allocated synchronous ensembles ( amout:", len(ensembles), "):", ensembles);


def one_oscillator_weight_2():
    template_dynamic(1, -2);

def one_oscillator_weight_4():
    template_dynamic(1, -4);
    
def two_oscillators_sync():
    "Comment: Different initial state - state of sync. will be reached."
    template_dynamic(2, -4, 1, [1, 0], [1, 1]);
    
def two_oscillators_desync():
    "Note: if initial state is the same for both oscillators then desync. will not be exist. It is very important to set different values if desync. is required."
    template_dynamic(2, -4, -1, [1, 0], [1, 1]);
    
def five_oscillators_positive_conn():
    "Note: Oscillations are dead in this case (sync. should be in ideal case)"
    template_dynamic(5, -4, 1, [1, 0.5, 0, -0.5, -1], [1, 1, 1, 1, 1]);
    template_dynamic(5, -4, 1, [1, 0.8, 0.6, 0.4, 0.2], [-1, -1, -1, -1, -1]);
    
def five_oscillators_negative_conn():
    "Comment: Full desync."
    template_dynamic(5, -4, -1, [1, 0.5, 0, -0.5, -1], [1, 1, 1, 1, 1]);


one_oscillator_weight_2();
one_oscillator_weight_4();
two_oscillators_sync();
two_oscillators_desync();
five_oscillators_positive_conn();
five_oscillators_negative_conn();