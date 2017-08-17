"""!

@brief Examples of usage and demonstration of abilities of Oscillatory Neural Network based on Kuramoto model and Landau-Stuart oscillator.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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

from pyclustering.nnet import conn_type;
from pyclustering.nnet.fsync import fsync_network, fsync_visualizer;


def template_dynamic_sync(num_osc, steps, time, frequency = 1.0, radius = 1.0, coupling = 1.0, conn = conn_type.ALL_TO_ALL, collect_dyn = True):
    network = fsync_network(num_osc, frequency, radius, coupling, type_conn = conn);

    fsync_output_dynamic = network.simulate_static(steps, time, collect_dynamic = collect_dyn);

    fsync_visualizer.show_output_dynamic(fsync_output_dynamic);
    return network;


def one_landau_stuart_oscillators():
    template_dynamic_sync(1, 100, 20, 1.0, 1.0, 1.0);

def five_oscillators_all_to_all_structure():
    template_dynamic_sync(5, 100, 20, 1.0, 1.0, 1.0, conn_type.ALL_TO_ALL);

def twenty_oscillators_all_to_all_structure():
    template_dynamic_sync(20, 100, 20, 1.0, 1.0, 1.0, conn_type.ALL_TO_ALL);

def five_oscillators_grid_four_structure():
    template_dynamic_sync(9, 100, 20, 1.0, 1.0, 1.0, conn_type.GRID_FOUR);

def five_oscillators_bidir_structure():
    template_dynamic_sync(5, 100, 20, 1.0, 1.0, 1.0, conn_type.LIST_BIDIR);


one_landau_stuart_oscillators();
five_oscillators_all_to_all_structure();
twenty_oscillators_all_to_all_structure();
five_oscillators_grid_four_structure();
five_oscillators_bidir_structure();