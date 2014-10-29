import unittest;

from clustering.kmeans import kmeans;

from support import read_sample;

from samples.definitions import SIMPLE_SAMPLES;

class Test(unittest.TestCase):
    def templateLengthProcessData(self, path_to_file, start_centers, expected_cluster_length, ccore = False):
        sample = read_sample(path_to_file);
        clusters = kmeans(sample, start_centers, 0.025, ccore);
    
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        assert len(sample) == sum(obtained_cluster_sizes);
        
        obtained_cluster_sizes.sort();
        expected_cluster_length.sort();
        assert obtained_cluster_sizes == expected_cluster_length;
    
    def testClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5]);
        
    def testClusterOneAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10]);

    def testClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8]);

    def testClusterOneAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23]);

    def testClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30]);    

    def testClusterOneAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60]);   

    def testClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15]);

    def testClusterOneAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[2.0, 5.0]], [75]);   

    def testClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15]);
  
    def testClusterOneAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60]);   
        
    def testClusterAllocationByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], True);
    
    def testClusterOneAllocationByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[2.0, 5.0]], [75], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60], True);
            
    
    def testDifferentDimensions(self):
        self.assertRaises(NameError, kmeans, [ [0, 1, 5], [0, 2, 3] ], [ [0, 3] ]);
        self.assertRaises(NameError, kmeans, [ [0, 1, 5, 2], [0, 2, 3, 7] ], [ [0] ]);


if __name__ == "__main__":
    unittest.main();
