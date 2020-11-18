"""!

@brief CCORE Wrapper for syncnet clustering algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from pyclustering.core.wrapper import *
from pyclustering.core.pyclustering_package import package_builder


def syncnet_create_network(sample, radius, initial_phases, enable_conn_weight):
    package_data = package_builder(sample, c_double).create()
    
    ccore = ccore_library.get()
    ccore.syncnet_create_network.restype = POINTER(c_void_p)
    pointer_network = ccore.syncnet_create_network(package_data, c_double(radius), c_bool(enable_conn_weight), c_uint(initial_phases))
    
    return pointer_network


def syncnet_destroy_network(pointer_network):
    ccore = ccore_library.get()
    ccore.syncnet_destroy_network(pointer_network)


def syncnet_process(network_pointer, order, solution, collect_dynamic):
    ccore = ccore_library.get()
    ccore.syncnet_process.restype = POINTER(c_void_p)
    return ccore.syncnet_process(network_pointer, c_double(order), c_uint(solution), c_bool(collect_dynamic))


def syncnet_analyser_destroy(pointer_analyser):
    ccore = ccore_library.get()
    ccore.syncnet_analyser_destroy(pointer_analyser)
    