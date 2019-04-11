"""!

@brief CCORE Wrapper for Fuzzy C-Means algorithm.

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