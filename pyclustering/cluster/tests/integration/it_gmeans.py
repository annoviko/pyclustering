"""!

@brief Integration-tests for G-Means algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.gmeans_templates import gmeans_test_template

from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS, FCPS_SAMPLES


class gmeans_integration_test(unittest.TestCase):
    def test_clustering_sample_01(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, True)

    def test_clustering_sample_01_kmax_correct(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, True, k_max=2)

    def test_clustering_sample_01_kmax_1(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [10], 1, True, k_max=1)

    def test_clustering_sample_01_kmax_10(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, True, k_max=10)

    def test_clustering_sample_02(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, True)

    def test_clustering_sample_02_kmax_correct(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, True, k_max=3)

    def test_clustering_sample_02_kmax_1(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [23], 1, True, k_max=1)

    def test_clustering_sample_02_kmax_2(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [8, 15], 1, True, k_max=2)

    def test_clustering_sample_03(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 1, True)

    def test_clustering_sample_03_kmax_1(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [60], 1, True, k_max=1)

    def test_clustering_sample_05(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, 1, True)

    def test_clustering_sample_06(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, 1, True)

    def test_clustering_sample_07(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, 1, True)

    def test_clustering_sample_08(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, 1, True)

    def test_clustering_sample_09(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, 1, True)

    def test_clustering_sample_10(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, 1, True)

    def test_clustering_sample_11(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, 1, True)

    def test_clustering_sample_12(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, 1, True)

    def test_clustering_sample_13(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, 1, True)

    def test_clustering_hepta_kmax_01(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 1, True, k_max=1, random_state=1)

    def test_clustering_hepta_kmax_01_rnd_1024(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 1, True, k_max=1, random_state=1024)

    def test_clustering_hepta_kmax_02(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 2, 1, True, k_max=2, random_state=1)

    def test_clustering_hepta_kmax_03(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 3, 1, True, k_max=3, random_state=1)

    def test_clustering_hepta_kmax_04(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 4, 1, True, k_max=4, random_state=1)

    def test_clustering_hepta_kmax_05(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 5, 1, True, k_max=5, random_state=1)

    def test_clustering_hepta_kmax_06(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 6, 1, True, k_max=6, random_state=1)

    def test_clustering_hepta_kmax_07(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, 1, True, k_max=7, random_state=1)

    def test_clustering_hepta_kmax_08(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, 1, True, k_max=8, random_state=1)

    def test_clustering_hepta_kmax_09(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, 1, True, k_max=9, random_state=1)

    def test_clustering_hepta_kmax_10(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, 1, True, k_max=10, random_state=1)
