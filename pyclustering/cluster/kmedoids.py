"""!

@brief Cluster analysis algorithm: K-Medoids (PAM - Partitioning Around Medoids).
@details Based on book description:
         - A.K. Jain, R.C Dubes, Algorithms for Clustering Data. 1988.
         - L. Kaufman, P.J. Rousseeuw, Finding Groups in Data: an Introduction to Cluster Analysis. 1990.

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


from pyclustering.utils import euclidean_distance_sqrt, median;

import pyclustering.core.kmedoids_wrapper as wrapper;


class kmedoids:
    """!
    @brief Class represents clustering algorithm K-Medoids (another one title is PAM - Parti).
    @details The algorithm is less sensitive to outliers tham K-Means. The principle difference between K-Medoids and K-Medians is that
             K-Medoids uses existed points from input data space as medoids, but median in K-Medians can be unreal object (not from
             input data space).
    
    Example:
    @code
        # load list of points for cluster analysis
        sample = read_sample(path);
        
        # create instance of K-Medoids algorithm
        kmedians_instance = kmedians(sample, [1, 10]);
        
        # run cluster analysis and obtain results
        kmedians_instance.process();
        kmedians_instance.get_clusters();    
    @endcode
    
    """
    
    
    def __init__(self, data, initial_index_medoids, tolerance = 0.25, ccore = False):
        """!
        @brief Constructor of clustering algorithm K-Medoids.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] initial_index_medoids (list): Indexes of intial medoids (indexes of points in input data).
        @param[in] tolerance (double): Stop condition: if maximum value of distance change of medoids of clusters is less than tolerance than algorithm will stop processing.
        @param[in] ccore (bool): If specified than CCORE library (C++ pyclustering library) is used for clustering instead of Python code.
        
        """
        self.__pointer_data = data;
        self.__clusters = [];
        self.__medoids = initial_index_medoids;
        self.__tolerance = tolerance;
        self.__ccore = ccore;


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Medoids algorithm.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_medoids()
        
        """
        
        if (self.__ccore is True):
            self.__clusters = wrapper.kmedoids(self.__pointer_data, self.__medoids, self.__tolerance);
            self.__medoids = self.__update_medoids();
        
        else:
            self.__medoids = [ self.__pointer_data[medoid_index] for medoid_index in self.__medoids ];
            
            changes = float('inf');
             
            stop_condition = self.__tolerance * self.__tolerance;   # Fast solution
            #stop_condition = self.__tolerance;              # Slow solution
             
            while (changes > stop_condition):
                self.__clusters = self.__update_clusters();
                updated_medoids = self.__update_medoids();  # changes should be calculated before asignment
             
                changes = max([euclidean_distance_sqrt(self.__medoids[index], updated_medoids[index]) for index in range(len(updated_medoids))]);    # Fast solution
                 
                self.__medoids = updated_medoids;


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_medoids()
        
        """
        
        return self.__clusters;
    
    
    def get_medoids(self):
        """!
        @brief Returns list of medoids of allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """

        return self.__medoids;


    def __update_clusters(self):
        """!
        @brief Calculate distance to each point from the each cluster. 
        @details Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters where each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for i in range(len(self.__medoids))];
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1;
            dist_optim = 0.0;
             
            for index in range(len(self.__medoids)):
                dist = euclidean_distance_sqrt(self.__pointer_data[index_point], self.__medoids[index]);
                 
                if ( (dist < dist_optim) or (index is 0)):
                    index_optim = index;
                    dist_optim = dist;
             
            clusters[index_optim].append(index_point);
        
        # If cluster is not able to capture object it should be removed
        clusters = [cluster for cluster in clusters if len(cluster) > 0];
        
        return clusters;
    
    
    def __update_medoids(self):
        """!
        @brief Find medoids of clusters in line with contained objects.
        
        @return (list) list of medoids for current number of clusters.
        
        """
         
        medoids = [[] for i in range(len(self.__clusters))];
        
        for index in range(len(self.__clusters)):
            medoid_index = median(self.__pointer_data, self.__clusters[index]);
            medoids[index] = self.__pointer_data[medoid_index];
             
        return medoids;