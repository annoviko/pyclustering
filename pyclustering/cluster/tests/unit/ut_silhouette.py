"""!

@brief Unit-tests for Silhouette algorithms.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.silhouette import silhouette, silhouette_ksearch_type
from pyclustering.cluster.tests.silhouette_templates import silhouette_test_template

from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS


class silhouette_unit_tests(unittest.TestCase):
    def test_correct_score_simple01(self):
        silhouette_test_template.correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, False)

    def test_correct_score_simple02(self):
        silhouette_test_template.correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, False)

    def test_correct_score_simple03(self):
        silhouette_test_template.correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, False)

    def test_correct_score_simple04(self):
        silhouette_test_template.correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, SIMPLE_ANSWERS.ANSWER_SIMPLE4, False)

    def test_correct_score_simple05(self):
        silhouette_test_template.correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, False)

    def test_correct_score_simple06(self):
        silhouette_test_template.correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, False)

    def test_correct_score_simple07(self):
        silhouette_test_template.correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, False)

    def test_correct_score_simple08(self):
        silhouette_test_template.correct_scores(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, False)


    def test_correct_ksearch_simple01(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple01_kmedoids(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 2, 10,
                                                 silhouette_ksearch_type.KMEDOIDS, False)

    def test_correct_ksearch_simple01_kmedians(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 2, 10,
                                                 silhouette_ksearch_type.KMEDIANS, False)

    def test_correct_ksearch_simple02(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple02_kmedoids(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 2, 10,
                                                 silhouette_ksearch_type.KMEDOIDS, False)

    def test_correct_ksearch_simple02_kmedians(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 2, 10,
                                                 silhouette_ksearch_type.KMEDIANS, False)

    def test_correct_ksearch_simple03(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple03_kmedoids(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 2, 10,
                                                 silhouette_ksearch_type.KMEDOIDS, False)

    def test_correct_ksearch_simple03_kmedians(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 2, 10,
                                                 silhouette_ksearch_type.KMEDIANS, False)

    def test_correct_ksearch_simple05(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple06(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple07(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple08(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple09(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple10(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple11(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple12(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_correct_ksearch_simple13(self):
        silhouette_test_template.correct_ksearch(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, 2, 10,
                                                 silhouette_ksearch_type.KMEANS, False)

    def test_distance_matrix_sample01(self):
        silhouette_test_template.correct_processing_data_types(SIMPLE_SAMPLES.SAMPLE_SIMPLE1,
                                                               SIMPLE_ANSWERS.ANSWER_SIMPLE1, False)

    def test_distance_matrix_sample02(self):
        silhouette_test_template.correct_processing_data_types(SIMPLE_SAMPLES.SAMPLE_SIMPLE2,
                                                               SIMPLE_ANSWERS.ANSWER_SIMPLE2, False)

    def test_distance_matrix_sample03(self):
        silhouette_test_template.correct_processing_data_types(SIMPLE_SAMPLES.SAMPLE_SIMPLE3,
                                                               SIMPLE_ANSWERS.ANSWER_SIMPLE3, False)

    def test_distance_matrix_sample04(self):
        silhouette_test_template.correct_processing_data_types(SIMPLE_SAMPLES.SAMPLE_SIMPLE4,
                                                               SIMPLE_ANSWERS.ANSWER_SIMPLE4, False)

    def test_distance_matrix_sample05(self):
        silhouette_test_template.correct_processing_data_types(SIMPLE_SAMPLES.SAMPLE_SIMPLE5,
                                                               SIMPLE_ANSWERS.ANSWER_SIMPLE5, False)

    def test_distance_matrix_sample06(self):
        silhouette_test_template.correct_processing_data_types(SIMPLE_SAMPLES.SAMPLE_SIMPLE6,
                                                               SIMPLE_ANSWERS.ANSWER_SIMPLE6, False)

    def test_distance_matrix_sample07(self):
        silhouette_test_template.correct_processing_data_types(SIMPLE_SAMPLES.SAMPLE_SIMPLE7,
                                                               SIMPLE_ANSWERS.ANSWER_SIMPLE7, False)

    def test_random_state_1_kmeans(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEANS, 1, False)

    def test_random_state_2_kmeans(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEANS, 2, False)

    def test_random_state_4_kmeans(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEANS, 4, False)

    def test_random_state_8_kmeans(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEANS, 8, False)

    def test_random_state_16_kmeans(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEANS, 16, False)

    def test_random_state_128_kmeans(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEANS, 128, False)

    def test_random_state_1024_kmeans(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEANS, 1024, False)

    def test_random_state_1_kmedians(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDIANS, 1, False)

    def test_random_state_2_kmedians(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDIANS, 2, False)

    def test_random_state_4_kmedians(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDIANS, 4, False)

    def test_random_state_128_kmedians(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDIANS, 128, False)

    def test_random_state_1024_kmedians(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDIANS, 1024, False)

    def test_random_state_1_kmedoids(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDOIDS, 1, False)

    def test_random_state_2_kmedoids(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDIANS, 2, False)

    def test_random_state_4_kmedoids(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDIANS, 4, False)

    def test_random_state_128_kmedoids(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDIANS, 128, False)

    def test_random_state_1024_kmedoids(self):
        silhouette_test_template.random_state(2, 10, silhouette_ksearch_type.KMEDIANS, 1024, False)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, silhouette, [], [[1, 2], [3, 4]])

    def test_incorrect_clusters(self):
        self.assertRaises(ValueError, silhouette, [[1], [2], [3], [4]], [])
