import unittest;

import support;

from clustering.dbscan import dbscan;

from samples.definitions import SIMPLE_SAMPLES;
from samples.definitions import FCPS_SAMPLES;

class Test(unittest.TestCase):  
    def templateClusteringResults(self, path, radius, neighbors, expected_length_clusters, ccore = False):
        sample = support.read_sample(path);
        
        dbscan_instance = dbscan(sample, radius, neighbors, ccore);
        dbscan_instance.process();
        
        clusters = dbscan_instance.get_clusters();
        noise = dbscan_instance.get_noise();
        
        assert sum([len(cluster) for cluster in clusters]) + len(noise) == len(sample);
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        assert sorted([len(cluster) for cluster in clusters]) == expected_length_clusters;
    
    
    def testClusteringSampleSimple1(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], False);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 2, [10], False);
    
    def testClusteringSampleSimple2(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, [5, 8, 10], False);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 2, [23], False);

    def testClusteringSampleSimple3(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, [10, 10, 10, 30], False);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 3, [60], False);
        
    def testClusteringSampleSimple4(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, [15, 15, 15, 15, 15], False);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 2, 3, [75], False);

    def testClusteringSampleSimple5(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, [15, 15, 15, 15], False);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 10, 3, [60], False);
        
    def testClusteringHepta(self):
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3, [30, 30, 30, 30, 30, 30, 32], False);
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 5, 3, [212], False);

    def testClusteringByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], True);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 2, [10], True);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, [5, 8, 10], True);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 2, [23], True);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, [10, 10, 10, 30], True);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 3, [60], True);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, [15, 15, 15, 15, 15], True);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 2, 3, [75], True);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, [15, 15, 15, 15], True);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 10, 3, [60], True);        
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3, [30, 30, 30, 30, 30, 30, 32], True);
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 5, 3, [212], True);
                
        
    def templateLengthProcessData(self, path_to_file, radius, min_number_neighbors, max_number_neighbors, ccore = False):
        for number_neighbors in range(min_number_neighbors, max_number_neighbors, 1):
            sample = support.read_sample(path_to_file);
            
            dbscan_instance = dbscan(sample, radius, min_number_neighbors, ccore);
            dbscan_instance.process();
            
            clusters = dbscan_instance.get_clusters();
            noise = dbscan_instance.get_noise();
            
            length = len(noise);
            length += sum([len(cluster) for cluster in clusters]);
        
            assert len(sample) == length;

    def testLengthProcessedSampleSimple1(self):    
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.7, 0, 10);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 0, 10); 
        
    def testLengthProcessedSampleSimple2(self):    
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.3, 0, 15);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0, 15);
        
    def testLengthProcessedSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.1, 0, 20);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0, 20);
        
    def testLengthProcessedSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.1, 0, 10);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 65, 75);
    
    def testLengthProcessedSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.1, 0, 10);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.3, 0, 10);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.6, 0, 10);
        
    def testLengthProcessedByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.7, 0, 10, True);  
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 0, 10, True); 
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.3, 0, 15, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0, 15, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.1, 0, 20, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0, 20, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.1, 0, 10, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 65, 75, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.1, 0, 10, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.3, 0, 10, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.6, 0, 10, True);


if __name__ == "__main__":
    unittest.main();