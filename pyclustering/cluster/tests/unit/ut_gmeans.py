"""!

@brief Unit-tests for G-Means algorithm.

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


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.samples import answer_reader
from pyclustering.cluster.gmeans import gmeans
from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS
from pyclustering.samples.definitions import FCPS_SAMPLES


class testable_gmeans(gmeans):
    @staticmethod
    def get_data_projection(data, vector):
        return gmeans._project_data(data, vector)


class gmeans_unit_test(unittest.TestCase):
    def test_data_projection(self):
        data = [[1, 1], [2, 2], [3, 3]]
        projection = testable_gmeans.get_data_projection(data, [2, 2])
        self.assertEqual([0.5, 1.0, 1.5], projection.tolist())

        projection = testable_gmeans.get_data_projection(data, [1, 1])
        self.assertEqual([1.0, 2.0, 3.0], projection.tolist())

    def template_clustering(self, sample_path, answer_path, amount, ccore):
        data = read_sample(sample_path)

        gmeans_instance = gmeans(data, amount, ccore).process()

        reader = answer_reader(answer_path)
        expected_length_clusters = sorted(reader.get_cluster_lengths())

        clusters = gmeans_instance.get_clusters()

        unique_indexes = set()
        for cluster in clusters:
            for index_point in cluster:
                unique_indexes.add(index_point)

        self.assertEqual(len(data), len(unique_indexes))
        self.assertEqual(sum(expected_length_clusters), sum([len(cluster) for cluster in clusters]))
        self.assertEqual(expected_length_clusters, sorted([len(cluster) for cluster in clusters]))

    def test_clustering_sample_01(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, False)

    def test_clustering_sample_02(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, False)

    def test_clustering_sample_03(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 1, False)
