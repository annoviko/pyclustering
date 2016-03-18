"""!

@brief Cluster analysis algorithm: CLARANS.
@details Implementation based on article:
         - T.Ng.Raymond and H.Jiawei. CLARANS: A Method for Clustering Objects for Spatial Data Mining. 1996.

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
import random;

from pyclustering.utils import euclidean_distance_sqrt;

class clarans:
    """!
    @brief Class represents clustering algorithm CLARANS (a method for clustering objects for spatial data mining).
    
    """
    
    __pointer_data = None;
    __numlocal = 0;
    __maxneighbor = 0;
    __number_clusters = 0;
    
    __clusters = None;
    __belong = None;
    __medoids = None;
    __current = None;
    
    def __init__(self, data, number_clusters, numlocal, maxneighbor):
        """!
        @brief Constructor of clustering algorithm CLARANS.
        @details The higher the value of maxneighbor, the closer is CLARANS to K-Medoids (PAM - Partitioning Around Medoids), and the longer is each search of a local minima.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] number_clusters (uint): amount of clusters that should be allocated.
        @param[in] numlocal (uint): the number of local minima obtained (amount of iterations for solving the problem).
        @param[in] maxneighbor (uint): the maximum number of neighbors examined.
        
        """
        
        self.__pointer_data = data;
        self.__numlocal = numlocal;
        self.__maxneighbor = maxneighbor;
        self.__number_clusters = number_clusters;
        
        self.__clusters = [];
        self.__medoids = [];
        self.__current = [];
        self.__belong = [];
    
    
    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of CLARANS algorithm.
        
        @see get_clusters()
        
        """
        
        random.seed();
        
        for iteration in range(0, self.__numlocal):
            # set (current) random medoids
            self.__current = random.sample(range(0, len(self.__pointer_data)), self.__number_clusters);
            
            # update clusters in line with random allocated medoids
            self.__update_clusters();
            
            # try to find better medoids
            index_neighbor = 0;
            while (index_neighbor < self.__maxneighbor):
                # get random current medoid that is to be replaced
                current_medoid_index = self.__current[random.randint(0, len(self.__number_clusters) - 1)];
                current_medoid_cluster_index = self.__belong[current_medoid_index];
                
                # get new candidate to be medoid
                candidate_medoid_index = random.randint(0, len(self.__pointer_data) - 1);
                candidate_medoid_cluster_index = self.__belong[candidate_medoid_index];
                
                while (candidate_medoid_index in self.__current):
                    candidate_medoid_index = random.randint(0, len(self.__pointer_data) - 1);
                
                candidate_cost = 0.0;
                for point_index in range(0, len(self.__pointer_data)):
                    if (point_index not in self.__current):
                        # get non-medoid point and its medoid
                        point_cluster_index = self.__belong[point_index];
                        point_medoid_index = self.__current[point_cluster_index];
                        
                        # get other medoid that is nearest to the point (except current and candidate)
                        other_medoid_index = -1;
                        other_distance_nearest = float('inf');
                        for index_medoid in self.__current:
                            if (index_medoid != current_medoid_index):
                                other_distance_candidate = euclidean_distance_sqrt(self.__pointer_data[point_index], self.__pointer_data[current_medoid_index]);
                                
                                if (other_distance_candidate < other_distance_nearest):
                                    other_distance_nearest = other_distance_candidate;
                                    other_medoid_index = index_medoid;
                        
                        other_medoid_cluster_index = self.__belong[other_medoid_index];
                        
                        # for optimization calculate all required distances
                        # from the point to current medoid
                        distance_current = euclidean_distance_sqrt(self.__pointer_data[point_index], self.__pointer_data[current_medoid_index]);
                        
                        # from the point to candidate median
                        distance_candidate = euclidean_distance_sqrt(self.__pointer_data[point_index], self.__pointer_data[candidate_medoid_index]);
                        
                        # from the point to nearest (own) medoid
                        distance_nearest = float('inf');
                        if ( (point_medoid_index != candidate_medoid_index) and (point_medoid_index != current_medoid_cluster_index) ):
                            distance_nearest = euclidean_distance_sqrt(self.__pointer_data[point_index], self.__pointer_data[point_medoid_index]);
                        
                        # apply rules for cost calculation
                        if (point_cluster_index == current_medoid_cluster_index):
                            # case 1:
                            if (distance_candidate >= distance_nearest):
                                candidate_cost += distance_nearest - distance_current;
                            
                            # case 2:
                            else:
                                candidate_cost += distance_candidate - distance_current;
                        
                        elif (point_cluster_index == other_medoid_cluster_index):
                            # case 3 ('nearest medoid' is the representative object of that cluster and object is more similar to 'nearest' than to 'candidate'):
                            if (distance_candidate > distance_nearest):
                                pass;
                            
                            # case 4:
                            else:
                                candidate_cost += distance_candidate - distance_nearest;
                
                if (candidate_cost < 0):
                    # set candidate that has won
                    self.__current[current_medoid_cluster_index] = candidate_medoid_index;
                    
                    # recalculate clusters
                    self.__update_clusters();
                    
                    # reset iterations and starts investigation from the begining
                    index_neighbor = 0;
                    
                else:
                    index_neighbor += 1;
                    
            
            # obtain cost of current cluster configuration and compare it with the best obtained
            assert(0); # under implementation
    
    
    def get_clusters(self):
        """!
        @brief Returns allocated clusters by the algorithm.
        
        @remark Allocated clusters can be returned only after data processing (use method process()), otherwise empty list is returned.
        
        @return (list) List of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        
        """
        
        return self.__clusters;
    
    
    def __update_clusters(self):
        """!
        @brief Calculates distance to each point from each medoid in each cluster and forms new clusters. 
        @details Nearest points are captured by according clusters and as a result clusters are updated.
        
        """
        
        self.__belong = [0] * len(self.__current);
        self.__clusters = [[] for i in range(len(self.__current))];
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1;
            dist_optim = 0.0;
             
            for index in range(len(self.__current)):
                dist = euclidean_distance_sqrt(self.__pointer_data[index_point], self.__current[index]);
                 
                if ( (dist < dist_optim) or (index is 0)):
                    index_optim = index;
                    dist_optim = dist;
             
            self.__clusters[index_optim].append(index_point);
            self.__belong[index_point] = index_optim;
        
        # If cluster is not able to capture object it should be removed
        self.__clusters = [cluster for cluster in self.__clusters if len(cluster) > 0];
        