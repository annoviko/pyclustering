"""!

@brief CCORE Wrapper for ROCK algorithm.

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


def rock(sample, eps, number_clusters, threshold):
    """
    @brief Clustering algorithm ROCK returns allocated clusters and noise that are consisted from input data. 
    @details Calculation is performed via CCORE (C/C++ part of the pyclustering)."
    
    @param[in] sample: input data - list of points where each point is represented by list of coordinates.
    @param[in] eps: connectivity radius (similarity threshold), points are neighbors if distance between them is less than connectivity radius.
    @param[in] number_clusters: defines number of clusters that should be allocated from the input data set.
    @param[in] threshold: value that defines degree of normalization that influences on choice of clusters for merging during processing.
    
    @return List of allocated clusters, each cluster contains indexes of objects in list of data.
    
    """
    
    pointer_data = create_pointer_data(sample);
    
    ccore = cdll.LoadLibrary(PATH_DLL_CCORE_64);
    package = ccore.rock_algorithm(pointer_data, c_double(eps), c_size_t(number_clusters), c_double(threshold));

    list_of_clusters = extract_pyclustering_package(package);
    ccore.free_pyclustering_package(package);
    
    return list_of_clusters;