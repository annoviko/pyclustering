"""!

@brief Integration-tests for DBSCAN algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest

import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.tests.dbscan_templates import DbscanTestTemplates
from pyclustering.cluster.dbscan import dbscan

from pyclustering.samples.definitions import SIMPLE_SAMPLES, SIMPLE_ANSWERS
from pyclustering.samples.definitions import FCPS_SAMPLES

from pyclustering.core.tests import remove_library


class DbscanIntegrationTest(unittest.TestCase):  
    def testClusteringByCore(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], True)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 2, [10], True)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, [5, 8, 10], True)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 2, [23], True)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, [10, 10, 10, 30], True)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 3, [60], True)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, [15, 15, 15, 15, 15], True)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 2, 3, [75], True)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, [15, 15, 15, 15], True)
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 10, 3, [60], True)
        DbscanTestTemplates.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3, [30, 30, 30, 30, 30, 30, 32], True)
        DbscanTestTemplates.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 5, 3, [212], True)

    def testClusteringDistanceMatrixByCore(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], True)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 2, [10], True)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, [5, 8, 10], True)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 2, [23], True)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, [10, 10, 10, 30], True)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 3, [60], True)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, [15, 15, 15, 15, 15], True)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 2, 3, [75], True)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, [15, 15, 15, 15], True)
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 10, 3, [60], True)

    def testClusteringTheSameData1ByCore(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 3, [10, 20], True)

    def testClusteringTheSameData1DistanceMatrixByCore(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1.0, 3, [10, 20], True)

    def testClusteringTheSameData2ByCore(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1.0, 2, [5, 5, 5], True)

    def testClusteringTheSameData2DistanceMatrixByCore(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1.0, 2, [5, 5, 5], True)

    def testClusteringSimple5WithoutNeighborsByCore(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 0, [15, 15, 15, 15], True)

    def testClusteringSimple5WithoutNeighborsDistanceMatrixByCore(self):
        DbscanTestTemplates.templateClusteringDistanceMatrix(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 0, [15, 15, 15, 15], True)


    def testLengthProcessedByCore(self):
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.7, 0, 10, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 0, 10, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.3, 0, 15, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0, 15, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.1, 0, 20, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0, 20, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.1, 0, 10, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 65, 75, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.1, 0, 10, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.3, 0, 10, True)
        DbscanTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.6, 0, 10, True)


    def testClusterAllocationOneDimensionDataByCore(self):
        DbscanTestTemplates.templateClusterAllocationOneDimensionData(True)

    def testClusterAllocationOneDimensionDataDistanceMatrixByCore(self):
        DbscanTestTemplates.templateClusterAllocationOneDimensionDistanceMatrix(True)

    def testCoreInterfaceIntInputData(self):
        dbscan_instance = dbscan([ [1], [2], [3], [20], [21], [22] ], 3, 2, True)
        dbscan_instance.process()
        assert len(dbscan_instance.get_clusters()) == 2


    def testPermutationSampleSimple14(self):
        DbscanTestTemplates.templateClusteringWithAnswers(SIMPLE_SAMPLES.SAMPLE_SIMPLE14,
                                                          SIMPLE_ANSWERS.ANSWER_SIMPLE14, 1.0, 5, False,
                                                          random_order=True,
                                                          repeat=20)

    def test_pickle_dump_load(self):
        DbscanTestTemplates.pickle_dump_load(True)

    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        DbscanTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], True)

