"""!

@brief CCORE Wrapper for Hodgkin-Huxley oscillatory network for image segmentation.

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
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder;


class c_hhn_params(Structure):
    _fields_ = [
        ("nu",                  c_double),
        ("gNa",                 c_double),
        ("gK",                  c_double),
        ("gL",                  c_double),
        ("vNa",                 c_double),
        ("vK",                  c_double),
        ("vL",                  c_double),
        ("vRest",               c_double),
        ("Icn1",                c_double),
        ("Icn2",                c_double),
        ("Vsyninh",             c_double),
        ("Vsynexc",             c_double),
        ("alfa_inhibitory",     c_double),
        ("betta_inhibitory",    c_double),
        ("alfa_excitatory",     c_double),
        ("betta_excitatory",    c_double),
        ("w1",                  c_double),
        ("w2",                  c_double),
        ("w3",                  c_double),
        ("deltah",              c_double),
        ("threshold",           c_double),
        ("eps",                 c_double),
    ];


def hhn_create(size, params):
    c_params = c_hhn_params();

    c_params.nu                 = params.nu;
    c_params.gNa                = params.gNa;
    c_params.gK                 = params.gK;
    c_params.gL                 = params.gL;
    c_params.vNa                = params.vNa;
    c_params.vK                 = params.vK;
    c_params.vL                 = params.vL;
    c_params.vRest              = params.vRest;
    c_params.Icn1               = params.Icn1;
    c_params.Icn2               = params.Icn2;
    c_params.Vsyninh            = params.Vsyninh;
    c_params.Vsynexc            = params.Vsynexc;
    c_params.alfa_inhibitory    = params.alfa_inhibitory;
    c_params.betta_inhibitory   = params.betta_inhibitory;
    c_params.alfa_excitatory    = params.alfa_excitatory;
    c_params.betta_excitatory   = params.betta_excitatory;
    c_params.w1                 = params.w1;
    c_params.w2                 = params.w2;
    c_params.w3                 = params.w3;
    c_params.deltah             = params.deltah;
    c_params.threshold          = params.threshold;
    c_params.eps                = params.eps;

    ccore = ccore_library.get();

    ccore.hhn_create.restype = POINTER(c_void_p);
    hhn_network_pointer = ccore.hhn_create(c_size_t(size), pointer(c_params));
    return hhn_network_pointer;


def hhn_destroy(hhn_network_pointer):
    ccore = ccore_library.get();
    ccore.hhn_destroy(hhn_network_pointer);


def hhn_dynamic_create(collect_membrane, collect_active_cond_sodium, collect_inactive_cond_sodium, collect_active_cond_potassium):
    ccore = ccore_library.get();

    ccore.hhn_dynamic_create.restype = POINTER(c_void_p);
    hhn_dynamic_pointer = ccore.hhn_dynamic_create(c_bool(collect_membrane),
                                                   c_bool(collect_active_cond_sodium),
                                                   c_bool(collect_inactive_cond_sodium),
                                                   c_bool(collect_active_cond_potassium));
    return hhn_dynamic_pointer;


def hhn_dynamic_destroy(hhn_dynamic_pointer):
    ccore = ccore_library.get();
    ccore.hhn_dynamic_destroy(hhn_dynamic_pointer);


def hhn_simulate(hhn_network_pointer, steps, time, solution, stimulus, ccore_hhn_dynamic_pointer):
    ccore = ccore_library.get();

    c_stimulus = package_builder(stimulus, c_double).create();
    ccore.hhn_simulate(hhn_network_pointer,
                       c_size_t(steps),
                       c_double(time),
                       c_size_t(solution),
                       c_stimulus,
                       ccore_hhn_dynamic_pointer);


def hhn_dynamic_get_peripheral_evolution(ccore_hhn_dynamic_pointer, index_collection):
    ccore = ccore_library.get();

    ccore.hhn_dynamic_get_peripheral_evolution.restype = POINTER(pyclustering_package);
    dynamic_package = ccore.hhn_dynamic_get_peripheral_evolution(ccore_hhn_dynamic_pointer, c_size_t(index_collection));

    result = package_extractor(dynamic_package).extract();
    ccore.free_pyclustering_package(dynamic_package);

    return result;


def hhn_dynamic_get_central_evolution(ccore_hhn_dynamic_pointer, index_collection):
    ccore = ccore_library.get();

    ccore.hhn_dynamic_get_central_evolution.restype = POINTER(pyclustering_package);
    dynamic_package = ccore.hhn_dynamic_get_central_evolution(ccore_hhn_dynamic_pointer, c_size_t(index_collection));

    result = package_extractor(dynamic_package).extract();
    ccore.free_pyclustering_package(dynamic_package);

    return result;


def hhn_dynamic_get_time(ccore_hhn_dynamic_pointer):
    ccore = ccore_library.get();

    ccore.hhn_dynamic_get_time.restype = POINTER(pyclustering_package);
    dynamic_package = ccore.hhn_dynamic_get_time(ccore_hhn_dynamic_pointer);

    result = package_extractor(dynamic_package).extract();
    ccore.free_pyclustering_package(dynamic_package);

    return result;


def hhn_dynamic_write(ccore_hhn_dynamic_pointer, filename):
    ccore = ccore_library.get();

    byte_filename = filename.encode('utf-8');
    ccore.hhn_dynamic_write(ccore_hhn_dynamic_pointer, c_char_p(byte_filename));


def hhn_dynamic_read(filename):
    ccore = ccore_library.get();

    byte_filename = filename.encode('utf-8');

    ccore.hhn_dynamic_read.restype = POINTER(c_void_p);
    hhn_dynamic_pointer = ccore.hhn_dynamic_read(byte_filename);

    return hhn_dynamic_pointer;