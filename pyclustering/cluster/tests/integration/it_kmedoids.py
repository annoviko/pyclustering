"""!

@brief Integration-tests for K-Medoids algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.kmedoids_templates import kmedoids_test_template
from pyclustering.cluster.kmedoids import kmedoids

from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS

from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric

from pyclustering.core.tests import remove_library


class KmedoidsIntegrationTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], True)

    def testClusterAllocationSampleSimple1WrongInitials1ByCore(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [1, 2, 3, 4], [2, 2, 3, 3], True)

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
        kmedoids_instance = kmedoids([[1], [2], [3], [20], [21], [22]], [2, 5], 0.025, True)
        kmedoids_instance.process()
        assert len(kmedoids_instance.get_clusters()) == 2


    def testAllocatedRequestedClustersSampleSimple04ByCore(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 10, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 25, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 40, None, True)


    def testAllocatedRequestedClustersWithTheSamePointsByCore(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [[0.0, 0.0], [0.1, 0.1], [0.0, 0.0], [0.1, 0.2]]
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 3, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 3, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 2, None, True)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 1, None, True)

    def testAllocatedRequestedClustersWithTheSamePoints2(self):
        sample = [[0.23, 0.2], [-0.1, 0.1], [0.0, 0.9], [0.1, -0.2], [0.8, 0.1], [-0.1, 0.1], [-0.4, -0.2], [0.0, 0.9]]
        answers = [1, 2, 3, 4, 5, 6, 6, 6]
        for expected_amount in answers:
            kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, expected_amount, None, True)

    def testAllocatedRequestedClustersWithTotallyTheSamePointsByCore(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
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


    def testSimple01AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, True, random_state=1000)

    def testSimple01AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, True, random_state=1000, data_type='distance_matrix')

    def testSimple02AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, True, random_state=1000)

    def testSimple02AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, True, random_state=1000, data_type='distance_matrix')

    def testSimple03AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, True, random_state=1000)

    def testSimple03AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, True, random_state=1000, data_type='distance_matrix')

    def testSimple04AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, SIMPLE_ANSWERS.ANSWER_SIMPLE4, True, random_state=1000)

    def testSimple04AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, SIMPLE_ANSWERS.ANSWER_SIMPLE4, True, random_state=1000, data_type='distance_matrix')

    def testSimple05AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, True, random_state=1000)

    def testSimple05AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, True, random_state=1000, data_type='distance_matrix')

    def testSimple06AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, True, random_state=1000)

    def testSimple06AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, True, random_state=1000, data_type='distance_matrix')

    def testSimple07AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, True, random_state=1000)

    def testSimple07AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, True, random_state=1000, data_type='distance_matrix')

    def testSimple08AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, True, random_state=1000)

    def testSimple08AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, True, random_state=1000, data_type='distance_matrix')

    def testSimple09AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, True, random_state=1000)

    def testSimple09AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, True, random_state=1000, data_type='distance_matrix')

    def testSimple10AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, True, random_state=1000)

    def testSimple10AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, True, random_state=1000, data_type='distance_matrix')

    def testSimple11AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, True, random_state=1000)

    def testSimple11AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, True, random_state=1000, data_type='distance_matrix')

    def testSimple12AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, True, random_state=1000)

    def testSimple12AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, True, random_state=1000, data_type='distance_matrix')

    def testSimple13AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, True, random_state=1000)

    def testSimple13AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, True, random_state=1000, data_type='distance_matrix')
