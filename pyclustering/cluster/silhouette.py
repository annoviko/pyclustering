"""!

@brief Silhouette - method of interpretation and validation of consistency.
@details Implementation based on paper @cite article::cluster::silhouette::1.

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


from pyclustering.utils.metric import distance_metric, type_metric


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

        @param[in] data (array_like): Input data that was used for cluster analysis.
        @param[in] clusters (list): Cluster that have been obtained after cluster analysis.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric').

        <b>Keyword Args:</b><br>
            - metric (distance_metric): Metric that was used for cluster analysis and should be used for Silhouette
               score calculation (by default Square Euclidean distance).

        """
        self.__data = data
        self.__clusters = clusters
        self.__metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE))

        self.__score = [0.0] * len(data)


    def process(self):
        """!
        @brief Calculates Silhouette score for each object from input data.

        @return (silhouette) Instance of the method (self).

        """
        for index_cluster in range(len(self.__clusters)):
            for index_point in self.__clusters[index_cluster]:
                self.__score[index_point] = self.__calculate_score(index_point, index_cluster)

        return self


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
        difference = self.__calculate_dataset_difference(index_point)

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
                candidate_score = self.__calculate_cluster_score(index_cluster, difference)
                if candidate_score < optimal_score:
                    optimal_score = candidate_score

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