"""!

@brief Cluster analysis algorithm: SOM-SC (Self-Organized Feature Map for Simple Clustering)
@details There is no paper on which implementation is based. Algorithm SOM-SC is adaptation of SOM for cluster analysis in simple way.
          Basic idea: amount of cluster that should be allocated is defines amount of neurons in the self-organized map. SOM-SC can be
          considered as neural network implementation of K-Means algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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


from pyclustering.cluster.encoder import type_encoding;

from pyclustering.nnet.som import som;
from pyclustering.nnet.som import type_conn;


class somsc:
    """!
    @brief Class represents simple clustering algorithm based on self-organized feature map. 
    @details This algorithm uses amount of clusters that should be allocated as a size of SOM map. Captured objects by neurons are clusters.
             Algorithm is able to process data with Gaussian distribution that has spherical forms.
             
             CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
    Example:
    @code
        # load list of points for cluster analysis
        sample = read_sample(path);
        
        # create instance of SOM-SC algorithm to allocated two clusters
        somsc_instance = somsc(sample, 2);
        
        # run cluster analysis and obtain results
        somsc_instance.process();
        somsc_instance.get_clusters();
    @endcode
    
    """
    
    def __init__(self, data, amount_clusters, epouch = 100, ccore = True):
        """!
        @brief Creates SOM-SC (Self Organized Map for Simple Clustering) algorithm for clustering analysis.
        
        @param[in] data (list): List of points that are used for processing.
        @param[in] amount_clusters (uint): Amount of clusters that should be allocated.
        @param[in] epouch (uint): Number of epochs for training of SOM.
        @param[in] ccore (bool): If it is True then CCORE implementation will be used for clustering analysis.
        
        """
        
        self.__data_pointer = data;
        self.__amount_clusters = amount_clusters;
        self.__epouch = epouch;
        self.__ccore = ccore;
        
        self.__network = None;


    def process(self):
        """!
        @brief Performs cluster analysis by competition between neurons of SOM.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        
        """
        
        self.__network = som(1, self.__amount_clusters, type_conn.grid_four, None, self.__ccore);
        self.__network.train(self.__data_pointer, self.__epouch, True);


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        
        """
        
        return self.__network.capture_objects;


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION;
