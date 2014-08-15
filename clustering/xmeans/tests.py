import unittest;

from clustering.xmeans import xmeans;

from support import read_sample;

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

class Test(unittest.TestCase):
    def templateLengthProcessData(self, path_to_file, start_centers, expected_cluster_length, ccore = False):
        sample = read_sample(path_to_file);
        clusters = xmeans(sample, start_centers, 20, ccore);
    
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        assert len(sample) == sum(obtained_cluster_sizes);
        
        obtained_cluster_sizes.sort();
        expected_cluster_length.sort();
        assert obtained_cluster_sizes == expected_cluster_length;
    
    def testClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5]);
        
    def testWrongStartClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5]);

    def testClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8]);

    def testWrongStartClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8]);

    def testClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30]);    

    def testWrongStartClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30]); 

    def testClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15]);

    def testWrongStartClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15]);

    def testClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15]);
        
    def testWrongStartClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15]);

    def testClusterAllocationSampleTwoDiamonds(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400]);

    def testWrongStartClusterAllocationSampleTwoDiamonds(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2]], [400, 400]);
    
    def testClusterAllocationByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], True);
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400], True);
        
    def testWrongStartClusterAllocationByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], True);
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2]], [400, 400], True);


if __name__ == "__main__":
    unittest.main();