"""!

@brief Cluster analysis algorithm: CHAMELEON
@details Implementation based on article:
         - G.Karypis, E.Han, V.Kumar. CHAMELEON: A Hierarchical Clustering Algorithm Using Dynamic Modeling. 1999.
         
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

from pyclustering.utils import euclidean_distance_sqrt, knearest;


class chameleon:
    """!
    @brief Class represents clustering algorithm CHAMELEON.
    @details CHAMELEON finds the clusters in the data set by using a two phase algorithm. During the first phase,
             CHAMELEON uses a graph partitioning algorithm to cluster the data items into a large number of relatively
             small sub-clusters. During the second phase, it uses an agglomerative hierarchical clustering algorithm
             to find the genuine clusters by repeatedly combining together these sub-clusters.
    
    Example:
    @code
        NO CODE
    @endcode
    
    """
    
    def __init__(self, data, knearest, ccore = False):
        self.__data = data;
        self.__clusters = [];
        self.__knearest = knearest;
        
        self.__graph = [ [] for _ in range(len(data)) ];
        self.__ccore = ccore;
        
    
    
    def process(self):
        self.__graph = knearest(self.__data, self.__knearest);
    
    
    
    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        
        """
        
        return self.__clusters;

