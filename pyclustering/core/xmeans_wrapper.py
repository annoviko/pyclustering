"""!

@brief CCORE Wrapper for X-Means algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_double, c_longlong, c_size_t, c_uint, POINTER

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder


def xmeans(sample, centers, kmax, tolerance, criterion, alpha, beta, repeat, random_state, metric_pointer):
    random_state = random_state or -1
    pointer_data = package_builder(sample, c_double).create()
    pointer_centers = package_builder(centers, c_double).create()
    
    ccore = ccore_library.get()
    
    ccore.xmeans_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.xmeans_algorithm(pointer_data, pointer_centers, c_size_t(kmax), c_double(tolerance),
                                     c_uint(criterion), c_double(alpha), c_double(beta), c_size_t(repeat),
                                     c_longlong(random_state), metric_pointer)
    
    result = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)
    
    return result
