"""!

@brief CCORE Wrapper for clustering Ant Means algorithm.

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


from pyclustering.core.wrapper import *
from pyclustering.core.pyclustering_package import pyclustering_package, package_builder, package_extractor


class c_antcolony_clustering_parameters(Structure):
    """
    double                  ro;
    double                  pheramone_init;
    unsigned int            iterations;
    unsigned int            count_ants;
    
    """
    _fields_ = [("ro", c_double),
                ("pheramone_init", c_double),
                ("iterations", c_uint),
                ("count_ants", c_uint)]


def antmean_clustering_process(params, count_clusters, samples):
    """ """

    ccore = load_core()
    
    algorithm_params = c_antcolony_clustering_parameters()
    algorithm_params.ro = c_double(params.ro)
    algorithm_params.pheramone_init = c_double(params.pheramone_init)
    algorithm_params.iterations = c_uint(params.iterations)
    algorithm_params.count_ants = c_uint(params.count_ants)
    
    algorithm_params = pointer(algorithm_params)
    
    sample_package = package_builder(samples, c_double).create()
    
    ccore.antmean_algorithm.restype = POINTER(pyclustering_package)
    package = ccore.antmean_algorithm(sample_package, algorithm_params, count_clusters)
    
    result = package_extractor(package).extract()
    ccore.free_pyclustering_package(package)

    return result
