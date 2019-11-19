"""!

@brief Integration-tests for X-Means algorithm.

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

from pyclustering.cluster.tests.xmeans_templates import XmeansTestTemplates
from pyclustering.cluster.xmeans import xmeans, splitting_type

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.core.tests import remove_library


class XmeansIntegrationTest(unittest.TestCase):
    def testBicClusterAllocationSampleSimple1ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple1RepeatByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True, repeat=2)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True, repeat=4)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True, repeat=8)

    def testBicSampleSimple1WithoutInitialCentersByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicSampleSimple1WithoutInitialCentersRepeatByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True, repeat=5)

    def testBicSampleSimple1MaxLessRealByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], None,
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 1, True)

    def testBicSampleSimple1MaxLessRealRepeatByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], None,
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 1, True, repeat=5)

    def testBicWrongStartClusterAllocationSampleSimple1ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicWrongStartClusterAllocationSampleSimpleRepeat1ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True, repeat=5)

    def testMndlClusterAllocationSampleSimple1ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)

    def testMndlSampleSimple1WithoutInitialCentersByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)

    def testMndlWrongStartClusterAllocationSampleSimple1ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)

    def testBicClusterAllocationSampleSimple2ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicMaxLessRealSampleSimple2ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], None,
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 2, True)

    def testBicWrongStartClusterAllocationSampleSimple2ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testMndlClusterAllocationSampleSimple2ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)

    def testMndlWrongStartClusterAllocationSampleSimple2ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)

    def testBicClusterAllocationSampleSimple3ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationMaxLessRealSampleSimple3ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], None,
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 3, True)

    def testBicWrongStartClusterClusterAllocationSampleSimple3ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 4, True)

    def testBicWrongStartClusterAllocationSampleSimple3ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [5.9, 5.9]], [10, 10, 10, 30],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testMndlClusterAllocationSampleSimple3ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)

    def testBicClusterAllocationSampleSimple4ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicWrongStartClusterAllocationSampleSimple4ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationMaxLessRealSampleSimple4ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 4.0]], None,
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 2, True)

    def testMndlClusterAllocationSampleSimple4ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)

    def testBicClusterAllocationSampleSimple5ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicWrongStartClusterAllocationSampleSimple5ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testMndlClusterAllocationSampleSimple5ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)

    def testMndlWrongStartClusterAllocationSampleSimple5ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)

    def testBicClusterAllocationSampleSimple6ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, [[3.5, 3.5], [3.7, 3.7]], [20, 21],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple6WithoutInitialByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, None, [20, 21],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple7ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [[1], [2]], [10, 10],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple7WithoutInitialByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, None, [10, 10],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple8ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-2.0], [3.0], [6.0], [12.0]], [15, 30, 20, 80],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple8WrongAmountCentersByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[3.0], [6.0]], [15, 30, 20, 80],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple9ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [[3.0], [6.0]], [10, 20],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple9WithoutInitialByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, None, [10, 20],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple10ByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, [[0.0, 0.3], [4.5, 3.4], [10.1, 10.6]], [11, 11, 11],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleSimple10WithoutInitialByCore(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, None, [11, 11, 11],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicClusterAllocationSampleTwoDiamondsByCore(self):
        XmeansTestTemplates.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testBicWrongStartClusterAllocationSampleTwoDiamondsByCore(self):
        XmeansTestTemplates.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2]], [400, 400],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)

    def testMndlClusterAllocationSampleTwoDiamondsByCore(self):
        XmeansTestTemplates.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400],
                                                      splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, True)


    def testClusterAllocationOneDimensionDataByCore(self):
        XmeansTestTemplates.templateClusterAllocationOneDimensionData(True)

    def testCoreInterfaceIntInputData(self):
        xmeans_instance = xmeans([[1], [2], [3], [20], [21], [22]], [[2], [21]], 5, ccore=True)
        xmeans_instance.process()
        assert len(xmeans_instance.get_clusters()) == 2


    def testKmax05Amount5Offset02Initial01(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(True, 10, 5, 2, 1, 5)

    def testKmax05Amount5Offset02Initial02(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(True, 10, 5, 2, 2, 5)

    def testKmax05Amount10Offset02Initial03(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(True, 10, 10, 2, 3, 5)

    def testKmax05Amount10Offset02Initial04(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(True, 10, 10, 2, 4, 5)

    def testKmax05Amount10Offset02Initial05(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(True, 10, 10, 2, 5, 5)

    def testKmax05Amount20Offset02Initial05(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(True, 20, 10, 2, 5, 5)

    def testKmax05Amount01Offset01Initial04(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(True, 1, 1000, 1, 4, 5)

    def testPredictOnePoint(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[0.3, 0.2]], 4, [0], True)
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[4.1, 1.1]], 4, [1], True)
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[2.1, 1.9]], 4, [2], True)
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[2.1, 4.1]], 4, [3], True)

    def testPredictTwoPoints(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[0.3, 0.2], [2.1, 1.9]], 4, [0, 2], True)
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[2.1, 4.1], [2.1, 1.9]], 4, [3, 2], True)

    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5],
                                                      splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, True)
