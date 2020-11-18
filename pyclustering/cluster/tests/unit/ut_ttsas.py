"""!

@brief Unit-tests for TTSAS algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest;
import matplotlib;

matplotlib.use('Agg');

from pyclustering.cluster.tests.ttsas_template import ttsas_test;
from pyclustering.utils.metric import type_metric, distance_metric;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class ttsas_unit_tests(unittest.TestCase):
    def testClusteringSampleSimple1(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], False);

    def testClusteringSampleSimple1Euclidean(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False, metric=distance_metric(type_metric.EUCLIDEAN));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], False, metric=distance_metric(type_metric.EUCLIDEAN));

    def testClusteringSampleSimple1EuclideanSquare(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [5, 5], False, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 100.0, 200.0, [10], False, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));

    def testClusteringSampleSimple1Manhattan(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False, metric=distance_metric(type_metric.MANHATTAN));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], False, metric=distance_metric(type_metric.MANHATTAN));

    def testClusteringSampleSimple1Chebyshev(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], False, metric=distance_metric(type_metric.CHEBYSHEV));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], False, metric=distance_metric(type_metric.CHEBYSHEV));

    def testClusteringSampleSimple2(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1.0, 2.0, [5, 8, 10], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 10.0, 20.0, [23], False);

    def testClusteringSampleSimple3(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.0, 2.0, [10, 10, 10, 30], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 10.0, 20.0, [60], False);

    def testOneDimentionalPoints1(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 1.0, 2.0, [10, 10], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 10.0, 20.0, [20], False);

    def testOneDimentionalPoints2(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 2.0, [10, 20], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 10.0, 20.0, [30], False);

    def testThreeDimentionalPoints(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1.0, 2.0, [10, 10], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 10.0, 20.0, [20], False);

    def testTheSamePoints1(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1.0, 1.5, [5, 5, 5], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 0.001, 0.002, [5, 5, 5], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1000, 2000, [15], False);

    def testTheSamePoints2(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 2.0, [10, 20], False);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 10.0, 20.0, [30], False);
