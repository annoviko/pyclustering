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
        attempts = 10

        failures = ""

        for _ in range(attempts):
            data = read_sample(sample_path)

            gmeans_instance = gmeans(data, amount, ccore).process()

            reader = answer_reader(answer_path)
            expected_length_clusters = sorted(reader.get_cluster_lengths())

            clusters = gmeans_instance.get_clusters()

            unique_indexes = set()
            for cluster in clusters:
                for index_point in cluster:
                    unique_indexes.add(index_point)

            if len(data) != len(unique_indexes):
                failures += "1. %d != %d\n" % (len(data), len(unique_indexes))
                continue

            expected_total_length = sum(expected_length_clusters)
            actual_total_length = sum([len(cluster) for cluster in clusters])
            if expected_total_length != actual_total_length:
                failures += "2. %d != %d\n" % (expected_total_length, actual_total_length)
                continue

            actual_length_clusters = sorted([len(cluster) for cluster in clusters])
            if expected_length_clusters != actual_length_clusters:
                failures += "3. %s != %s\n" % (str(expected_length_clusters), str(actual_length_clusters))
                continue

            return

        self.fail("Expected result is not obtained during %d attempts: %s\n" % (attempts, failures))

    def test_clustering_sample_01(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, False)

    def test_clustering_sample_02(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, False)

    def test_clustering_sample_03(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 1, False)

    def test_clustering_sample_05(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, 1, False)

    def test_clustering_sample_06(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, 1, False)

    def test_clustering_sample_07(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, 1, False)

    def test_clustering_sample_08(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, 1, False)

    def test_clustering_sample_09(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, 1, False)

    def test_clustering_sample_10(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, 1, False)

    def test_clustering_sample_11(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, 1, False)

    def test_clustering_sample_12(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, 1, False)

    def test_clustering_sample_13(self):
        self.template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, 1, False)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, gmeans, [], 1, False, tolerance=0.05, repeat=3)

    def test_incorrect_k_init(self):
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], -1, False, tolerance=0.05, repeat=3)
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], 0, False, tolerance=0.05, repeat=3)

    def test_incorrect_tolerance(self):
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], 3, False, tolerance=0, repeat=3)

    def test_incorrect_repeat(self):
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], 3, False, tolerance=1, repeat=0)
