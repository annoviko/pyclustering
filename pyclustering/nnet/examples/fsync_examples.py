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

from pyclustering.nnet import solve_type, conn_type;
from pyclustering.nnet.fsync import fsync_network, fsync_visualizer;


def template_dynamic_sync(num_osc, steps, time, conn = conn_type.ALL_TO_ALL, type_solution = solve_type.RK4, collect_dyn = True):
    network = fsync_network(num_osc, type_conn = conn);

    fsync_output_dynamic = network.simulate_static(steps, time, collect_dynamic = collect_dyn, solution = type_solution);

    fsync_visualizer.show_output_dynamic(fsync_output_dynamic);
    return network;


def all_to_all_10_oscillators():
    template_dynamic_sync(10, 100, 5);


all_to_all_10_oscillators();