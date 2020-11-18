"""!

@brief Integration-tests for ROCK algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest;

import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.tests.rock_templates import RockTestTemplates;
from pyclustering.cluster.rock import rock;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.core.tests import remove_library;


class RockIntegrationTest(unittest.TestCase):  
    def testClusterAllocationByCore(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 0.5, [5, 5], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 1, 0.5, [10], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 0.5, [10, 5, 8], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 1, 0.5, [23], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 0.5, [10, 10, 10, 30], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.7, 4, 0.5, [10, 10, 10, 30], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 0.5, [15, 15, 15, 15, 15], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1.5, 5, 0.5, [15, 15, 15, 15, 15], True);
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 0.5, [15, 15, 15, 15], True); 

    def testClusterAllocationByCoreIncorrectNumberOfClusters(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 4, 0.5, [15, 15, 15, 15, 15], True);

    def testClusterTheSameData1ByCore(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, 2, 0.5, [10, 20], True);

    def testClusterTheSameData2ByCore(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, 2, 0.5, [5, 5, 5], True);

    def testClusterAllocationOneDimensionDataByCore(self):
        RockTestTemplates.templateClusterAllocationOneDimensionData(True);

    def testCoreInterfaceIntInputData(self):
        optics_instance = rock([ [1], [2], [3], [20], [21], [22] ], 3, 2, 0.5, True);
        optics_instance.process();
        assert len(optics_instance.get_clusters()) == 2;


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        RockTestTemplates.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 0.5, [5, 5], True);
