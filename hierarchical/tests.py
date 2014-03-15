import unittest;

from hierarchical import hierarchical;
from support import read_sample;

class Test(unittest.TestCase):
    def templateClusteringResults(self, path, number_clusters, expected_length_clusters):
        sample = read_sample(path);
        clusters = hierarchical(sample, number_clusters);
        
        assert sum([len(cluster) for cluster in clusters]) == len(sample);
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        assert sorted([len(cluster) for cluster in clusters]) == expected_length_clusters;
    
    def testClusteringSampleSimple1(self):
        self.templateClusteringResults("../samples/SampleSimple1.txt", 2, [5, 5]);
        self.templateClusteringResults("../samples/SampleSimple1.txt", 1, [10]);

    def testClusteringSampleSimple2(self):
        self.templateClusteringResults("../samples/SampleSimple2.txt", 3, [5, 8, 10]);
        self.templateClusteringResults("../samples/SampleSimple2.txt", 1, [23]);

    def testClusteringSampleSimple3(self):
        self.templateClusteringResults("../samples/SampleSimple3.txt", 4, [10, 10, 10, 30]);
        self.templateClusteringResults("../samples/SampleSimple3.txt", 1, [60]);
        
    def testClusteringSampleSimple4(self):
        self.templateClusteringResults("../samples/SampleSimple4.txt", 5, [15, 15, 15, 15, 15]);
        self.templateClusteringResults("../samples/SampleSimple4.txt", 1, [75]);
        
    def testClusteringSampleSimple5(self):
        self.templateClusteringResults("../samples/SampleSimple5.txt", 4, [15, 15, 15, 15]);
        self.templateClusteringResults("../samples/SampleSimple5.txt", 1, [60]);    
        
    def testClusteringHepta(self):
        self.templateClusteringResults("../samples/SampleHepta.txt", 7, [30, 30, 30, 30, 30, 30, 32]);
        self.templateClusteringResults("../samples/SampleHepta.txt", 1, [212]);    


if __name__ == "__main__":
    unittest.main();
