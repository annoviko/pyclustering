import unittest

from syncnet import syncnet;
from support import read_sample;


class Test(unittest.TestCase):
    def templateClustering(self, file, radius, order):
        sample = read_sample(file);
        network = syncnet(sample);
        network.process(radius, order);
        return network.get_clusters(0.05);
    
    
    def testClusteringSampleSimple1(self):
        clusters = self.templateClustering('../Samples/SampleSimple1.txt', 1, 0.998);
        assert len(clusters) == 2;
        assert sorted([len(cluster) for cluster in clusters]) == [5, 5];
        
        
    def testClusteringSampleSimple2(self):
        clusters = self.templateClustering('../Samples/SampleSimple2.txt', 1, 0.998);
        assert len(clusters) == 3;
        assert sorted([len(cluster) for cluster in clusters]) == [5, 8, 10];

    
    def testClusteringSampleSimple3(self):
        clusters = self.templateClustering('../Samples/SampleSimple3.txt', 1, 0.998);
        assert len(clusters) == 4;
        assert sorted([len(cluster) for cluster in clusters]) == [10, 10, 10, 30];
    
    
    def testClusteringSampleSimple4(self):
        clusters = self.templateClustering('../Samples/SampleSimple4.txt', 0.7, 0.998);
        assert len(clusters) == 5;
        assert sorted([len(cluster) for cluster in clusters]) == [15, 15, 15, 15, 15];        
    
    
    def testClusteringSampleSimple5(self):
        clusters = self.templateClustering('../Samples/SampleSimple5.txt', 1, 0.998);
        assert len(clusters) == 4;
        assert sorted([len(cluster) for cluster in clusters]) == [15, 15, 15, 15];        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()