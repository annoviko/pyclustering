"""!

Unit-tests for metric functions.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
@copyright GNU Public License

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


import unittest;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.tests.assertion import assertion;

import pyclustering.utils.metric as metric;


class MetricUnitTest(unittest.TestCase):
    def testCalculateMetric(self):
        assertion.eq(1.0, metric.distance_metric(metric.type_metric.EUCLIDEAN)([0.0, 1.0], [0.0, 0.0]));
        assertion.eq(4.0, metric.distance_metric(metric.type_metric.EUCLIDEAN_SQUARE)([2.0, 2.0], [4.0, 2.0]));
        assertion.eq(4.0, metric.distance_metric(metric.type_metric.MANHATTAN)([1.0, 1.0], [-1.0, -1.0]));
        assertion.eq(2.0, metric.distance_metric(metric.type_metric.CHEBYSHEV)([2.0, -2.0], [0.0, 0.0]));
        assertion.eq(2.0, metric.distance_metric(metric.type_metric.MINKOWSKI)([-3.0, -3.0], [-5.0, -3.0]));
        assertion.eq(2.0, metric.distance_metric(metric.type_metric.MINKOWSKI, degree=2)([-3.0, -3.0], [-5.0, -3.0]));
        assertion.eq(4.0, metric.distance_metric(metric.type_metric.USER_DEFINED, func=metric.euclidean_distance_square)([2.0, 2.0], [4.0, 2.0]));

        user_function = lambda point1, point2: point1[0] + point2[0] + 2;
        assertion.eq(5.0, metric.distance_metric(metric.type_metric.USER_DEFINED, func=user_function)([2.0, 3.0], [1.0, 3.0]));


    def testEuclideanDistance(self):
        assertion.eq(0.0, metric.euclidean_distance([0], [0]));
        assertion.eq(1.0, metric.euclidean_distance([0.0, 1.0], [0.0, 0.0]));
        assertion.eq(2.0, metric.euclidean_distance([3.0, 3.0], [5.0, 3.0]));
        assertion.eq(2.0, metric.euclidean_distance([-3.0, -3.0], [-5.0, -3.0]));


    def testEuclideanDistanceSquare(self):
        assertion.eq(0.0, metric.euclidean_distance_square([0], [0]));
        assertion.eq(1.0, metric.euclidean_distance_square([0.0, 1.0], [0.0, 0.0]));
        assertion.eq(4.0, metric.euclidean_distance_square([2.0, 2.0], [4.0, 2.0]));
        assertion.eq(4.0, metric.euclidean_distance_square([-2.0, 2.0], [-4.0, 2.0]));


    def testManhattanDistance(self):
        assertion.eq(0.0, metric.manhattan_distance([0], [0]));
        assertion.eq(1.0, metric.manhattan_distance([0.0, 1.0], [0.0, 0.0]));
        assertion.eq(2.0, metric.manhattan_distance([1.0, 1.0], [0.0, 0.0]));
        assertion.eq(4.0, metric.manhattan_distance([1.0, 1.0], [-1.0, -1.0]));
        assertion.eq(2.0, metric.manhattan_distance([-1.0, -1.0], [-2.0, -2.0]));


    def testChebyshevDistance(self):
        assertion.eq(0.0, metric.chebyshev_distance([0], [0]));
        assertion.eq(1.0, metric.chebyshev_distance([1.0, 0.0], [0.0, 0.0]));
        assertion.eq(1.0, metric.chebyshev_distance([1.0, 1.0], [0.0, 0.0]));
        assertion.eq(1.0, metric.chebyshev_distance([1.0, -1.0], [0.0, 0.0]));
        assertion.eq(2.0, metric.chebyshev_distance([2.0, 0.0], [0.0, 0.0]));
        assertion.eq(2.0, metric.chebyshev_distance([2.0, 1.0], [0.0, 0.0]));
        assertion.eq(2.0, metric.chebyshev_distance([2.0, -2.0], [0.0, 0.0]));
        assertion.eq(3.0, metric.chebyshev_distance([2.0, -2.0], [-1.0, -1.0]));


    def testMinkowskiDistance(self):
        assertion.eq(0.0, metric.minkowski_distance([0], [0]));
        assertion.eq(0.0, metric.minkowski_distance([0], [0], 2));
        assertion.eq(-2.0, metric.minkowski_distance([3.0, 3.0], [5.0, 3.0], 1));
        assertion.eq(2.0, metric.minkowski_distance([3.0, 3.0], [5.0, 3.0], 2));
        assertion.eq(2.0, metric.minkowski_distance([3.0, 3.0], [5.0, 3.0], 4));


if __name__ == "__main__":
    unittest.main();