"""!

@brief Cluster analysis algorithm: Fuzzy C-Means
@details Implementation based on paper @cite book::pattern_recognition_with_fuzzy.

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

from pyclustering.core.wrapper import ccore_library


class fcm:
    """!
    @brief Class represents Fuzzy C-means clustering (FCM).
    @details Fuzzy clustering is a form of clustering in which each data point can belong to more than one cluster.

    """

    def __init__(self, data, initial_centers, **kwargs):
        """!
        @brief Initialize Fuzzy C-Means algorithm.

        @param[in] data (array_like): Input data that is presented as array of points (objects), each point should be represented by array_like data structure.
        @param[in] initial_centers (array_like): Initial coordinates of centers of clusters that are represented by array_like data structure: [center1, center2, ...].
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'tolerance', 'itermax', 'm').

        <b>Keyword Args:</b><br>
            - ccore (bool): Defines should be CCORE library (C++ pyclustering library) used instead of Python code or not.
            - tolerance (float): Stop condition: if maximum value of change of centers of clusters is less than tolerance then algorithm stops processing.
            - itermax (uint): Maximum number of iterations that is used for clustering process (by default: 200).
            - m (float): Hyper-parameter that controls how fuzzy the cluster will be. The higher it is, the fuzzier the cluster will be in the end.
               This parameter should be greater than 1 (by default: 2).

        """

        self.__ccore = kwargs.get('ccore', True)
        if self.__ccore is True:
            self.__ccore = ccore_library.workable()

        self.__data = numpy.array(data)
        self.__clusters = []
        self.__centers = numpy.array(initial_centers)
        self.__membership = []

        self.__tolerance = kwargs.get('tolerance', 0.001)
        self.__itermax = kwargs.get('itermax', 200)
        self.__m = kwargs.get('m', 2)

        self.__degree = 2.0 / (kwargs.get('m', 2) - 1)


    def process(self):
        """!
        @brief Performs cluster analysis in line with Fuzzy C-Means algorithm.

        @see get_clusters()
        @see get_centers()
        @see get_membership()

        """
        self.__process_by_python()
        return self


    def get_clusters(self):
        """!
        @brief Returns allocated clusters that consists of points that most likely (in line with membership) belong to
                these clusters.

        @remark Allocated clusters can be returned only after data processing (use method process()). Otherwise empty list is returned.

        @return (list) List of allocated clusters, each cluster contains indexes from input data.

        @see process()
        @see get_centers()
        @see get_membership()

        """
        return self.__clusters


    def get_centers(self):
        """!
        @brief Returns list of centers of allocated clusters.

        @return (array_like) Cluster centers.

        @see process()
        @see get_clusters()
        @see get_membership()

        """
        return self.__centers


    def get_membership(self):
        """!
        @brief Returns cluster membership (probability) for each point in data.

        @return (array_like) Membership for each point in format [[Px1(c1), Px1(c2), ...], [Px2(c1), Px2(c2), ...], ...],
                 where [Px1(c1), Px1(c2), ...] membership for point x1.

        @see process()
        @see get_clusters()
        @see get_centers()

        """
        return self.__membership


    def __process_by_python(self):
        """!
        @brief Performs cluster analysis using Python implementation.

        """
        self.__membership = numpy.random.rand(len(self.__data), len(self.__centers))
        self.__membership = self.__membership / self.__membership.sum(axis=1)[:, None]

        change = float('inf')
        iteration = 0

        while change > self.__tolerance and iteration < self.__itermax:
            self.__update_membership()
            centers = self.__calculate_centers()
            change = self.__calculate_changes(centers)

            self.__centers = centers
            iteration += 1

        self.__extract_clusters()


    def __calculate_centers(self):
        """!
        @brief Calculate center using membership of each cluster: TODO: formula

        @return (list) Updated clusters as list of clusters. Each cluster contains indexes of objects from data.

        @return (numpy.array) Updated centers.

        """
        dimension = self.__data.shape[1]
        centers = numpy.zeros((len(self.__centers), dimension))

        for i in range(len(self.__centers)):
            # multiplication '@' requires python version 3.5
            centers[i] = numpy.divide(self.__membership[:, i] @ self.__data, numpy.sum(self.__membership[:, i]))

        return centers


    def __update_membership(self):
        """!
        @brief Update membership for each point in line with current cluster centers.

        """
        data_difference = numpy.zeros((len(self.__centers), len(self.__data)))

        for i in range(len(self.__centers)):
            data_difference[i] = numpy.sum(numpy.square(self.__data - self.__centers[i]), axis=1)

        for i in range(len(self.__data)):
            for j in range(len(self.__centers)):
                divider = sum([pow(data_difference[j][i] / data_difference[k][i], self.__degree) for k in range(len(self.__centers))])
                self.__membership[i][j] = 1.0 / divider


    def __calculate_changes(self, updated_centers):
        """!
        @brief Calculate changes between centers.

        @return (float) Maximum change between centers.

        """
        changes = numpy.sum(numpy.square(self.__centers - updated_centers), axis=1).T
        return numpy.max(changes)


    def __extract_clusters(self):
        self.__clusters = [[] for i in range(len(self.__centers))]
        belongs = numpy.argmax(self.__membership, axis=1)

        for i in range(len(belongs)):
            self.__clusters[belongs[i]].append(i)
