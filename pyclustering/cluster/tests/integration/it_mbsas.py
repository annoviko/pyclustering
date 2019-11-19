"""!

@brief Integration-tests for MBSAS algorithm.

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

from pyclustering.cluster.tests.mbsas_templates import mbsas_test_template;
from pyclustering.utils.metric import type_metric, distance_metric;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class mbsas_integration_test(unittest.TestCase):
    def testClusteringSampleSimple1(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 1.0, [5, 5], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [10], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 1.0, [10], True);

    def testClusteringSampleSimple1Euclidean(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], True, metric=distance_metric(type_metric.EUCLIDEAN));
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [10], True, metric=distance_metric(type_metric.EUCLIDEAN));

    def testClusteringSampleSimple1EuclideanSquare(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], True, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [5, 5], True, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 100.0, [10], True, metric=distance_metric(type_metric.EUCLIDEAN_SQUARE));

    def testClusteringSampleSimple1Manhattan(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], True, metric=distance_metric(type_metric.MANHATTAN));
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [10], True, metric=distance_metric(type_metric.MANHATTAN));

    def testClusteringSampleSimple1Chebyshev(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], True, metric=distance_metric(type_metric.CHEBYSHEV));
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 10.0, [10], True, metric=distance_metric(type_metric.CHEBYSHEV));

    def testClusteringSampleSimple2(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1.0, [5, 8, 10], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 10.0, [23], True);

    def testClusteringSampleSimple3(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, 2.0, [10, 10, 10, 30], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, 10.0, [60], True);

    def testOneDimentionalPoints1(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 1.0, [10, 10], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 10.0, [20], True);

    def testOneDimentionalPoints2(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 1.0, [10, 20], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 10.0, [30], True);

    def testThreeDimentionalPoints(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, 1.0, [10, 10], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, 10.0, [20], True);

    def testTheSamePoints1(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 3, 1.0, [5, 5, 5], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 30, 1.0, [5, 5, 5], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 3, 10.0, [15], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, 1.0, [15], True);

    def testTheSamePoints2(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 3, 1.0, [10, 20], True);
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 3, 10.0, [30], True);


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        mbsas_test_template.clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0, [5, 5], True);
