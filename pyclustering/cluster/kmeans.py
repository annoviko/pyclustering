"""!

@brief Cluster analysis algorithm: K-Means
@details Based on book description:
         - J.B.MacQueen. Some Methods for Classification and Analysis of Multivariate Observations. 1967.

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


import numpy;

import pyclustering.core.kmeans_wrapper as wrapper;

from pyclustering.core.wrapper import ccore_library;

from pyclustering.cluster.encoder import type_encoding;


class kmeans:
    """!
    @brief Class represents clustering algorithm K-Means.
    @details CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
             CCORE implementation of the algorithm uses thread pool to parallelize the clustering process.
             
             K-Means clustering results depend on initial centers. Algorithm K-Means++ can used for initialization 
             initial centers from module 'pyclustering.cluster.center_initializer'.
    
    Example #1 - Trivial clustering:
    @code
        # load list of points for cluster analysis
        sample = read_sample(path);
        
        # create instance of K-Means algorithm
        kmeans_instance = kmeans(sample, [ [0.0, 0.1], [2.5, 2.6] ]);
        
        # run cluster analysis and obtain results
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();
    @endcode
    
    Example #2 - Clustering using K-Means++ for center initialization:
    @code
        # load list of points for cluster analysis
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        
        # initialize initial centers using K-Means++ method
        initial_centers = kmeans_plusplus_initializer(sample, 3).initialize();
        
        # create instance of K-Means algorithm with prepared centers
        kmeans_instance = kmeans(sample, initial_centers);
        
        # run cluster analysis and obtain results
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();
        final_centers = kmeans_instance.get_centers();
    @endcode
    
    @see center_initializer
    
    """
    
    def __init__(self, data, initial_centers, tolerance = 0.001, ccore = True):
        """!
        @brief Constructor of clustering algorithm K-Means.
        @details Center initializer can be used for creating initial centers, for example, K-Means++ method.
        
        @param[in] data (array_like): Input data that is presented as array of points (objects), each point should be represented by array_like data structure.
        @param[in] initial_centers (array_like): Initial coordinates of centers of clusters that are represented by array_like data structure: [center1, center2, ...].
        @param[in] tolerance (double): Stop condition: if maximum value of change of centers of clusters is less than tolerance then algorithm stops processing.
        @param[in] ccore (bool): Defines should be CCORE library (C++ pyclustering library) used instead of Python code or not.
        
        @see center_initializer
        
        """
        self.__pointer_data = numpy.matrix(data);
        self.__clusters = [];
        self.__centers = numpy.matrix(initial_centers);
        self.__tolerance = tolerance;
        
        self.__ccore = ccore;
        if (self.__ccore):
            self.__ccore = ccore_library.workable();


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Means algorithm.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_centers()
        
        """
        
        if (self.__ccore is True):
            self.__clusters = wrapper.kmeans(self.__pointer_data, self.__centers, self.__tolerance);
            self.__centers = self.__update_centers();
        else:
            maximum_change = float('inf');
             
            stop_condition = self.__tolerance * self.__tolerance;   # Fast solution
            #stop_condition = self.__tolerance;              # Slow solution
             
            # Check for dimension
            if (len(self.__pointer_data[0]) != len(self.__centers[0])):
                raise NameError('Dimension of the input data and dimension of the initial cluster centers must be equal.');
             
            while (maximum_change > stop_condition):
                self.__clusters = self.__update_clusters();
                updated_centers = self.__update_centers();  # changes should be calculated before asignment
                
                if (len(self.__centers) != len(updated_centers)):
                    maximum_change = float('inf');
                
                else:
                    changes = numpy.sum(numpy.square(self.__centers - updated_centers), axis=1);
                    maximum_change = numpy.max(changes);
                
                self.__centers = updated_centers;


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_centers()
        
        """
        
        return self.__clusters;
    
    
    def get_centers(self):
        """!
        @brief Returns list of centers of allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """

        return self.__centers.tolist();


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION;


    def __update_clusters(self):
        """!
        @brief Calculate Euclidean distance to each point from the each cluster. Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters. Each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for _ in range(len(self.__centers))];
        
        dataset_differences = numpy.zeros((len(clusters), len(self.__pointer_data)));
        for index_center in range(len(self.__centers)):
            dataset_differences[index_center] = numpy.sum(numpy.square(self.__pointer_data - self.__centers[index_center]), axis=1).T;
        
        optimum_indexes = numpy.argmin(dataset_differences, axis=0);
        for index_point in range(len(optimum_indexes)):
            index_cluster = optimum_indexes[index_point];
            clusters[index_cluster].append(index_point);
        
        clusters = [cluster for cluster in clusters if len(cluster) > 0];
        
        return clusters;
    
    
    def __update_centers(self):
        """!
        @brief Calculate centers of clusters in line with contained objects.
        
        @return (numpy.matrix) Updated centers as list of centers.
        
        """
        
        dimension = self.__pointer_data.shape[1];
        centers = numpy.zeros((len(self.__clusters), dimension));
        
        for index in range(len(self.__clusters)):
            cluster_points = self.__pointer_data[self.__clusters[index], :];
            centers[index] = cluster_points.mean(axis=0);

        return numpy.matrix(centers);
