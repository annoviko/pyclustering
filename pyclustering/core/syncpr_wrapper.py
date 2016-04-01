"""!

@brief CCORE Wrapper for oscillatory neural network for pattern recognition (syncpr).

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

def pack_pattern(pattern):
    c_pattern = (c_int * len(pattern))();
    c_pattern[:] = pattern[:];

    package = pyclustering_package();
    package.size = len(pattern);
    package.type = pyclustering_type_data.PYCLUSTERING_TYPE_INT;
    package.data = cast(c_pattern, POINTER(c_void_p));
    
    return package;
    

def syncpr_create(num_osc, increase_strength1, increase_strength2):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    pointer_network = ccore.syncpr_create(c_uint(num_osc), c_double(increase_strength1), c_double(increase_strength2));
    
    return pointer_network;


def syncpr_destroy(pointer_network):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.syncpr_destroy(pointer_network);


def syncpr_get_size(pointer_network):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.syncpr_get_size(pointer_network);
    

def syncpr_train(pointer_network, patterns):
    c_patterns = (POINTER(pyclustering_package) * len(patterns))();
    
    for i in range(len(patterns)):
        c_patterns[i] = pointer(pack_pattern(patterns[i]));
    
    package = pyclustering_package();
    package.size = len(patterns);
    package.type = pyclustering_type_data.PYCLUSTERING_TYPE_LIST;
    package.data = cast(c_patterns, POINTER(c_void_p));
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.syncpr_train(pointer_network, pointer(package));    
    
    
def syncpr_simulate_static(pointer_network, steps, time, pattern, solution, collect_dynamic):
    package_pattern = pack_pattern(pattern);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.syncpr_simulate_static(pointer_network, c_uint(steps), c_double(time), pointer(package_pattern), c_uint(solution), c_bool(collect_dynamic));


def syncpr_simulate_dynamic(pointer_network, pattern, order, solution, collect_dynamic, step):
    package_pattern = pack_pattern(pattern);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.syncpr_simulate_dynamic(pointer_network, pointer(package_pattern), c_double(order), c_uint(solution), c_bool(collect_dynamic), c_double(step));


def syncpr_memory_order(pointer_network, pattern):
    package_pattern = pack_pattern(pattern);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    
    ccore.syncpr_memory_order.restype = c_double;
    return ccore.syncpr_memory_order(pointer_network, pointer(package_pattern));


def syncpr_dynamic_get_size(pointer_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.syncpr_dynamic_get_size(pointer_dynamic);


def syncpr_dynamic_destroy(pointer_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.syncpr_dynamic_destroy(pointer_dynamic);


def syncpr_dynamic_allocate_sync_ensembles(pointer_dynamic, tolerance):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.syncpr_dynamic_allocate_sync_ensembles(pointer_dynamic, c_double(tolerance));
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def syncpr_dynamic_get_output(pointer_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.syncpr_dynamic_get_output(pointer_dynamic);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def syncpr_dynamic_get_time(pointer_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.syncpr_dynamic_get_time(pointer_dynamic);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;