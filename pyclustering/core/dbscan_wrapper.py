"""!

@brief CCORE Wrapper for DBSCAN algorithm.

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

def dbscan(sample, eps, min_neighbors, return_noise = False):
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.dbscan_algorithm(pointer_data, c_double(eps), c_size_t(min_neighbors));

    list_of_clusters = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    noise = list_of_clusters[len(list_of_clusters) - 1];
    list_of_clusters.remove(noise);

    return (list_of_clusters, noise);