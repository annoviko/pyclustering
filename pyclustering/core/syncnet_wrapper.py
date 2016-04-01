"""!

@brief CCORE Wrapper for syncnet clustering algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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


def syncnet_create_network(sample, radius, initial_phases, enable_conn_weight):
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    pointer_network = ccore.syncnet_create_network(pointer_data, c_double(radius), c_uint(initial_phases), c_bool(enable_conn_weight));
    
    return pointer_network;


def syncnet_destroy_network(pointer_network):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.syncnet_destroy_network(pointer_network);


def syncnet_process(network_pointer, order, solution, collect_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.syncnet_process(network_pointer, c_double(order), c_uint(solution), c_bool(collect_dynamic));


def syncnet_analyser_destroy(pointer_analyser):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.syncnet_analyser_destroy(pointer_analyser);
    