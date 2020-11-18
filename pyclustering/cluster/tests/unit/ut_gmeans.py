"""!

@brief Unit-tests for G-Means algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.gmeans_templates import gmeans_test_template

from pyclustering.cluster.gmeans import gmeans
from pyclustering.utils import read_sample, distance_metric, type_metric

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES, SIMPLE_ANSWERS


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


    def test_clustering_sample_01(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, False)

    def test_clustering_sample_01_kmax_correct(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, False, k_max=2)

    def test_clustering_sample_01_kmax_1(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [10], 1, False, k_max=1)

    def test_clustering_sample_01_kmax_10(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, 1, False, k_max=10)

    def test_clustering_sample_02(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, False)

    def test_clustering_sample_02_kmax_correct(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, 1, False, k_max=3)

    def test_clustering_sample_02_kmax_1(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [23], 1, False, k_max=1)

    def test_clustering_sample_02_kmax_2(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [8, 15], 1, False, k_max=2)

    def test_clustering_sample_03(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, 1, False, random_state=1000)

    def test_clustering_sample_03_kmax_1(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [60], 1, False, k_max=1, random_state=1000)

    def test_clustering_sample_05(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, 1, False)

    def test_clustering_sample_06(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, 1, False)

    def test_clustering_sample_07(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, 1, False)

    def test_clustering_sample_08(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, 1, False)

    def test_clustering_sample_09(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, 1, False)

    def test_clustering_sample_10(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, 1, False)

    def test_clustering_sample_11(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, 1, False)

    def test_clustering_sample_12(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, 1, False)

    def test_clustering_sample_13(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, 1, False)

    def test_clustering_sample_15(self):
        gmeans_test_template().clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE15, SIMPLE_ANSWERS.ANSWER_SIMPLE15, 1, False, random_state=1200)

    def test_clustering_hepta_kmax_01(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 1, False, k_max=1)

    def test_clustering_hepta_kmax_02(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 2, 1, False, k_max=2, random_state=1000)

    def test_clustering_hepta_kmax_03(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 3, 1, False, k_max=3, random_state=1000)

    def test_clustering_hepta_kmax_04(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 4, 1, False, k_max=4, random_state=1000)

    def test_clustering_hepta_kmax_05(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 5, 1, False, k_max=5, random_state=1000)

    def test_clustering_hepta_kmax_06(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 6, 1, False, k_max=6, random_state=1000)

    def test_clustering_hepta_kmax_07(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, 1, False, k_max=7, random_state=1000)

    def test_clustering_hepta_kmax_08(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, 1, False, k_max=8, random_state=1000)

    def test_clustering_hepta_kmax_09(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, 1, False, k_max=9, random_state=1000)

    def test_clustering_hepta_kmax_10(self):
        gmeans_test_template().clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, 1, False, k_max=10, random_state=1000)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, gmeans, [], 1, False, tolerance=0.05, repeat=3)

    def test_incorrect_k_init(self):
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], -1, False, tolerance=0.05, repeat=3)
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], 0, False, tolerance=0.05, repeat=3)

    def test_incorrect_tolerance(self):
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], 3, False, tolerance=0, repeat=3)

    def test_incorrect_repeat(self):
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], 3, False, tolerance=1, repeat=0)

    def test_incorrect_kmax_zero(self):
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], 3, False, tolerance=1, repeat=0, kmax=0)

    def test_incorrect_kmax_negative(self):
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], 3, False, tolerance=1, repeat=0, kmax=-2)

    def test_kmax_less_than_kinit(self):
        self.assertRaises(ValueError, gmeans, [[0], [1], [2]], 3, False, tolerance=1, repeat=0, kmax=2)

    def test_predict_without_process(self):
        self.assertEqual([], gmeans([[0], [1]]).predict([0]))


    def template_predict(self, path, amount, points, ccore):
        metric = distance_metric(type_metric.EUCLIDEAN)

        sample = read_sample(path)
        gmeans_instance = gmeans(sample, amount, ccore).process()
        centers = gmeans_instance.get_centers()

        closest_clusters = gmeans_instance.predict(points)

        self.assertEqual(len(points), len(closest_clusters))

        for i in range(len(points)):
            cluster_index = closest_clusters[i]
            distance = metric(centers[cluster_index], points[i])
            for center_index in range(len(centers)):
                if center_index != cluster_index:
                    other_distance = metric(centers[center_index], points[i])
                    self.assertLessEqual(distance, other_distance)

    def test_predict_one_point(self):
        self.template_predict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [[0.3, 0.2]], False)
        self.template_predict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [[4.1, 1.1]], False)
        self.template_predict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [[2.1, 1.9]], False)
        self.template_predict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [[2.1, 4.1]], False)

    def test_predict_two_points(self):
        self.template_predict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [[0.3, 0.2], [2.1, 1.9]], False)
        self.template_predict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [[2.1, 4.1], [2.1, 1.9]], False)
