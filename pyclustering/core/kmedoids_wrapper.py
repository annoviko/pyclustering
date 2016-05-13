"""!

@brief CCORE Wrapper for K-Medoids algorithm (PAM).

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


from ctypes import cdll, c_double, c_size_t, c_void_p, cast, pointer, POINTER;

from pyclustering.core.wrapper import PATH_DLL_CCORE_64, create_pointer_data, pyclustering_package, pyclustering_type_data, extract_pyclustering_package;


def kmedoids(sample, medoids, tolerance):
    pointer_data = create_pointer_data(sample);
    
    c_medoids = (c_size_t * len(medoids))();
    c_medoids[:] = medoids[:];
    
    medoids_package = pyclustering_package();
    medoids_package.size = len(medoids);
    medoids_package.type = pyclustering_type_data.PYCLUSTERING_TYPE_SIZE_T;
    medoids_package.data = cast(c_medoids, POINTER(c_void_p));
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.kmedoids_algorithm(pointer_data, pointer(medoids_package), c_double(tolerance));
    
    result = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);

    return result;
