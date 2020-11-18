"""!

@brief Examples of usage and demonstration of abilities of Oscillatory Neural Network based on Kuramoto model and Landau-Stuart oscillator.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from pyclustering.nnet import conn_type;
from pyclustering.nnet.fsync import fsync_network, fsync_visualizer;


def template_dynamic_sync(num_osc, steps, time, frequency = 1.0, radius = 1.0, coupling = 1.0, conn = conn_type.ALL_TO_ALL, collect_dyn = True):
    network = fsync_network(num_osc, frequency, radius, coupling, type_conn = conn);

    fsync_output_dynamic = network.simulate(steps, time, collect_dynamic = collect_dyn);
    fsync_visualizer.show_output_dynamic(fsync_output_dynamic);
    return network;


def one_landau_stuart_oscillators():
    template_dynamic_sync(1, 100, 20, 1.0, 1.0, 1.0);

def five_oscillators_all_to_all_structure():
    template_dynamic_sync(5, 100, 20, 1.0, 1.0, 1.0, conn_type.ALL_TO_ALL);

def twenty_oscillators_all_to_all_structure():
    template_dynamic_sync(20, 100, 20, 1.0, 1.0, 1.0, conn_type.ALL_TO_ALL);

def twenty_oscillators_all_to_all_structure_weak_coupling():
    template_dynamic_sync(20, 100, 20, 1.0, 1.0, 0.01, conn_type.ALL_TO_ALL);

def five_oscillators_grid_four_structure():
    template_dynamic_sync(9, 100, 20, 1.0, 1.0, 1.0, conn_type.GRID_FOUR);

def five_oscillators_bidir_structure():
    template_dynamic_sync(5, 100, 20, 1.0, 1.0, 1.0, conn_type.LIST_BIDIR);

def two_oscillators_different_frequency():
    template_dynamic_sync(2, 100, 20, [1.0, 2.0], 1.0, 1.0, conn_type.ALL_TO_ALL);

def two_oscillators_different_radius():
    template_dynamic_sync(2, 100, 20, 1.0, [1.0, 4.0], 1.0, conn_type.ALL_TO_ALL);

def three_oscillators_different_properties():
    template_dynamic_sync(3, 100, 20, [1.0, 1.3, 1.6], [1.0, 4.0, 2.0], 1.0, conn_type.ALL_TO_ALL);

def three_oscillators_different_properties_weak_coupling():
    template_dynamic_sync(3, 100, 20, [1.0, 1.1, 1.2], [1.0, 4.0, 2.0], 0.1, conn_type.ALL_TO_ALL);


one_landau_stuart_oscillators();
five_oscillators_all_to_all_structure();
twenty_oscillators_all_to_all_structure();
twenty_oscillators_all_to_all_structure_weak_coupling();
five_oscillators_grid_four_structure();
five_oscillators_bidir_structure();
two_oscillators_different_frequency();
two_oscillators_different_radius();
three_oscillators_different_properties();
three_oscillators_different_properties_weak_coupling();