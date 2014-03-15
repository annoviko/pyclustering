import unittest;

from support import read_sample;
from hsyncnet import hsyncnet;

class Test(unittest.TestCase):
    def templateClusteringResults(self, path, number_clusters, expected_length_clusters):
        sample = read_sample(path);
        network = hsyncnet(sample);
        
        (t, d) = network.process(number_clusters, order = 0.999, collect_dynamic = True);
        clusters = network.get_clusters();
        
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        
        if (sorted([len(cluster) for cluster in clusters]) != expected_length_clusters):
#             print("Result: ", sorted([len(cluster) for cluster in clusters]), "Expect: ", expected_length_clusters);
#             network.show_network();
#             draw_dynamics(t, d);
#             draw_clusters(sample, clusters);
            
            assert sorted([len(cluster) for cluster in clusters]) == expected_length_clusters;
        
    def testClusteringSampleSimple1(self):
        self.templateClusteringResults("../Samples/SampleSimple1.txt", 2, [5, 5]);
        self.templateClusteringResults("../Samples/SampleSimple1.txt", 1, [10]);

    def testClusteringSampleSimple2(self):
        self.templateClusteringResults("../Samples/SampleSimple2.txt", 3, [5, 8, 10]);
        self.templateClusteringResults("../Samples/SampleSimple2.txt", 1, [23]);

    def testClusteringSampleSimple3(self):
        self.templateClusteringResults("../Samples/SampleSimple3.txt", 4, [10, 10, 10, 30]);
        self.templateClusteringResults("../Samples/SampleSimple3.txt", 1, [60]);
        
    def testClusteringSampleSimple4(self):
        self.templateClusteringResults("../Samples/SampleSimple4.txt", 5, [15, 15, 15, 15, 15]);
        self.templateClusteringResults("../Samples/SampleSimple4.txt", 1, [75]);
        
    def testClusteringSampleSimple5(self):
        self.templateClusteringResults("../Samples/SampleSimple5.txt", 4, [15, 15, 15, 15]);
        self.templateClusteringResults("../Samples/SampleSimple5.txt", 1, [60]);        


if __name__ == "__main__":
    unittest.main()