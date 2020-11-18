"""!

@brief CCORE Wrapper for K-Medoids algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_double, c_size_t, POINTER

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.converter import convert_data_type
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder


def kmedoids(sample, medoids, tolerance, itermax, metric_pointer, data_type):
    pointer_data = package_builder(sample, c_double).create()
    medoids_package = package_builder(medoids, c_size_t).create()
    c_data_type = convert_data_type(data_type)
    
    ccore = ccore_library.get()
    
    ccore.kmedoids_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.kmedoids_algorithm(pointer_data, medoids_package, c_double(tolerance), c_size_t(itermax), metric_pointer, c_data_type)
    
    result = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    return result[0], result[1]
