"""!

@brief Unit-tests for agglomerative algorithm.

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

from pyclustering.cluster.tests.agglomerative_templates import AgglomerativeTestTemplates

from pyclustering.samples.definitions import SIMPLE_SAMPLES
from pyclustering.cluster.agglomerative import agglomerative, type_link


class AgglomerativeUnitTests(unittest.TestCase):
    def testClusteringSampleSimple1LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.AVERAGE_LINK, [5, 5], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.AVERAGE_LINK, [10], False)

    def testClusteringSampleSimple1LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.CENTROID_LINK, [5, 5], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.CENTROID_LINK, [10], False)

    def testClusteringSampleSimple1LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.COMPLETE_LINK, [5, 5], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.COMPLETE_LINK, [10], False)

    def testClusteringSampleSimple1LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.SINGLE_LINK, [5, 5], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.SINGLE_LINK, [10], False)

    def testClusteringSampleSimple2LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.AVERAGE_LINK, [5, 8, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.AVERAGE_LINK, [23], False)

    def testClusteringSampleSimple2LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.CENTROID_LINK, [5, 8, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.CENTROID_LINK, [23], False)

    def testClusteringSampleSimple2LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.COMPLETE_LINK, [5, 8, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.COMPLETE_LINK, [23], False)

    def testClusteringSampleSimple2LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.SINGLE_LINK, [5, 8, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.SINGLE_LINK, [23], False)

    def testClusteringSampleSimple3LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.AVERAGE_LINK, [10, 10, 10, 30], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.AVERAGE_LINK, [60], False)
        
    def testClusteringSampleSimple3LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.CENTROID_LINK, [10, 10, 10, 30], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.CENTROID_LINK, [60], False)
        
    def testClusteringSampleSimple3LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.COMPLETE_LINK, [10, 10, 10, 30], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.COMPLETE_LINK, [60], False)
        
    def testClusteringSampleSimple3LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.SINGLE_LINK, [10, 10, 10, 30], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.SINGLE_LINK, [60], False)
        
    def testClusteringSampleSimple4LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.AVERAGE_LINK, [15, 15, 15, 15, 15], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.AVERAGE_LINK, [75], False)
        
    def testClusteringSampleSimple4LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.CENTROID_LINK, [15, 15, 15, 15, 15], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.CENTROID_LINK, [75], False)
        
    def testClusteringSampleSimple4LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.COMPLETE_LINK, [15, 15, 15, 15, 15], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.COMPLETE_LINK, [75], False)
        
    def testClusteringSampleSimple4LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.SINGLE_LINK, [15, 15, 15, 15, 15], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.SINGLE_LINK, [75], False)
        
    def testClusteringSampleSimple5LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.AVERAGE_LINK, [15, 15, 15, 15], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.AVERAGE_LINK, [60], False)
        
    def testClusteringSampleSimple5LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.CENTROID_LINK, [15, 15, 15, 15], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.CENTROID_LINK, [60], False)
        
    def testClusteringSampleSimple5LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.COMPLETE_LINK, [15, 15, 15, 15], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.COMPLETE_LINK, [60], False)
        
    def testClusteringSampleSimple5LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.SINGLE_LINK, [15, 15, 15, 15], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.SINGLE_LINK, [60], False)


    def testClusteringTheSameData1LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, type_link.AVERAGE_LINK, [10, 20], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, type_link.AVERAGE_LINK, [30], False)

    def testClusteringTheSameData1LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, type_link.CENTROID_LINK, [10, 20], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, type_link.CENTROID_LINK, [30], False)

    def testClusteringTheSameData1LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, type_link.COMPLETE_LINK, [10, 20], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, type_link.COMPLETE_LINK, [30], False)

    def testClusteringTheSameData1LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, type_link.SINGLE_LINK, [10, 20], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 1, type_link.SINGLE_LINK, [30], False)

    def testClusteringTheSameData2LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, type_link.AVERAGE_LINK, [5, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, type_link.AVERAGE_LINK, [15], False)

    def testClusteringTheSameData2LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, type_link.CENTROID_LINK, [5, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, type_link.CENTROID_LINK, [15], False)

    def testClusteringTheSameData2LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, type_link.COMPLETE_LINK, [5, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, type_link.COMPLETE_LINK, [15], False)

    def testClusteringTheSameData2LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, type_link.SINGLE_LINK, [5, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 1, type_link.SINGLE_LINK, [15], False)

    def testClusteringThreeDimensionalData1LinkAverage(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, type_link.AVERAGE_LINK, [10, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, type_link.AVERAGE_LINK, [20], False)

    def testClusteringThreeDimensionalData1LinkCentroid(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, type_link.CENTROID_LINK, [10, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, type_link.CENTROID_LINK, [20], False)

    def testClusteringThreeDimensionalData1LinkComplete(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, type_link.COMPLETE_LINK, [10, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, type_link.COMPLETE_LINK, [20], False)

    def testClusteringThreeDimensionalData1LinkSingle(self):
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, type_link.SINGLE_LINK, [10, 10], False)
        AgglomerativeTestTemplates.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, type_link.SINGLE_LINK, [20], False)


    def testClusterAllocationOneDimensionDataLinkAverage(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.AVERAGE_LINK, False)

    def testClusterAllocationOneDimensionDataLinkCentroid(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.CENTROID_LINK, False)

    def testClusterAllocationOneDimensionDataLinkComplete(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.COMPLETE_LINK, False)

    def testClusterAllocationOneDimensionDataLinkSingle(self):
        AgglomerativeTestTemplates.templateClusterAllocationOneDimensionData(type_link.SINGLE_LINK, False)


    def testTwoClusterAllocationTheSameObjectsLinkAverage(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.AVERAGE_LINK, False)

    def testTwoClusterAllocationTheSameObjectLinkCentroid(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.CENTROID_LINK, False)

    def testTwoClusterAllocationTheSameObjectLinkComplete(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.COMPLETE_LINK, False)

    def testTwoClusterAllocationTheSameObjectLinkSingle(self):
        AgglomerativeTestTemplates.templateClusterAllocationTheSameObjects(10, 2, type_link.SINGLE_LINK, False)


    def test_incorrect_data(self):
        self.assertRaises(ValueError, agglomerative, [], 1)

    def test_incorrect_amount_clusters(self):
        self.assertRaises(ValueError, agglomerative, [[0], [1], [2]], -1)
        self.assertRaises(ValueError, agglomerative, [[0], [1], [2]], 0)
