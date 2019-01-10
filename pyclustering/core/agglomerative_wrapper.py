"""!

@brief CCORE Wrapper for agglomerative algorithm.

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

from ctypes import c_size_t, c_double, POINTER;

from pyclustering.core.wrapper import ccore_library;
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder;

def agglomerative_algorithm(data, number_clusters, link):
    pointer_data = package_builder(data, c_double).create();

    ccore = ccore_library.get();
    ccore.agglomerative_algorithm.restype = POINTER(pyclustering_package);
    package = ccore.agglomerative_algorithm(pointer_data, c_size_t(number_clusters), c_size_t(link));

    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);

    return result;
