import unittest

from syncnet import syncnet;
from support import read_sample;
from numpy import pi;

class Test(unittest.TestCase):
    def templateClustering(self, file, radius, order):
        sample = read_sample(file);
        network = syncnet(sample);
        network.process(radius, order);
        return network.get_clusters(0.05);
    
    
    def testClusteringSampleSimple1(self):
        clusters = self.templateClustering('../Samples/SampleSimple1.txt', 1, 0.998);
        assert len(clusters) == 2;
        assert sum([len(cluster) for cluster in clusters]) == 10;
        assert sorted([len(cluster) for cluster in clusters]) == [5, 5];
        
        
    def testClusteringSampleSimple2(self):
        clusters = self.templateClustering('../Samples/SampleSimple2.txt', 1, 0.998);
        assert len(clusters) == 3;
        assert sum([len(cluster) for cluster in clusters]) == 23;
        assert sorted([len(cluster) for cluster in clusters]) == [5, 8, 10];

    
    def testClusteringSampleSimple3(self):
        clusters = self.templateClustering('../Samples/SampleSimple3.txt', 1, 0.998);
        assert len(clusters) == 4;
        assert sum([len(cluster) for cluster in clusters]) == 60;
        assert sorted([len(cluster) for cluster in clusters]) == [10, 10, 10, 30];
    
    
    def testClusteringSampleSimple4(self):
        clusters = self.templateClustering('../Samples/SampleSimple4.txt', 0.7, 0.998);
        assert len(clusters) == 5;
        assert sum([len(cluster) for cluster in clusters]) == 75;
        assert sorted([len(cluster) for cluster in clusters]) == [15, 15, 15, 15, 15];        
    
    
    def testClusteringSampleSimple5(self):
        clusters = self.templateClustering('../Samples/SampleSimple5.txt', 1, 0.998);
        assert len(clusters) == 4;
        assert sum([len(cluster) for cluster in clusters]) == 60;
        assert sorted([len(cluster) for cluster in clusters]) == [15, 15, 15, 15];    
        
    
    def templateClusterAllocationHighTolerance(self, file, radius, order):
        sample = read_sample(file);
        network = syncnet(sample);
        network.process(radius, order);
        clusters = network.get_clusters(2 * pi);
        
        assert sum([len(cluster) for cluster in clusters]) == network.num_osc;
                
    
    def testClusterAllocationHighToleranceSampleSimple1(self):
        self.templateClusterAllocationHighTolerance('../Samples/SampleSimple1.txt', 1, 0.998);
        
        
    def testClusterAllocationHighToleranceSampleSimple2(self):
        self.templateClusterAllocationHighTolerance('../Samples/SampleSimple2.txt', 1, 0.998);
        
        
    def testClusterAllocationHighToleranceSampleSimple3(self):
        self.templateClusterAllocationHighTolerance('../Samples/SampleSimple3.txt', 1, 0.998);
    
    
    def testClusterAllocationHighToleranceSampleSimple4(self):
        self.templateClusterAllocationHighTolerance('../Samples/SampleSimple4.txt', 0.7, 0.998);
    
    
    def testClusterAllocationHighToleranceSampleSimple5(self):
        self.templateClusterAllocationHighTolerance('../Samples/SampleSimple5.txt', 1, 0.998);
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()