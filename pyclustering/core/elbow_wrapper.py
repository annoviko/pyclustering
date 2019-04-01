"""!

@brief CCORE Wrapper for Elbow method.

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
from pyclustering.core.pyclustering_package import pyclustering_package, package_builder, package_extractor

from enum import IntEnum


class elbow_package_indexer:
    ELBOW_PACKAGE_INDEX_AMOUNT = 0
    ELBOW_PACKAGE_INDEX_WCE = 1


class elbow_center_initializer(IntEnum):
    KMEANS_PLUS_PLUS = 0
    RANDOM = 1


def elbow(sample, kmin, kmax, initializer):
    pointer_data = package_builder(sample, c_double).create()

    ccore = ccore_library.get()
    if initializer == elbow_center_initializer.KMEANS_PLUS_PLUS:
        ccore.elbow_method_ikpp.restype = POINTER(pyclustering_package)
        package = ccore.elbow_method_ikpp(pointer_data, c_size_t(kmin), c_size_t(kmax))
    elif initializer == elbow_center_initializer.RANDOM:
        ccore.elbow_method_irnd.restype = POINTER(pyclustering_package)
        package = ccore.elbow_method_irnd(pointer_data, c_size_t(kmin), c_size_t(kmax))
    else:
        raise ValueError("Not supported type of center initializer '" + str(initializer) + "'.")

    results = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    return (results[elbow_package_indexer.ELBOW_PACKAGE_INDEX_AMOUNT][0],
            results[elbow_package_indexer.ELBOW_PACKAGE_INDEX_WCE])
