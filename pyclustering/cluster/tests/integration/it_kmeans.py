"""!

@brief Integration-tests for K-Means algorithm.

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

import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.kmeans_templates import KmeansTestTemplates
from pyclustering.cluster.kmeans import kmeans

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.core.tests import remove_library

from pyclustering.utils.metric import distance_metric, type_metric


class KmeansIntegrationTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True)

    def testClusterOneAllocationSampleSimple1ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10], True)

    def testClusterAllocationSampleSimple1EuclideanByCore(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, metric=metric)

    def testClusterAllocationSampleSimple1EuclideanSquareByCore(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, metric=metric)

    def testClusterAllocationSampleSimple1ManhattanByCore(self):
        metric = distance_metric(type_metric.MANHATTAN)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, metric=metric)

    def testClusterAllocationSampleSimple1ChebyshevByCore(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, metric=metric)

    def testClusterAllocationSampleSimple1Minkowski01ByCore(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, metric=metric)

    def testClusterAllocationSampleSimple1Minkowski02ByCore(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=4)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, metric=metric)

    def testClusterAllocationSampleSimple1UserDefinedByCore(self):
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, metric=metric)

    def testClusterAllocationSampleSimple1Canberra(self):
        metric = distance_metric(type_metric.CANBERRA)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, metric=metric)

    def testClusterAllocationSampleSimple1ChiSquare(self):
        metric = distance_metric(type_metric.CHI_SQUARE)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, metric=metric)

    def testClusterAllocationSampleSimple2ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], True)

    def testClusterOneAllocationSampleSimple2ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23], True)

    def testClusterAllocationSampleSimple3ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], True)

    def testClusterOneAllocationSampleSimple3ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60], True)

    def testClusterAllocationSampleSimple4ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], True)

    def testClusterOneAllocationSampleSimple4ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[2.0, 5.0]], [75], True)

    def testClusterAllocationSampleSimple5ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], True)

    def testClusterOneAllocationSampleSimple5ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60], True)

    def testClusterAllocationSampleSimple5Canberra(self):
        metric = distance_metric(type_metric.CANBERRA)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [30, 30], True, metric=metric)

    def testClusterAllocationSampleSimple5ChiSquare(self):
        metric = distance_metric(type_metric.CHI_SQUARE)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[3.4, 2.6], [3.4, -3.2], [-3.4, -3.4], [-3.1, 3.3]], [15, 15, 15, 15], True, metric=metric)

    def testClusterOneDimensionSampleSimple7ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [[-3.0], [2.0]], [10, 10], True)

    def testClusterOneDimensionSampleSimple8ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-4.0], [3.1], [6.1], [12.0]], [15, 30, 20, 80], True)

    def testWrongNumberOfCentersSimpleSample1ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.0, 4.5], [3.3, 6.5], [5.0, 7.8]], None, True)

    def testWrongNumberOfCentersSimpleSample2ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[1.3, 1.5], [5.2, 8.5], [5.0, 7.8], [11.0, -3.0]], None, True)

    def testTheSameData1ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [ [4.0], [8.0] ], [10, 20], True)

    def testTheSameData2ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [ [1.0, 1.0], [2.5, 2.5], [4.0, 4.0] ], [5, 5, 5], True)

    def testClusterAllocationOneDimensionDataByCore(self):
        KmeansTestTemplates.templateClusterAllocationOneDimensionData(True)


    def testEncoderProcedureSampleSimple4ByCore(self):
        KmeansTestTemplates.templateEncoderProcedures(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], 5, True)

    def testCoreInterfaceIntInputData(self):
        kmeans_instance = kmeans([ [1], [2], [3], [20], [21], [22] ], [ [2], [21] ], 0.025, True)
        kmeans_instance.process()
        assert len(kmeans_instance.get_clusters()) == 2


    def testObserveSampleSimple1ByCore(self):
        KmeansTestTemplates.templateCollectEvolution(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.5, 5.6], [6.8, 7.4]], [5, 5], True)

    def testObserveSampleSimple1OneClusterByCore(self):
        KmeansTestTemplates.templateCollectEvolution(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.3, 5.4]], [10], True)

    def testObserveSampleSimple2ByCore(self):
        KmeansTestTemplates.templateCollectEvolution(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.4, 4.9], [6.8, 7.1], [7.6, 0.4]], [10, 5, 8], True)


    def testItermax0ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [], True, itermax=0)

    def testItermax1ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, itermax=1)

    def testItermax10Simple01ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True, itermax=10)

    def testItermax10Simple02ByCore(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], True, itermax=10)


    def testShowResultsSampleSimple01(self):
        KmeansTestTemplates.templateShowClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.5, 5.6], [6.8, 7.4]], True)

    def testShowResultsSampleSimple02(self):
        KmeansTestTemplates.templateShowClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.4, 4.9], [6.8, 7.1], [7.6, 0.4]], True)

    def testShowResultsOneDimensionalData(self):
        KmeansTestTemplates.templateShowClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-2.0], [3.0], [6.0], [12.0]], True)

    def testShowResultsThreeDimensionalData(self):
        KmeansTestTemplates.templateShowClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, [[1.0, 0.6, 0.8], [4.1, 4.2, 4.3]], True)


    def testAnimateResultsSampleSimple01(self):
        KmeansTestTemplates.templateAnimateClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.5, 5.6], [6.8, 7.4]], True)

    def testAnimateResultsSampleSimple02(self):
        KmeansTestTemplates.templateAnimateClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.4, 4.9], [6.8, 7.1], [7.6, 0.4]], True)

    def testAnimateResultsOneDimensionalData(self):
        KmeansTestTemplates.templateAnimateClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-2.0], [3.0], [6.0], [12.0]], True)

    def testAnimateResultsThreeDimensionalData(self):
        KmeansTestTemplates.templateAnimateClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, [[1.0, 0.6, 0.8], [4.1, 4.2, 4.3]], True)



    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True)
