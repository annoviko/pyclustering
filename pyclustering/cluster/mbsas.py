"""!

@brief Cluster analysis algorithm: MBSAS (Modified Basic Sequential Algorithmic Scheme).
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


from pyclustering.core.mbsas_wrapper import mbsas as mbsas_wrapper
from pyclustering.core.metric_wrapper import metric_wrapper

from pyclustering.cluster.bsas import bsas


class mbsas(bsas):
    """!
    @brief Class represents MBSAS (Modified Basic Sequential Algorithmic Scheme).
    @details Interface of MBSAS algorithm is the same as for BSAS. This algorithm performs clustering in two steps.
              The first - is determination of amount of clusters. The second - is assignment of points that were not
              marked as a cluster representatives to clusters.

    Code example of MBSAS usage:
    @code
        from pyclustering.cluster.bsas import bsas_visualizer
        from pyclustering.cluster.mbsas import mbsas
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import SIMPLE_SAMPLES

        # Read data sample from 'Simple02.data'.
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)

        # Prepare algorithm's parameters.
        max_clusters = 3
        threshold = 1.0

        # Create instance of MBSAS algorithm.
        mbsas_instance = mbsas(sample, max_clusters, threshold)
        mbsas_instance.process()

        # Get clustering results.
        clusters = mbsas_instance.get_clusters()
        representatives = mbsas_instance.get_representatives()

        # Display results.
        bsas_visualizer.show_clusters(sample, clusters, representatives)
    @endcode

    @see pyclustering.cluster.bsas, pyclustering.cluster.ttsas

    """

    def __init__(self, data, maximum_clusters, threshold, ccore=True, **kwargs):
        """!
        @brief Creates MBSAS algorithm.

        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] maximum_clusters: Maximum allowable number of clusters that can be allocated during processing.
        @param[in] threshold: Threshold of dissimilarity (maximum distance) between points.
        @param[in] ccore (bool): If True than DLL CCORE (C++ solution) will be used for solving.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric').

        <b>Keyword Args:</b><br>
            - metric (distance_metric): Metric that is used for distance calculation between two points.

        """
        super().__init__(data, maximum_clusters, threshold, ccore, **kwargs)


    def process(self):
        """!
        @brief Performs cluster analysis in line with MBSAS algorithm.

        @return (mbsas) Returns itself (MBSAS instance).

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
        self._clusters, self._representatives = mbsas_wrapper(self._data, self._amount, self._threshold, ccore_metric.get_pointer())


    def __prcess_by_python(self):
        self._clusters.append([0]);
        self._representatives.append(self._data[0]);

        skipped_objects = [];

        for i in range(1, len(self._data)):
            point = self._data[i];
            index_cluster, distance = self._find_nearest_cluster(point);

            if (distance > self._threshold) and (len(self._clusters) < self._amount):
                self._representatives.append(point);
                self._clusters.append([i]);
            else:
                skipped_objects.append(i);

        for i in skipped_objects:
            point = self._data[i];
            index_cluster, _ = self._find_nearest_cluster(point);

            self._clusters[index_cluster].append(i);
            self._update_representative(index_cluster, point);