"""!

@brief Cluster analysis algorithm: BIRCH
@details Implementation based on article:
         - T.Zhang, R.Ramakrishnan, M.Livny. BIRCH: An Efficient Data Clustering Method for Very Large Databases. 1996.
         
@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
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

import pyclustering.core.antmean_wrapper as wrapper


class antmean_clustering_params:

    def __init__(self):
        
        # used for pheramone evaporation
        self.ro = 0.9
        
        # initial value for pheramones
        self.pheramone_init = 0.1
        
        # amount of iterations that is used for solving
        self.iterations = 50
        
        # amount of ants that is used on each iteration
        self.count_ants = 20


class antmean:

    def __init__(self, parameters):

        self.__parameters = parameters if parameters is not None else antmean_clustering_params()
    
    def process(self, count_clusters, samples):
        return wrapper.antmean_clustering_process(self.__parameters, count_clusters, samples)
