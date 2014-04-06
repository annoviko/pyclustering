import unittest;

from nnet.sync import initial_type;

from support import read_sample;

from hsyncnet import hsyncnet;

from samples.definitions import SIMPLE_SAMPLES;

class Test(unittest.TestCase):
    def templateClusteringResults(self, path, number_clusters, expected_length_clusters):
        sample = read_sample(path);
        network = hsyncnet(sample, initial_type.EQUIPARTITION); # EQUIPARTITION - makes test more stable.
        
        (t, d) = network.process(number_clusters, order = 0.998, collect_dynamic = True);
        clusters = network.get_clusters();
        
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        
        if (sorted([len(cluster) for cluster in clusters]) != expected_length_clusters):
            assert sorted([len(cluster) for cluster in clusters]) == expected_length_clusters;
        
    def testClusteringSampleSimple1(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10]);

    def testClusteringSampleSimple2(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [5, 8, 10]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23]);

    def testClusteringSampleSimple3(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [10, 10, 10, 30]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, [60]);
        
    def testClusteringSampleSimple4(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, [15, 15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, [75]);
        
    def testClusteringSampleSimple5(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, [15, 15, 15, 15]);
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, [60]);        


if __name__ == "__main__":
    unittest.main()