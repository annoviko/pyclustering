import unittest

from syncnet import syncnet;
from support import read_sample;


class Test(unittest.TestCase):
    def templateClustering(self, file, radius, order):
        sample = read_sample(file);
        network = syncnet(sample);
        network.process(radius, order);
        return network.get_clusters(0.05);
    
    def testTwoClusters(self):
        clusters = self.templateClustering('../Samples/SampleSimple1.txt', 1, 0.998);
        assert len(clusters) == 2;
        assert len(clusters[0]) == 5;
        assert len(clusters[1]) == 5;
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()