"""!

@brief Unit-tests for BANG algorithm.

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

from pyclustering.cluster.tests.bang_templates import bang_test_template

from pyclustering.cluster.bang import bang
from pyclustering.samples.definitions import SIMPLE_SAMPLES


class bang_unit_test(unittest.TestCase):
    def test_clustering_sample_simple_1(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0.0, [5, 5], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 7, 0.0, [5, 5], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 0.0, [5, 5], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 0.0, [5, 5], 0, False)

    def test_clustering_sample_simple_1_one_cluster(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.0, [10], 0, False)

    def test_clustering_diagonal_neighbors(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, 0.0, [10], 0, False)

    def test_clustering_sample_simple_1_noise_only(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 1000.0, [], 10, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 0.0, [], 10, False, amount_threshold=20)

    def test_clustering_sample_simple_2(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 7, 0.0, [5, 8, 10], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 6, 0.0, [5, 8, 10], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.0, [23], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 6, 500.0, [], 23, False)

    def test_clustering_sample_simple_3(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 7, 0.0, [10, 10, 10, 30], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 8, 0.0, [10, 10, 10, 30], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.0, [60], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 6, 500.0, [], 60, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 6, 0.0, [], 60, False, amount_threshold=100)

    def test_clustering_sample_simple_3_half_noise(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, 2.5, [30], 30, False)

    def test_clustering_sample_simple_4_one_cluster(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 7, 0.0, [75], 0, False)

    def test_clustering_sample_simple_5(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 8, 0.0, [15, 15, 15, 15], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 7, 0.0, [15, 15, 15, 15], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 6, 0.0, [15, 15, 15, 15], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 5, 0.0, [15, 15, 15, 15], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0.0, [60], 0, False)

    def test_clustering_one_dimensional_data1(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 4, 0.0, [10, 10], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 0.0, [20], 0, False)

    def test_clustering_one_dimensional_data2(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 7, 0.0, [15, 20, 30, 80], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 2, 0.0, [145], 0, False)

    def test_clustering_one_dimensional_data_3_Similar(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 7, 0.0, [10, 20], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 0.0, [30], 0, False)

    def test_clustering_sample_simple_10(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 8, 0.0, [11, 11, 11], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 7, 0.0, [11, 11, 11], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 2, 0.0, [33], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 1, 0.0, [33], 0, False)

    def test_clustering_three_dimensional_data1(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 8, 0.0, [10, 10], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 7, 0.0, [10, 10], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, 0.0, [20], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, 0.0, [20], 0, False)

    def test_clustering_similar_points(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 8, 0.0, [5, 5, 5], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 7, 0.0, [5, 5, 5], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, 0.0, [5, 5, 5], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, 0.0, [15], 0, False)


    def test_clustering_zero_column(self):
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 6, 0.0, [5, 5], 0, False)
        bang_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 1, 0.0, [10], 0, False)


    def test_visualize_no_failure_one_dimensional(self):
        bang_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 4, 0.0, False)
        bang_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 7, 0.0, False)

    def test_visualize_no_failure_two_dimensional(self):
        bang_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0.0, False)
        bang_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.0, False)

    def test_visualize_no_failure_three_dimensional(self):
        bang_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 8, 0.0, False)
        bang_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, 0.0, False)


    def test_animate_no_failure(self):
        bang_test_template.animate(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0.0, False)
        bang_test_template.animate(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 8, 0.0, False)


    def test_argument_invalid_levels(self):
        bang_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0, 0.0, False)
        bang_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, -1, 0.0, False)
        bang_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, -10, 0.0, False)

    def test_argument_invalid_density(self):
        bang_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, -1.0, False)
        bang_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, -2.0, False)

    def test_argument_empty_data(self):
        bang_test_template.exception(ValueError, [], 1, 0.0, False)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, bang, [], 1)

    def test_incorrect_levels(self):
        self.assertRaises(ValueError, bang, [[0], [1], [2]], 0)

    def test_incorrect_density_threshold(self):
        self.assertRaises(ValueError, bang, [[0], [1], [2]], 1, density_threshold=-0.1)

    def test_incorrect_amount_threshold(self):
        self.assertRaises(ValueError, bang, [[0], [1], [2]], 2, amount_threshold=-1)
