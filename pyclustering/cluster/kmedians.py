"""!

@brief Cluster analysis algorithm: K-Medians
@details Based on book description:
         - A.K. Jain, R.C Dubes, Algorithms for Clustering Data. 1988.

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

import math;

from pyclustering.utils import euclidean_distance_sqrt;

import pyclustering.core.kmedians_wrapper as wrapper;

class kmedians:
    """!
    @brief Class represents clustering algorithm K-Medians.
    @details The algorithm is less sensitive to outliers than K-Means. Medians are calculated instead of centroids.
    
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
    
    def __init__(self, data, initial_centers, tolerance = 0.25, ccore = False):
        """!
        @brief Constructor of clustering algorithm K-Medians.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] initial_centers (list): Initial coordinates of medians of clusters that are represented by list: [center1, center2, ...].
        @param[in] tolerance (double): Stop condition: if maximum value of change of centers of clusters is less than tolerance than algorithm will stop processing
        @param[in] ccore (bool): Defines should be CCORE library (C++ pyclustering library) used instead of Python code or not.
        
        """
        self.__pointer_data = data;
        self.__clusters = [];
        self.__medians = initial_centers[:];
        self.__tolerance = tolerance;
        self.__ccore = ccore;


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Medians algorithm.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_medians()
        
        """
        
        if (self.__ccore is True):
            self.__clusters = wrapper.kmedians(self.__pointer_data, self.__medians, self.__tolerance);
            self.__medians = self.__update_medians();
            
        else:
            changes = float('inf');
             
            stop_condition = self.__tolerance * self.__tolerance;   # Fast solution
            #stop_condition = self.__tolerance;              # Slow solution
             
            # Check for dimension
            if (len(self.__pointer_data[0]) != len(self.__medians[0])):
                raise NameError('Dimension of the input data and dimension of the initial cluster medians must be equal.');
             
            while (changes > stop_condition):
                self.__clusters = self.__update_clusters();
                updated_centers = self.__update_medians();  # changes should be calculated before asignment
             
                changes = max([euclidean_distance_sqrt(self.__medians[index], updated_centers[index]) for index in range(len(updated_centers))]);    # Fast solution
                 
                self.__medians = updated_centers;


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_medians()
        
        """
        
        return self.__clusters;
    
    
    def get_medians(self):
        """!
        @brief Returns list of centers of allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """

        return self.__medians;


    def __update_clusters(self):
        """!
        @brief Calculate Manhattan distance to each point from the each cluster. 
        @details Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters where each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for i in range(len(self.__medians))];
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1;
            dist_optim = 0.0;
             
            for index in range(len(self.__medians)):
                dist = euclidean_distance_sqrt(self.__pointer_data[index_point], self.__medians[index]);
                 
                if ( (dist < dist_optim) or (index is 0)):
                    index_optim = index;
                    dist_optim = dist;
             
            clusters[index_optim].append(index_point);
            
        # If cluster is not able to capture object it should be removed
        clusters = [cluster for cluster in clusters if len(cluster) > 0];
        
        return clusters;
    
    
    def __update_medians(self):
        """!
        @brief Calculate medians of clusters in line with contained objects.
        
        @return (list) list of medians for current number of clusters.
        
        """
         
        medians = [[] for i in range(len(self.__clusters))];
         
        for index in range(len(self.__clusters)):
            medians[index] = [ 0.0 for i in range(len(self.__pointer_data[0]))];
            length_cluster = len(self.__clusters[index]);
            
            for index_dimension in range(len(self.__pointer_data[0])):
                sorted_cluster = sorted(self.__clusters[index], key = lambda x: self.__pointer_data[x][index_dimension]);
                
                relative_index_median = math.floor(length_cluster / 2);
                index_median = sorted_cluster[relative_index_median];
                
                if ( (length_cluster % 2) and (relative_index_median + 1 < len(sorted_cluster)) ):
                    index_median_second = sorted_cluster[relative_index_median + 1];
                    medians[index][index_dimension] =  (self.__pointer_data[index_median][index_dimension] + self.__pointer_data[index_median_second][index_dimension]) / 2.0;
                    
                else:
                    medians[index][index_dimension] = self.__pointer_data[index_median][index_dimension];
             
        return medians;