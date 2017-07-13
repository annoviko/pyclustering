"""!

@brief Wrapper for CCORE library (part of this project).

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

from ctypes import *;

from pyclustering.core.definitions import *;


# API that is required for interaction with DLL.
def create_pointer_data(sample):
    "Allocates memory for representing input data for processing that is described by structure 'data_representation' and returns pointer this structure."
    
    "(in) sample    - dataset for processing."
    
    "Returns pointer to the data for processing."
    
    input_data = data_representation();
    input_data.number_objects = len(sample);
    input_data.dimension = len(sample[0]);
    
    pointer_objects = (POINTER(c_double) * input_data.number_objects)();

    for index in range(0, input_data.number_objects):
        point = (c_double * input_data.dimension)();
        for dimension in range(0, input_data.dimension):
            point[dimension] = sample[index][dimension];
            
        pointer_objects[index] = cast(point, POINTER(c_double));
       
    input_data.pointer_objects = cast(pointer_objects, POINTER(POINTER(c_double)));
    input_data = pointer(input_data);
    
    return input_data;


# Implemented algorithms.
"CCORE Interface for HSYNCNET oscillatory network"

def hsyncnet_create_network(sample, number_clusters, initial_phases, initial_neighbors, increase_persent):
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.hsyncnet_create_network.restype = POINTER(c_void_p);
    pointer_network = ccore.hsyncnet_create_network(pointer_data, c_uint(number_clusters), c_uint(initial_phases), c_uint(initial_neighbors), c_double(increase_persent));
    
    return pointer_network;


def hsyncnet_destroy_network(pointer_network):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.hsyncnet_destroy_network(pointer_network);


def hsyncnet_process(network_pointer, order, solution, collect_dynamic):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.hsyncnet_process.restype = POINTER(c_void_p);
    return ccore.hsyncnet_process(network_pointer, c_double(order), c_uint(solution), c_bool(collect_dynamic));


def hsyncnet_analyser_destroy(pointer_analyser):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.syncnet_analyser_destroy(pointer_analyser);

