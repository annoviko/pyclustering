"""!

@brief Unit-tests for agglomerative algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2015
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

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.cluster.agglomerative import agglomerative, type_link;
from pyclustering.utils import read_sample;

from random import random;

class Test(unittest.TestCase):
    def templateClusteringResults(self, path, number_clusters, link, expected_length_clusters):
        sample = read_sample(path);
        
        agglomerative_instance = agglomerative(sample, number_clusters, link);
        agglomerative_instance.process();
        
        clusters = agglomerative_instance.get_clusters();
        
        assert sum([len(cluster) for cluster in clusters]) == len(sample);
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        assert sorted([len(cluster) for cluster in clusters]) == expected_length_clusters;
    
    def testClusteringSampleSimple1LinkAverage(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.AVERAGE_LINK, [5, 5]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.AVERAGE_LINK, [10]);
        
    def testClusteringSampleSimple1LinkCentroid(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.CENTROID_LINK, [5, 5]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.CENTROID_LINK, [10]);

    def testClusteringSampleSimple1LinkComplete(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.COMPLETE_LINK, [5, 5]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.COMPLETE_LINK, [10]);
        
    def testClusteringSampleSimple1LinkSingle(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, type_link.SINGLE_LINK, [5, 5]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, type_link.SINGLE_LINK, [10]);

    def testClusteringSampleSimple2LinkAverage(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.AVERAGE_LINK, [5, 8, 10]);        
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.AVERAGE_LINK, [23]);

    def testClusteringSampleSimple2LinkCentroid(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.CENTROID_LINK, [5, 8, 10]);        
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.CENTROID_LINK, [23]);
        
    def testClusteringSampleSimple2LinkComplete(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.COMPLETE_LINK, [5, 8, 10]);        
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.COMPLETE_LINK, [23]);
        
    def testClusteringSampleSimple2LinkSingle(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, type_link.SINGLE_LINK, [5, 8, 10]);        
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, type_link.SINGLE_LINK, [23]);

    def testClusteringSampleSimple3LinkAverage(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.AVERAGE_LINK, [10, 10, 10, 30]);        
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.AVERAGE_LINK, [60]);
        
    def testClusteringSampleSimple3LinkCentroid(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.CENTROID_LINK, [10, 10, 10, 30]);        
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.CENTROID_LINK, [60]);
        
    def testClusteringSampleSimple3LinkComplete(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.COMPLETE_LINK, [10, 10, 10, 30]);        
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.COMPLETE_LINK, [60]);
        
    def testClusteringSampleSimple3LinkSingle(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, type_link.SINGLE_LINK, [10, 10, 10, 30]);        
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, type_link.SINGLE_LINK, [60]);
        
    def testClusteringSampleSimple4LinkAverage(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.AVERAGE_LINK, [15, 15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.AVERAGE_LINK, [75]);
        
    def testClusteringSampleSimple4LinkCentroid(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.CENTROID_LINK, [15, 15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.CENTROID_LINK, [75]);
        
    def testClusteringSampleSimple4LinkComplete(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.COMPLETE_LINK, [15, 15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.COMPLETE_LINK, [75]);
        
    def testClusteringSampleSimple4LinkSingle(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, type_link.SINGLE_LINK, [15, 15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, type_link.SINGLE_LINK, [75]);
        
    def testClusteringSampleSimple5LinkAverage(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.AVERAGE_LINK, [15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.AVERAGE_LINK, [60]);
        
    def testClusteringSampleSimple5LinkCentroid(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.CENTROID_LINK, [15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.CENTROID_LINK, [60]); 
        
    def testClusteringSampleSimple5LinkComplete(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.COMPLETE_LINK, [15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.COMPLETE_LINK, [60]); 
        
    def testClusteringSampleSimple5LinkSingle(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, type_link.SINGLE_LINK, [15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, type_link.SINGLE_LINK, [60]); 
        
    
    def templateClusterAllocationOneDimensionData(self, link):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ];
        
        agglomerative_instance = agglomerative(input_data, 4, link);
        agglomerative_instance.process();
        clusters = agglomerative_instance.get_clusters();
        
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;
                
    def testClusterAllocationOneDimensionDataLinkAverage(self):
        self.templateClusterAllocationOneDimensionData(type_link.AVERAGE_LINK);

    def testClusterAllocationOneDimensionDataLinkCentroid(self):
        self.templateClusterAllocationOneDimensionData(type_link.CENTROID_LINK);
        
    def testClusterAllocationOneDimensionDataLinkComplete(self):
        self.templateClusterAllocationOneDimensionData(type_link.COMPLETE_LINK);
        
    def testClusterAllocationOneDimensionDataLinkSingle(self):
        self.templateClusterAllocationOneDimensionData(type_link.SINGLE_LINK);

if __name__ == "__main__":
    unittest.main();