"""!

@brief Cluster analysis algorithm: K-Medians
@details Implementation based on paper @cite book::algorithms_for_clustering_data.

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


import math

from pyclustering.cluster.encoder import type_encoding

from pyclustering.utils.metric import distance_metric, type_metric

import pyclustering.core.kmedians_wrapper as wrapper

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.metric_wrapper import metric_wrapper


class kmedians:
    """!
    @brief Class represents clustering algorithm K-Medians.
    @details The algorithm is less sensitive to outliers than K-Means. Medians are calculated instead of centroids.
    
             CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
    Example:
    @code
        # load list of points for cluster analysis
        sample = read_sample(path);
        
        # create instance of K-Medians algorithm
        kmedians_instance = kmedians(sample, [ [0.0, 0.1], [2.5, 2.6] ]);
        
        # run cluster analysis and obtain results
        kmedians_instance.process();
        kmedians_instance.get_clusters();    
    @endcode
    
    """
    
    def __init__(self, data, initial_centers, tolerance=0.001, ccore=True, **kwargs):
        """!
        @brief Constructor of clustering algorithm K-Medians.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] initial_centers (list): Initial coordinates of medians of clusters that are represented by list: [center1, center2, ...].
        @param[in] tolerance (double): Stop condition: if maximum value of change of centers of clusters is less than tolerance than algorithm will stop processing
        @param[in] ccore (bool): Defines should be CCORE library (C++ pyclustering library) used instead of Python code or not.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric').

        <b>Keyword Args:</b><br>
            - metric (distance_metric): Metric that is used for distance calculation between two points.
        
        """
        self.__pointer_data = data
        self.__clusters = []
        self.__medians = initial_centers[:]
        self.__tolerance = tolerance

        self.__metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))
        if self.__metric is None:
            self.__metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)

        self.__ccore = ccore and self.__metric.get_type() != type_metric.USER_DEFINED
        if self.__ccore:
            self.__ccore = ccore_library.workable()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Medians algorithm.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_medians()
        
        """
        
        if self.__ccore is True:
            ccore_metric = metric_wrapper.create_instance(self.__metric)

            self.__clusters = wrapper.kmedians(self.__pointer_data, self.__medians, self.__tolerance, ccore_metric.get_pointer())
            self.__medians = self.__update_medians()
            
        else:
            changes = float('inf')
             
            # Check for dimension
            if len(self.__pointer_data[0]) != len(self.__medians[0]):
                raise NameError('Dimension of the input data and dimension of the initial medians must be equal.')
             
            while changes > self.__tolerance:
                self.__clusters = self.__update_clusters()
                updated_centers = self.__update_medians()
             
                changes = max([self.__metric(self.__medians[index], updated_centers[index]) for index in range(len(updated_centers))])
                 
                self.__medians = updated_centers


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_medians()
        
        """
        
        return self.__clusters
    
    
    def get_medians(self):
        """!
        @brief Returns list of centers of allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """

        return self.__medians


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def __update_clusters(self):
        """!
        @brief Calculate Manhattan distance to each point from the each cluster. 
        @details Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters where each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for i in range(len(self.__medians))]
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1
            dist_optim = 0.0
             
            for index in range(len(self.__medians)):
                dist = self.__metric(self.__pointer_data[index_point], self.__medians[index])
                 
                if (dist < dist_optim) or (index is 0):
                    index_optim = index
                    dist_optim = dist
             
            clusters[index_optim].append(index_point)
            
        # If cluster is not able to capture object it should be removed
        clusters = [cluster for cluster in clusters if len(cluster) > 0]
        
        return clusters
    
    
    def __update_medians(self):
        """!
        @brief Calculate medians of clusters in line with contained objects.
        
        @return (list) list of medians for current number of clusters.
        
        """
         
        medians = [[] for i in range(len(self.__clusters))]
         
        for index in range(len(self.__clusters)):
            medians[index] = [ 0.0 for i in range(len(self.__pointer_data[0]))]
            length_cluster = len(self.__clusters[index])
            
            for index_dimension in range(len(self.__pointer_data[0])):
                sorted_cluster = sorted(self.__clusters[index], key=lambda x: self.__pointer_data[x][index_dimension])
                
                relative_index_median = int(math.floor((length_cluster - 1) / 2))
                index_median = sorted_cluster[relative_index_median]
                
                if (length_cluster % 2) == 0:
                    index_median_second = sorted_cluster[relative_index_median + 1]
                    medians[index][index_dimension] = (self.__pointer_data[index_median][index_dimension] + self.__pointer_data[index_median_second][index_dimension]) / 2.0
                    
                else:
                    medians[index][index_dimension] = self.__pointer_data[index_median][index_dimension]
             
        return medians
