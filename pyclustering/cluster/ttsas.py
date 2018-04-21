"""!

@brief Cluster analysis algorithm: TTSAS (Two-Threshold Sequential Algorithmic Scheme).
@details Implementation based on book:
         - Theodoridis, Koutroumbas, Konstantinos. Elsevier Academic Press - Pattern Recognition - 2nd Edition. 2003.

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


from pyclustering.cluster.bsas import bsas;


class ttsas(bsas):
    """!
    @brief Class represents TTSAS (Two-Threshold Sequential Algorithmic Scheme).

    @see pyclustering.cluster.bsas, pyclustering.cluster.mbsas

    """

    def __init__(self, data, threshold1, threshold2, ccore, **kwargs):
        """!
        @brief Creates TTSAS algorithm.

        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] maximum_clusters: Maximum allowable number of clusters that can be allocated during processing.
        @param[in] threshold1: Dissimilarity level (distance) between point and its closest cluster, if the distance is
                    less than 'threshold1' value then point is assigned to the cluster.
        @param[in] threshold2: Dissimilarity level (distance) between point and its closest cluster, if the distance is
                    greater than 'threshold2' value then point is considered as a new cluster.
        @param[in] ccore (bool): If True than DLL CCORE (C++ solution) will be used for solving.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric').

        Keyword Args:
            metric (distance_metric): Metric that is used for distance calculation between two points.

        """

        self._threshold2 = threshold2;
        self._amount_skipped_objects = len(data);
        self._skipped_objects = [ True ] * len(data);

        super().__init__(data, len(data), threshold1, ccore, **kwargs);


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of BSAS algorithm.

        @remark Results of clustering can be obtained using corresponding get methods.

        @see get_clusters()
        @see get_representatives()

        """

        changes = 0;
        while self._amount_skipped_objects != 0:
            previous_amount = self._amount_skipped_objects;
            self.__process_objects(changes);

            changes = previous_amount - self._amount_skipped_objects;


    def __process_objects(self, changes):
        index_point = self._skipped_objects.index(True);

        if changes == 0:
            self.__allocate_cluster(index_point, self._data[index_point]);
            index_point += 1;

        for i in range(index_point, len(self._data)):
            if self._skipped_objects[i] is True:
                self.__process_skipped_object(i);


    def __process_skipped_object(self, index_point):
        point = self._data[index_point];

        index_cluster, distance = self._find_nearest_cluster(point);

        if distance < self._threshold:
            self.__append_to_cluster(index_cluster, index_point, point);
        elif distance > self._threshold2:
            self.__allocate_cluster(index_point, point);


    def __append_to_cluster(self, index_cluster, index_point, point):
        self._clusters[index_cluster].append(index_point);
        self._update_representative(index_cluster, point);

        self._amount_skipped_objects -= 1;
        self._skipped_objects[index_point] = False;


    def __allocate_cluster(self, index_point, point):
        self._clusters.append( [index_point] );
        self._representatives.append(point);

        self._amount_skipped_objects -= 1;
        self._skipped_objects[index_point] = False;
