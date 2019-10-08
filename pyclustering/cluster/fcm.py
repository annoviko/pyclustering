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

import pyclustering.core.fcm_wrapper as wrapper

from pyclustering.core.wrapper import ccore_library


class fcm:
    """!
    @brief Class represents Fuzzy C-means (FCM) clustering algorithm.
    @details Fuzzy clustering is a form of clustering in which each data point can belong to more than one cluster.

    Fuzzy C-Means algorithm uses two general formulas for cluster analysis. The first is to updated membership of each
    point:
    \f[w_{ij}=\frac{1}{\sum_{k=0}^{c}\left ( \frac{\left \| x_{i}-c_{j} \right \|}{\left \| x_{i}-c_{k} \right \|} \right )^{\frac{2}{m-1}}}\f]

    The second formula is used to update centers in line with obtained centers:
    \f[c_{k}=\frac{\sum_{i=0}^{N}w_{k}\left ( x_{i} \right )^{m}x_{i}}{\sum_{i=0}^{N}w_{k}\left ( x_{i} \right )^{m}}\f]

    Fuzzy C-Means clustering results depend on initial centers. Algorithm K-Means++ can used for center initialization
    from module 'pyclustering.cluster.center_initializer'.

    CCORE implementation of the algorithm uses thread pool to parallelize the clustering process.

    Here is an example how to perform cluster analysis using Fuzzy C-Means algorithm:
    @code
        from pyclustering.samples.definitions import FAMOUS_SAMPLES
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
        from pyclustering.cluster.fcm import fcm
        from pyclustering.utils import read_sample

        # load list of points for cluster analysis
        sample = read_sample(FAMOUS_SAMPLES.SAMPLE_OLD_FAITHFUL)

        # initialize
        initial_centers = kmeans_plusplus_initializer(sample, 2, kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE).initialize()

        # create instance of Fuzzy C-Means algorithm
        fcm_instance = fcm(sample, initial_centers)

        # run cluster analysis and obtain results
        fcm_instance.process()
        clusters = fcm_instance.get_clusters()
        centers = fcm_instance.get_centers()

        # visualize clustering results
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.append_cluster(centers, marker='*', markersize=10)
        visualizer.show()
    @endcode

    The next example shows how to perform image segmentation using Fuzzy C-Means algorithm:
    @code
        from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
        from pyclustering.cluster.fcm import fcm
        from pyclustering.utils import read_image, draw_image_mask_segments

        # load list of points for cluster analysis
        data = read_image("stpetersburg_admiral.jpg")

        # initialize
        initial_centers = kmeans_plusplus_initializer(data, 3, kmeans_plusplus_initializer.FARTHEST_CENTER_CANDIDATE).initialize()

        # create instance of Fuzzy C-Means algorithm
        fcm_instance = fcm(data, initial_centers)

        # run cluster analysis and obtain results
        fcm_instance.process()
        clusters = fcm_instance.get_clusters()

        # visualize segmentation results
        draw_image_mask_segments("stpetersburg_admiral.jpg", clusters)
    @endcode

    @image html fcm_segmentation_stpetersburg.png "Image segmentation using Fuzzy C-Means algorithm."

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

        self.__data = data
        self.__clusters = []
        self.__centers = initial_centers
        self.__membership = []

        self.__tolerance = kwargs.get('tolerance', 0.001)
        self.__itermax = kwargs.get('itermax', 200)
        self.__m = kwargs.get('m', 2)

        self.__degree = 2.0 / (self.__m - 1)

        self.__ccore = kwargs.get('ccore', True)
        if self.__ccore is True:
            self.__ccore = ccore_library.workable()

        self.__verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis in line with Fuzzy C-Means algorithm.

        @return (fcm) Returns itself (Fuzzy C-Means instance).

        @see get_clusters()
        @see get_centers()
        @see get_membership()

        """
        if self.__ccore is True:
            self.__process_by_ccore()
        else:
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


    def __process_by_ccore(self):
        """!
        @brief Performs cluster analysis using C/C++ implementation.

        """
        result = wrapper.fcm_algorithm(self.__data, self.__centers, self.__m, self.__tolerance, self.__itermax)

        self.__clusters = result[wrapper.fcm_package_indexer.INDEX_CLUSTERS]
        self.__centers = result[wrapper.fcm_package_indexer.INDEX_CENTERS]
        self.__membership = result[wrapper.fcm_package_indexer.INDEX_MEMBERSHIP]


    def __process_by_python(self):
        """!
        @brief Performs cluster analysis using Python implementation.

        """
        self.__data = numpy.array(self.__data)
        self.__centers = numpy.array(self.__centers)

        self.__membership = numpy.zeros((len(self.__data), len(self.__centers)))

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
        @brief Calculate center using membership of each cluster.

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
                divider = sum([pow(data_difference[j][i] / data_difference[k][i], self.__degree) for k in range(len(self.__centers)) if data_difference[k][i] != 0.0])

                if divider != 0.0:
                    self.__membership[i][j] = 1.0 / divider
                else:
                    self.__membership[i][j] = 1.0


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


    def __verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self.__data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self.__data))

        if len(self.__centers) == 0:
            raise ValueError("Initial centers are empty (size: '%d')." % len(self.__centers))
