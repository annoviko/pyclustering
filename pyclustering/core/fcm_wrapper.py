"""!

@brief CCORE Wrapper for Fuzzy C-Means algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_double, c_size_t, POINTER

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder


class fcm_package_indexer:
    INDEX_CLUSTERS = 0
    INDEX_CENTERS = 1
    INDEX_MEMBERSHIP = 2


def fcm_algorithm(sample, centers, m, tolerance, itermax):
    pointer_data = package_builder(sample, c_double).create()
    pointer_centers = package_builder(centers, c_double).create()

    ccore = ccore_library.get()

    ccore.fcm_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.fcm_algorithm(pointer_data, pointer_centers, c_double(m), c_double(tolerance), c_size_t(itermax))

    result = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    return result