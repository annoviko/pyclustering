"""!

@brief CCORE Wrapper for Local Excitatory Global Inhibitory Oscillatory Network (LEGION)

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

from pyclustering.core.wrapper import *
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder


class c_legion_parameters(Structure):
    _fields_ = [
        ("eps",                 c_double),
        ("alpha",               c_double),
        ("gamma",               c_double),
        ("betta",               c_double),
        ("lamda",               c_double),
        ("teta",                c_double),
        ("teta_x",              c_double),
        ("teta_p",              c_double),
        ("teta_xz",             c_double),
        ("teta_zx",             c_double),
        ("T",                   c_double),
        ("mu",                  c_double),
        ("Wz",                  c_double),
        ("Wt",                  c_double),
        ("fi",                  c_double),
        ("ro",                  c_double),
        ("I",                   c_double),
        ("ENABLE_POTENTIONAL",  c_bool)
    ];


def legion_create(size, conn_type, params):
    ccore = ccore_library.get();
    
    c_params = c_legion_parameters();
    c_params.eps = params.eps;
    c_params.alpha = params.alpha;
    c_params.gamma = params.gamma;
    c_params.betta = params.betta;
    c_params.lamda = params.lamda;
    c_params.teta = params.teta;
    c_params.teta_x = params.teta_x;
    c_params.teta_p = params.teta_p;
    c_params.teta_xz = params.teta_xz;
    c_params.T = params.T;
    c_params.mu = params.mu;
    c_params.Wz = params.Wz;
    c_params.Wt = params.Wt;
    c_params.fi = params.fi;
    c_params.ro = params.ro;
    c_params.I = params.I;
    c_params.ENABLE_POTENTIONAL = params.ENABLE_POTENTIONAL;
    
    ccore.legion_create.restype = POINTER(c_void_p);
    legion_network_pointer = ccore.legion_create(c_uint(size), c_uint(conn_type), pointer(c_params));
    
    return legion_network_pointer;


def legion_destroy(legion_network_pointer):
    ccore = ccore_library.get();
    ccore.legion_destroy(legion_network_pointer);
    
    
def legion_simulate(legion_network_pointer, steps, time, solver, collect_dynamic, stimulus):
    ccore = ccore_library.get();
    
    c_stimulus = package_builder(stimulus, c_double).create();
    
    ccore.legion_simulate.restype = POINTER(c_void_p);
    return ccore.legion_simulate(legion_network_pointer, c_uint(steps), c_double(time), c_uint(solver), c_bool(collect_dynamic), c_stimulus);


def legion_get_size(legion_network_pointer):
    ccore = ccore_library.get();
    ccore.legion_get_size.restype = c_size_t;
    return ccore.legion_get_size(legion_network_pointer);


def legion_dynamic_destroy(legion_dynamic_pointer):
    ccore = ccore_library.get();
    ccore.legion_dynamic_destroy(legion_dynamic_pointer);


def legion_dynamic_get_output(legion_dynamic_pointer):
    ccore = ccore_library.get();
    
    ccore.legion_dynamic_get_output.restype = POINTER(pyclustering_package);
    package = ccore.legion_dynamic_get_output(legion_dynamic_pointer);
    
    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);
    
    return result;


def legion_dynamic_get_inhibitory_output(legion_dynamic_pointer):
    ccore = ccore_library.get();
    
    ccore.legion_dynamic_get_inhibitory_output.restype = POINTER(pyclustering_package);
    package = ccore.legion_dynamic_get_inhibitory_output(legion_dynamic_pointer);
    
    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);
    
    return result;


def legion_dynamic_get_time(legion_dynamic_pointer):
    ccore = ccore_library.get();
    
    ccore.legion_dynamic_get_time.restype = POINTER(pyclustering_package);
    package = ccore.legion_dynamic_get_time(legion_dynamic_pointer);
    
    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);
    
    return result;


def legion_dynamic_get_size(legion_dynamic_pointer):
    ccore = ccore_library.get();
    ccore.legion_dynamic_get_size.restype = c_size_t;
    return ccore.legion_dynamic_get_size(legion_dynamic_pointer);
    