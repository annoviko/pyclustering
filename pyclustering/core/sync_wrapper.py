"""!

@brief CCORE Wrapper for oscillatory neural network based on Kuramoto model.

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

def sync_create_network(num_osc, weight, frequency, type_conn, initial_phases):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    pointer_network = ccore.sync_create_network(c_uint(num_osc), c_double(weight), c_double(frequency), c_uint(type_conn), c_uint(initial_phases));
    
    return pointer_network;


def sync_destroy_network(pointer_network):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.sync_destroy_network(pointer_network);


def sync_simulate_static(pointer_network, steps, time, solution, collect_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.sync_simulate_static(pointer_network, c_uint(steps), c_double(time), c_uint(solution), c_bool(collect_dynamic));


def sync_simulate_dynamic(pointer_network, order, solution, collect_dynamic, step, int_step, threshold_changes):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.sync_simulate_dynamic(pointer_network, c_double(order), c_uint(solution), c_bool(collect_dynamic), c_double(step), c_double(int_step), c_double(threshold_changes));


def sync_order(pointer_network):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.sync_order.restype = c_double;
    
    return ccore.sync_order(pointer_network);
    
    
def sync_local_order(pointer_network):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.sync_local_order.restype = c_double;
    
    return ccore.sync_local_order(pointer_network);


def sync_dynamic_get_size(pointer_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.sync_dynamic_get_size(pointer_dynamic);


def sync_dynamic_destroy(pointer_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.sync_dynamic_destroy(pointer_dynamic);


def sync_dynamic_allocate_sync_ensembles(pointer_dynamic, tolerance, iteration):
    if (iteration is None):
        iteration = sync_dynamic_get_size(pointer_dynamic) - 1;
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.sync_dynamic_allocate_sync_ensembles(pointer_dynamic, c_double(tolerance), c_size_t(iteration));
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def sync_dynamic_allocate_correlation_matrix(pointer_dynamic, iteration):
    analyse_iteration = iteration;
    if (analyse_iteration is None):
        analyse_iteration = sync_dynamic_get_size(pointer_dynamic) - 1;
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.sync_dynamic_allocate_correlation_matrix(pointer_dynamic, c_uint(analyse_iteration));
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def sync_dynamic_get_output(pointer_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.sync_dynamic_get_output(pointer_dynamic);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def sync_dynamic_get_time(pointer_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.sync_dynamic_get_time(pointer_dynamic);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;
