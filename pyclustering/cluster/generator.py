"""!

@brief Cluster generator.

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


import collections
import random


class data_generator:
    """!
    @brief Data generator provides services to generate data with clusters with normal distribution.

    """

    def __init__(self, amount_clusters, dimension, cluster_sizes, cluster_centers=None, cluster_width=1.0):
        """!
        @brief Constructs data generator for generating data-sets.

        @param[in] amount_clusters (uint): Amount of clusters that should be generated.
        @param[in] dimension (uint): Dimension of each generated point.
        @param[in] cluster_sizes (uint|array_like): Size of each cluster. In case of 'array_like' input clusters with
                    corresponding sizes are generated.
        @param[in] cluster_centers (array_like): Optional parameter that defines cluster centers (means).
        @param[in] cluster_width (uint|array_like): Optional parameter that defines cluster width (standard deviation).
                    In case of 'array_like' input each cluster has own standard deviation.

        """

        self.__amount_clusters = amount_clusters
        self.__dimension = dimension

        self.__cluster_sizes = cluster_sizes
        if not isinstance(self.__cluster_sizes, collections.Iterable):
            self.__cluster_sizes = [self.__cluster_sizes] * amount_clusters

        self.__cluster_width = cluster_width
        if not isinstance(self.__cluster_width, collections.Iterable):
            self.__cluster_width = [self.__cluster_width] * amount_clusters

        self.__cluster_centers = cluster_centers
        if self.__cluster_centers is None:
            self.__cluster_centers = self.__generate_cluster_centers(self.__cluster_width)


    def generate(self):
        """!
        @brief Generates data in line with generator parameters.

        """
        data_points = []

        for index_cluster in range(self.__amount_clusters):
            for _ in range(self.__cluster_sizes[index_cluster]):
                point = self.__generate_point(index_cluster)
                data_points.append(point)

        return data_points


    def __generate_point(self, index_cluster):
        """!
        @brief Generates point in line with parameters of specified cluster.

        @param[in] index_cluster (uint): Index of cluster whose parameters are used for point generation.

        @return (list) New generated point in line with normal distribution and cluster parameters.

        """
        return [ random.gauss(self.__cluster_centers[index_cluster][index_dimension],
                              self.__cluster_width[index_cluster] / 2.0)
                 for index_dimension in range(self.__dimension) ]


    def __generate_cluster_centers(self, width):
        """!
        @brief Generates centers (means in statistical term) for clusters.

        @param[in] width (list): Width of generated clusters.

        @return (list) Generated centers in line with normal distribution.

        """
        centers = []
        default_offset = max(width) * 4.0
        for i in range(self.__amount_clusters):
            center = [ random.gauss(i * default_offset, width[i] / 2.0) for _ in range(self.__dimension) ]
            centers.append(center)

        return centers