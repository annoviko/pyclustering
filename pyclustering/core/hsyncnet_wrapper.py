"""!

@brief CCORE Wrapper for hsyncnet oscillatory based clustering algorithm.

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

from pyclustering.core.wrapper import *;
from pyclustering.core.pyclustering_package import package_builder


def hsyncnet_create_network(sample, number_clusters, initial_phases, initial_neighbors, increase_persent):
    data_package = package_builder(sample, c_double).create();
    
    ccore = ccore_library.get();
    ccore.hsyncnet_create_network.restype = POINTER(c_void_p);
    pointer_network = ccore.hsyncnet_create_network(data_package, c_uint(number_clusters), c_uint(initial_phases), c_uint(initial_neighbors), c_double(increase_persent));
    
    return pointer_network;


def hsyncnet_destroy_network(pointer_network):
    ccore = ccore_library.get();
    ccore.hsyncnet_destroy_network(pointer_network);


def hsyncnet_process(network_pointer, order, solution, collect_dynamic):
    ccore = ccore_library.get();
    ccore.hsyncnet_process.restype = POINTER(c_void_p);
    return ccore.hsyncnet_process(network_pointer, c_double(order), c_uint(solution), c_bool(collect_dynamic));


def hsyncnet_analyser_destroy(pointer_analyser):
    ccore = ccore_library.get();
    ccore.syncnet_analyser_destroy(pointer_analyser);