"""!

@brief The module contains G-Means algorithm and other related services.
@details Implementation based on paper @cite inproceedings::gmeans::1.

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

from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.kmeans import kmeans


class gmeans:
    """!
    @brief Class implements G-Means clustering algorithm.
    @details The G-means algorithm starts with a small number of centers, and grows the number of centers.
              Each iteration of the G-Means algorithm splits into two those centers whose data appear not to come from a
              Gaussian distribution. G-means repeatedly makes decisions based on a statistical test for the data
              assigned to each center.

    Implementation based on the paper @cite inproceedings::gmeans::1.

    """

    def __init__(self, data, k_init, ccore=True, **kwargs):
        """!
        @brief Initializes G-Means algorithm.

        @param[in] data (array_like): Input data that is presented as array of points (objects), each point should be
                    represented by array_like data structure.
        @param[in] k_init (uint): Initial amount of centers.
        @param[in] ccore (bool): Defines whether CCORE library (C/C++ part of the library) should be used instead of
                    Python code.

        """
        self.__data = data
        self.__k_init = k_init

        self.__clusters = []
        self.__centers = []
        self.__total_wce = 0.0

        self.__tolerance = kwargs.get('tolerance', 0.025)
        self.__repeat = kwargs.get('repeat', 3)

        self._verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of G-Means algorithm.

        @return (gmeans) Returns itself (G-Means instance).

        @see get_clusters()
        @see get_centers()

        """
        self.__clusters, self.__centers, _ = self._search_optimal_parameters(self.__data, self.__k_init)
        while True:
            current_amount_clusters = len(self.__clusters)
            self._statistical_optimization()

            if current_amount_clusters == len(self.__centers):
                break

            self._perform_clustering()

        return self


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
        points = [self.__data[index_point] for index_point in cluster]
        new_clusters, new_centers, _ = self._search_optimal_parameters(points, 2)

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
