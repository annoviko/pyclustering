"""!

@brief Unit-tests for X-Means algorithm.

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


class XmeansUnitTest(unittest.TestCase):
    def testBicClusterAllocationSampleSimple1(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple1Repeat(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, repeat=5)

    def testBicSampleSimple1WithoutInitialCenters(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicSampleSimple1WithoutInitialCentersRepeat(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, repeat=3)

    def testBicSampleSimple1MaxLessReal(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], None, splitting_type.BAYESIAN_INFORMATION_CRITERION, 1, False)

    def testBicSampleSimple1MaxLessRealRepeat(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], None, splitting_type.BAYESIAN_INFORMATION_CRITERION, 1, False, repeat=5)

    def testBicWrongStartClusterAllocationSampleSimple1(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleSimple1(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testMndlSampleSimple1WithoutInitialCenters(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testBicClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple2Repeat(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, repeat=5)

    def testBicWrongStartClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testMndlWrongStartClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testBicClusterAllocationSampleSimple3(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple3Repeat(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, repeat=5)

    def testBicWrongStartClusterAllocationSampleSimple3(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [5.9, 5.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationMaxLessRealSampleSimple3(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], None, splitting_type.BAYESIAN_INFORMATION_CRITERION, 3, False)

    def testBicWrongStartClusterClusterAllocationSampleSimple3(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION, 4, False)

    def testMndlClusterAllocationSampleSimple3(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testBicClusterAllocationSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple4Repeat(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, repeat=5)

    def testBicWrongStartClusterAllocationSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationMaxLessRealSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 4.0]], None, splitting_type.BAYESIAN_INFORMATION_CRITERION, 2, False)

    def testMndlClusterAllocationSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testMndlClusterAllocationMaxLessRealSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 4.0]], None, splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 2, False)

    def testBicClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicWrongStartClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testMndlWrongStartClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testBicClusterAllocationSampleSimple6(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, [[3.5, 3.5], [3.7, 3.7]], [20, 21], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple6WithoutInitial(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, None, [20, 21], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple7(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [[1], [2]], [10, 10], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple7WithoutInitial(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, None, [10, 10], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple8(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-2.0], [3.0], [6.0], [12.0]], [15, 30, 20, 80], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple8WrongAmountCenters(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[3.0], [6.0]], [15, 30, 20, 80], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple9(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [[3.0], [6.0]], [10, 20], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple9WithoutInitial(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, None, [10, 20], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple10(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, [[0.0, 0.3], [4.5, 3.4], [10.1, 10.6]], [11, 11, 11], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple10WithoutInitial(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, None, [11, 11, 11], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleTwoDiamonds(self):
        XmeansTestTemplates.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicWrongStartClusterAllocationSampleTwoDiamonds(self):
        XmeansTestTemplates.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2]], [400, 400], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleTwoDiamonds(self):
        XmeansTestTemplates.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testMathErrorDomainBic(self):
        # This is test for bug that was found in #407: 0.0 under logarithm function.
        XmeansTestTemplates.templateLengthProcessData([[0], [0], [10], [10], [20], [20]], [[5], [20]], [2, 2, 2], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMathErrorDomainMndl(self):
        XmeansTestTemplates.templateLengthProcessData([[0], [0], [10], [10], [20], [20]], [[5], [20]], [2, 2, 2], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)


    def testClusterAllocationOneDimensionData(self):
        XmeansTestTemplates.templateClusterAllocationOneDimensionData(False)


    def testKmax05Amount3Offset02Initial01(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(False, 10, 3, 2, 1, 2)

    def testKmax05Amount5Offset02Initial01(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(False, 10, 5, 2, 1, 5)

    def testKmax05Amount5Offset02Initial02(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(False, 10, 5, 2, 2, 5)

    def testKmax05Amount10Offset02Initial03(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(False, 10, 10, 2, 3, 5)

    def testKmax05Amount10Offset02Initial04(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(False, 10, 10, 2, 4, 5)

    def testKmax05Amount10Offset02Initial05(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(False, 10, 10, 2, 5, 5)

    def testKmax05Amount20Offset02Initial05(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(False, 20, 10, 2, 5, 5)

    def testKmax05Amount01Offset01Initial04(self):
        XmeansTestTemplates.templateMaxAllocatedClusters(False, 1, 1000, 1, 4, 5)

    def testPredictOnePoint(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[0.3, 0.2]], 4, [0], False)
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[4.1, 1.1]], 4, [1], False)
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[2.1, 1.9]], 4, [2], False)
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[2.1, 4.1]], 4, [3], False)

    def testPredictTwoPoints(self):
        centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[0.3, 0.2], [2.1, 1.9]], 4, [0, 2], False)
        XmeansTestTemplates.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, centers, [[2.1, 4.1], [2.1, 1.9]], 4, [3, 2], False)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, xmeans, [])

    def test_incorrect_centers(self):
        self.assertRaises(ValueError, xmeans, [[0], [1], [2]], [])

    def test_incorrect_tolerance(self):
        self.assertRaises(ValueError, xmeans, [[0], [1], [2]], [[1]], 20, -1)

    def test_incorrect_repeat(self):
        self.assertRaises(ValueError, xmeans, [[0], [1], [2]], repeat=0)
