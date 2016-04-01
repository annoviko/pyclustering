"""!

@brief CCORE Wrapper for Pulse Coupled Neural Network (PCNN)

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

class c_pcnn_parameters(Structure):   
    _fields_ = [("VF", c_double),
                ("VL", c_double),
                ("VT", c_double),
                ("AF", c_double),
                ("AL", c_double),
                ("AT", c_double),
                ("W", c_double),
                ("M", c_double),
                ("B", c_double),
                ("FAST_LINKING", c_bool)];


def pcnn_create(size, conn_type, height, width, params):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    
    c_parameters = c_pcnn_parameters();
    c_parameters.VF = params.VF;
    c_parameters.VL = params.VL;
    c_parameters.VT = params.VT;
    c_parameters.AF = params.AF;
    c_parameters.AL = params.AL;
    c_parameters.AT = params.AT;
    c_parameters.W = params.W;
    c_parameters.M = params.M;
    c_parameters.FAST_LINKING = params.FAST_LINKING;
    
    pcnn_pointer = ccore.pcnn_create(c_uint(size), c_uint(conn_type), c_uint(height), c_uint(width), pointer(c_parameters));
    return pcnn_pointer;
    

def pcnn_destroy(network_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.pcnn_destroy(network_pointer);


def pcnn_simulate(network_pointer, steps, stimulus):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    
    c_stimulus = (c_double * len(stimulus))();
    c_stimulus[:] = stimulus[:];
    
    package = pyclustering_package();
    package.size = len(stimulus);
    package.type = pyclustering_type_data.PYCLUSTERING_TYPE_DOUBLE;
    package.data = cast(c_stimulus, POINTER(c_void_p));
    
    return ccore.pcnn_simulate(network_pointer, c_uint(steps), pointer(package));


def pcnn_get_size(network_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.pcnn_get_size(network_pointer);


def pcnn_dynamic_destroy(dynamic_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.pcnn_dynamic_destroy(dynamic_pointer);
    

def pcnn_dynamic_allocate_sync_ensembles(dynamic_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.pcnn_dynamic_allocate_sync_ensembles(dynamic_pointer);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def pcnn_dynamic_allocate_spike_ensembles(dynamic_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.pcnn_dynamic_allocate_spike_ensembles(dynamic_pointer);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def pcnn_dynamic_allocate_time_signal(dynamic_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.pcnn_dynamic_allocate_time_signal(dynamic_pointer);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def pcnn_dynamic_get_output(dynamic_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.pcnn_dynamic_get_output(dynamic_pointer);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def pcnn_dynamic_get_time(dynamic_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.pcnn_dynamic_get_time(dynamic_pointer);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;

def pcnn_dynamic_get_size(dynamic_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    return ccore.pcnn_dynamic_get_size(dynamic_pointer);
