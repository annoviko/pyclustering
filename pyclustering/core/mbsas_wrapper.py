"""!

@brief CCORE Wrapper for MBSAS algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_double, c_size_t, POINTER;

from pyclustering.core.wrapper import ccore_library;
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder;


def mbsas(sample, amount, threshold, metric_pointer):
    pointer_data = package_builder(sample, c_double).create();

    ccore = ccore_library.get();

    ccore.mbsas_algorithm.restype = POINTER(pyclustering_package);
    package = ccore.mbsas_algorithm(pointer_data, c_size_t(amount), c_double(threshold), metric_pointer);

    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);

    return result[0], result[1];