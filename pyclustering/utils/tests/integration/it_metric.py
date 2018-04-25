"""!

@brief Integration-tests for metrics.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.tests.assertion import assertion;

from pyclustering.core.metric_wrapper import metric_wrapper;

from pyclustering.utils.metric import type_metric;


class MetricUnitTest(unittest.TestCase):
    def testEuclideanMetric(self):
        metric_instance = metric_wrapper(type_metric.EUCLIDEAN, [], None);
        assertion.eq(2.0, metric_instance([0.0, 0.0], [2.0, 0.0]));


    def testSquareEuclideanMetric(self):
        metric_instance = metric_wrapper(type_metric.EUCLIDEAN_SQUARE, [], None);
        assertion.eq(4.0, metric_instance([0.0, 0.0], [2.0, 0.0]));


    def testManhattanMetric(self):
        metric_instance = metric_wrapper(type_metric.MANHATTAN, [], None);
        assertion.eq(3.0, metric_instance([1.0, 2.0], [0.0, 0.0]));


    def testChebyshevMetric(self):
        metric_instance = metric_wrapper(type_metric.CHEBYSHEV, [], None);
        assertion.eq(4.0, metric_instance([1.0, 4.0], [0.0, 0.0]));


    def testMinkowskiMetric(self):
        metric_instance = metric_wrapper(type_metric.MINKOWSKI, [2.0], None);
        assertion.eq(2.0, metric_instance([0.0, 0.0], [2.0, 0.0]));


    # TODO: doesn't work for some platforms.
    #def testUserDefinedMetric(self):
    #    user_metric = lambda p1, p2 : p1[0] + p2[0];
    #    metric_instance = metric_wrapper(type_metric.USER_DEFINED, [], user_metric);
    #    assertion.eq(2.0, metric_instance([0.0, 0.0], [2.0, 0.0]));
    #    assertion.eq(4.0, metric_instance([3.0, 2.0], [1.0, 5.0]));