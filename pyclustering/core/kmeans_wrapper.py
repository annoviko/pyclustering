"""!

@brief CCORE Wrapper for K-Means algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_double, c_bool, c_size_t, POINTER

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder


def kmeans(sample, centers, tolerance, itermax, observe, metric_pointer):
    pointer_data = package_builder(sample, c_double).create()
    pointer_centers = package_builder(centers, c_double).create()
    
    ccore = ccore_library.get()
    
    ccore.kmeans_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.kmeans_algorithm(pointer_data, pointer_centers, c_double(tolerance), c_size_t(itermax),
                                     c_bool(observe), metric_pointer)
    
    result = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)
    
    return result