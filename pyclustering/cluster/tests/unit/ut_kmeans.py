"""!

@brief Unit-tests for K-Means algorithm.

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

from pyclustering.cluster.tests.kmeans_templates import KmeansTestTemplates

from pyclustering.cluster.kmeans import kmeans

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.utils.metric import distance_metric, type_metric


class KmeansUnitTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False)

    def testClusterOneAllocationSampleSimple1(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10], False)

    def testClusterAllocationSampleSimple1Euclidean(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1EuclideanSquare(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1Manhattan(self):
        metric = distance_metric(type_metric.MANHATTAN)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1Chebyshev(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1Minkowski01(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1Minkowski02(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=4)
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple1UserDefined(self):
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN, numpy_usage=True))
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], False, metric=metric)

    def testClusterAllocationSampleSimple2(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], False)

    def testClusterOneAllocationSampleSimple2(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23], False)

    def testClusterAllocationSampleSimple3(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], False)

    def testClusterOneAllocationSampleSimple3(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60], False)

    def testClusterAllocationSampleSimple4(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], False)

    def testClusterOneAllocationSampleSimple4(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[2.0, 5.0]], [75], False)

    def testClusterAllocationSampleSimple5(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], False)

    def testClusterOneAllocationSampleSimple5(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60], False)

    def testClusterOneDimensionSampleSimple7(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [[-3.0], [2.0]], [10, 10], False)

    def testClusterOneDimensionSampleSimple8(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-4.0], [3.1], [6.1], [12.0]], [15, 30, 20, 80], False)

    def testWrongNumberOfCentersSimpleSample1(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.0, 4.5], [3.3, 6.5], [5.0, 7.8]], None, False)

    def testWrongNumberOfCentersSimpleSample2(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[1.3, 1.5], [5.2, 8.5], [5.0, 7.8], [11.0, -3.0]], None, False)

    def testWrongNumberOfCentersSimpleSample3(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[4.5, 3.4], [-1.7, 4.3], [1.5, 1.0], [11.3, 1.2], [-4.6, -5.2]], None, False)

    def testWrongNumberOfCentersSimpleSample4(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[2.4, -1.4], [-5.2, -8.5], [-5.0, 3.1], [6.2, 1.4], [7.9, 2.4]], None, False)

    def testWrongNumberOfCentersSimpleSample5(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[-1.9, 3.2], [1.2, 34.5], [15.2, 34.8], [192, 234], [-32.3, -106]], None, False)

    def testTheSameData1(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [ [4.0], [8.0] ], [10, 20], False)

    def testTheSameData2(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [ [1.0, 1.0], [2.5, 2.5], [4.0, 4.0] ], [5, 5, 5], False)

    def testOneDimensionalData1(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-2.0], [3.0], [6.0], [12.0]], [15, 30, 20, 80], False)

    def testOneDimensionalData2(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [[4.5], [6.2]], [20, 10], False)

    def testThreeDimensionalData1(self):
        KmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, [[1.0, 0.6, 0.8], [4.1, 4.2, 4.3]], [10, 10], False)

    def testDifferentDimensions(self):
        kmeans_instance = kmeans([ [0, 1, 5], [0, 2, 3] ], [ [0, 3] ], ccore=False)
        self.assertRaises(ValueError, kmeans_instance.process)


    def testClusterAllocationOneDimensionData(self):
        KmeansTestTemplates.templateClusterAllocationOneDimensionData(False)


    def testObserveSampleSimple1(self):
        KmeansTestTemplates.templateCollectEvolution(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.5, 5.6], [6.8, 7.4]], [5, 5], False)

    def testObserveSampleSimple1OneCluster(self):
        KmeansTestTemplates.templateCollectEvolution(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.3, 5.4]], [10], False)

    def testObserveSampleSimple2(self):
        KmeansTestTemplates.templateCollectEvolution(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.4, 4.9], [6.8, 7.1], [7.6, 0.4]], [10, 5, 8], False)


    def testEncoderProcedureSampleSimple4(self):
        KmeansTestTemplates.templateEncoderProcedures(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], 5, False)


    def testShowResultsSampleSimple01(self):
        KmeansTestTemplates.templateShowClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.5, 5.6], [6.8, 7.4]], False)

    def testShowResultsSampleSimple02(self):
        KmeansTestTemplates.templateShowClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.4, 4.9], [6.8, 7.1], [7.6, 0.4]], False)

    def testShowResultsOneDimensionalData(self):
        KmeansTestTemplates.templateShowClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-2.0], [3.0], [6.0], [12.0]], False)

    def testShowResultsThreeDimensionalData(self):
        KmeansTestTemplates.templateShowClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, [[1.0, 0.6, 0.8], [4.1, 4.2, 4.3]], False)


    def testAnimateResultsSampleSimple01(self):
        KmeansTestTemplates.templateAnimateClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.5, 5.6], [6.8, 7.4]], False)

    def testAnimateResultsSampleSimple02(self):
        KmeansTestTemplates.templateAnimateClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.4, 4.9], [6.8, 7.1], [7.6, 0.4]], False)

    def testAnimateResultsOneDimensionalData(self):
        KmeansTestTemplates.templateAnimateClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-2.0], [3.0], [6.0], [12.0]], False)

    def testAnimateResultsThreeDimensionalData(self):
        KmeansTestTemplates.templateAnimateClusteringResultNoFailure(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, [[1.0, 0.6, 0.8], [4.1, 4.2, 4.3]], False)


if __name__ == "__main__":
    unittest.main()
