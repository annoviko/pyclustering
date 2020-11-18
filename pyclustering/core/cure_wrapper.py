"""!

@brief CCORE Wrapper for CURE algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from ctypes import c_double, c_size_t, POINTER, c_void_p

from pyclustering.core.wrapper import ccore_library;
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder;


def cure_algorithm(sample, number_clusters, number_represent_points, compression):
    pointer_data = package_builder(sample, c_double).create();
    
    ccore = ccore_library.get();
    ccore.cure_algorithm.restype = POINTER(c_void_p);
    cure_data_pointer = ccore.cure_algorithm(pointer_data, c_size_t(number_clusters), c_size_t(number_represent_points), c_double(compression));
    
    return cure_data_pointer;


def cure_data_destroy(cure_data_pointer):
    ccore = ccore_library.get();
    ccore.cure_data_destroy(cure_data_pointer);


def cure_get_clusters(cure_data_pointer):
    ccore = ccore_library.get();
    
    ccore.cure_get_clusters.restype = POINTER(pyclustering_package);
    package = ccore.cure_get_clusters(cure_data_pointer);
    
    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);
    
    return result;


def cure_get_representors(cure_data_pointer):
    ccore = ccore_library.get();
    
    ccore.cure_get_representors.restype = POINTER(pyclustering_package);
    package = ccore.cure_get_representors(cure_data_pointer);
    
    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);
    
    return result;


def cure_get_means(cure_data_pointer):
    ccore = ccore_library.get();
    
    ccore.cure_get_means.restype = POINTER(pyclustering_package);
    package = ccore.cure_get_means(cure_data_pointer);
    
    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);
    
    return result;