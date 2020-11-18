"""!

@brief Unit-tests for X-Means algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.xmeans_templates import XmeansTestTemplates
from pyclustering.cluster.xmeans import xmeans, splitting_type

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.utils import read_sample
from pyclustering.utils.metric import distance_metric, type_metric


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

    def testBicClusterAllocationSampleSimple1MetricEuclidean(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, metric=metric)

    def testBicClusterAllocationSampleSimple1MetricEuclideanSquare(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, metric=metric)

    def testBicClusterAllocationSampleSimple1MetricManhattan(self):
        metric = distance_metric(type_metric.MANHATTAN)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, metric=metric)

    def testBicClusterAllocationSampleSimple1MetricChebyshev(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, metric=metric)

    def testBicClusterAllocationSampleSimple1MetricMinkowski2(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, metric=metric)

    def testBicClusterAllocationSampleSimple1MetricMinkowski4(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=4)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, metric=metric)

    def testBicClusterAllocationSampleSimple1MetricCanberra(self):
        metric = distance_metric(type_metric.CANBERRA)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, metric=metric)

    def testBicClusterAllocationSampleSimple1MetricChiSquare(self):
        metric = distance_metric(type_metric.CHI_SQUARE)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, metric=metric)

    def testBicClusterAllocationSampleSimple1MetricGower(self):
        metric = distance_metric(type_metric.GOWER, data=read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1))
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, metric=metric)

    def testMndlClusterAllocationSampleSimple1MetricEuclidean(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, metric=metric)

    def testMndlClusterAllocationSampleSimple1MetricEuclideanSquare(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, metric=metric, alpha=0.1, beta=0.1)

    def testMndlClusterAllocationSampleSimple1MetricManhattan(self):
        metric = distance_metric(type_metric.MANHATTAN)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, metric=metric)

    def testMndlClusterAllocationSampleSimple1MetricChebyshev(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, metric=metric)

    def testMndlClusterAllocationSampleSimple1MetricMinkowski2(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, metric=metric)

    def testMndlClusterAllocationSampleSimple1MetricMinkowski4(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=4)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, metric=metric)

    def testMndlClusterAllocationSampleSimple1MetricCanberra(self):
        metric = distance_metric(type_metric.CANBERRA)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, metric=metric)

    def testMndlClusterAllocationSampleSimple1MetricChiSquare(self):
        metric = distance_metric(type_metric.CHI_SQUARE)
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, metric=metric, alpha=0.1, beta=0.1, random_state=1000)

    def testMndlClusterAllocationSampleSimple1MetricGower(self):
        metric = distance_metric(type_metric.GOWER, data=read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1))
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, metric=metric)

    def testBicWrongStartClusterAllocationSampleSimple1(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleSimple1(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, alpha=0.1, beta=0.1)

    def testMndlSampleSimple1WithoutInitialCenters(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, alpha=0.1, beta=0.1)

    def testMndlWrongStartClusterAllocationSampleSimple1(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, alpha=0.1, beta=0.1)

    def testBicClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple2Repeat(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, repeat=5)

    def testBicWrongStartClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, alpha=0.1, beta=0.1)

    def testMndlWrongStartClusterAllocationSampleSimple2(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, alpha=0.1, beta=0.1)

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
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, alpha=0.2, beta=0.2)

    def testMndlWrongStartClusterClusterAllocationSampleSimple3(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 4, False, alpha=0.2, beta=0.2)

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

    def testMndlWrongStartClusterAllocationSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testMndlClusterAllocationMaxLessRealSampleSimple4(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 4.0]], None, splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 2, False)

    def testBicClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicWrongStartClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, random_state=1000)

    def testMndlWrongStartClusterAllocationSampleSimple5(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, random_state=1000)

    def testBicClusterAllocationSampleSimple6(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, [[3.5, 3.5], [3.7, 3.7]], [20, 21], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple6WithoutInitial(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, None, [20, 21], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleSimple6(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, [[3.5, 3.5], [3.7, 3.7]], [20, 21], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testMndlClusterAllocationSampleSimple6WithoutInitial(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, None, [20, 21], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False)

    def testBicClusterAllocationSampleSimple7(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [[1], [2]], [10, 10], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple7WithoutInitial(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, None, [10, 10], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleSimple7(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [[1], [2]], [10, 10], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, alpha=0.01, beta=0.01)

    def testMndlClusterAllocationSampleSimple7WithoutInitial(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, None, [10, 10], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, alpha=0.01, beta=0.01)

    def testBicClusterAllocationSampleSimple8(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-2.0], [3.0], [6.0], [12.0]], [15, 30, 20, 80], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testBicClusterAllocationSampleSimple8WrongAmountCenters(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[3.0], [6.0]], [15, 30, 20, 80], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False)

    def testMndlClusterAllocationSampleSimple8WrongAmountCenters(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[3.0], [6.0]], [15, 30, 20, 80], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, 20, False, alpha=0.2, beta=0.2)

    def testBicClusterAllocationSampleSimple8WrongAmountCentersRandomState(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[3.0], [6.0]], [15, 30, 20, 80], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, random_state=1000)

    def testMndlClusterAllocationSampleSimple8WrongAmountCentersRandomState(self):
        XmeansTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[3.0], [6.0]], [15, 30, 20, 80], splitting_type.BAYESIAN_INFORMATION_CRITERION, 20, False, random_state=1000)

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


    def test_random_state_1(self):
        XmeansTestTemplates.random_state(False, 2, 10, 1)

    def test_random_state_2(self):
        XmeansTestTemplates.random_state(False, 2, 10, 2)

    def test_random_state_4(self):
        XmeansTestTemplates.random_state(False, 2, 10, 4)

    def test_random_state_32(self):
        XmeansTestTemplates.random_state(False, 2, 10, 32)

    def test_random_state_1024(self):
        XmeansTestTemplates.random_state(False, 2, 10, 1024)

    def test_random_state_65536(self):
        XmeansTestTemplates.random_state(False, 2, 10, 65536)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, xmeans, [])

    def test_incorrect_centers(self):
        self.assertRaises(ValueError, xmeans, [[0], [1], [2]], [])

    def test_incorrect_tolerance(self):
        self.assertRaises(ValueError, xmeans, [[0], [1], [2]], [[1]], 20, -1)

    def test_incorrect_repeat(self):
        self.assertRaises(ValueError, xmeans, [[0], [1], [2]], repeat=0)
