"""!

@brief CCORE Wrapper for Silhouette method and Silhouette K-Search algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""


from ctypes import c_double, c_size_t, POINTER

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


def silhoeutte_ksearch(sample, kmin, kmax, allocator):
    pointer_data = package_builder(sample, c_double).create()

    ccore = ccore_library.get()
    ccore.silhouette_ksearch_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.silhouette_ksearch_algorithm(pointer_data, c_size_t(kmin), c_size_t(kmax), c_size_t(allocator))

    results = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    return (results[silhouette_ksearch_package_indexer.SILHOUETTE_KSEARCH_PACKAGE_INDEX_AMOUNT][0],
            results[silhouette_ksearch_package_indexer.SILHOUETTE_KSEARCH_PACKAGE_INDEX_SCORE][0],
            results[silhouette_ksearch_package_indexer.SILHOUETTE_KSEARCH_PACKAGE_INDEX_SCORES])
