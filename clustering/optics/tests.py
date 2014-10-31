import unittest;

from clustering.optics import optics;

from support import read_sample;

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

class Test(unittest.TestCase):
    def templateClusteringResults(self, path, radius, neighbors, expected_length_clusters, ccore):
        sample = read_sample(path);
        
        optics_instance = optics(sample, radius, neighbors);
        optics_instance.process();
        
        clusters = optics_instance.get_clusters();
        noise = optics_instance.get_noise();
        
        assert sum([len(cluster) for cluster in clusters]) + len(noise) == len(sample);
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        assert sorted([len(cluster) for cluster in clusters]) == expected_length_clusters;
    
    def testClusteringSampleSimple1(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], False);
    
    def testClusteringSampleSimple2(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, [5, 8, 10], False);

    def testClusteringSampleSimple3(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, [10, 10, 10, 30], False);
        
    def testClusteringSampleSimple4(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, [15, 15, 15, 15, 15], False);

    def testClusteringSampleSimple5(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, [15, 15, 15, 15], False);
        
    def testClusteringHepta(self):
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3, [30, 30, 30, 30, 30, 30, 32], False); 
    
    
if __name__ == "__main__":
    unittest.main();