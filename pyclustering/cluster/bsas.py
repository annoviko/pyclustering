"""!

@brief Cluster analysis algorithm: BSAS (Basic Sequential Algorithmic Scheme).
@details Implementation based on paper @cite book::pattern_recognition::2009.

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


from pyclustering.core.wrapper import ccore_library
from pyclustering.core.bsas_wrapper import bsas as bsas_wrapper
from pyclustering.core.metric_wrapper import metric_wrapper

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.encoder import type_encoding

from pyclustering.utils.metric import type_metric, distance_metric


class bsas_visualizer:
    """!
    @brief Visualizer of BSAS algorithm's results.
    @details BSAS visualizer provides visualization services that are specific for BSAS algorithm.

    """

    @staticmethod
    def show_clusters(sample, clusters, representatives, **kwargs):
        """!
        @brief Display BSAS clustering results.

        @param[in] sample (list): Dataset that was used for clustering.
        @param[in] clusters (array_like): Clusters that were allocated by the algorithm.
        @param[in] representatives (array_like): Allocated representatives correspond to clusters.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'figure', 'display', 'offset').

        <b>Keyword Args:</b><br>
            - figure (figure): If 'None' then new is figure is created, otherwise specified figure is used for visualization.
            - display (bool): If 'True' then figure will be shown by the method, otherwise it should be shown manually using matplotlib function 'plt.show()'.
            - offset (uint): Specify axes index on the figure where results should be drawn (only if argument 'figure' is specified).

        @return (figure) Figure where clusters were drawn.

        """

        figure = kwargs.get('figure', None)
        display = kwargs.get('display', True)
        offset = kwargs.get('offset', 0)

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample, canvas=offset)

        for cluster_index in range(len(clusters)):
            visualizer.append_cluster_attribute(offset, cluster_index, [representatives[cluster_index]], '*', 10)

        return visualizer.show(figure=figure, display=display)


class bsas:
    """!
    @brief Class represents BSAS clustering algorithm - basic sequential algorithmic scheme.
    @details Algorithm has two mandatory parameters: maximum allowable number of clusters and threshold
              of dissimilarity or in other words maximum distance between points. Distance metric also can
              be specified using 'metric' parameters, by default 'Manhattan' distance is used.
              BSAS using following rule for updating cluster representative:

    \f[
    \vec{m}_{C_{k}}^{new}=\frac{ \left ( n_{C_{k}^{new}} - 1 \right )\vec{m}_{C_{k}}^{old} + \vec{x} }{n_{C_{k}^{new}}}
    \f]

    Clustering results of this algorithm depends on objects order in input data.

    Example:
    @code
        from pyclustering.cluster.bsas import bsas, bsas_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import SIMPLE_SAMPLES

        # Read data sample from 'Simple02.data'.
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)

        # Prepare algorithm's parameters.
        max_clusters = 3
        threshold = 1.0

        # Create instance of BSAS algorithm.
        bsas_instance = bsas(sample, max_clusters, threshold)
        bsas_instance.process()

        # Get clustering results.
        clusters = bsas_instance.get_clusters()
        representatives = bsas_instance.get_representatives()

        # Display results.
        bsas_visualizer.show_clusters(sample, clusters, representatives)
    @endcode

    @see pyclustering.cluster.mbsas, pyclustering.cluster.ttsas

    """

    def __init__(self, data, maximum_clusters, threshold, ccore=True, **kwargs):
        """!
        @brief Creates classical BSAS algorithm.

        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] maximum_clusters: Maximum allowable number of clusters that can be allocated during processing.
        @param[in] threshold: Threshold of dissimilarity (maximum distance) between points.
        @param[in] ccore (bool): If True than CCORE (C++ part of the library) will be used for solving.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric').

        <b>Keyword Args:</b><br>
            - metric (distance_metric): Metric that is used for distance calculation between two points.

        """

        self._data = data
        self._amount = maximum_clusters
        self._threshold = threshold
        self._metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN))
        self._ccore = ccore and self._metric.get_type() != type_metric.USER_DEFINED

        self._clusters = []
        self._representatives = []

        if self._ccore is True:
            self._ccore = ccore_library.workable()

        self._verify_arguments()


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of BSAS algorithm.

        @return (bsas) Returns itself (BSAS instance).

        @remark Results of clustering can be obtained using corresponding get methods.

        @see get_clusters()
        @see get_representatives()

        """

        if self._ccore is True:
            self.__process_by_ccore()
        else:
            self.__prcess_by_python()

        return self


    def __process_by_ccore(self):
        ccore_metric = metric_wrapper.create_instance(self._metric)
        self._clusters, self._representatives = bsas_wrapper(self._data, self._amount, self._threshold, ccore_metric.get_pointer())


    def __prcess_by_python(self):
        self._clusters.append([0])
        self._representatives.append(self._data[0])

        for i in range(1, len(self._data)):
            point = self._data[i]
            index_cluster, distance = self._find_nearest_cluster(point)

            if (distance > self._threshold) and (len(self._clusters) < self._amount):
                self._representatives.append(point)
                self._clusters.append([i])
            else:
                self._clusters[index_cluster].append(i)
                self._update_representative(index_cluster, point)


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.

        @see process()
        @see get_representatives()

        """
        return self._clusters


    def get_representatives(self):
        """!
        @brief Returns list of representatives of allocated clusters.

        @see process()
        @see get_clusters()

        """
        return self._representatives


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.

        @return (type_encoding) Clustering result representation.

        @see get_clusters()

        """

        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def _find_nearest_cluster(self, point):
        """!
        @brief Find nearest cluster to the specified point.

        @param[in] point (list): Point from dataset.

        @return (uint, double) Index of nearest cluster and distance to it.

        """
        index_cluster = -1
        nearest_distance = float('inf')

        for index in range(len(self._representatives)):
            distance = self._metric(point, self._representatives[index])
            if distance < nearest_distance:
                index_cluster = index
                nearest_distance = distance

        return index_cluster, nearest_distance


    def _update_representative(self, index_cluster, point):
        """!
        @brief Update cluster representative in line with new cluster size and added point to it.

        @param[in] index_cluster (uint): Index of cluster whose representative should be updated.
        @param[in] point (list): Point that was added to cluster.

        """
        length = len(self._clusters[index_cluster])
        rep = self._representatives[index_cluster]

        for dimension in range(len(rep)):
            rep[dimension] = ( (length - 1) * rep[dimension] + point[dimension] ) / length


    def _verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self._data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self._data))

        if self._amount <= 0:
            raise ValueError("Amount of cluster (current value: '%d') for allocation should be greater than 0." %
                             self._amount)

        if self._threshold < 0:
            raise ValueError("Threshold of dissimilarity (current value: '%d') between points should be greater or "
                             "equal to 0." % self._threshold)