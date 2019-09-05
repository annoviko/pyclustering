"""!

@brief Examples of usage and demonstration of abilities of oscillatory network
       based on Hodgkin-Huxley model of neuron.

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


from pyclustering.nnet.dynamic_visualizer import dynamic_visualizer

from pyclustering.nnet.hhn import hhn_network, hhn_parameters


def template_dynamic_hhn(num_osc, steps, time, stimulus=None, params=None, separate=False, ccore_flag=False):
    net = hhn_network(num_osc, stimulus, params, ccore=ccore_flag)

    (t, dyn_peripheral, dyn_central) = net.simulate(steps, time)

    amount_canvases = 1
    if (isinstance(separate, list)):
        amount_canvases = len(separate) + 2
    elif (separate is True):
        amount_canvases = len(dyn_peripheral[0]) + 2
    
    visualizer = dynamic_visualizer(amount_canvases, x_title="Time", y_title="V", y_labels=False)
    visualizer.append_dynamics(t, dyn_peripheral, 0, separate)
    visualizer.append_dynamics(t, dyn_central, amount_canvases - 2, True)
    visualizer.show()


def one_oscillator_unstimulated():
    template_dynamic_hhn(1, 750, 100, separate=True, ccore_flag=False)
    template_dynamic_hhn(1, 750, 100, separate=True, ccore_flag=True)


def one_oscillator_stimulated():
    template_dynamic_hhn(1, 750, 100, [25], separate=True, ccore_flag=False)
    template_dynamic_hhn(1, 750, 100, [25], separate=True, ccore_flag=True)


def three_oscillators_stimulated():
    template_dynamic_hhn(3, 750, 100, [25] * 3, separate=True, ccore_flag=False)
    template_dynamic_hhn(3, 750, 100, [25] * 3, separate=True, ccore_flag=True)


def two_sync_ensembles():
    template_dynamic_hhn(4, 400, 200, [25, 25, 50, 50], separate=True, ccore_flag=False)
    template_dynamic_hhn(4, 800, 200, [25, 25, 50, 50], separate=True, ccore_flag=True)


def ten_oscillators_stimulated_desync():
    params = hhn_parameters()
    params.w1 = 0
    params.w2 = 0
    params.w3 = 0

    stumulus = [25, 25, 25, 25, 25, 11, 11, 11, 11, 11]

    template_dynamic_hhn(10, 750, 100, stumulus, params, separate=True, ccore_flag=False)
    template_dynamic_hhn(10, 750, 100, stumulus, params, separate=True, ccore_flag=True)


def ten_oscillators_stimulated_sync():
    params = hhn_parameters()
    params.w1 = 0.1
    params.w2 = 0.0
    params.w3 = 0

    stumulus = [25, 25, 25, 25, 25, 27, 27, 27, 27, 27]

    template_dynamic_hhn(10, 750, 100, stumulus, params, separate=True, ccore_flag=False)
    template_dynamic_hhn(10, 750, 100, stumulus, params, separate=True, ccore_flag=True)


def ten_oscillators_stimulated_partial_sync():
    params = hhn_parameters()
    params.w1 = 0.1
    params.w2 = 5.0
    params.w3 = 0

    stimulus = [25, 25, 25, 25, 25, 11, 11, 11, 11, 11]
    template_dynamic_hhn(10, 750, 200, stimulus, params, separate=True, ccore_flag=False)
    template_dynamic_hhn(10, 750, 200, stimulus, params, separate=True, ccore_flag=True)
    

def six_oscillators_mix_2_stimulated():
    params = hhn_parameters()
    params.deltah = 400

    stimulus = [25, 25, 25, 47, 47, 47]
    template_dynamic_hhn(6, 1200, 600, stimulus, params, separate=True, ccore_flag=False)
    template_dynamic_hhn(6, 2400, 600, stimulus, params, separate=True, ccore_flag=True)


def six_oscillators_mix_3_stimulated():
    params = hhn_parameters()
    params.deltah = 400

    stimulus = [0, 0, 25, 25, 47, 47]
    template_dynamic_hhn(6, 1200, 600, stimulus, params, separate=True, ccore_flag=False)
    template_dynamic_hhn(6, 2400, 600, stimulus, params, separate=True, ccore_flag=True)


def three_sync_ensembles():
    params = hhn_parameters()
    params.deltah = 400

    stimulus = [25, 26, 25, 25, 26, 45, 46, 45, 44, 45, 65, 65, 65, 64, 66]
    separate = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]
    num_osc = len(stimulus)
    template_dynamic_hhn(num_osc, 2400, 600, stimulus, params, separate=separate, ccore_flag=True)


def four_ensembles_80_oscillators():
    params = hhn_parameters()
    params.deltah = 650
    params.w1 = 0.1
    params.w2 = 9.0
    params.w3 = 5.0
    params.threshold = -10
    
    expected_ensembles = []
    stimulus = []
    
    base_stimulus = 10
    step_stimulus = 10
    amount_ensebles = 4
    region_size = 20
    for i in range(amount_ensebles):
        expected_ensembles += [ [i for i in range(region_size * i, region_size * i + region_size)] ]
        stimulus += [ base_stimulus + step_stimulus * i ] * region_size
    
    template_dynamic_hhn(len(stimulus), 4000, 1000, stimulus, params, separate=expected_ensembles, ccore_flag=True)


one_oscillator_unstimulated()
one_oscillator_stimulated()
three_oscillators_stimulated()
two_sync_ensembles()
ten_oscillators_stimulated_desync()
ten_oscillators_stimulated_sync()
ten_oscillators_stimulated_partial_sync()
six_oscillators_mix_2_stimulated()
six_oscillators_mix_3_stimulated()
three_sync_ensembles()
four_ensembles_80_oscillators()
