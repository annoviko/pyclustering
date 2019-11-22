"""!

@brief Cluster analysis algorithm: SOM-SC (Self-Organized Feature Map for Simple Clustering)
@details There is no paper on which implementation is based. Algorithm SOM-SC is adaptation of SOM for cluster analysis in simple way.
          Basic idea: amount of cluster that should be allocated is defines amount of neurons in the self-organized map. SOM-SC can be
          considered as neural network implementation of K-Means algorithm.
          Implementation based on paper @cite article::nnet::som::1.

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


from pyclustering.cluster.encoder import type_encoding

from pyclustering.nnet.som import som
from pyclustering.nnet.som import type_conn


class somsc:
    """!
    @brief Class represents simple clustering algorithm based on self-organized feature map. 
    @details This algorithm uses amount of clusters that should be allocated as a size of SOM map. Captured objects by neurons are clusters.
             Algorithm is able to process data with Gaussian distribution that has spherical forms.
    
    Example:
    @code
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.cluster.somsc import somsc
        from pyclustering.samples.definitions import FCPS_SAMPLES
        from pyclustering.utils import read_sample

        # Load list of points for cluster analysis
        sample = read_sample(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

        # Create instance of SOM-SC algorithm to allocated two clusters
        somsc_instance = somsc(sample, 2)

        # Run cluster analysis and obtain results
        somsc_instance.process()
        clusters = somsc_instance.get_clusters()

        # Visualize clustering results.
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    @endcode
    
    """
    
    def __init__(self, data, amount_clusters, epouch=100, ccore=True):
        """!
        @brief Creates SOM-SC (Self Organized Map for Simple Clustering) algorithm for clustering analysis.
        
        @param[in] data (list): List of points that are used for processing.
        @param[in] amount_clusters (uint): Amount of clusters that should be allocated.
        @param[in] epouch (uint): Number of epochs for training of SOM.
        @param[in] ccore (bool): If it is True then CCORE implementation will be used for clustering analysis.
        
        """
        
        self.__data_pointer = data
        self.__amount_clusters = amount_clusters
        self.__epouch = epouch
        self.__ccore = ccore
        
        self.__network = None

        self.__verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis by competition between neurons of SOM.
        
        @return (somsc) Returns itself (SOM Simple Clustering instance).
        
        @see get_clusters()
        
        """
        
        self.__network = som(1, self.__amount_clusters, type_conn.grid_four, None, self.__ccore)
        self.__network.train(self.__data_pointer, self.__epouch, True)
        return self


    def predict(self, points):
        """!
        @brief Calculates the closest cluster to each point.

        @param[in] points (array_like): Points for which closest clusters are calculated.

        @return (list) List of closest clusters for each point. Each cluster is denoted by index. Return empty
                 collection if 'process()' method was not called.

        """

        result = []
        for point in points:
            index_cluster = self.__network.simulate(point)
            result.append(index_cluster)

        return result


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        
        """
        
        return self.__network.capture_objects


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__data_pointer) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__data_pointer))

        if self.__amount_clusters <= 0:
            raise ValueError("Amount of clusters (current value: '%d') should be greater than 0." %
                             self.__amount_clusters)

        if self.__epouch < 0:
            raise ValueError("Amount of epouch (current value: '%d') should be greater or equal to 0." %
                             self.__epouch)
