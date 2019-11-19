"""!

@brief Integration-tests for TTSAS algorithm.

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

import unittest;
import matplotlib;

matplotlib.use('Agg');

from pyclustering.core.tests import remove_library;

from pyclustering.cluster.tests.ttsas_template import ttsas_test;
from pyclustering.utils.metric import type_metric, distance_metric;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class ttsas_integration_tests(unittest.TestCase):
    def testClusteringSampleSimple1(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], True);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], True);

    def testClusteringSampleSimple1Euclidean(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], True, metric=distance_metric(type_metric.EUCLIDEAN));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], True, metric=distance_metric(type_metric.EUCLIDEAN));

    def testClusteringSampleSimple1EuclideanSquare(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], True, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [5, 5], True, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 100.0, 200.0, [10], True, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));

    def testClusteringSampleSimple1Manhattan(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], True, metric=distance_metric(type_metric.MANHATTAN));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], True, metric=distance_metric(type_metric.MANHATTAN));

    def testClusteringSampleSimple1Chebyshev(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], True, metric=distance_metric(type_metric.CHEBYSHEV));
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10.0, 20.0, [10], True, metric=distance_metric(type_metric.CHEBYSHEV));

    def testClusteringSampleSimple2(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1.0, 2.0, [5, 8, 10], True);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 10.0, 20.0, [23], True);

    def testClusteringSampleSimple3(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.0, 2.0, [10, 10, 10, 30], True);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 10.0, 20.0, [60], True);

    def testOneDimentionalPoints1(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 1.0, 2.0, [10, 10], True);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 10.0, 20.0, [20], True);

    def testOneDimentionalPoints2(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 2.0, [10, 20], True);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 10.0, 20.0, [30], True);

    def testThreeDimentionalPoints(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1.0, 2.0, [10, 10], True);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 10.0, 20.0, [20], True);

    def testTheSamePoints1(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1.0, 1.5, [5, 5, 5], True);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 0.001, 0.002, [5, 5, 5], True);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1000, 2000, [15], True);

    def testTheSamePoints2(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 2.0, [10, 20], True);
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 10.0, 20.0, [30], True);


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        ttsas_test.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0, [5, 5], True);
