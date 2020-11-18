"""!

@brief Integration-tests for agglomerative algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest;

import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.tests.agglomerative_templates import AgglomerativeTestTemplates;
from pyclustering.cluster.agglomerative import agglomerative, type_link;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.core.tests import remove_library, corrupt_library;


class AgglomerativeIntegrationTest(unittest.TestCase):
    def testClusteringSampleSimple1LinkAverageByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.AVERAGE_LINK, [5, 5], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.AVERAGE_LINK, [10], True);

    def testClusteringSampleSimple1LinkCentroidByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.CENTROID_LINK, [5, 5], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.CENTROID_LINK, [10], True);

    def testClusteringSampleSimple1LinkCompleteByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.COMPLETE_LINK, [5, 5], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.COMPLETE_LINK, [10], True);

    def testClusteringSampleSimple1LinkSingleByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.SINGLE_LINK, [5, 5], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.SINGLE_LINK, [10], True);

    def testClusteringSampleSimple2LinkAverageByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.AVERAGE_LINK, [5, 8, 10], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.AVERAGE_LINK, [23], True);

    def testClusteringSampleSimple2LinkCentroidByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.CENTROID_LINK, [5, 8, 10], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.CENTROID_LINK, [23], True);

    def testClusteringSampleSimple2LinkCompleteByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.COMPLETE_LINK, [5, 8, 10], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.COMPLETE_LINK, [23], True);

    def testClusteringSampleSimple2LinkSingleByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.SINGLE_LINK, [5, 8, 10], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.SINGLE_LINK, [23], True);


    def testClusteringTheSameData1LinkAverageByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, type_link.AVERAGE_LINK, [10, 20], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, type_link.AVERAGE_LINK, [30], True); 

    def testClusteringTheSameData1LinkCentroidByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, type_link.CENTROID_LINK, [10, 20], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, type_link.CENTROID_LINK, [30], True); 

    def testClusteringTheSameData1LinkCompleteByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, type_link.COMPLETE_LINK, [10, 20], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, type_link.COMPLETE_LINK, [30], True); 

    def testClusteringTheSameData1LinkSingleByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, type_link.SINGLE_LINK, [10, 20], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, type_link.SINGLE_LINK, [30], True); 

    def testClusteringTheSameData2LinkAverageByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, type_link.AVERAGE_LINK, [5, 10], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, type_link.AVERAGE_LINK, [15], True); 

    def testClusteringTheSameData2LinkCentroidByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, type_link.CENTROID_LINK, [5, 10], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, type_link.CENTROID_LINK, [15], True); 

    def testClusteringTheSameData2LinkCompleteByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, type_link.COMPLETE_LINK, [5, 10], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, type_link.COMPLETE_LINK, [15], True); 

    def testClusteringTheSameData2LinkSingleByCore(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, type_link.SINGLE_LINK, [5, 10], True);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, type_link.SINGLE_LINK, [15], True); 


    def testClusterAllocationOneDimensionDataLinkAverageByCore(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.AVERAGE_LINK, True);

    def testClusterAllocationOneDimensionDataLinkCentroidByCore(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.CENTROID_LINK, True);

    def testClusterAllocationOneDimensionDataLinkCompleteByCore(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.COMPLETE_LINK, True);

    def testClusterAllocationOneDimensionDataLinkSingleByCore(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.SINGLE_LINK, True);


    def testTwoClusterAllocationTheSameObjectsLinkAverageByCore(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.AVERAGE_LINK, True);

    def testTwoClusterAllocationTheSameObjectLinkCentroidByCore(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.CENTROID_LINK, True);

    def testTwoClusterAllocationTheSameObjectLinkCompleteByCore(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.COMPLETE_LINK, True); 

    def testTwoClusterAllocationTheSameObjectLinkSingleByCore(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.SINGLE_LINK, True);

    def testCoreInterfaceIntInputData(self):
        agglomerative_instance = agglomerative([ [1], [2], [3], [20], [21], [22] ], 2, type_link.SINGLE_LINK, True);
        agglomerative_instance.process();
        assert len(agglomerative_instance.get_clusters()) == 2;

    @remove_library
    def testProcessingWhenLibraryCoreRemoved(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.AVERAGE_LINK, [5, 5], True);

    @corrupt_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.AVERAGE_LINK, [5, 5], True);
