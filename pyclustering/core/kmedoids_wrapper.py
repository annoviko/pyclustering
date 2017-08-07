"""!

@brief CCORE Wrapper for K-Medoids algorithm (PAM).

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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


from ctypes import c_double, c_size_t, POINTER;

from pyclustering.core.wrapper import load_core;
from pyclustering.core.pyclustering_package import pyclustering_package, package_extractor, package_builder;


def kmedoids(sample, medoids, tolerance):
    pointer_data = package_builder(sample, c_double).create();
    medoids_package = package_builder(medoids, c_size_t).create();
    
    ccore = load_core();
    
    ccore.kmedoids_algorithm.restype = POINTER(pyclustering_package);
    package = ccore.kmedoids_algorithm(pointer_data, medoids_package, c_double(tolerance));
    
    result = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);

    return result;
