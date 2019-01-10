"""!

@brief pyclustering module for samples.

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
        self.__clusters = None
        self.__noise = None


    def get_clusters(self):
        """!
        @brief Read proper clustering results.

        @return (list) Clusters where each cluster is represented by list of index point from dataset.

        """
        self.__read_answer()
        return self.__clusters


    def get_noise(self):
        """!
        @brief Read proper clustering results

        @return (list) Noise where each outlier is represented by index point from dataset.

        """
        self.__read_answer()
        return self.__noise


    def get_cluster_lengths(self):
        """!
        @brief Read proper cluster lengths.
        @details Cluster length means amount of point in a cluster.

        @return (list) Cluster lengths where each length means amount of points in a cluster.

        """
        clusters = self.get_clusters()
        return [len(cluster) for cluster in clusters]


    def __read_answer_from_line(self, index_point, line):
        """!
        @brief Read information about point from the specific line and place it to cluster or noise in line with that
                information.

        @param[in] index_point (uint): Index point that should be placed to cluster or noise.
        @param[in] line (string): Line where information about point should be read.

        """

        if line[0] == 'n':
            self.__noise.append(index_point)
        else:
            index_cluster = int(line)
            if index_cluster >= len(self.__clusters):
                self.__clusters.append([index_point])
            else:
                self.__clusters[index_cluster].append(index_point)


    def __read_answer(self):
        """!
        @brief Read information about proper clusters and noises from the file.

        """

        if self.__clusters is not None:
            return

        file = open(self.__answer_path, 'r')

        self.__clusters, self.__noise = [], []

        index_point = 0
        for line in file:
            self.__read_answer_from_line(index_point, line)
            index_point += 1

        file.close()
