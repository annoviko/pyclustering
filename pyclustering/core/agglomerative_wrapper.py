"""!

@brief CCORE Wrapper for agglomerative algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from ctypes import c_size_t, c_double, POINTER;

from pyclustering.core.wrapper import ccore_library;
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder;

def agglomerative_algorithm(data, number_clusters, link):
    pointer_data = package_builder(data, c_double).create();

    ccore = ccore_library.get();
    ccore.agglomerative_algorithm.restype = POINTER(pyclustering_package);
    package = ccore.agglomerative_algorithm(pointer_data, c_size_t(number_clusters), c_size_t(link));

    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);

    return result;
