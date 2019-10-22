"""!

@brief The module contains G-Means algorithm and other related services.
@details Implementation based on paper @cite inproceedings::cluster::gmeans::1.

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
import scipy.stats

from pyclustering.core.gmeans_wrapper import gmeans as gmeans_wrapper
from pyclustering.core.wrapper import ccore_library

from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.kmeans import kmeans
from pyclustering.utils import distance_metric, type_metric


class gmeans:
    """!
    @brief Class implements G-Means clustering algorithm.
    @details The G-means algorithm starts with a small number of centers, and grows the number of centers.
              Each iteration of the G-Means algorithm splits into two those centers whose data appear not to come from a
              Gaussian distribution. G-means repeatedly makes decisions based on a statistical test for the data
              assigned to each center.

    Implementation based on the paper @cite inproceedings::cluster::gmeans::1.

    @image html gmeans_example_clustering.png "G-Means clustering results on most common data-sets."

    Example #1. In this example, G-Means starts analysis from single cluster.
    @code
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.cluster.gmeans import gmeans
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import FCPS_SAMPLES

        # Read sample 'Lsun' from file.
        sample = read_sample(FCPS_SAMPLES.SAMPLE_LSUN)

        # Create instance of G-Means algorithm. By default the algorithm starts search from a single cluster.
        gmeans_instance = gmeans(sample).process()

        # Extract clustering results: clusters and their centers
        clusters = gmeans_instance.get_clusters()
        centers = gmeans_instance.get_centers()

        # Print total sum of metric errors
        print("Total WCE:", gmeans_instance.get_total_wce())

        # Visualize clustering results
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    @endcode

    Example #2. Sometimes G-Means may found local optimum. 'repeat' value can be used to increase probability to
    find global optimum. Argument 'repeat' defines how many times K-Means clustering with K-Means++
    initialization should be run to find optimal clusters.
    @code
        # Read sample 'Tetra' from file.
        sample = read_sample(FCPS_SAMPLES.SAMPLE_TETRA)

        # Create instance of G-Means algorithm. By default algorithm start search from single cluster.
        gmeans_instance = gmeans(sample, repeat=10).process()

        # Extract clustering results: clusters and their centers
        clusters = gmeans_instance.get_clusters()

        # Visualize clustering results
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    @endcode

    """

    def __init__(self, data, k_init=1, ccore=True, **kwargs):
        """!
        @brief Initializes G-Means algorithm.

        @param[in] data (array_like): Input data that is presented as array of points (objects), each point should be
                    represented by array_like data structure.
        @param[in] k_init (uint): Initial amount of centers (by default started search from 1).
        @param[in] ccore (bool): Defines whether CCORE library (C/C++ part of the library) should be used instead of
                    Python code.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'tolerance', 'repeat').

        <b>Keyword Args:</b><br>
            - tolerance (double): tolerance (double): Stop condition for each K-Means iteration: if maximum value of
               change of centers of clusters is less than tolerance than algorithm will stop processing.
            - repeat (unit): How many times K-Means should be run to improve parameters (by default is 3).
               With larger 'repeat' values suggesting higher probability of finding global optimum.

        """
        self.__data = data
        self.__k_init = k_init

        self.__clusters = []
        self.__centers = []
        self.__total_wce = 0.0
        self.__ccore = ccore

        self.__tolerance = kwargs.get('tolerance', 0.025)
        self.__repeat = kwargs.get('repeat', 3)

        if self.__ccore is True:
            self.__ccore = ccore_library.workable()

        self._verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of G-Means algorithm.

        @return (gmeans) Returns itself (G-Means instance).

        @see get_clusters()
        @see get_centers()

        """
        if self.__ccore is True:
            return self._process_by_ccore()

        return self._process_by_python()


    def _process_by_ccore(self):
        """!
        @brief Performs cluster analysis using CCORE (C/C++ part of pyclustering library).

        """
        self.__clusters, self.__centers, self.__total_wce = gmeans_wrapper(self.__data, self.__k_init, self.__tolerance, self.__repeat)
        return self


    def _process_by_python(self):
        """!
        @brief Performs cluster analysis using Python.

        """
        self.__clusters, self.__centers, _ = self._search_optimal_parameters(self.__data, self.__k_init)
        while True:
            current_amount_clusters = len(self.__clusters)
            self._statistical_optimization()

            if current_amount_clusters == len(self.__centers):
                break

            self._perform_clustering()

        return self


    def predict(self, points):
        """!
        @brief Calculates the closest cluster to each point.

        @param[in] points (array_like): Points for which closest clusters are calculated.

        @return (list) List of closest clusters for each point. Each cluster is denoted by index. Return empty
                 collection if 'process()' method was not called.

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

        @return (array_like) Allocated clusters.

        @see process()
        @see get_centers()

        """
        return self.__clusters


    def get_centers(self):
        """!
        @brief Returns list of centers of allocated clusters.

        @return (array_like) Allocated centers.

        @see process()
        @see get_clusters()

        """
        return self.__centers


    def get_total_wce(self):
        """!
        @brief Returns sum of metric errors that depends on metric that was used for clustering (by default SSE - Sum of Squared Errors).
        @details Sum of metric errors is calculated using distance between point and its center:
                 \f[error=\sum_{i=0}^{N}distance(x_{i}-center(x_{i}))\f]

        @see process()
        @see get_clusters()

        """

        return self.__total_wce


    def _statistical_optimization(self):
        """!
        @brief Try to split cluster into two to find optimal amount of clusters.

        """
        centers = []
        for index in range(len(self.__clusters)):
            new_centers = self._split_and_search_optimal(self.__clusters[index])
            if new_centers is None:
                centers.append(self.__centers[index])
            else:
                centers += new_centers

        self.__centers = centers


    def _split_and_search_optimal(self, cluster):
        """!
        @brief Split specified cluster into two by performing K-Means clustering and check correctness by
                Anderson-Darling test.

        @param[in] cluster (array_like) Cluster that should be analysed and optimized by splitting if it is required.

        @return (array_like) Two new centers if two new clusters are considered as more suitable.
                (None) If current cluster is more suitable.
        """
        if len(cluster) == 1:
            return None

        points = [self.__data[index_point] for index_point in cluster]
        new_clusters, new_centers, _ = self._search_optimal_parameters(points, 2)

        if len(new_centers) > 1:
            accept_null_hypothesis = self._is_null_hypothesis(points, new_centers)
            if not accept_null_hypothesis:
                return new_centers  # If null hypothesis is rejected then use two new clusters

        return None


    def _is_null_hypothesis(self, data, centers):
        """!
        @brief Returns whether H0 hypothesis is accepted using Anderson-Darling test statistic.

        @param[in] data (array_like): N-dimensional data for statistical test.
        @param[in] centers (array_like): Two new allocated centers.

        @return (bool) True is null hypothesis is acceptable.

        """
        v = numpy.subtract(centers[0], centers[1])
        points = self._project_data(data, v)

        estimation, critical, _ = scipy.stats.anderson(points, dist='norm')  # the Anderson-Darling test statistic

        # If the returned statistic is larger than these critical values then for the corresponding significance level,
        # the null hypothesis that the data come from the chosen distribution can be rejected.
        return estimation < critical[-1]  # False - not a gaussian distribution (reject H0)


    @staticmethod
    def _project_data(data, vector):
        """!
        @brief Transform input data by project it onto input vector using formula:

        \f[
        x_{i}^{*}=\frac{\left \langle x_{i}, v \right \rangle}{\left \| v \right \|^{2}}.
        \f]

        @param[in] data (array_like): Input data that is represented by points.
        @param[in] vector (array_like): Input vector that is used for projection.

        @return (array_like) Transformed 1-dimensional data.

        """
        square_norm = numpy.sum(numpy.multiply(vector, vector))
        return numpy.divide(numpy.sum(numpy.multiply(data, vector), axis=1), square_norm)


    def _search_optimal_parameters(self, data, amount):
        """!
        @brief Performs cluster analysis for specified data several times to find optimal clustering result in line
                with WCE.

        @param[in] data (array_like): Input data that should be clustered.
        @param[in] amount (unit): Amount of clusters that should be allocated.

        @return (tuple) Optimal clustering result: (clusters, centers, wce).

        """
        best_wce, best_clusters, best_centers = float('+inf'), [], []
        for _ in range(self.__repeat):
            initial_centers = kmeans_plusplus_initializer(data, amount).initialize()
            solver = kmeans(data, initial_centers, tolerance=self.__tolerance, ccore=False).process()

            candidate_wce = solver.get_total_wce()
            if candidate_wce < best_wce:
                best_wce = candidate_wce
                best_clusters = solver.get_clusters()
                best_centers = solver.get_centers()

            if len(initial_centers) == 1:
                break   # No need to rerun clustering for one initial center.

        return best_clusters, best_centers, best_wce


    def _perform_clustering(self):
        """!
        @brief Performs cluster analysis using K-Means algorithm using current centers are initial.

        @param[in] data (array_like): Input data for cluster analysis.

        """
        solver = kmeans(self.__data, self.__centers, tolerance=self.__tolerance, ccore=False).process()
        self.__clusters = solver.get_clusters()
        self.__centers = solver.get_centers()
        self.__total_wce = solver.get_total_wce()


    def _verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__data))

        if self.__k_init <= 0:
            raise ValueError("Initial amount of centers should be greater than 0 "
                             "(current value: '%d')." % self.__k_init)

        if self.__tolerance <= 0.0:
            raise ValueError("Tolerance should be greater than 0 (current value: '%f')." % self.__tolerance)

        if self.__repeat <= 0:
            raise ValueError("Amount of attempt to find optimal parameters should be greater than 0 "
                             "(current value: '%d')." % self.__repeat)
