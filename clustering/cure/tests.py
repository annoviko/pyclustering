import unittest;

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from support import read_sample;

from clustering.cure import cure;
from clustering.cure import create_queue;

class Test(unittest.TestCase):
    def template_cluster_allocation(self, path, cluster_sizes, number_cluster, number_represent_points = 5, compression = 0.5, ccore_flag = False):
        sample = read_sample(path);
        clusters = cure(sample, number_cluster, ccore = ccore_flag);

        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        
        total_length = sum(obtained_cluster_sizes);
        assert total_length == len(sample);
        
        cluster_sizes.sort();
        obtained_cluster_sizes.sort();
        assert cluster_sizes == obtained_cluster_sizes;

    def testClusterAllocationSampleSimple1(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 2);
    
    def testClusterAllocationSampleSimple2(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10, 5, 8], 3);
        
    def testClusterAllocationSampleSimple3(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [10, 10, 10, 30], 4);
        
    def testClusterAllocationSampleSimple4(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [15, 15, 15, 15, 15], 5);
        
    def testClusterAllocationSampleSimple5(self):
        self.template_cluster_allocation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [15, 15, 15, 15], 4);

    def testClusterAllocationSampleTwoDiamonds(self):
        self.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [399, 401], 2);

    def testClusterAllocationSampleLsun(self):
        self.template_cluster_allocation(FCPS_SAMPLES.SAMPLE_LSUN, [100, 101, 202], 3);


    def template_queue_creation(self, path):
        sample = read_sample(path);
        queue = create_queue(sample);
        
        cursor_distance = 0;
        for cluster in queue:
            assert cluster.points != None;
            assert len(cluster.points) == 1;
            assert cluster.mean == cluster.points[0];
            assert cluster.rep != None;
            assert cluster.rep == cluster.points;
            assert cluster.closest != None;
            assert cluster.closest is not cluster;
            assert cluster.closest in queue;
            assert cluster.distance >= cursor_distance;
            
            cursor_distance = cluster.distance;

    def testCreateQueue(self):
        self.template_queue_creation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
        self.template_queue_creation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        self.template_queue_creation(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
        self.template_queue_creation(SIMPLE_SAMPLES.SAMPLE_SIMPLE4);
        self.template_queue_creation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5);
        

if __name__ == "__main__":
    unittest.main();