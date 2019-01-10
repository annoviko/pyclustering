"""!

@brief CCORE Wrapper for ROCK algorithm.

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

from ctypes import c_double, c_size_t, POINTER;

from pyclustering.core.wrapper import ccore_library;
from pyclustering.core.pyclustering_package import pyclustering_package, package_builder, package_extractor;


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
    
    pointer_data = package_builder(sample, c_double).create();

    ccore = ccore_library.get();

    ccore.rock_algorithm.restype = POINTER(pyclustering_package);
    package = ccore.rock_algorithm(pointer_data, c_double(eps), c_size_t(number_clusters), c_double(threshold));

    list_of_clusters = package_extractor(package).extract();
    ccore.free_pyclustering_package(package);
    
    return list_of_clusters;