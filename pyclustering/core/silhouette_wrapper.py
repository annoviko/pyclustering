"""!

@brief CCORE Wrapper for Silhouette method and Silhouette K-Search algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from ctypes import c_double, c_longlong, c_size_t, POINTER

from pyclustering.core.converter import convert_data_type
from pyclustering.core.wrapper import ccore_library
from pyclustering.core.pyclustering_package import pyclustering_package, package_builder, package_extractor


class silhouette_ksearch_package_indexer:
    SILHOUETTE_KSEARCH_PACKAGE_INDEX_AMOUNT = 0
    SILHOUETTE_KSEARCH_PACKAGE_INDEX_SCORE = 1
    SILHOUETTE_KSEARCH_PACKAGE_INDEX_SCORES = 2


def silhoeutte(sample, clusters, pointer_metric, data_type):
    pointer_data = package_builder(sample, c_double).create()
    pointer_clusters = package_builder(clusters, c_size_t).create()
    c_data_type = convert_data_type(data_type)

    ccore = ccore_library.get()
    ccore.silhouette_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.silhouette_algorithm(pointer_data, pointer_clusters, pointer_metric, c_data_type)

    result = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    return result


def silhoeutte_ksearch(sample, kmin, kmax, allocator, random_state):
    random_state = random_state or -1
    pointer_data = package_builder(sample, c_double).create()

    ccore = ccore_library.get()
    ccore.silhouette_ksearch_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.silhouette_ksearch_algorithm(pointer_data, c_size_t(kmin), c_size_t(kmax), c_size_t(allocator), c_longlong(random_state))

    results = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    return (results[silhouette_ksearch_package_indexer.SILHOUETTE_KSEARCH_PACKAGE_INDEX_AMOUNT][0],
            results[silhouette_ksearch_package_indexer.SILHOUETTE_KSEARCH_PACKAGE_INDEX_SCORE][0],
            results[silhouette_ksearch_package_indexer.SILHOUETTE_KSEARCH_PACKAGE_INDEX_SCORES])
