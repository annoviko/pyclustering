"""!

@brief Integration-tests for CLIQUE algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.clique import clique
from pyclustering.cluster.tests.clique_templates import clique_test_template

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.core.tests import remove_library

from pyclustering.tests.assertion import assertion


class clique_integration_test(unittest.TestCase):
    def test_clustering_sample_simple_1_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0, [5, 5], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 7, 0, [5, 5], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 0, [5, 5], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 0, [5, 5], 0, True)

    def test_clustering_sample_simple_1_one_cluster_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0, [10], 0, True)

    def test_clustering_diagonal_blocks_arent_neoghbors_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 0, [5, 5], 0, True)

    def test_clustering_sample_simple_1_noise_only_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 1000, [], 10, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 6, 10, [], 10, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 5, [], 10, True)

    def test_clustering_sample_simple_2_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 7, 0, [5, 8, 10], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 6, 0, [5, 8, 10], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0, [23], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 6, 500, [], 23, True)

    def test_clustering_sample_simple_3_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 9, 0, [10, 10, 10, 30], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 8, 0, [10, 10, 10, 30], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0, [60], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 6, 500, [], 60, True)

    def test_clustering_sample_simple_3_one_point_noise_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 9, [59], 1, True)

    def test_clustering_sample_simple_4_one_cluster_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0, [75], 0, True)

    def test_clustering_sample_simple_5_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 8, 0, [15, 15, 15, 15], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 7, 0, [15, 15, 15, 15], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 6, 0, [15, 15, 15, 15], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 5, 0, [15, 15, 15, 15], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0, [60], 0, True)

    def test_clustering_one_dimensional_data1_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 4, 0, [10, 10], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 0, [20], 0, True)

    def test_clustering_one_dimensional_data2_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 15, 0, [15, 20, 30, 80], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 2, 0, [145], 0, True)

    def test_clustering_one_dimensional_data_3_similar_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 7, 0, [10, 20], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 0, [30], 0, True)

    def test_clustering_sample_simple_10_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 8, 0, [11, 11, 11], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 7, 0, [11, 11, 11], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 2, 0, [33], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 1, 0, [33], 0, True)

    def test_clustering_three_dimensional_data1_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 6, 0, [10, 10], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 5, 0, [10, 10], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, 0, [20], 0, True)

    def test_clustering_similar_points_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 8, 0, [5, 5, 5], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 7, 0, [5, 5, 5], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, 0, [5, 5, 5], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, 0, [15], 0, True)

    def test_clustering_zero_column_by_core(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 3, 0, [5, 5], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 2, 0, [5, 5], 0, True)
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 1, 0, [10], 0, True)

    def test_clustering_fcps_lsun_by_core(self):
        clique_test_template.clustering(FCPS_SAMPLES.SAMPLE_LSUN, 15, 0, [100, 101, 202], 0, True)

    def test_clustering_fcps_hepta_by_core(self):
        clique_test_template.clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 9, 0, [30, 30, 30, 30, 30, 30, 32], 0, True)


    def test_visualize_no_failure_one_dimensional_by_core(self):
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 4, 0, True)
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 7, 0, True)

    def test_visualize_no_failure_two_dimensional_by_core(self):
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0, True)
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0, True)

    def test_visualize_no_failure_three_dimensional_by_core(self):
        clique_test_template.visualize(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 3, 0, True)

    def test_high_dimension_data_failure(self):
        data = [[0, 1, 2, 1, 3, 4, 5, 1, 2, 3, 3, 1, 3], [0, 1, 0, 1, 3, 8, 5, 5, 3, 3, 3, 0, 0]]
        clique_instance = clique(data, 15, 0)
        assertion.exception(RuntimeError, clique_instance.process)

    @remove_library
    def test_processing_when_library_core_corrupted(self):
        clique_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0, [5, 5], 0, True)
