"""!

@brief Unit-tests for K-Medians algorithm.

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
import random

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.kmedians_templates import KmediansTestTemplates

from pyclustering.cluster.kmedians import kmedians

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.utils.metric import type_metric, distance_metric


class KmediansUnitTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False)

    def testClusterAllocationSampleSimple1Euclidean(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1EuclideanSquare(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1Manhattan(self):
        metric = distance_metric(type_metric.MANHATTAN)
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1Chebyshev(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1Minkowski(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2.0)
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1UserDefined(self):
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterOneAllocationSampleSimple1(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10], False)

    def testClusterAllocationSampleSimple2(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], False)

    def testClusterOneAllocationSampleSimple2(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23], False)

    def testClusterAllocationSampleSimple3(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], False)

    def testClusterOneAllocationSampleSimple3(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60], False)

    def testClusterAllocationSampleSimple5(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], False)

    def testClusterOneAllocationSampleSimple5(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60], False)

    def testClusterAllocationSample1WrongInitialNumberCenters1(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.8, 9.5], [3.5, 6.6], [1.3, 4.0]], None, False)

    def testClusterAllocationSample1WrongInitialNumberCenters2(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.8, 9.5], [3.5, 6.6], [1.3, 4.0], [1.2, 4.5]], None, False)

    def testClusterAllocationSample2WrongInitialNumberCenters(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5], [7.3, 4.5], [3.1, 5.4]], None, False)

    def testClusterTheSameData1(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [ [4.1], [7.3] ], [10, 20], False)

    def testClusterTheSameData2(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [ [1.1, 1.0], [3.0, 3.1], [5.0, 4.9] ], [5, 5, 5], False)

    def testOddSize(self):
        # Bug issue #428 (https://github.com/annoviko/pyclustering/issues/428)
        data = [[59.00732, 9.748167], [59.00608, 9.749117], [59.0047, 9.749933]]
        KmediansTestTemplates.templateLengthProcessData(data, [[59.00732, 9.748167], [59.00608, 9.749117]], None, False, tolerance=10)


    def testDifferentDimensions(self):
        kmedians_instance = kmedians([ [0, 1, 5], [0, 2, 3] ], [ [0, 3] ], ccore=False)
        self.assertRaises(NameError, kmedians_instance.process)


    def testClusterAllocationOneDimensionData(self):
        KmediansTestTemplates.templateClusterAllocationOneDimensionData(False)


    def testClusterAllocationTheSameObjectsOneInitialCenter(self):
        KmediansTestTemplates.templateClusterAllocationTheSameObjects(20, 1, False)

    def testClusterAllocationTheSameObjectsTwoInitialCenters(self):
        KmediansTestTemplates.templateClusterAllocationTheSameObjects(15, 2, False)

    def testClusterAllocationTheSameObjectsThreeInitialCenters(self):
        KmediansTestTemplates.templateClusterAllocationTheSameObjects(25, 3, False)

    def testClusterAllocationSampleRoughMediansSimple10(self):
        initial_medians = [[0.0772944481804071, 0.05224990900863469], [1.6021689021213712, 1.0347579135245601], [2.3341008076636096, 1.280022869739064]]
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, initial_medians, None, False)

    def testTotalWCESimple4(self):
        sample = [[0, 1, 5], [7, 8, 9], [0, 2, 3], [4, 5, 6]]
        initial_medians = [[0, 3, 2], [4, 6, 5]]
        kmedians_instance = kmedians(sample, initial_medians, ccore=False)
        self.assertNotEqual(self, kmedians_instance.get_total_wce(), 16.0)

    def testPredictOnePoint(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[0.3, 0.2]], [0], False)
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[4.1, 1.1]], [1], False)
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[2.1, 1.9]], [2], False)
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[2.1, 4.1]], [3], False)

    def testPredictOnePointUserMetric(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[0.3, 0.2]], [0], False, metric=metric)

    def testPredictTwoPoints(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[0.3, 0.2], [2.1, 1.9]], [0, 2], False)
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[2.1, 4.1], [2.1, 1.9]], [3, 2], False)

    def testPredictTwoPointsUserMetric(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[0.3, 0.2], [2.1, 1.9]], [0, 2], False, metric=metric)

    def testPredictFourPoints(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        to_predict = [[0.3, 0.2], [4.1, 1.1], [2.1, 1.9], [2.1, 4.1]]
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, to_predict, [0, 1, 2, 3], False)

    def testPredictFivePoints(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        to_predict = [[0.3, 0.2], [4.1, 1.1], [3.9, 1.1], [2.1, 1.9], [2.1, 4.1]]
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, to_predict, [0, 1, 1, 2, 3], False)

    def testPredictFivePointsUserMetric(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        to_predict = [[0.3, 0.2], [4.1, 1.1], [3.9, 1.1], [2.1, 1.9], [2.1, 4.1]]
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        KmediansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, to_predict, [0, 1, 1, 2, 3], False, metric=metric)


    def testItermax0(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [], False, itermax=0)

    def testItermax1(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, itermax=1)

    def testItermax10Simple01(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, itermax=10)

    def testItermax10Simple02(self):
        KmediansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], False, itermax=10)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, kmedians, [], [[1]])

    def test_incorrect_centers(self):
        self.assertRaises(ValueError, kmedians, [[0], [1], [2]], [])

    def test_incorrect_tolerance(self):
        self.assertRaises(ValueError, kmedians, [[0], [1], [2]], [[1]], -1.0)

    def test_incorrect_itermax(self):
        self.assertRaises(ValueError, kmedians, [[0], [1], [2]], [[1]], itermax=-5)
