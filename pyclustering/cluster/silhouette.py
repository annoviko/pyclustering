"""!

@brief Silhouette - method of interpretation and validation of consistency.
@details Implementation based on paper @cite article::cluster::silhouette::1.

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


from enum import IntEnum

import numpy

from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.kmedians import kmedians
from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer

from pyclustering.utils.metric import distance_metric, type_metric

from pyclustering.core.wrapper import ccore_library
from pyclustering.core.metric_wrapper import metric_wrapper

import pyclustering.core.silhouette_wrapper as wrapper


class silhouette:
    """!
    @brief Represents Silhouette method that is used interpretation and validation of consistency.
    @details The silhouette value is a measure of how similar an object is to its own cluster compared to other clusters.
              Be aware that silhouette method is applicable for K algorithm family, such as K-Means, K-Medians,
              K-Medoids, X-Means, etc., not not applicable for DBSCAN, OPTICS, CURE, etc. The Silhouette value is
              calculated using following formula:
              \f[s\left ( i \right )=\frac{ b\left ( i \right ) - a\left ( i \right ) }{ max\left \{ a\left ( i \right ), b\left ( i \right ) \right \}}\f]
              where \f$a\left ( i \right )\f$ - is average distance from object i to objects in its own cluster,
              \f$b\left ( i \right )\f$ - is average distance from object i to objects in the nearest cluster (the appropriate among other clusters).

    Here is an example where Silhouette score is calculated for K-Means's clustering result:
    @code
        from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
        from pyclustering.cluster.kmeans import kmeans
        from pyclustering.cluster.silhouette import silhouette

        from pyclustering.samples.definitions import SIMPLE_SAMPLES
        from pyclustering.utils import read_sample

        # Read data 'SampleSimple3' from Simple Sample collection.
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);

        # Prepare initial centers
        centers = kmeans_plusplus_initializer(sample, 4).initialize();

        # Perform cluster analysis
        kmeans_instance = kmeans(sample, centers);
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();

        # Calculate Silhouette score
        score = silhouette(sample, clusters).process().get_score()
    @endcode

    @see kmeans, kmedoids, kmedians, xmeans, elbow

    """

    def __init__(self, data, clusters, **kwargs):
        """!
        @brief Initializes Silhouette method for analysis.

        @param[in] data (array_like): Input data that was used for cluster analysis and that is presented as list of
                    points or distance matrix (defined by parameter 'data_type', by default data is considered as a list
                    of points).
        @param[in] clusters (list): Cluster that have been obtained after cluster analysis.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric').

        <b>Keyword Args:</b><br>
            - metric (distance_metric): Metric that was used for cluster analysis and should be used for Silhouette
               score calculation (by default Square Euclidean distance).
            - data_type (string): Data type of input sample 'data' that is processed by the algorithm ('points', 'distance_matrix').
            - ccore (bool): If True then CCORE (C++ implementation of pyclustering library) is used (by default True).

        """
        self.__data = data
        self.__clusters = clusters
        self.__metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))
        self.__data_type = kwargs.get('data_type', 'points')

        if self.__metric.get_type() != type_metric.USER_DEFINED:
            self.__metric.enable_numpy_usage()
        else:
            self.__metric.disable_numpy_usage()

        self.__score = [0.0] * len(data)

        self.__ccore = kwargs.get('ccore', True) and self.__metric.get_type() != type_metric.USER_DEFINED
        if self.__ccore:
            self.__ccore = ccore_library.workable()

        if self.__ccore is False:
            self.__data = numpy.array(data)

        self.__verify_arguments()


    def process(self):
        """!
        @brief Calculates Silhouette score for each object from input data.

        @return (silhouette) Instance of the method (self).

        """
        if self.__ccore is True:
            self.__process_by_ccore()
        else:
            self.__process_by_python()

        return self


    def __process_by_ccore(self):
        """!
        @brief Performs processing using CCORE (C/C++ part of pyclustering library).

        """
        ccore_metric = metric_wrapper.create_instance(self.__metric)
        self.__score = wrapper.silhoeutte(self.__data, self.__clusters, ccore_metric.get_pointer(), self.__data_type)


    def __process_by_python(self):
        """!
        @brief Performs processing using python code.

        """
        for index_cluster in range(len(self.__clusters)):
            for index_point in self.__clusters[index_cluster]:
                self.__score[index_point] = self.__calculate_score(index_point, index_cluster)


    def get_score(self):
        """!
        @brief Returns Silhouette score for each object from input data.

        @see process

        """
        return self.__score


    def __calculate_score(self, index_point, index_cluster):
        """!
        @brief Calculates Silhouette score for the specific object defined by index_point.

        @param[in] index_point (uint): Index point from input data for which Silhouette score should be calculated.
        @param[in] index_cluster (uint): Index cluster to which the point belongs to.

        @return (float) Silhouette score for the object.

        """
        if self.__data_type == 'points':
            difference = self.__calculate_dataset_difference(index_point)
        else:
            difference = self.__data[index_point]

        a_score = self.__calculate_within_cluster_score(index_cluster, difference)
        b_score = self.__caclulate_optimal_neighbor_cluster_score(index_cluster, difference)

        return (b_score - a_score) / max(a_score, b_score)


    def __calculate_within_cluster_score(self, index_cluster, difference):
        """!
        @brief Calculates 'A' score for the specific object in cluster to which it belongs to.

        @param[in] index_point (uint): Index point from input data for which 'A' score should be calculated.
        @param[in] index_cluster (uint): Index cluster to which the point is belong to.

        @return (float) 'A' score for the object.

        """

        score = self.__calculate_cluster_difference(index_cluster, difference)
        if len(self.__clusters[index_cluster]) == 1:
            return float('nan')
        return score / (len(self.__clusters[index_cluster]) - 1)


    def __calculate_cluster_score(self, index_cluster, difference):
        """!
        @brief Calculates 'B*' score for the specific object for specific cluster.

        @param[in] index_point (uint): Index point from input data for which 'B*' score should be calculated.
        @param[in] index_cluster (uint): Index cluster to which the point is belong to.

        @return (float) 'B*' score for the object for specific cluster.

        """

        score = self.__calculate_cluster_difference(index_cluster, difference)
        return score / len(self.__clusters[index_cluster])


    def __caclulate_optimal_neighbor_cluster_score(self, index_cluster, difference):
        """!
        @brief Calculates 'B' score for the specific object for the nearest cluster.

        @param[in] index_point (uint): Index point from input data for which 'B' score should be calculated.
        @param[in] index_cluster (uint): Index cluster to which the point is belong to.

        @return (float) 'B' score for the object.

        """

        optimal_score = float('inf')
        for index_neighbor_cluster in range(len(self.__clusters)):
            if index_cluster != index_neighbor_cluster:
                candidate_score = self.__calculate_cluster_score(index_neighbor_cluster, difference)
                if candidate_score < optimal_score:
                    optimal_score = candidate_score

        if optimal_score == float('inf'):
            optimal_score = -1.0

        return optimal_score


    def __calculate_cluster_difference(self, index_cluster, difference):
        """!
        @brief Calculates distance from each object in specified cluster to specified object.

        @param[in] index_point (uint): Index point for which difference is calculated.

        @return (list) Distance from specified object to each object from input data in specified cluster.

        """
        cluster_difference = 0.0
        for index_point in self.__clusters[index_cluster]:
            cluster_difference += difference[index_point]

        return cluster_difference


    def __calculate_dataset_difference(self, index_point):
        """!
        @brief Calculate distance from each object to specified object.

        @param[in] index_point (uint): Index point for which difference with other points is calculated.

        @return (list) Distance to each object from input data from the specified.

        """

        if self.__metric.get_type() != type_metric.USER_DEFINED:
            dataset_differences = self.__metric(self.__data, self.__data[index_point])
        else:
            dataset_differences = [self.__metric(point, self.__data[index_point]) for point in self.__data]

        return dataset_differences


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__data))

        if len(self.__clusters) == 0:
            raise ValueError("Input clusters are empty (size: '%d')." % len(self.__clusters))



class silhouette_ksearch_type(IntEnum):
    """!
    @brief Defines algorithms that can be used to find optimal number of cluster using Silhouette method.

    @see silhouette_ksearch

    """

    ## K-Means algorithm for searching optimal number of clusters.
    KMEANS = 0

    ## K-Medians algorithm for searching optimal number of clusters.
    KMEDIANS = 1

    ## K-Medoids algorithm for searching optimal number of clusters.
    KMEDOIDS = 2

    def get_type(self):
        """!
        @brief Returns algorithm type that corresponds to specified enumeration value.

        @return (type) Algorithm type for cluster analysis.

        """
        if self == silhouette_ksearch_type.KMEANS:
            return kmeans
        elif self == silhouette_ksearch_type.KMEDIANS:
            return kmedians
        elif self == silhouette_ksearch_type.KMEDOIDS:
            return kmedoids
        else:
            return None



class silhouette_ksearch:
    """!
    @brief Represent algorithm for searching optimal number of clusters using specified K-algorithm (K-Means,
            K-Medians, K-Medoids) that is based on Silhouette method.

    @details This algorithm uses average value of scores for estimation and applicable for clusters that are well
              separated. Here is an example where clusters are well separated (sample 'Hepta'):
    @code
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
        from pyclustering.cluster.kmeans import kmeans
        from pyclustering.cluster.silhouette import silhouette_ksearch_type, silhouette_ksearch
        from pyclustering.samples.definitions import FCPS_SAMPLES
        from pyclustering.utils import read_sample

        sample = read_sample(FCPS_SAMPLES.SAMPLE_HEPTA)
        search_instance = silhouette_ksearch(sample, 2, 10, algorithm=silhouette_ksearch_type.KMEANS).process()

        amount = search_instance.get_amount()
        scores = search_instance.get_scores()

        print("Scores: '%s'" % str(scores))

        initial_centers = kmeans_plusplus_initializer(sample, amount).initialize()
        kmeans_instance = kmeans(sample, initial_centers).process()

        clusters = kmeans_instance.get_clusters()

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    @endcode

    Obtained Silhouette scores for each K:
    @code
    Scores: '{2: 0.418434, 3: 0.450906, 4: 0.534709, 5: 0.689970, 6: 0.588460, 7: 0.882674, 8: 0.804725, 9: 0.780189}'
    @endcode

    K = 7 has the bigger average Silhouette score and it means that it is optimal amount of clusters:
    @image html silhouette_ksearch_hepta.png "Silhouette ksearch's analysis with further K-Means clustering (sample 'Hepta')."

    @see silhouette_ksearch_type

    """

    def __init__(self, data, kmin, kmax, **kwargs):
        """!
        @brief Initialize Silhouette search algorithm to find out optimal amount of clusters.

        @param[in] data (array_like): Input data that is used for searching optimal amount of clusters.
        @param[in] kmin (uint): Amount of clusters from which search is performed. Should be equal or greater than 2.
        @param[in] kmax (uint): Amount of clusters to which search is performed. Should be equal or less than amount of
                    points in input data.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'algorithm').

        <b>Keyword Args:</b><br>
            - algorithm (silhouette_ksearch_type): Defines algorithm that is used for searching optimal number of
               clusters (by default K-Means).
            - ccore (bool): If True then CCORE (C++ implementation of pyclustering library) is used (by default True).

        """
        self.__data = data
        self.__kmin = kmin
        self.__kmax = kmax

        self.__algorithm = kwargs.get('algorithm', silhouette_ksearch_type.KMEANS)
        self.__return_index = self.__algorithm == silhouette_ksearch_type.KMEDOIDS

        self.__amount = -1
        self.__score = -1.0
        self.__scores = {}

        self.__verify_arguments()

        self.__ccore = kwargs.get('ccore', True)
        if self.__ccore:
            self.__ccore = ccore_library.workable()


    def process(self):
        """!
        @brief Performs analysis to find optimal amount of clusters.

        @see get_amount, get_score, get_scores

        @return (silhouette_search) Itself instance (silhouette_search)

        """
        if self.__ccore is True:
            self.__process_by_ccore()
        else:
            self.__process_by_python()

        return self


    def __process_by_ccore(self):
        """!
        @brief Performs processing using CCORE (C/C++ part of pyclustering library).

        """
        results = wrapper.silhoeutte_ksearch(self.__data, self.__kmin, self.__kmax, self.__algorithm)

        self.__amount = results[0]
        self.__score = results[1]
        self.__scores = results[2]


    def __process_by_python(self):
        """!
        @brief Performs processing using python code.

        """
        self.__scores = {}

        for k in range(self.__kmin, self.__kmax):
            clusters = self.__calculate_clusters(k)
            if len(clusters) != k:
                self.__scores[k] = float('nan')
                continue

            score = silhouette(self.__data, clusters).process().get_score()

            self.__scores[k] = sum(score) / len(score)

            if self.__scores[k] > self.__score:
                self.__score = self.__scores[k]
                self.__amount = k


    def get_amount(self):
        """!
        @brief Returns optimal amount of clusters that has been found during analysis.

        @return (uint) Optimal amount of clusters.

        @see process

        """
        return self.__amount


    def get_score(self):
        """!
        @brief Returns silhouette score that belongs to optimal amount of clusters (k).

        @return (float) Score that belong to optimal amount of clusters.

        @see process, get_scores

        """
        return self.__score


    def get_scores(self):
        """!
        @brief Returns silhouette score for each K value (amount of clusters).

        @return (dict) Silhouette score for each K value, where key is a K value and value is a silhouette score.

        @see process, get_score

        """
        return self.__scores


    def __calculate_clusters(self, k):
        """!
        @brief Performs cluster analysis using specified K value.

        @param[in] k (uint): Amount of clusters that should be allocated.

        @return (array_like) Allocated clusters.

        """
        initial_values = kmeans_plusplus_initializer(self.__data, k).initialize(return_index=self.__return_index)
        algorithm_type = self.__algorithm.get_type()
        return algorithm_type(self.__data, initial_values).process().get_clusters()


    def __verify_arguments(self):
        """!
        @brief Checks algorithm's arguments and if some of them is incorrect then exception is thrown.

        """
        if self.__kmax > len(self.__data):
            raise ValueError("K max value '" + str(self.__kmax) + "' is bigger than amount of objects '" +
                             str(len(self.__data)) + "' in input data.")

        if self.__kmin <= 1:
            raise ValueError("K min value '" + str(self.__kmin) + "' should be greater than 1 (impossible to provide "
                             "silhouette score for only one cluster).")
