"""!

@brief Cluster analysis algorithm: X-Means
@details Based on article description:
         - D.Pelleg, A.Moore. X-means: Extending K-means with Efficient Estimation of the Number of Clusters. 2000.

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

import numpy;
import math;

from enum import IntEnum;

import pyclustering.core.wrapper as wrapper;

from pyclustering.utils import euclidean_distance, euclidean_distance_sqrt;
from pyclustering.utils import list_math_addition_number, list_math_addition, list_math_multiplication, list_math_division_number, list_math_subtraction;


class splitting_type(IntEnum):
    """!
    @brief Enumeration of splitting types that can be used as splitting creation of cluster in X-Means algorithm.
    
    """
    
    ## Bayesian information criterion to approximate the correct number of clusters.
    BAYESIAN_INFORMATION_CRITERION = 0;
    
    ## Minimum noiseless description length to approximate the correct number of clusters.
    MINIMUM_NOISELESS_DESCRIPTION_LENGTH = 1;


class xmeans:
    """!
    @brief Class represents clustering algorithm X-Means.
    
    Example:
    @code
        # sample for cluster analysis (represented by list)
        sample = read_sample(path_to_sample);
        
        # create object of X-Means algorithm that uses CCORE for processing
        xmeans_instance = xmeans(sample, [ [0.0, 0.5] ], ccore = True);
        
        # run cluster analysis
        xmeans_instance.process();
        
        # obtain results of clustering
        clusters = xmeans_instance.get_clusters();
        
        # display allocated clusters
        draw_clusters(sample, clusters);
    @endcode
    """
    
    def __init__(self, data, initial_centers, kmax = 20, tolerance = 0.025, criterion = splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore = False):
        """!
        @brief Constructor of clustering algorithm X-Means.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] initial_centers (list): Initial coordinates of centers of clusters that are represented by list: [center1, center2, ...].
        @param[in] kmax (uint): Maximum number of clusters that can be allocated.
        @param[in] tolerance (double): Stop condition for each iteration: if maximum value of change of centers of clusters is less than tolerance than algorithm will stop processing.
        @param[in] criterion (splitting_type): Type of splitting creation.
        @param[in] ccore (bool): Defines should be CCORE (C++ pyclustering library) used instead of Python code or not.
        
        """
           
        self.__pointer_data = data;
        self.__clusters = [];
        self.__centers = initial_centers[:];
         
        self.__kmax = kmax;
        self.__tolerance = tolerance;
        self.__criterion = criterion;
         
        self.__ccore = ccore;
         
    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of X-Means algorithm.
        
        @remark Results of clustering can be obtained using corresponding gets methods.
        
        @see get_clusters()
        @see get_centers()
        
        """
        
        if (self.__ccore is True):
            self.__clusters = wrapper.xmeans(self.__pointer_data, self.__centers, self.__kmax, self.__tolerance);
            self.__clusters = [ cluster for cluster in self.__clusters if len(cluster) > 0 ]; 
            
            self.__centers = self.__update_centers(self.__clusters);
        else:
            self.__clusters = [];
            while ( len(self.__centers) < self.__kmax ):
                current_cluster_number = len(self.__centers);
                 
                (self.__clusters, self.__centers) = self.__improve_parameters(self.__centers);
                allocated_centers = self.__improve_structure(self.__clusters, self.__centers);
                
                if ( (current_cluster_number == len(allocated_centers)) ):
                    break;
                else:
                    self.__centers = allocated_centers;
                    
     
    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @return (list) List of allocated clusters.
        
        @see process()
        @see get_centers()
        
        """
         
        return self.__clusters;
     
     
    def get_centers(self):
        """!
        @brief Returns list of centers for allocated clusters.
        
        @return (list) List of centers for allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """
         
        return self.__centers;      
     
     
    def __improve_parameters(self, centers, available_indexes = None):
        """!
        @brief Performs k-means clustering in the specified region.
        
        @param[in] centers (list): Centers of clusters.
        @param[in] available_indexes (list): Indexes that defines which points can be used for k-means clustering, if None - then all points are used.
        
        @return (list) List of allocated clusters, each cluster contains indexes of objects in list of data.
        
        """
        
        changes = numpy.Inf;
        
        stop_condition = self.__tolerance * self.__tolerance; # Fast solution
          
        clusters = [];
          
        while (changes > stop_condition):
            clusters = self.__update_clusters(centers, available_indexes);
            clusters = [ cluster for cluster in clusters if len(cluster) > 0 ]; 
            
            updated_centers = self.__update_centers(clusters);
          
            changes = max([euclidean_distance_sqrt(centers[index], updated_centers[index]) for index in range(len(updated_centers))]);    # Fast solution
              
            centers = updated_centers;
          
        return (clusters, centers);
     
     
    def __improve_structure(self, clusters, centers):
        """!
        @brief Check for best structure: divides each cluster into two and checks for best results using splitting criterion.
        
        @param[in] clusters (list): Clusters that have been allocated (each cluster contains indexes of points from data).
        @param[in] centers (list): Centers of clusters.
        
        @return (list) Allocated centers for clustering.
        
        """
         
        difference = 0.001;
          
        allocated_centers = [];
          
        for index_cluster in range(len(clusters)):
            # split cluster into two child clusters
            parent_child_centers = [];
            parent_child_centers.append(list_math_addition_number(centers[index_cluster], -difference));
            parent_child_centers.append(list_math_addition_number(centers[index_cluster], difference));
          
            # solve k-means problem for children where data of parent are used.
            (parent_child_clusters, parent_child_centers) = self.__improve_parameters(parent_child_centers, clusters[index_cluster]);
              
            # If it's possible to split current data
            if (len(parent_child_clusters) > 1):
                # Calculate splitting criterion
                parent_scores = self.__splitting_criterion([ clusters[index_cluster] ], [ centers[index_cluster] ]);
                child_scores = self.__splitting_criterion([ parent_child_clusters[0], parent_child_clusters[1] ], parent_child_centers);
              
                split_require = False;
                
                # Reallocate number of centers (clusters) in line with scores        
                if (self.__criterion == splitting_type.BAYESIAN_INFORMATION_CRITERION):
                    if (parent_scores < child_scores): split_require = True;
                    
                elif (self.__criterion == splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH):
                    if (parent_scores > child_scores): split_require = True;
                    
                if (split_require is True):
                    allocated_centers.append(parent_child_centers[0]);
                    allocated_centers.append(parent_child_centers[1]);
                else:
                    allocated_centers.append(centers[index_cluster]);

                    
            else:
                allocated_centers.append(centers[index_cluster]);
          
        return allocated_centers;
     
     
    def __splitting_criterion(self, clusters, centers):
        """!
        @brief Calculates splitting criterion for input clusters.
        
        @param[in] clusters (list): Clusters for which splitting criterion should be calculated.
        @param[in] centers (list): Centers of the clusters.
        
        @return (double) Returns splitting criterion. High value of splitting cretion means that current structure is much better.
        
        @see __bayesian_information_criterion(clusters, centers)
        @see __minimum_noiseless_description_length(clusters, centers)
        
        """
        
        if (self.__criterion == splitting_type.BAYESIAN_INFORMATION_CRITERION):
            return self.__bayesian_information_criterion(clusters, centers);
        
        elif (self.__criterion == splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH):
            return self.__minimum_noiseless_description_length(clusters, centers);
        
        else:
            assert 0;
 
    
    def __minimum_noiseless_description_length(self, clusters, centers):
        """!
        @brief Calculates splitting criterion for input clusters using minimum noiseless description length criterion.
        
        @param[in] clusters (list): Clusters for which splitting criterion should be calculated.
        @param[in] centers (list): Centers of the clusters.
        
        @return (double) Returns splitting criterion in line with bayesian information criterion. 
                Low value of splitting cretion means that current structure is much better.
        
        @see __bayesian_information_criterion(clusters, centers)
        
        """
                
        scores = [0.0] * len(clusters);
        
        W = 0.0;
        K = len(clusters);
        N = 0.0;

        sigma_sqrt = 0.0;
        
        alpha = 0.9;
        betta = 0.9;
                
        for index_cluster in range(0, len(clusters), 1):
            for index_object in clusters[index_cluster]:
                delta_vector = list_math_subtraction(self.__pointer_data[index_object], centers[index_cluster]);
                delta_sqrt = sum(list_math_multiplication(delta_vector, delta_vector));
                
                W += delta_sqrt;
                sigma_sqrt += delta_sqrt;
            
            N += len(clusters[index_cluster]);     
        
        if (N - K != 0):
            W /= N;
            
            sigma_sqrt /= (N - K);
            sigma = sigma_sqrt ** 0.5;
            
            for index_cluster in range(0, len(clusters), 1):
                Kw = (1.0 - K / N) * sigma_sqrt;
                Ks = ( 2.0 * alpha * sigma / (N ** 0.5) ) + ( (alpha ** 2.0) * sigma_sqrt / N + W - Kw / 2.0 ) ** 0.5;
                U = W - Kw + 2.0 * (alpha ** 2.0) * sigma_sqrt / N + Ks;
                
                Z = K * sigma_sqrt / N + U + betta * ( (2.0 * K) ** 0.5 ) * sigma_sqrt / N;
                
                if (Z == 0.0):
                    scores[index_cluster] = float("inf");
                else:
                    scores[index_cluster] = Z;
                
        else:
            scores = [float("inf")] * len(clusters);
        
        return sum(scores);
 
    def __bayesian_information_criterion(self, clusters, centers):
        """!
        @brief Calculates splitting criterion for input clusters using bayesian information criterion.
        
        @param[in] clusters (list): Clusters for which splitting criterion should be calculated.
        @param[in] centers (list): Centers of the clusters.
        
        @return (double) Splitting criterion in line with bayesian information criterion.
                High value of splitting cretion means that current structure is much better.
                
        @see __minimum_noiseless_description_length(clusters, centers)
        
        """

        scores = [0.0] * len(clusters)     # splitting criterion
        dimension = len(self.__pointer_data[0]);
          
        # estimation of the noise variance in the data set
        sigma = 0.0;
        K = len(clusters);
        N = 0.0;
          
        for index_cluster in range(0, len(clusters), 1):
            for index_object in clusters[index_cluster]:
                sigma += (euclidean_distance(self.__pointer_data[index_object], centers[index_cluster]));  # It works

            N += len(clusters[index_cluster]);
      
        if (N - K != 0):
            sigma /= (N - K);
        
            # splitting criterion    
            for index_cluster in range(0, len(clusters), 1):
                n = len(clusters[index_cluster]);
                
                if (sigma > 0.0):
                    scores[index_cluster] = n * math.log(n) - n * math.log(N) - n * math.log(2.0 * numpy.pi) / 2.0 - n * dimension * math.log(sigma) / 2.0 - (n - K) / 2.0;
                  
        return sum(scores);
 
 
    def __update_clusters(self, centers, available_indexes = None):
        """!
        @brief Calculates Euclidean distance to each point from the each cluster.
               Nearest points are captured by according clusters and as a result clusters are updated.
               
        @param[in] centers (list): Coordinates of centers of clusters that are represented by list: [center1, center2, ...].
        @param[in] available_indexes (list): Indexes that defines which points can be used from imput data, if None - then all points are used.
        
        @return (list) Updated clusters.
        
        """
            
        bypass = None;
        if (available_indexes is None):
            bypass = range(len(self.__pointer_data));
        else:
            bypass = available_indexes;
          
        clusters = [[] for i in range(len(centers))];
        for index_point in bypass:
            index_optim = -1;
            dist_optim = 0.0;
              
            for index in range(len(centers)):
                # dist = euclidean_distance(data[index_point], centers[index]);         # Slow solution
                dist = euclidean_distance_sqrt(self.__pointer_data[index_point], centers[index]);      # Fast solution
                  
                if ( (dist < dist_optim) or (index is 0)):
                    index_optim = index;
                    dist_optim = dist;
              
            clusters[index_optim].append(index_point);
              
        return clusters;
             
     
    def __update_centers(self, clusters):
        """!
        @brief Updates centers of clusters in line with contained objects.
        
        @param[in] clusters (list): Clusters that contain indexes of objects from data.
        
        @return (list) Updated centers.
        
        """
         
        centers = [[] for i in range(len(clusters))];
        dimension = len(self.__pointer_data[0])
          
        for index in range(len(clusters)):
            point_sum = [0.0] * dimension;
              
            for index_point in clusters[index]:
                point_sum = list_math_addition(point_sum, self.__pointer_data[index_point]);
            
            centers[index] = list_math_division_number(point_sum, len(clusters[index]));
              
        return centers;
