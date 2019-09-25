"""!

@brief Cluster analysis algorithm: TTSAS (Two-Threshold Sequential Algorithmic Scheme).
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


from pyclustering.core.ttsas_wrapper import ttsas as ttsas_wrapper
from pyclustering.core.metric_wrapper import metric_wrapper

from pyclustering.cluster.bsas import bsas


class ttsas(bsas):
    """!
    @brief Class represents TTSAS (Two-Threshold Sequential Algorithmic Scheme).
    @details Clustering results of BSAS and MBSAS are strongly dependent on the order in which the points in data.
              TTSAS helps to overcome this shortcoming by using two threshold parameters. The first - if the distance
              to the nearest cluster is less than the first threshold then point is assigned to the cluster. The
              second - if distance to the nearest cluster is greater than the second threshold then new cluster is
              allocated.

    Code example of TTSAS usage:
    @code
        from pyclustering.cluster.bsas import bsas_visualizer
        from pyclustering.cluster.ttsas import ttsas
        from pyclustering.samples.definitions import SIMPLE_SAMPLES
        from pyclustering.utils import read_sample

        # Read data sample from 'Simple03.data'.
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

        # Prepare algorithm's parameters.
        threshold1 = 1.0
        threshold2 = 2.0

        # Create instance of TTSAS algorithm.
        ttsas_instance = ttsas(sample, threshold1, threshold2)
        ttsas_instance.process()

        # Get clustering results.
        clusters = ttsas_instance.get_clusters()
        representatives = ttsas_instance.get_representatives()

        # Display results using BSAS visualizer.
        bsas_visualizer.show_clusters(sample, clusters, representatives)
    @endcode

    @see pyclustering.cluster.bsas, pyclustering.cluster.mbsas

    """

    def __init__(self, data, threshold1, threshold2, ccore=True, **kwargs):
        """!
        @brief Creates TTSAS algorithm.

        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] threshold1: Dissimilarity level (distance) between point and its closest cluster, if the distance is
                    less than 'threshold1' value then point is assigned to the cluster.
        @param[in] threshold2: Dissimilarity level (distance) between point and its closest cluster, if the distance is
                    greater than 'threshold2' value then point is considered as a new cluster.
        @param[in] ccore (bool): If True than DLL CCORE (C++ solution) will be used for solving.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric').

        <b>Keyword Args:</b><br>
            - metric (distance_metric): Metric that is used for distance calculation between two points.

        """

        self._threshold2 = threshold2
        self._amount_skipped_objects = len(data)
        self._skipped_objects = [ True ] * len(data)

        super().__init__(data, len(data), threshold1, ccore, **kwargs)


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of TTSAS algorithm.

        @return (ttsas) Returns itself (TTSAS instance).

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
        self._clusters, self._representatives = ttsas_wrapper(self._data, self._threshold, self._threshold2, ccore_metric.get_pointer())


    def __prcess_by_python(self):
        changes = 0
        while self._amount_skipped_objects != 0:
            previous_amount = self._amount_skipped_objects
            self.__process_objects(changes)

            changes = previous_amount - self._amount_skipped_objects


    def __process_objects(self, changes):
        index_point = self._skipped_objects.index(True)

        if changes == 0:
            self.__allocate_cluster(index_point, self._data[index_point])
            index_point += 1

        for i in range(index_point, len(self._data)):
            if self._skipped_objects[i] is True:
                self.__process_skipped_object(i)


    def __process_skipped_object(self, index_point):
        point = self._data[index_point]

        index_cluster, distance = self._find_nearest_cluster(point)

        if distance <= self._threshold:
            self.__append_to_cluster(index_cluster, index_point, point)
        elif distance > self._threshold2:
            self.__allocate_cluster(index_point, point)


    def __append_to_cluster(self, index_cluster, index_point, point):
        self._clusters[index_cluster].append(index_point)
        self._update_representative(index_cluster, point)

        self._amount_skipped_objects -= 1
        self._skipped_objects[index_point] = False


    def __allocate_cluster(self, index_point, point):
        self._clusters.append( [index_point] )
        self._representatives.append(point)

        self._amount_skipped_objects -= 1
        self._skipped_objects[index_point] = False
