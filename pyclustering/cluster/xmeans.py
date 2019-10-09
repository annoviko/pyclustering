"""!

@brief Cluster analysis algorithm: X-Means
@details Implementation based on paper @cite article::xmeans::1.

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


import numpy
import random

from enum import IntEnum

from math import log

from pyclustering.cluster.encoder import type_encoding
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer

from pyclustering.core.wrapper import ccore_library

import pyclustering.core.xmeans_wrapper as wrapper

from pyclustering.utils import euclidean_distance_square, euclidean_distance, distance_metric, type_metric


class splitting_type(IntEnum):
    """!
    @brief Enumeration of splitting types that can be used as splitting creation of cluster in X-Means algorithm.
    
    """
    
    ## Bayesian information criterion (BIC) to approximate the correct number of clusters.
    ## Kass's formula is used to calculate BIC:
    ## \f[BIC(\theta) = L(D) - \frac{1}{2}pln(N)\f]
    ##
    ## The number of free parameters \f$p\f$ is simply the sum of \f$K - 1\f$ class probabilities, \f$MK\f$ centroid coordinates, and one variance estimate:
    ## \f[p = (K - 1) + MK + 1\f]
    ##
    ## The log-likelihood of the data:
    ## \f[L(D) = n_jln(n_j) - n_jln(N) - \frac{n_j}{2}ln(2\pi) - \frac{n_jd}{2}ln(\hat{\sigma}^2) - \frac{n_j - K}{2}\f]
    ##
    ## The maximum likelihood estimate (MLE) for the variance:
    ## \f[\hat{\sigma}^2 = \frac{1}{N - K}\sum\limits_{j}\sum\limits_{i}||x_{ij} - \hat{C}_j||^2\f]
    BAYESIAN_INFORMATION_CRITERION = 0
    
    ## Minimum noiseless description length (MNDL) to approximate the correct number of clusters.
    ## Beheshti's formula is used to calculate upper bound:
    ## \f[Z = \frac{\sigma^2 \sqrt{2K} }{N}(\sqrt{2K} + \beta) + W - \sigma^2 + \frac{2\alpha\sigma}{\sqrt{N}}\sqrt{\frac{\alpha^2\sigma^2}{N} + W - \left(1 - \frac{K}{N}\right)\frac{\sigma^2}{2}} + \frac{2\alpha^2\sigma^2}{N}\f]
    ##
    ## where \f$\alpha\f$ and \f$\beta\f$ represent the parameters for validation probability and confidence probability.
    ##
    ## To improve clustering results some contradiction is introduced:
    ## \f[W = \frac{1}{n_j}\sum\limits_{i}||x_{ij} - \hat{C}_j||\f]
    ## \f[\hat{\sigma}^2 = \frac{1}{N - K}\sum\limits_{j}\sum\limits_{i}||x_{ij} - \hat{C}_j||\f]
    MINIMUM_NOISELESS_DESCRIPTION_LENGTH = 1


class xmeans:
    """!
    @brief Class represents clustering algorithm X-Means.
    @details X-means clustering method starts with the assumption of having a minimum number of clusters, 
             and then dynamically increases them. X-means uses specified splitting criterion to control 
             the process of splitting clusters. Method K-Means++ can be used for calculation of initial centers.
             
             CCORE implementation of the algorithm uses thread pool to parallelize the clustering process.
    
    Here example how to perform cluster analysis using X-Means algorithm:
    @code
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.cluster.xmeans import xmeans
        from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import SIMPLE_SAMPLES

        # Read sample 'simple3' from file.
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

        # Prepare initial centers - amount of initial centers defines amount of clusters from which X-Means will
        # start analysis.
        amount_initial_centers = 2
        initial_centers = kmeans_plusplus_initializer(sample, amount_initial_centers).initialize()

        # Create instance of X-Means algorithm. The algorithm will start analysis from 2 clusters, the maximum
        # number of clusters that can be allocated is 20.
        xmeans_instance = xmeans(sample, initial_centers, 20)
        xmeans_instance.process()

        # Extract clustering results: clusters and their centers
        clusters = xmeans_instance.get_clusters()
        centers = xmeans_instance.get_centers()

        # Print total sum of metric errors
        print("Total WCE:", xmeans_instance.get_total_wce())

        # Visualize clustering results
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.append_cluster(centers, None, marker='*', markersize=10)
        visualizer.show()
    @endcode

    Visualization of clustering results that were obtained using code above and where X-Means algorithm allocates four clusters.
    @image html xmeans_clustering_simple3.png "Fig. 1. X-Means clustering results (data 'Simple3')."
    
    @see center_initializer
    
    """
    
    def __init__(self, data, initial_centers=None, kmax=20, tolerance=0.025, criterion=splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore=True, **kwargs):
        """!
        @brief Constructor of clustering algorithm X-Means.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] initial_centers (list): Initial coordinates of centers of clusters that are represented by list: [center1, center2, ...], 
                    if it is not specified then X-Means starts from the random center.
        @param[in] kmax (uint): Maximum number of clusters that can be allocated.
        @param[in] tolerance (double): Stop condition for each iteration: if maximum value of change of centers of clusters is less than tolerance than algorithm will stop processing.
        @param[in] criterion (splitting_type): Type of splitting creation.
        @param[in] ccore (bool): Defines should be CCORE (C++ pyclustering library) used instead of Python code or not.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'repeat').

        <b>Keyword Args:</b><br>
            - repeat (unit): How many times K-Means should be run to improve parameters (by default is 1).
               With larger 'repeat' values suggesting higher probability of finding global optimum.

        """
        
        self.__pointer_data = data
        self.__clusters = []
        
        if initial_centers is not None:
            self.__centers = initial_centers[:]
        else:
            self.__centers = kmeans_plusplus_initializer(data, 2).initialize()
        
        self.__kmax = kmax
        self.__tolerance = tolerance
        self.__criterion = criterion
        self.__total_wce = 0.0
        self.__repeat = kwargs.get('repeat', 1)
         
        self.__ccore = ccore
        if self.__ccore:
            self.__ccore = ccore_library.workable()

        self.__verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of X-Means algorithm.
        
        @return (xmeans) Returns itself (X-Means instance).
        
        @see get_clusters()
        @see get_centers()
        
        """
        
        if self.__ccore is True:
            self.__process_by_ccore()

        else:
            self.__process_by_python()

        return self


    def __process_by_ccore(self):
        """!
        @brief Performs cluster analysis using CCORE (C/C++ part of pyclustering library).

        """

        result = wrapper.xmeans(self.__pointer_data, self.__centers, self.__kmax, self.__tolerance, self.__criterion, self.__repeat)
        self.__clusters = result[0]
        self.__centers = result[1]
        self.__total_wce = result[2][0]


    def __process_by_python(self):
        """!
        @brief Performs cluster analysis using python code.

        """

        self.__clusters = []
        while len(self.__centers) <= self.__kmax:
            current_cluster_number = len(self.__centers)

            self.__clusters, self.__centers, _ = self.__improve_parameters(self.__centers)
            allocated_centers = self.__improve_structure(self.__clusters, self.__centers)

            if current_cluster_number == len(allocated_centers):
                break
            else:
                self.__centers = allocated_centers

        self.__clusters, self.__centers, self.__total_wce = self.__improve_parameters(self.__centers)


    def predict(self, points):
        """!
        @brief Calculates the closest cluster to each point.

        @param[in] points (array_like): Points for which closest clusters are calculated.

        @return (list) List of closest clusters for each point. Each cluster is denoted by index. Return empty
                 collection if 'process()' method was not called.

        An example how to calculate (or predict) the closest cluster to specified points.
        @code
            from pyclustering.cluster.xmeans import xmeans
            from pyclustering.samples.definitions import SIMPLE_SAMPLES
            from pyclustering.utils import read_sample

            # Load list of points for cluster analysis.
            sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

            # Initial centers for sample 'Simple3'.
            initial_centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]

            # Create instance of X-Means algorithm with prepared centers.
            xmeans_instance = xmeans(sample, initial_centers)

            # Run cluster analysis.
            xmeans_instance.process()

            # Calculate the closest cluster to following two points.
            points = [[0.25, 0.2], [2.5, 4.0]]
            closest_clusters = xmeans_instance.predict(points)
            print(closest_clusters)
        @endcode

        """
        nppoints = numpy.array(points)
        if len(self.__clusters) == 0:
            return []

        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE, numpy_usage=True)

        differences = numpy.zeros((len(nppoints), len(self.__centers)))
        for index_point in range(len(nppoints)):
            differences[index_point] = metric(nppoints[index_point], self.__centers)

        return numpy.argmin(differences, axis=1)


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @return (list) List of allocated clusters.
        
        @see process()
        @see get_centers()
        @see get_total_wce()
        
        """

        return self.__clusters


    def get_centers(self):
        """!
        @brief Returns list of centers for allocated clusters.
        
        @return (list) List of centers for allocated clusters.
        
        @see process()
        @see get_clusters()
        @see get_total_wce()
        
        """
         
        return self.__centers


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def get_total_wce(self):
        """!
        @brief Returns sum of Euclidean Squared metric errors (SSE - Sum of Squared Errors).
        @details Sum of metric errors is calculated using distance between point and its center:
                 \f[error=\sum_{i=0}^{N}euclidean_square_distance(x_{i}-center(x_{i}))\f]

        @see process()
        @see get_clusters()

        """

        return self.__total_wce


    def __search_optimial_parameters(self, local_data):
        """!
        @brief Split data of the region into two cluster and tries to find global optimum by running k-means clustering
                several times (defined by 'repeat' argument).

        @param[in] local_data (list): Points of a region that should be split into two clusters.

        @return (tuple) List of allocated clusters, list of centers and total WCE (clusters, centers, wce).

        """
        optimal_wce, optimal_centers, optimal_clusters = float('+inf'), None, None

        for _ in range(self.__repeat):
            candidates = 5
            if len(local_data) < candidates:
                candidates = len(local_data)

            local_centers = kmeans_plusplus_initializer(local_data, 2, candidates).initialize()

            kmeans_instance = kmeans(local_data, local_centers, tolerance=self.__tolerance, ccore=False)
            kmeans_instance.process()

            local_wce = kmeans_instance.get_total_wce()
            if local_wce < optimal_wce:
                optimal_centers = kmeans_instance.get_centers()
                optimal_clusters = kmeans_instance.get_clusters()
                optimal_wce = local_wce

        return optimal_clusters, optimal_centers, optimal_wce


    def __improve_parameters(self, centers, available_indexes=None):
        """!
        @brief Performs k-means clustering in the specified region.
        
        @param[in] centers (list): Cluster centers, if None then automatically generated two centers using center initialization method.
        @param[in] available_indexes (list): Indexes that defines which points can be used for k-means clustering, if None then all points are used.
        
        @return (tuple) List of allocated clusters, list of centers and total WCE (clusters, centers, wce).
        
        """

        if available_indexes and len(available_indexes) == 1:
            index_center = available_indexes[0]
            return [available_indexes], self.__pointer_data[index_center], 0.0

        local_data = self.__pointer_data
        if available_indexes:
            local_data = [self.__pointer_data[i] for i in available_indexes]

        local_centers = centers
        if centers is None:
            clusters, local_centers, local_wce = self.__search_optimial_parameters(local_data)
        else:
            kmeans_instance = kmeans(local_data, local_centers, tolerance=self.__tolerance, ccore=False).process()

            local_wce = kmeans_instance.get_total_wce()
            local_centers = kmeans_instance.get_centers()
            clusters = kmeans_instance.get_clusters()

        if available_indexes:
            clusters = self.__local_to_global_clusters(clusters, available_indexes)
        
        return clusters, local_centers, local_wce


    def __local_to_global_clusters(self, local_clusters, available_indexes):
        """!
        @brief Converts clusters in local region define by 'available_indexes' to global clusters.

        @param[in] local_clusters (list): Local clusters in specific region.
        @param[in] available_indexes (list): Map between local and global point's indexes.

        @return Global clusters.

        """

        clusters = []
        for local_cluster in local_clusters:
            current_cluster = []
            for index_point in local_cluster:
                current_cluster.append(available_indexes[index_point])

            clusters.append(current_cluster)

        return clusters

    
    def __improve_structure(self, clusters, centers):
        """!
        @brief Check for best structure: divides each cluster into two and checks for best results using splitting criterion.
        
        @param[in] clusters (list): Clusters that have been allocated (each cluster contains indexes of points from data).
        @param[in] centers (list): Centers of clusters.
        
        @return (list) Allocated centers for clustering.
        
        """

        allocated_centers = []
        amount_free_centers = self.__kmax - len(centers)

        for index_cluster in range(len(clusters)):
            # solve k-means problem for children where data of parent are used.
            (parent_child_clusters, parent_child_centers, _) = self.__improve_parameters(None, clusters[index_cluster])

            # If it's possible to split current data
            if len(parent_child_clusters) > 1:
                # Calculate splitting criterion
                parent_scores = self.__splitting_criterion([clusters[index_cluster]], [centers[index_cluster]])
                child_scores = self.__splitting_criterion([parent_child_clusters[0], parent_child_clusters[1]], parent_child_centers)
              
                split_require = False
                
                # Reallocate number of centers (clusters) in line with scores
                if self.__criterion == splitting_type.BAYESIAN_INFORMATION_CRITERION:
                    if parent_scores < child_scores: split_require = True
                    
                elif self.__criterion == splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH:
                    # If its score for the split structure with two children is smaller than that for the parent structure, 
                    # then representing the data samples with two clusters is more accurate in comparison to a single parent cluster.
                    if parent_scores > child_scores: split_require = True;
                
                if (split_require is True) and (amount_free_centers > 0):
                    allocated_centers.append(parent_child_centers[0])
                    allocated_centers.append(parent_child_centers[1])
                    
                    amount_free_centers -= 1
                else:
                    allocated_centers.append(centers[index_cluster])

            else:
                allocated_centers.append(centers[index_cluster])
          
        return allocated_centers
     
     
    def __splitting_criterion(self, clusters, centers):
        """!
        @brief Calculates splitting criterion for input clusters.
        
        @param[in] clusters (list): Clusters for which splitting criterion should be calculated.
        @param[in] centers (list): Centers of the clusters.
        
        @return (double) Returns splitting criterion. High value of splitting cretion means that current structure is much better.
        
        @see __bayesian_information_criterion(clusters, centers)
        @see __minimum_noiseless_description_length(clusters, centers)
        
        """
        
        if self.__criterion == splitting_type.BAYESIAN_INFORMATION_CRITERION:
            return self.__bayesian_information_criterion(clusters, centers)
        
        elif self.__criterion == splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH:
            return self.__minimum_noiseless_description_length(clusters, centers)

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
        
        scores = float('inf')
        
        W = 0.0
        K = len(clusters)
        N = 0.0

        sigma_sqrt = 0.0
        
        alpha = 0.9
        betta = 0.9
        
        for index_cluster in range(0, len(clusters), 1):
            Ni = len(clusters[index_cluster])
            if Ni == 0:
                return float('inf')
            
            Wi = 0.0
            for index_object in clusters[index_cluster]:
                # euclidean_distance_square should be used in line with paper, but in this case results are
                # very poor, therefore square root is used to improved.
                Wi += euclidean_distance(self.__pointer_data[index_object], centers[index_cluster])
            
            sigma_sqrt += Wi
            W += Wi / Ni
            N += Ni
        
        if N - K > 0:
            sigma_sqrt /= (N - K)
            sigma = sigma_sqrt ** 0.5
            
            Kw = (1.0 - K / N) * sigma_sqrt
            Ks = ( 2.0 * alpha * sigma / (N ** 0.5) ) * ( (alpha ** 2.0) * sigma_sqrt / N + W - Kw / 2.0 ) ** 0.5
            
            scores = sigma_sqrt * (2 * K)**0.5 * ((2 * K)**0.5 + betta) / N + W - sigma_sqrt + Ks + 2 * alpha**0.5 * sigma_sqrt / N
        
        return scores


    def __bayesian_information_criterion(self, clusters, centers):
        """!
        @brief Calculates splitting criterion for input clusters using bayesian information criterion.
        
        @param[in] clusters (list): Clusters for which splitting criterion should be calculated.
        @param[in] centers (list): Centers of the clusters.
        
        @return (double) Splitting criterion in line with bayesian information criterion.
                High value of splitting criterion means that current structure is much better.
                
        @see __minimum_noiseless_description_length(clusters, centers)
        
        """

        scores = [float('inf')] * len(clusters)     # splitting criterion
        dimension = len(self.__pointer_data[0])
          
        # estimation of the noise variance in the data set
        sigma_sqrt = 0.0
        K = len(clusters)
        N = 0.0
          
        for index_cluster in range(0, len(clusters), 1):
            for index_object in clusters[index_cluster]:
                sigma_sqrt += euclidean_distance_square(self.__pointer_data[index_object], centers[index_cluster])

            N += len(clusters[index_cluster])
      
        if N - K > 0:
            sigma_sqrt /= (N - K)
            p = (K - 1) + dimension * K + 1

            # in case of the same points, sigma_sqrt can be zero (issue: #407)
            sigma_multiplier = 0.0
            if sigma_sqrt <= 0.0:
                sigma_multiplier = float('-inf')
            else:
                sigma_multiplier = dimension * 0.5 * log(sigma_sqrt)
            
            # splitting criterion    
            for index_cluster in range(0, len(clusters), 1):
                n = len(clusters[index_cluster])

                L = n * log(n) - n * log(N) - n * 0.5 * log(2.0 * numpy.pi) - n * sigma_multiplier - (n - K) * 0.5
                
                # BIC calculation
                scores[index_cluster] = L - p * 0.5 * log(N)
                
        return sum(scores)


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__pointer_data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__pointer_data))

        if len(self.__centers) == 0:
            raise ValueError("Initial centers are empty (size: '%d')." % len(self.__pointer_data))

        if self.__tolerance < 0:
            raise ValueError("Tolerance (current value: '%d') should be greater or equal to 0." %
                             self.__tolerance)

        if self.__repeat <= 0:
            raise ValueError("Repeat (current value: '%d') should be greater than 0." %
                             self.__repeat)
