"""!

@brief pyclustering module for samples.

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


class answer_reader:
    """!
    @brief Answer reader for samples that are used by pyclustering library.

    """

    def __init__(self, answer_path):
        """!
        @brief Creates instance of answer reader to read proper clustering results of samples.

        @param[in] answer_path (string): Path to clustering results (answers).

        """
        self.__answer_path = answer_path


    def get_clusters(self):
        """!
        @brief Read proper clustering results.

        @return (list) Clusters where each cluster is represented by list of index point from dataset.

        """
        file = open(self.__answer_path, 'r')

        clusters = []
        index_point = 0
        for line in file:
            index_cluster = int(line)
            if index_cluster >= len(clusters):
                clusters.append([index_point])
            else:
                clusters[index_cluster].append(index_point)

            index_point += 1

        file.close()
        return clusters


    def get_cluster_lengths(self):
        """!
        @brief Read proper cluster lengths.
        @details Cluster length means amount of point in a cluster.

        @return (list) Cluster lengths where each length means amount of points in a cluster.

        """
        clusters = self.get_clusters()
        return [len(cluster) for cluster in clusters]
