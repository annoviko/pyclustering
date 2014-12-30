import unittest;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from pyclustering.support import read_sample;
from pyclustering.support.cftree import measurement_type;

from pyclustering.clustering.birch import birch;


class Test(unittest.TestCase):
    def templateClusterAllocation(self, path, cluster_sizes, number_clusters, branching_factor = 5, max_node_entries = 5, initial_diameter = 0.1, type_measurement = measurement_type.CENTROID_EUCLIDIAN_DISTANCE, entry_size_limit = 200, ccore = True):
        sample = read_sample(path);
        
        cure_instance = birch(sample, number_clusters, branching_factor, max_node_entries, initial_diameter, type_measurement, entry_size_limit, ccore);
        cure_instance.process();
        clusters = cure_instance.get_clusters();

        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        
        total_length = sum(obtained_cluster_sizes);
        assert total_length == len(sample);
        
        cluster_sizes.sort();
        obtained_cluster_sizes.sort();
        assert cluster_sizes == obtained_cluster_sizes;
        
    def testClusterAllocationSampleSimple1(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2);
    
    def testClusterAllocationSampleSimple2(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3);
        
    def testClusterAllocationSampleSimple3(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4);
        
    def testClusterAllocationSampleSimple4(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [15, 15, 15, 15, 15], 5);
        
    def testClusterAllocationSampleSimple5(self):
        self.templateClusterAllocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [15, 15, 15, 15], 4);


if __name__ == "__main__":
    unittest.main();