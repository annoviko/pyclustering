"""!

@brief CCORE Wrapper for OPTICS algorithm.

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


class optics_package_indexer:
    OPTICS_PACKAGE_INDEX_CLUSTERS = 0
    OPTICS_PACKAGE_INDEX_NOISE = 1
    OPTICS_PACKAGE_INDEX_ORDERING = 2
    OPTICS_PACKAGE_INDEX_RADIUS = 3
    OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_INDEX = 4
    OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_CORE_DISTANCE = 5
    OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_REACHABILITY_DISTANCE = 6


def optics(sample, radius, minimum_neighbors, amount_clusters, data_type):
    amount = amount_clusters
    if amount is None:
        amount = 0

    pointer_data = package_builder(sample, c_double).create()
    c_data_type = convert_data_type(data_type)
    
    ccore = ccore_library.get()
    
    ccore.optics_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.optics_algorithm(pointer_data, c_double(radius), c_size_t(minimum_neighbors), c_size_t(amount), c_data_type)

    results = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    return (results[optics_package_indexer.OPTICS_PACKAGE_INDEX_CLUSTERS], 
            results[optics_package_indexer.OPTICS_PACKAGE_INDEX_NOISE], 
            results[optics_package_indexer.OPTICS_PACKAGE_INDEX_ORDERING],
            results[optics_package_indexer.OPTICS_PACKAGE_INDEX_RADIUS][0],
            results[optics_package_indexer.OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_INDEX],
            results[optics_package_indexer.OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_CORE_DISTANCE],
            results[optics_package_indexer.OPTICS_PACKAGE_INDEX_OPTICS_OBJECTS_REACHABILITY_DISTANCE])