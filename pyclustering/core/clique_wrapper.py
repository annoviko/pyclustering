"""!

@brief CCORE Wrapper for CLIQUE algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from ctypes import c_double, c_size_t, POINTER

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.pyclustering_package import pyclustering_package, package_builder, package_extractor


class clique_package_indexer:
    CLIQUE_PACKAGE_INDEX_CLUSTERS = 0
    CLIQUE_PACKAGE_INDEX_NOISE = 1
    CLIQUE_PACKAGE_INDEX_LOGICAL_LOCATION = 2
    CLIQUE_PACKAGE_INDEX_MAX_CORNER = 3
    CLIQUE_PACKAGE_INDEX_MIN_CORNER = 4
    CLIQUE_PACKAGE_INDEX_BLOCK_POINTS = 5


def clique(sample, intervals, threshold):
    pointer_data = package_builder(sample, c_double).create()

    ccore = ccore_library.get()

    ccore.clique_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.clique_algorithm(pointer_data, c_size_t(intervals), c_size_t(threshold))

    results = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    if isinstance(results, bytes):
        raise RuntimeError(results.decode('utf-8'))

    return (results[clique_package_indexer.CLIQUE_PACKAGE_INDEX_CLUSTERS],
            results[clique_package_indexer.CLIQUE_PACKAGE_INDEX_NOISE],
            results[clique_package_indexer.CLIQUE_PACKAGE_INDEX_LOGICAL_LOCATION],
            results[clique_package_indexer.CLIQUE_PACKAGE_INDEX_MAX_CORNER],
            results[clique_package_indexer.CLIQUE_PACKAGE_INDEX_MIN_CORNER],
            results[clique_package_indexer.CLIQUE_PACKAGE_INDEX_BLOCK_POINTS])
