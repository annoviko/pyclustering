"""!

@brief Cluster analysis algorithm: hierarchical algorithm.
@details Implementation based on article:
         - K.Anil, J.C.Dubes, R.C.Dubes. Algorithms for Clustering Data. 1988.

@authors Andrei Novikov (spb.andr@yandex.ru)
@version 1.0
@date 2014-2015
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

from pyclustering.support import euclidean_distance_sqrt;

import pyclustering.core.wrapper as wrapper;


class hierarchical:
    """!
    @brief Class represents hierarchical algorithm for cluster analysis.
    
    Example:
    @code
        # sample for cluster analysis (represented by list)
        sample = read_sample(path_to_sample);
        
        # create object that uses python code only
        hierarchical_instance = hierarchical(sample, 2, False)
        
        # cluster analysis
        hierarchical_instance.process();
        
        # obtain results of clustering
        clusters = hierarchical_instance.get_clusters();  
    @endcode
    
    """
        
    __pointer_data = None;
    __number_clusters = 0;
    
    __ccore = False;
    
    __clusters = None;
    __centers = None;
    
    def __init__(self, data, number_clusters, ccore):
        """!
        @brief Constructor of clustering algorithm hierarchical.
        
        @param[in] data (list): Input data that is presented as a list of points (objects), each point should be represented by a list or tuple.
        @param[in] number_clusters (uint): Number of clusters that should be allocated.
        @param[in] ccore (bool): if True than DLL CCORE (C++ solution) will be used for solving the problem.
        
        """  
        self.__pointer_data = data;
        self.__number_clusters = number_clusters;
        self.__ccore = None;
        
        self.__clusters = [];
        self.__centers = [];
        
    
    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of hierarchical algorithm.
        
        @see get_clusters()
        
        """
        if (self.__ccore is True):
            self.__clusters = wrapper.hierarchical(self.__pointer_data, self.__number_clusters); 
        else:        
            self.__centers = self.__pointer_data.copy();
            self.__clusters = [[index] for index in range(0, len(self.__pointer_data))];
            
            current_number_clusters = len(self.__clusters);
            
            while (current_number_clusters > self.__number_clusters):
                indexes = self.__find_nearest_clusters();
                 
                self.__clusters[indexes[0]] += self.__clusters[indexes[1]];
                self.__centers[indexes[0]] = self.__calculate_center(self.__clusters[indexes[0]]);
                 
                self.__clusters.pop(indexes[1]);   # remove merged cluster.
                self.__centers.pop(indexes[1]);    # remove merged center.
                
                current_number_clusters = len(self.__clusters);
        
        
    def get_clusters(self):
        """!
        @brief Performs cluster analysis in line with rules of heirarchical algorithm.
        
        @remark Results of clustering can be obtained using corresponding gets methods.
        
        @return (list) List of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        
        """
        
        return self.__clusters;


    def __find_nearest_clusters(self):
        """!
        @brief Find two indexes of two clusters whose distance is the smallest.
        
        @return (list) List with two indexes of two clusters whose distance is the smallest.
        
        """     
        
        min_dist = 0;
        indexes = None;
        
        for index1 in range(0, len(self.__centers)):
            for index2 in range(index1 + 1, len(self.__centers)):
                distance = euclidean_distance_sqrt(self.__centers[index1], self.__centers[index2]);
                if ( (distance < min_dist) or (indexes == None) ):
                    min_dist = distance;
                    indexes = [index1, index2];
        
        return indexes; 
    
           
    def __calculate_center(self, cluster):
        """!
        @brief Calculates new center.
        
        @return (list) New value of the center of the specified cluster.
        
        """
         
        dimension = len(self.__pointer_data[cluster[0]]);
        center = [0] * dimension;
        for index_point in cluster:
            for index_dimension in range(0, dimension):
                center[index_dimension] += self.__pointer_data[index_point][index_dimension];
         
        for index_dimension in range(0, dimension):
            center[index_dimension] /= len(cluster);
             
        return center;
