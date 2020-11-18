"""!

@brief CCORE Wrapper for TTSAS algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_double, POINTER;

from pyclustering.core.wrapper import ccore_library;
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder;


def ttsas(sample, threshold1, threshold2, metric_pointer):
    pointer_data = package_builder(sample, c_double).create();

    ccore = ccore_library.get();

    ccore.ttsas_algorithm.restype = POINTER(pyclustering_package);
    package = ccore.ttsas_algorithm(pointer_data, c_double(threshold1), c_double(threshold2), metric_pointer);

    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);

    return result[0], result[1];