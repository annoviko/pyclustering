"""!

@brief Unit-tests for CLIQUE algorithm.

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

from pyclustering.cluster.clique import clique_block
from pyclustering.cluster.tests.clique_templates import clique_test_template

from pyclustering.tests.assertion import assertion

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES


class clique_unit_test(unittest.TestCase):
    def test_clustering_sample_simple_1(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0, [5, 5], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 7, 0, [5, 5], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 0, [5, 5], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 0, [5, 5], 0, False)

    def test_clustering_sample_simple_1_one_cluster(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0, [10], 0, False)

    def test_clustering_diagonal_blocks_arent_neoghbors(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 0, [5, 5], 0, False)

    def test_clustering_sample_simple_1_noise_only(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 1000, [], 10, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 10, [], 10, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 5, [], 10, False)

    def test_clustering_sample_simple_2(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 7, 0, [5, 8, 10], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 6, 0, [5, 8, 10], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0, [23], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 6, 500, [], 23, False)

    def test_clustering_sample_simple_3(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 9, 0, [10, 10, 10, 30], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 8, 0, [10, 10, 10, 30], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0, [60], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 6, 500, [], 60, False)

    def test_clustering_sample_simple_3_one_point_noise(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 9, [59], 1, False)

    def test_clustering_sample_simple_4_one_cluster(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0, [75], 0, False)

    def test_clustering_sample_simple_5(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 8, 0, [15, 15, 15, 15], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 7, 0, [15, 15, 15, 15], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 6, 0, [15, 15, 15, 15], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 5, 0, [15, 15, 15, 15], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0, [60], 0, False)

    def test_clustering_one_dimensional_data1(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 4, 0, [10, 10], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 0, [20], 0, False)

    def test_clustering_one_dimensional_data2(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 15, 0, [15, 20, 30, 80], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 2, 0, [145], 0, False)

    def test_clustering_one_dimensional_data_3_similar(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 7, 0, [10, 20], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 0, [30], 0, False)

    def test_clustering_sample_simple_10(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 8, 0, [11, 11, 11], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 7, 0, [11, 11, 11], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 2, 0, [33], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 1, 0, [33], 0, False)

    def test_clustering_three_dimensional_data1(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 6, 0, [10, 10], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 5, 0, [10, 10], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, 0, [20], 0, False)

    def test_clustering_similar_points(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 8, 0, [5, 5, 5], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 7, 0, [5, 5, 5], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, 0, [5, 5, 5], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, 0, [15], 0, False)

    def test_clustering_zero_column(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 3, 0, [5, 5], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 2, 0, [5, 5], 0, False)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 1, 0, [10], 0, False)

    def test_clustering_fcps_lsun(self):
        clique_test_template.clustering(FCPS_SAMPLES.SAMPLE_LSUN, 15, 0, [100, 101, 202], 0, False)

    def test_clustering_fcps_hepta(self):
        clique_test_template.clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 9, 0, [30, 30, 30, 30, 30, 30, 32], 0, False)


    def test_visualize_no_failure_one_dimensional(self):
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 4, 0, False)
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 7, 0, False)

    def test_visualize_no_failure_two_dimensional(self):
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0, False)
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0, False)

    def test_visualize_no_failure_three_dimensional(self):
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 3, 0, False)


    def test_argument_invalid_levels(self):
        clique_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0, 0.0, False)
        clique_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, -1, 0.0, False)
        clique_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, -10, 0.0, False)

    def test_argument_invalid_density(self):
        clique_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, -1.0, False)
        clique_test_template.exception(ValueError, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, -2.0, False)

    def test_argument_empty_data(self):
        clique_test_template.exception(ValueError, [], 1, 0.0, False)

    def test_logical_block_neighbors(self):
        block = clique_block()
        block.logical_location = [1, 1]

        neighbors = block.get_location_neighbors(3)
        assertion.eq(4, len(neighbors))
        assertion.true([0, 1] in neighbors)
        assertion.true([2, 1] in neighbors)
        assertion.true([1, 0] in neighbors)
        assertion.true([1, 2] in neighbors)

    def test_logical_block_neighbors_on_edge(self):
        block = clique_block()
        block.logical_location = [1, 1]

        neighbors = block.get_location_neighbors(2)
        assertion.eq(2, len(neighbors))
        assertion.true([0, 1] in neighbors)
        assertion.true([1, 0] in neighbors)

        block.logical_location = [0, 0]
        neighbors = block.get_location_neighbors(2)
        assertion.eq(2, len(neighbors))
        assertion.true([0, 1] in neighbors)
        assertion.true([1, 0] in neighbors)
