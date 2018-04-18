"""!

@brief Cluster analysis algorithm: BSAS (Basic Sequential Algorithmic Scheme).
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


from pyclustering.cluster.encoder import type_encoding;

from pyclustering.utils.metric import type_metric, distance_metric;


class bsas:
    """!
    @brief Class represents BSAS clustering algorithm - basic sequential algorithmic scheme.
    @details Algorithm has two mandatory parameters: maximum allowable number of clusters and threshold
              of dissimilarity or in other words maximum distance between points. Distance metric also can
              be specified using 'metric' parameters. BSAS using following rule for updating cluster representative:

    \f[
    \vec{m}_{C_{k}}^{new}=\frac{ \left ( n_{C_{k}^{new}} - 1 \right )\vec{m}_{C_{k}}^{old} + \vec{x} }{n_{C_{k}^{new}}}
    \f]

    @see pyclustering.cluster.mbsas, pyclustering.cluster.ttsas

    """

    def __init__(self,  data, maximum_clusters, threshold, ccore=True, **kwargs):
        """!
        @brief Creates classical BSAS algorithm.

        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] maximum_clusters: Maximum allowable number of clusters that can be allocated during processing.
        @param[in] threshold: Threshold of dissimilarity (maximum distance) between points.
        @param[in] ccore (bool): If True than DLL CCORE (C++ solution) will be used for solving.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric').

        Keyword Args:
            metric (distance_metric): Metric that is used for distance calculation between two points.

        """

        self.__data = data;
        self.__amount = maximum_clusters;
        self.__threshold = threshold;
        self.__ccore = ccore;
        self.__metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN));

        self.__clusters = [];
        self.__representatives = [];


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of BSAS algorithm.

        @remark Results of clustering can be obtained using corresponding get methods.

        @see get_clusters()
        @see get_medians()

        """

        self.__clusters.append([0]);
        self.__representatives.append(self.__data[0]);

        for i in range(1, len(self.__data)):
            point = self.__data[i];
            index_cluster, distance = self.__find_nearest_cluster(point);

            if (distance > self.__threshold) and (len(self.__clusters) < self.__amount):
                self.__representatives.append(point);
                self.__clusters.append([i]);
            else:
                self.__clusters[index_cluster].append(i);
                self.__update_representative(index_cluster, point);


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.

        @see process()
        @see get_representatives()

        """
        return self.__clusters;


    def get_representatives(self):
        """!
        @brief Returns list of representatives of allocated clusters.

        @see process()
        @see get_clusters()

        """
        return self.__representatives;


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.

        @return (type_encoding) Clustering result representation.

        @see get_clusters()

        """

        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION;


    def __find_nearest_cluster(self, point):
        """!
        @brief Find nearest cluster to the specified point.

        @param[in] point (list): Point from dataset.

        @return (uint, double) Index of nearest cluster and distance to it.

        """
        index_cluster = -1;
        nearest_distance = float('inf');

        for index in range(len(self.__representatives)):
            distance = self.__metric(point, self.__representatives[index]);
            if distance < nearest_distance:
                index_cluster = index;
                nearest_distance = distance;

        return index_cluster, nearest_distance;


    def __update_representative(self, index_cluster, point):
        """!
        @brief Update cluster representative in line with new cluster size and added point to it.

        @param[in] index_cluster (uint): Index of cluster whose representative should be updated.
        @param[in] point (list): Point that was added to cluster.

        """
        length = len(self.__clusters[index_cluster]);
        rep = self.__representatives[index_cluster];

        for dimension in range(len(rep)):
            rep[dimension] = ( (length - 1) * rep[dimension] + point[dimension] ) / length;