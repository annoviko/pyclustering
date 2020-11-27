"""!

@brief Unit-tests for K-Medoids algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster.tests.kmedoids_templates import kmedoids_test_template

from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS

from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric


class KmedoidsUnitTest(unittest.TestCase):
    def testClusterAllocationSampleSimple1(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], False)

    def testClusterAllocationSampleSimple1WrongInitials1(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [1, 2, 3, 4], [2, 2, 3, 3], False)

    def testClusterAllocationSampleSimple1DistanceMatrix(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1DistanceMatrixNumpy(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], False, data_type='distance_matrix', input_type='numpy')

    def testClusterAllocationSampleSimple1Euclidean(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1EuclideanDistanceMatrix(self):
        metric = distance_metric(type_metric.EUCLIDEAN)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1SquareEuclidean(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1SquareEuclideanDistanceMatrix(self):
        metric = distance_metric(type_metric.EUCLIDEAN_SQUARE)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1Manhattan(self):
        metric = distance_metric(type_metric.MANHATTAN)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1ManhattanDistanceMatrix(self):
        metric = distance_metric(type_metric.MANHATTAN)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1Chebyshev(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1ChebyshevDistanceMatrix(self):
        metric = distance_metric(type_metric.CHEBYSHEV)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1Minkowski(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2.0)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1MinkowskiDistanceMatrix(self):
        metric = distance_metric(type_metric.MINKOWSKI, degree=2.0)
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1Gower(self):
        metric = distance_metric(type_metric.GOWER, data=read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1))
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1GowerDistanceMatrix(self):
        metric = distance_metric(type_metric.GOWER, data=read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1))
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1UserDefined(self):
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False)

    def testClusterAllocationSampleSimple1UserDefinedDistanceMatrix(self):
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        kmedoids_test_template.templateLengthProcessWithMetric(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], metric, False, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple1(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10], False)

    def testClusterOneAllocationSampleSimple1DistanceMatrix(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10], False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple1WithMedoidsInitializer(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, None, [5, 5], False, initialize_medoids=2)

    def testClusterAllocationSampleSimple2(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], False)

    def testClusterAllocationSampleSimple2DistanceMatrix(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], False, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple2(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23], False)

    def testClusterOneAllocationSampleSimple2DistanceMatrix(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23], False, data_type='distance_matrix')

    def testClusterAllocationSampleSimple2WithMedoidsInitializer(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, None, [10, 5, 8], False, initialize_medoids=3)

    def testClusterAllocationSampleSimple3(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 12, 25, 37], [10, 10, 10, 30], False)

    def testClusterAllocationSampleSimple3DistanceMatrix(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 12, 25, 37], [10, 10, 10, 30], False, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple3(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [30], [60], False)

    def testClusterAllocationSampleSimple3WithMedoidsInitializer(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, None, [10, 10, 10, 30], False, initialize_medoids=4)

    def testClusterAllocationSampleSimple5(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 18, 34, 55], [15, 15, 15, 15], False)

    def testClusterAllocationSampleSimple5DistanceMatrix(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 18, 34, 55], [15, 15, 15, 15], False, data_type='distance_matrix')

    def testClusterOneAllocationSampleSimple5(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [35], [60], False)

    def testClusterTheSameData1(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [2, 20], [10, 20], False)

    def testClusterTheSameData1DistanceMatrix(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [2, 20], [10, 20], False, data_type='distance_matrix')

    def testClusterTheSameData2(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [2, 7, 12], [5, 5, 5], False)

    def testClusterTheSameData2DistanceMatrix(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, [2, 7, 12], [5, 5, 5], False, data_type='distance_matrix')


    def testClusterAllocationOneDimensionData(self):
        kmedoids_test_template.templateClusterAllocationOneDimensionData(False)


    def testClusterAllocationTheSameObjectsOneInitialMedoid(self):
        kmedoids_test_template.templateClusterAllocationTheSameObjects(20, 1, False)

    def testClusterAllocationTheSameObjectsTwoInitialMedoids(self):
        kmedoids_test_template.templateClusterAllocationTheSameObjects(15, 2, False)

    def testClusterAllocationTheSameObjectsThreeInitialMedoids(self):
        kmedoids_test_template.templateClusterAllocationTheSameObjects(25, 3, False)


    def testPredictOnePoint(self):
        medoids = [4, 12, 25, 37]
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, [[0.3, 0.2]], [0], False)
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, [[4.1, 1.1]], [3], False)
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, [[2.1, 1.9]], [2], False)
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, [[2.1, 4.1]], [1], False)

    def testPredictOnePointUserMetric(self):
        medoids = [4, 12, 25, 37]
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, [[0.3, 0.2]], [0], False, metric=metric)

    def testPredictTwoPoints(self):
        medoids = [4, 12, 25, 37]
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, [[0.3, 0.2], [2.1, 1.9]], [0, 2], False)
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, [[2.1, 4.1], [2.1, 1.9]], [1, 2], False)

    def testPredictTwoPointsUserMetric(self):
        medoids = [4, 12, 25, 37]
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, [[0.3, 0.2], [2.1, 1.9]], [0, 2], False, metric=metric)

    def testPredictFourPoints(self):
        medoids = [4, 12, 25, 37]
        to_predict = [[0.3, 0.2], [4.1, 1.1], [2.1, 1.9], [2.1, 4.1]]
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, to_predict, [0, 3, 2, 1], False)

    def testPredictFivePoints(self):
        medoids = [4, 12, 25, 37]
        to_predict = [[0.3, 0.2], [4.1, 1.1], [3.9, 1.1], [2.1, 1.9], [2.1, 4.1]]
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, to_predict, [0, 3, 3, 2, 1], False)

    def testPredictFivePointsUserMetric(self):
        medoids = [4, 12, 25, 37]
        to_predict = [[0.3, 0.2], [4.1, 1.1], [3.9, 1.1], [2.1, 1.9], [2.1, 4.1]]
        metric = distance_metric(type_metric.USER_DEFINED, func=distance_metric(type_metric.EUCLIDEAN))
        kmedoids_test_template.templatePredict(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, medoids, to_predict, [0, 3, 3, 2, 1], False, metric=metric)


    def testAllocatedRequestedClustersSampleSimple01(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 1, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 2, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 3, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 4, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 5, None, False)

    def testAllocatedRequestedClustersSampleSimple02(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 1, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 2, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 3, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 4, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 5, None, False)

    def testAllocatedRequestedClustersSampleSimple03(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 2, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 5, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 8, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 10, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 15, None, False)

    def testAllocatedRequestedClustersSampleSimple04(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 10, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 25, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 40, None, False)


    def testAllocatedRequestedClustersWithTheSamePoints1(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [[0.0, 0.0], [0.1, 0.1], [0.0, 0.0], [0.1, 0.2]]
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 3, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 3, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 2, None, False)
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 1, None, False)

    def testAllocatedRequestedClustersWithTheSamePoints2(self):
        sample = [[0.23, 0.2], [-0.1, 0.1], [0.0, 0.9], [0.1, -0.2], [0.8, 0.1], [-0.1, 0.1], [-0.4, -0.2], [0.0, 0.9]]
        answers = [1, 2, 3, 4, 5, 6, 6, 6]
        for expected_amount in answers:
            kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, expected_amount, None, False)

    def testAllocatedRequestedClustersWithTotallyTheSamePoints(self):
        # Bug issue #366 - Kmedoids returns incorrect number of clusters.
        sample = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
        kmedoids_test_template.templateAllocateRequestedClusterAmount(sample, 1, None, False)


    def testItermax0(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [], False, itermax=0)

    def testItermax1(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], False, itermax=1)

    def testItermax10Simple01(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], False, itermax=10)

    def testItermax10Simple02(self):
        kmedoids_test_template.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], False, itermax=10)


    def testSimple01AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, False, random_state=1000)

    def testSimple01AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, SIMPLE_ANSWERS.ANSWER_SIMPLE1, False, random_state=1000, data_type='distance_matrix')

    def testSimple02AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, False, random_state=1000)

    def testSimple02AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, SIMPLE_ANSWERS.ANSWER_SIMPLE2, False, random_state=1000, data_type='distance_matrix')

    def testSimple03AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, False, random_state=1000)

    def testSimple03AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, SIMPLE_ANSWERS.ANSWER_SIMPLE3, False, random_state=1000, data_type='distance_matrix')

    def testSimple04AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, SIMPLE_ANSWERS.ANSWER_SIMPLE4, False, random_state=1000)

    def testSimple04AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, SIMPLE_ANSWERS.ANSWER_SIMPLE4, False, random_state=1000, data_type='distance_matrix')

    def testSimple05AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, False, random_state=1000)

    def testSimple05AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, SIMPLE_ANSWERS.ANSWER_SIMPLE5, False, random_state=1000, data_type='distance_matrix')

    def testSimple06AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, False, random_state=1000)

    def testSimple06AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, SIMPLE_ANSWERS.ANSWER_SIMPLE6, False, random_state=1000, data_type='distance_matrix')

    def testSimple07AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, False, random_state=1000)

    def testSimple07AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, SIMPLE_ANSWERS.ANSWER_SIMPLE7, False, random_state=1000, data_type='distance_matrix')

    def testSimple08AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, False, random_state=1000)

    def testSimple08AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, SIMPLE_ANSWERS.ANSWER_SIMPLE8, False, random_state=1000, data_type='distance_matrix')

    def testSimple09AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, False, random_state=1000)

    def testSimple09AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, SIMPLE_ANSWERS.ANSWER_SIMPLE9, False, random_state=1000, data_type='distance_matrix')

    def testSimple10AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, False, random_state=1000)

    def testSimple10AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, SIMPLE_ANSWERS.ANSWER_SIMPLE10, False, random_state=1000, data_type='distance_matrix')

    def testSimple11AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, False, random_state=1000)

    def testSimple11AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, SIMPLE_ANSWERS.ANSWER_SIMPLE11, False, random_state=1000, data_type='distance_matrix')

    def testSimple12AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, False, random_state=1000)

    def testSimple12AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, SIMPLE_ANSWERS.ANSWER_SIMPLE12, False, random_state=1000, data_type='distance_matrix')

    def testSimple13AnswerByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, False, random_state=1000)

    def testSimple13AnswerDistanceMatrixByCore(self):
        kmedoids_test_template.clustering_with_answer(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, SIMPLE_ANSWERS.ANSWER_SIMPLE13, False, random_state=1000, data_type='distance_matrix')


    def test_incorrect_data(self):
        self.assertRaises(ValueError, kmedoids, [], [1])

    def test_incorrect_centers(self):
        self.assertRaises(ValueError, kmedoids, [[0], [1], [2]], [])

    def test_incorrect_tolerance(self):
        self.assertRaises(ValueError, kmedoids, [[0], [1], [2]], [1], -1.0)

    def test_incorrect_itermax(self):
        self.assertRaises(ValueError, kmedoids, [[0], [1], [2]], [1], itermax=-5)
