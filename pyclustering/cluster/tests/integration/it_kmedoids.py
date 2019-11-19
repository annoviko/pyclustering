"""!

@brief Integration-tests for K-Medoids algorithm.

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

from pyclustering.cluster.tests.kmedoids_templates import kmedoids_test_template
from pyclustering.cluster.kmedoids import kmedoids

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric

from pyclustering.core.tests import remove_library


class KmedoidsIntegrationTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], True)

    def testClusterAllocationSampleSimple1DistanceMatrixByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], True, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1EuclideanByCore(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True)

    def testClusterAllocationSampleSimple1EuclideanDistanceMatrixByCore(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1SquareEuclideanByCore(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True)

    def testClusterAllocationSampleSimple1SquareEuclideanDistanceMatrixByCore(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1ManhattanByCore(self):
        metric = distance_metric(type_metric.MANHATTAN)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True)

    def testClusterAllocationSampleSimple1ManhattanDistanceMatrixByCore(self):
        metric = distance_metric(type_metric.MANHATTAN)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1ChebyshevByCore(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True)

    def testClusterAllocationSampleSimple1ChebyshevDistanceMatrixByCore(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1MinkowskiByCore(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2.0)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True)

    def testClusterAllocationSampleSimple1MinkowskiDistanceMatrixByCore(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2.0)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1GowerByCore(self):
        metric = distance_metric(type_metric.GOWER, data=read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1))
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True)

    def testClusterAllocationSampleSimple1GowerDistanceMatrixByCore(self):
        metric = distance_metric(type_metric.GOWER, data=read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1))
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1UserDefinedByCore(self):
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True)

    def testClusterAllocationSampleSimple1UserDefinedDistanceMatrixByCore(self):
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, True, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple1ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10], True)

    def testClusterOneAllocationSampleSimple1DistanceMatrixByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10], True, data_type='distance_matrix')

    def testClusterAllocationSampleSimple2ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], True)

    def testClusterAllocationSampleSimple2DistanceMatrixByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], True, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple2ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23], True)

    def testClusterOneAllocationSampleSimple2DistanceMatrixByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23], True, data_type='distance_matrix')

    def testClusterAllocationSampleSimple3ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 12, 25, 37], [10, 10, 10, 30], True)

    def testClusterOneAllocationSampleSimple3ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [30], [60], True)

    def testClusterAllocationSampleSimple5ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 18, 34, 55], [15, 15, 15, 15], True)

    def testClusterOneAllocationSampleSimple5ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [35], [60], True)

    def testClusterTheSameData1ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [2, 20], [10, 20], True)

    def testClusterTheSameData2ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [2, 7, 12], [5, 5, 5], True)


    def testClusterAllocationTheSameObjectsOneInitialMedoidByCore(self):
        kmedoids_test_template.templateClusterAllocationTheSameObjects(20, 1, True)

    def testClusterAllocationTheSameObjectsTwoInitialMedoidsByCore(self):
        kmedoids_test_template.templateClusterAllocationTheSameObjects(15, 2, True)

    def testClusterAllocationTheSameObjectsThreeInitialMedoidsByCore(self):
        kmedoids_test_template.templateClusterAllocationTheSameObjects(25, 3, True)

    def testCoreInterfaceIntInputData(self):
        kmedoids_instance = kmedoids([ [1], [2], [3], [20], [21], [22] ], [ 2, 5 ], 0.025, True)
        kmedoids_instance.process()
        assert len(kmedoids_instance.get_clusters()) == 2


    def testAllocatedRequestedClustersSampleSimple04ByCore(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 10, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 25, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 40, None, True)


    def testAllocatedRequestedClustersWithTheSamePointsByCore(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [ [0.0, 0.0], [0.1, 0.1], [0.0, 0.0], [0.1, 0.2] ]
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 4, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 3, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 2, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 1, None, True)

    def testAllocatedRequestedClustersWithTotallyTheSamePointsByCore(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [ [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0] ]
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 4, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 3, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 2, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 1, None, True)


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], True)


    def testItermax0(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [], True, itermax=0)

    def testItermax1(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], True, itermax=1)

    def testItermax10Simple01(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], True, itermax=10)

    def testItermax10Simple02(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], True, itermax=10)
