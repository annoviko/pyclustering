"""!

@brief CCORE Wrapper for DBSCAN algorithm.

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
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder


def dbscan(sample, eps, min_neighbors, data_type):
    pointer_data = package_builder(sample, c_double).create()
    c_data_type = convert_data_type(data_type)
    
    ccore = ccore_library.get()
    
    ccore.dbscan_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.dbscan_algorithm(pointer_data, c_double(eps), c_size_t(min_neighbors), c_data_type)

    list_of_clusters = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)
    
    noise = list_of_clusters[len(list_of_clusters) - 1]
    list_of_clusters.remove(noise)

    return list_of_clusters, noise