"""!

@brief CCORE Wrapper for Elbow method.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_double, c_longlong, c_size_t, POINTER

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.pyclustering_package import pyclustering_package, package_builder, package_extractor

from enum import IntEnum


class elbow_package_indexer:
    ELBOW_PACKAGE_INDEX_AMOUNT = 0
    ELBOW_PACKAGE_INDEX_WCE = 1


class elbow_center_initializer(IntEnum):
    KMEANS_PLUS_PLUS = 0
    RANDOM = 1


def elbow(sample, kmin, kmax, kstep, initializer, random_state):
    random_state = random_state or -1
    pointer_data = package_builder(sample, c_double).create()

    ccore = ccore_library.get()
    if initializer == elbow_center_initializer.KMEANS_PLUS_PLUS:
        ccore.elbow_method_ikpp.restype = POINTER(pyclustering_package)
        package = ccore.elbow_method_ikpp(pointer_data, c_size_t(kmin), c_size_t(kmax), c_size_t(kstep), c_longlong(random_state))
    elif initializer == elbow_center_initializer.RANDOM:
        ccore.elbow_method_irnd.restype = POINTER(pyclustering_package)
        package = ccore.elbow_method_irnd(pointer_data, c_size_t(kmin), c_size_t(kmax), c_size_t(kstep), c_longlong(random_state))
    else:
        raise ValueError("Not supported type of center initializer '" + str(initializer) + "'.")

    results = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    if isinstance(results, bytes):
        raise RuntimeError(results.decode('utf-8'))

    return (results[elbow_package_indexer.ELBOW_PACKAGE_INDEX_AMOUNT][0],
            results[elbow_package_indexer.ELBOW_PACKAGE_INDEX_WCE])
