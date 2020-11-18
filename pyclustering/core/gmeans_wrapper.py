"""!

@brief CCORE Wrapper for G-Means algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from ctypes import c_double, c_size_t, c_longlong, POINTER

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder


def gmeans(sample, kinit, tolerance, repeat, kmax, random_state):
    random_state = random_state or -1
    pointer_data = package_builder(sample, c_double).create()

    ccore = ccore_library.get()

    ccore.gmeans_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.gmeans_algorithm(pointer_data, c_size_t(kinit), c_double(tolerance), c_size_t(repeat), c_longlong(kmax), c_longlong(random_state))

    result = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    return result[0], result[1], result[2][0]
