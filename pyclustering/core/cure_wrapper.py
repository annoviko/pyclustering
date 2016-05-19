"""!

@brief CCORE Wrapper for CURE algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

from ctypes import cdll, c_double, c_size_t;

from pyclustering.core.wrapper import PATH_DLL_CCORE_64, create_pointer_data, extract_pyclustering_package;


def cure_algorithm(sample, number_clusters, number_represent_points, compression):
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    cure_data_pointer = ccore.cure_algorithm(pointer_data, c_size_t(number_clusters), c_size_t(number_represent_points), c_double(compression));
    
    return cure_data_pointer;


def cure_data_destroy(cure_data_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    ccore.cure_data_destroy(cure_data_pointer);


def cure_get_clusters(cure_data_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.cure_get_clusters(cure_data_pointer);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def cure_get_representors(cure_data_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.cure_get_representors(cure_data_pointer);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;


def cure_get_means(cure_data_pointer):
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.cure_get_means(cure_data_pointer);
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return result;