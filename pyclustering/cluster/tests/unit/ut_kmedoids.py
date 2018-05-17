"""!

@brief Unit-tests for K-Medoids algorithm.

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


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.kmedoids_templates import KmedoidsTestTemplates

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric


class KmedoidsUnitTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], False)

    def testClusterAllocationSampleSimple1DistanceMatrix(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1DistanceMatrixNumpy(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], False, data_type='distance_matrix', input_type='numpy')

    def testClusterAllocationSampleSimple1Euclidean(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1EuclideanDistanceMatrix(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1SquareEuclidean(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1SquareEuclideanDistanceMatrix(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1Manhattan(self):
        metric = distance_metric(type_metric.MANHATTAN)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1ManhattanDistanceMatrix(self):
        metric = distance_metric(type_metric.MANHATTAN)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1Chebyshev(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1ChebyshevDistanceMatrix(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1Minkowski(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2.0)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1MinkowskiDistanceMatrix(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2.0)
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1UserDefined(self):
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1UserDefinedDistanceMatrix(self):
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        KmedoidsTestTemplates.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple1(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10], False)

    def testClusterOneAllocationSampleSimple1DistanceMatrix(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10], False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple2(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], False)

    def testClusterAllocationSampleSimple2DistanceMatrix(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], False, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple2(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23], False)

    def testClusterOneAllocationSampleSimple2DistanceMatrix(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23], False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple3(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 12, 25, 37], [10, 10, 10, 30], False)

    def testClusterAllocationSampleSimple3DistanceMatrix(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 12, 25, 37], [10, 10, 10, 30], False, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple3(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [30], [60], False)

    def testClusterAllocationSampleSimple5(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 18, 34, 55], [15, 15, 15, 15], False)

    def testClusterAllocationSampleSimple5DistanceMatrix(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 18, 34, 55], [15, 15, 15, 15], False, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple5(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [35], [60], False)

    def testClusterTheSameData1(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [2, 20], [10, 20], False)

    def testClusterTheSameData1DistanceMatrix(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [2, 20], [10, 20], False, data_type='distance_matrix')

    def testClusterTheSameData2(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [2, 7, 12], [5, 5, 5], False)

    def testClusterTheSameData2DistanceMatrix(self):
        KmedoidsTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [2, 7, 12], [5, 5, 5], False, data_type='distance_matrix')


    def testClusterAllocationOneDimensionData(self):
        KmedoidsTestTemplates.templateClusterAllocationOneDimensionData(False)


    def testClusterAllocationTheSameObjectsOneInitialMedoid(self):
        KmedoidsTestTemplates.templateClusterAllocationTheSameObjects(20, 1, False)

    def testClusterAllocationTheSameObjectsTwoInitialMedoids(self):
        KmedoidsTestTemplates.templateClusterAllocationTheSameObjects(15, 2, False)

    def testClusterAllocationTheSameObjectsThreeInitialMedoids(self):
        KmedoidsTestTemplates.templateClusterAllocationTheSameObjects(25, 3, False)


    def testAllocatedRequestedClustersSampleSimple01(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 1, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 3, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 4, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 5, None, False)

    def testAllocatedRequestedClustersSampleSimple02(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 1, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 3, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 4, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 5, None, False)

    def testAllocatedRequestedClustersSampleSimple03(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 5, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 8, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 10, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 15, None, False)

    def testAllocatedRequestedClustersSampleSimple04(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 10, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 25, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 40, None, False)

    def testAllocatedRequestedClustersWithTheSamePoints(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [ [0.0, 0.0], [0.1, 0.1], [0.0, 0.0], [0.1, 0.2] ]
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 4, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 3, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 1, None, False)


    def testAllocatedRequestedClustersWithTotallyTheSamePoints(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [ [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0] ]
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 4, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 3, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 2, None, False)
        KmedoidsTestTemplates.templateAllocateRequestedClusterAmount(sample, 1, None, False)


if __name__ == "__main__":
    unittest.main()
