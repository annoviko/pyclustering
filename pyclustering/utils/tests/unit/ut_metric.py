"""!

Unit-tests for metric functions.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

import numpy

from pyclustering.tests.assertion import assertion

import pyclustering.utils.metric as metric


class MetricUnitTest(unittest.TestCase):
    def testCalculateMetric(self):
        assertion.eq(1.0, metric.distance_metric(metric.type_metric.EUCLIDEAN)([0.0, 1.0], [0.0, 0.0]))
        assertion.eq(4.0, metric.distance_metric(metric.type_metric.EUCLIDEAN_SQUARE)([2.0, 2.0], [4.0, 2.0]))
        assertion.eq(4.0, metric.distance_metric(metric.type_metric.MANHATTAN)([1.0, 1.0], [-1.0, -1.0]))
        assertion.eq(2.0, metric.distance_metric(metric.type_metric.CHEBYSHEV)([2.0, -2.0], [0.0, 0.0]))
        assertion.eq(2.0, metric.distance_metric(metric.type_metric.MINKOWSKI)([-3.0, -3.0], [-5.0, -3.0]))
        assertion.eq(2.0, metric.distance_metric(metric.type_metric.MINKOWSKI, degree=2)([-3.0, -3.0], [-5.0, -3.0]))
        assertion.eq(0.5, metric.distance_metric(metric.type_metric.GOWER, max_range=([2.0, 0.0]))([-3.0, -3.0], [-5.0, -3.0]))
        assertion.eq(0.5, metric.distance_metric(metric.type_metric.GOWER, data=[[-3.0, -3.0], [-4.0, -3.0], [-4.5, -3.0], [-5.0, -3.0]])([-3.0, -3.0],[-5.0, -3.0]))
        assertion.eq(4.0, metric.distance_metric(metric.type_metric.USER_DEFINED, func=metric.euclidean_distance_square)([2.0, 2.0], [4.0, 2.0]))

        user_function = lambda point1, point2: point1[0] + point2[0] + 2
        assertion.eq(5.0, metric.distance_metric(metric.type_metric.USER_DEFINED, func=user_function)([2.0, 3.0], [1.0, 3.0]))


    def testEuclideanDistance(self):
        assertion.eq(0.0, metric.euclidean_distance([0], [0]))
        assertion.eq(0.0, metric.euclidean_distance_numpy(numpy.array([0]), numpy.array([0])))
        assertion.eq(1.0, metric.euclidean_distance([0.0, 1.0], [0.0, 0.0]))
        assertion.eq(1.0, metric.euclidean_distance_numpy(numpy.array([0.0, 1.0]), numpy.array([0.0, 0.0])))
        assertion.eq(2.0, metric.euclidean_distance([3.0, 3.0], [5.0, 3.0]))
        assertion.eq(2.0, metric.euclidean_distance_numpy(numpy.array([3.0, 3.0]), numpy.array([5.0, 3.0])))
        assertion.eq(2.0, metric.euclidean_distance([-3.0, -3.0], [-5.0, -3.0]))
        assertion.eq(2.0, metric.euclidean_distance_numpy(numpy.array([-3.0, -3.0]), numpy.array([-5.0, -3.0])))


    def testEuclideanDistanceSquare(self):
        assertion.eq(0.0, metric.euclidean_distance_square([0], [0]))
        assertion.eq(1.0, metric.euclidean_distance_square([0.0, 1.0], [0.0, 0.0]))
        assertion.eq(4.0, metric.euclidean_distance_square([2.0, 2.0], [4.0, 2.0]))
        assertion.eq(4.0, metric.euclidean_distance_square([-2.0, 2.0], [-4.0, 2.0]))


    def testManhattanDistance(self):
        assertion.eq(0.0, metric.manhattan_distance([0], [0]))
        assertion.eq(1.0, metric.manhattan_distance([0.0, 1.0], [0.0, 0.0]))
        assertion.eq(2.0, metric.manhattan_distance([1.0, 1.0], [0.0, 0.0]))
        assertion.eq(4.0, metric.manhattan_distance([1.0, 1.0], [-1.0, -1.0]))
        assertion.eq(2.0, metric.manhattan_distance([-1.0, -1.0], [-2.0, -2.0]))


    def testChebyshevDistance(self):
        assertion.eq(0.0, metric.chebyshev_distance([0], [0]))
        assertion.eq(1.0, metric.chebyshev_distance([1.0, 0.0], [0.0, 0.0]))
        assertion.eq(1.0, metric.chebyshev_distance([1.0, 1.0], [0.0, 0.0]))
        assertion.eq(1.0, metric.chebyshev_distance([1.0, -1.0], [0.0, 0.0]))
        assertion.eq(2.0, metric.chebyshev_distance([2.0, 0.0], [0.0, 0.0]))
        assertion.eq(2.0, metric.chebyshev_distance([2.0, 1.0], [0.0, 0.0]))
        assertion.eq(2.0, metric.chebyshev_distance([2.0, -2.0], [0.0, 0.0]))
        assertion.eq(3.0, metric.chebyshev_distance([2.0, -2.0], [-1.0, -1.0]))


    def testMinkowskiDistance(self):
        assertion.eq(0.0, metric.minkowski_distance([0], [0]))
        assertion.eq(0.0, metric.minkowski_distance([0], [0], 2))
        assertion.eq(-2.0, metric.minkowski_distance([3.0, 3.0], [5.0, 3.0], 1))
        assertion.eq(2.0, metric.minkowski_distance([3.0, 3.0], [5.0, 3.0], 2))
        assertion.eq(2.0, metric.minkowski_distance([3.0, 3.0], [5.0, 3.0], 4))


    def testCanberraDistance(self):
        assertion.eq(0.0, metric.canberra_distance([0], [0]))
        assertion.eq(0.0, metric.canberra_distance_numpy(numpy.array([0]), numpy.array([0])))
        assertion.eq(2.0, metric.canberra_distance([0.0, 0.0], [1.0, 1.0]))
        assertion.eq(2.0, metric.canberra_distance_numpy(numpy.array([0.0, 0.0]), numpy.array([1.0, 1.0])))
        assertion.eq(1.0, metric.canberra_distance([0.75, 0.75], [0.25, 0.25]))
        assertion.eq(1.0, metric.canberra_distance_numpy(numpy.array([0.75, 0.75]), numpy.array([0.25, 0.25])))
        assertion.eq(0.0, metric.canberra_distance([-1.0, -1.0], [-1.0, -1.0]))
        assertion.eq(0.0, metric.canberra_distance_numpy(numpy.array([-1.0, -1.0]), numpy.array([-1.0, -1.0])))
        assertion.eq(0.4, metric.canberra_distance([-2.0, -2.0], [-3.0, -3.0]))
        assertion.eq(0.4, metric.canberra_distance_numpy(numpy.array([-2.0, -2.0]), numpy.array([-3.0, -3.0])))


    def testChiSquareDistance(self):
        assertion.eq(0.0, metric.chi_square_distance([0], [0]))
        assertion.eq(0.0, metric.chi_square_distance_numpy(numpy.array([0]), numpy.array([0])))
        assertion.eq(2.0, metric.chi_square_distance([0.0, 0.0], [1.0, 1.0]))
        assertion.eq(2.0, metric.chi_square_distance_numpy(numpy.array([0.0, 0.0]), numpy.array([1.0, 1.0])))
        assertion.eq(0.5, metric.chi_square_distance([0.75, 0.75], [0.25, 0.25]))
        assertion.eq(0.5, metric.chi_square_distance_numpy(numpy.array([0.75, 0.75]), numpy.array([0.25, 0.25])))
        assertion.eq(0.0, metric.chi_square_distance([-1.0, -1.0], [-1.0, -1.0]))
        assertion.eq(0.0, metric.chi_square_distance_numpy(numpy.array([-1.0, -1.0]), numpy.array([-1.0, -1.0])))
        assertion.eq(0.4, metric.chi_square_distance([-2.0, -2.0], [-3.0, -3.0]))
        assertion.eq(0.4, metric.chi_square_distance_numpy(numpy.array([-2.0, -2.0]), numpy.array([-3.0, -3.0])))


    def testGowerDistance(self):
        assertion.eq(0.0, metric.gower_distance([0], [0], [0.0]))
        assertion.eq(0.0, metric.gower_distance_numpy(numpy.array([0]), numpy.array([0]), numpy.array([0.0])))
        assertion.eq(1.0, metric.gower_distance([0.0, 0.0], [1.0, 1.0], [1.0, 1.0]))
        assertion.eq(1.0, metric.gower_distance_numpy(numpy.array([0.0, 0.0]), numpy.array([1.0, 1.0]), numpy.array([1.0, 1.0])))
        assertion.eq(1.0, metric.gower_distance([0.75, 0.75], [0.25, 0.25], [0.5, 0.5]))
        assertion.eq(1.0, metric.gower_distance_numpy(numpy.array([0.75, 0.75]), numpy.array([0.25, 0.25]), numpy.array([0.5, 0.5])))
        assertion.eq(0.0, metric.gower_distance([-1.0, -1.0], [-1.0, -1.0], [0.0, 0.0]))
        assertion.eq(0.0, metric.gower_distance_numpy(numpy.array([-1.0, -1.0]), numpy.array([-1.0, -1.0]), numpy.array([0.0, 0.0])))
        assertion.eq(1.0, metric.gower_distance([-2.0, -2.0], [-3.0, -3.0], [1.0, 1.0]))
        assertion.eq(1.0, metric.gower_distance_numpy(numpy.array([-2.0, -2.0]), numpy.array([-3.0, -3.0]), numpy.array([1.0, 1.0])))


    def testGowerDistanceIntegrity(self):
        a, b = [1.2, 3.4], [1.0, 2.2]
        npa, npb = numpy.array(a), numpy.array(b)

        gower = metric.distance_metric(metric.type_metric.GOWER, data=[a, b], numpy_usage=False)
        gower_numpy = metric.distance_metric(metric.type_metric.GOWER, data=numpy.array([a, b]), numpy_usage=True)
        assertion.eq(gower(a, b), gower_numpy(npa, npb))


    def testCommonAndNumPyMetricsTwoDimension(self):
        a = [1.2, 3.4]
        b = [5.4, -7.1]
        npa = numpy.array(a)
        npb = numpy.array(b)

        assertion.eq(metric.euclidean_distance(a, b), metric.euclidean_distance_numpy(npa, npb))
        assertion.eq(metric.euclidean_distance_square(a, b), metric.euclidean_distance_square_numpy(npa, npb))
        assertion.eq(metric.manhattan_distance(a, b), metric.manhattan_distance_numpy(npa, npb))
        assertion.eq(metric.chebyshev_distance(a, b), metric.chebyshev_distance_numpy(npa, npb))
        assertion.eq(metric.minkowski_distance(a, b, 2), metric.minkowski_distance_numpy(npa, npb, 2))
        assertion.eq(metric.minkowski_distance(a, b, 4), metric.minkowski_distance_numpy(npa, npb, 4))
        assertion.eq(metric.canberra_distance(a, b), metric.canberra_distance_numpy(npa, npb))
        assertion.eq(metric.chi_square_distance(a, b), metric.chi_square_distance_numpy(npa, npb))
        assertion.eq(metric.chi_square_distance(a, b), metric.chi_square_distance_numpy(npa, npb))

        gower = metric.distance_metric(metric.type_metric.GOWER, data=[a, b], numpy_usage=False)
        gower_numpy = metric.distance_metric(metric.type_metric.GOWER, data=[a, b], numpy_usage=True)
        assertion.eq(gower(a, b), gower_numpy(npa, npb))
