"""!

@brief CCORE Wrapper for X-Means algorithm.

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


from ctypes import cdll, c_double, c_size_t, c_uint, POINTER;

from pyclustering.core.wrapper import PATH_DLL_CCORE_64, create_pointer_data, extract_pyclustering_package, pyclustering_package;


def xmeans(sample, centers, kmax, tolerance, criterion):
    pointer_data = create_pointer_data(sample);
    pointer_centers = create_pointer_data(centers);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    
    ccore.xmeans_algorithm.restype = POINTER(pyclustering_package);
    package = ccore.xmeans_algorithm(pointer_data, pointer_centers, c_size_t(kmax), c_double(tolerance), c_uint(criterion));
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;