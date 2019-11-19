"""!

@brief Integration-tests for metrics.

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

import numpy

from pyclustering.core.metric_wrapper import metric_wrapper
from pyclustering.utils.metric import type_metric, distance_metric


class MetricUnitTest(unittest.TestCase):
    def testEuclideanMetric(self):
        metric_instance = metric_wrapper(type_metric.EUCLIDEAN, [], None)
        self.assertEqual(2.0, metric_instance([0.0, 0.0], [2.0, 0.0]))


    def testSquareEuclideanMetric(self):
        metric_instance = metric_wrapper(type_metric.EUCLIDEAN_SQUARE, [], None)
        self.assertEqual(4.0, metric_instance([0.0, 0.0], [2.0, 0.0]))


    def testManhattanMetric(self):
        metric_instance = metric_wrapper(type_metric.MANHATTAN, [], None)
        self.assertEqual(3.0, metric_instance([1.0, 2.0], [0.0, 0.0]))


    def testChebyshevMetric(self):
        metric_instance = metric_wrapper(type_metric.CHEBYSHEV, [], None)
        self.assertEqual(4.0, metric_instance([1.0, 4.0], [0.0, 0.0]))


    def testMinkowskiMetric(self):
        metric_instance = metric_wrapper(type_metric.MINKOWSKI, [2.0], None)
        self.assertEqual(2.0, metric_instance([0.0, 0.0], [2.0, 0.0]))


    def testCanberraMetric(self):
        metric_instance = metric_wrapper(type_metric.CANBERRA, [], None)
        self.assertEqual(0.0, metric_instance([0.0, 0.0], [0.0, 0.0]))
        self.assertEqual(2.0, metric_instance([0.0, 0.0], [1.0, 1.0]))
        self.assertEqual(1.0, metric_instance([0.75, 0.75], [0.25, 0.25]))
        self.assertEqual(0.0, metric_instance([-1.0, -1.0], [-1.0, -1.0]))
        self.assertEqual(0.4, metric_instance([-2.0, -2.0], [-3.0, -3.0]))


    def testChiSquareMetric(self):
        metric_instance = metric_wrapper(type_metric.CHI_SQUARE, [], None)
        self.assertEqual(0.0, metric_instance([0.0, 0.0], [0.0, 0.0]))
        self.assertEqual(2.0, metric_instance([0.0, 0.0], [1.0, 1.0]))
        self.assertEqual(0.5, metric_instance([0.75, 0.75], [0.25, 0.25]))
        self.assertEqual(0.0, metric_instance([-1.0, -1.0], [-1.0, -1.0]))
        self.assertEqual(0.4, metric_instance([-2.0, -2.0], [-3.0, -3.0]))


    def testGowerDistance(self):
        metric_instance = metric_wrapper(type_metric.GOWER, [0.0], None)
        self.assertEqual(0.0, metric_instance([0.0], [0.0]))

        metric_instance = metric_wrapper(type_metric.GOWER, [1.0, 1.0], None)
        self.assertEqual(1.0, metric_instance([0.0, 0.0], [1.0, 1.0]))

        metric_instance = metric_wrapper(type_metric.GOWER, [0.5, 0.5], None)
        self.assertEqual(1.0, metric_instance([0.75, 0.75], [0.25, 0.25]))

        metric_instance = metric_wrapper(type_metric.GOWER, [0.0, 0.0], None)
        self.assertEqual(0.0, metric_instance([-1.0, -1.0], [-1.0, -1.0]))

        metric_instance = metric_wrapper(type_metric.GOWER, [1.0, 1.0], None)
        self.assertEqual(1.0, metric_instance([-2.0, -2.0], [-3.0, -3.0]))


    def testBuildGowerDistanceFromMetricWithMaxRange(self):
        metric = distance_metric(type_metric.GOWER, max_range=[2.0, 0.0])
        ccore_metric = metric_wrapper.create_instance(metric)
        self.assertEqual(0.5, ccore_metric([-3.0, -3.0], [-5.0, -3.0]))


    def testBuildGowerDistanceFromMetricWithNumpyMaxRange(self):
        metric = distance_metric(type_metric.GOWER, max_range=numpy.array([2.0, 0.0]))
        ccore_metric = metric_wrapper.create_instance(metric)
        self.assertEqual(0.5, ccore_metric([-3.0, -3.0], [-5.0, -3.0]))


    def testBuildGowerDistanceFromMetricWithData(self):
        metric = distance_metric(type_metric.GOWER, data=[[-3.0, -3.0], [-4.0, -3.0], [-4.5, -3.0], [-5.0, -3.0]])
        ccore_metric = metric_wrapper.create_instance(metric)
        self.assertEqual(0.5, ccore_metric([-3.0, -3.0], [-5.0, -3.0]))


    def testBuildGowerDistanceFromMetricWithNumpyData(self):
        metric = distance_metric(type_metric.GOWER, data=numpy.array([[-3.0, -3.0], [-4.0, -3.0], [-4.5, -3.0], [-5.0, -3.0]]))
        ccore_metric = metric_wrapper.create_instance(metric)
        self.assertEqual(0.5, ccore_metric([-3.0, -3.0], [-5.0, -3.0]))


    # TODO: doesn't work for some platforms.
    #def testUserDefinedMetric(self):
    #    user_metric = lambda p1, p2 : p1[0] + p2[0];
    #    metric_instance = metric_wrapper(type_metric.USER_DEFINED, [], user_metric);
    #    assertion.eq(2.0, metric_instance([0.0, 0.0], [2.0, 0.0]));
    #    assertion.eq(4.0, metric_instance([3.0, 2.0], [1.0, 5.0]));