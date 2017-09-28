"""!

@brief Integration-tests for agglomerative algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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


import unittest;

import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.tests.agglomerative_templates import AgglomerativeTestTemplates;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.cluster.agglomerative import agglomerative, type_link;


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


if __name__ == "__main__":
    unittest.main();