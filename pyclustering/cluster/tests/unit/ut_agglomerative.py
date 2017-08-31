"""!

@brief Unit-tests for agglomerative algorithm.

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

from pyclustering.cluster.tests.agglomerative_templates import AgglomerativeTestTemplates;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.cluster.agglomerative import agglomerative, type_link;


class AgglomerativeUnitTests(unittest.TestCase):
    def testClusteringSampleSimple1LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.AVERAGE_LINK, [5, 5]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.AVERAGE_LINK, [10]);

    def testClusteringSampleSimple1LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.CENTROID_LINK, [5, 5]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.CENTROID_LINK, [10]);

    def testClusteringSampleSimple1LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.COMPLETE_LINK, [5, 5]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.COMPLETE_LINK, [10]);

    def testClusteringSampleSimple1LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.SINGLE_LINK, [5, 5]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.SINGLE_LINK, [10]);

    def testClusteringSampleSimple2LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.AVERAGE_LINK, [5, 8, 10]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.AVERAGE_LINK, [23]);

    def testClusteringSampleSimple2LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.CENTROID_LINK, [5, 8, 10]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.CENTROID_LINK, [23]);

    def testClusteringSampleSimple2LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.COMPLETE_LINK, [5, 8, 10]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.COMPLETE_LINK, [23]);

    def testClusteringSampleSimple2LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.SINGLE_LINK, [5, 8, 10]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.SINGLE_LINK, [23]);

    def testClusteringSampleSimple3LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.AVERAGE_LINK, [10, 10, 10, 30]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.AVERAGE_LINK, [60]);
        
    def testClusteringSampleSimple3LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.CENTROID_LINK, [10, 10, 10, 30]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.CENTROID_LINK, [60]);
        
    def testClusteringSampleSimple3LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.COMPLETE_LINK, [10, 10, 10, 30]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.COMPLETE_LINK, [60]);
        
    def testClusteringSampleSimple3LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.SINGLE_LINK, [10, 10, 10, 30]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.SINGLE_LINK, [60]);
        
    def testClusteringSampleSimple4LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.AVERAGE_LINK, [15, 15, 15, 15, 15]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.AVERAGE_LINK, [75]);
        
    def testClusteringSampleSimple4LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.CENTROID_LINK, [15, 15, 15, 15, 15]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.CENTROID_LINK, [75]);
        
    def testClusteringSampleSimple4LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.COMPLETE_LINK, [15, 15, 15, 15, 15]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.COMPLETE_LINK, [75]);
        
    def testClusteringSampleSimple4LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.SINGLE_LINK, [15, 15, 15, 15, 15]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.SINGLE_LINK, [75]);
        
    def testClusteringSampleSimple5LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.AVERAGE_LINK, [15, 15, 15, 15]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.AVERAGE_LINK, [60]);
        
    def testClusteringSampleSimple5LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.CENTROID_LINK, [15, 15, 15, 15]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.CENTROID_LINK, [60]); 
        
    def testClusteringSampleSimple5LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.COMPLETE_LINK, [15, 15, 15, 15]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.COMPLETE_LINK, [60]); 
        
    def testClusteringSampleSimple5LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.SINGLE_LINK, [15, 15, 15, 15]);
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.SINGLE_LINK, [60]); 



    def testClusterAllocationOneDimensionDataLinkAverage(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.AVERAGE_LINK);

    def testClusterAllocationOneDimensionDataLinkCentroid(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.CENTROID_LINK);

    def testClusterAllocationOneDimensionDataLinkComplete(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.COMPLETE_LINK);

    def testClusterAllocationOneDimensionDataLinkSingle(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.SINGLE_LINK);


    def testTwoClusterAllocationTheSameObjectsLinkAverage(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.AVERAGE_LINK, False);

    def testTwoClusterAllocationTheSameObjectLinkCentroid(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.CENTROID_LINK, False);

    def testTwoClusterAllocationTheSameObjectLinkComplete(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.COMPLETE_LINK, False);

    def testTwoClusterAllocationTheSameObjectLinkSingle(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.SINGLE_LINK, False); 


if __name__ == "__main__":
    unittest.main();