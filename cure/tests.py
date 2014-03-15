import unittest;

import numpy;

from support import read_sample;

from cure import cure;
from cure import create_queue;

class Test(unittest.TestCase):
    def template_cluster_allocation(self, path, cluster_sizes, number_cluster, number_represent_points = 5, compression = 0.5):
        sample = read_sample(path);
        cure_clusters = cure(sample, number_cluster);

        clusters = [ cure_cluster.points for cure_cluster in cure_clusters ];
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        
        total_length = sum(obtained_cluster_sizes);
        assert total_length == len(sample);
        
        cluster_sizes.sort();
        obtained_cluster_sizes.sort();
        assert cluster_sizes == obtained_cluster_sizes;

    def testClusterAllocationSampleSimple1(self):
        self.template_cluster_allocation('../Samples/SampleSimple1.txt', [5, 5], 2);
    
    def testClusterAllocationSampleSimple2(self):
        self.template_cluster_allocation('../Samples/SampleSimple2.txt', [10, 5, 8], 3);
        
    def testClusterAllocationSampleSimple3(self):
        self.template_cluster_allocation('../Samples/SampleSimple3.txt', [10, 10, 10, 30], 4);
        
    def testClusterAllocationSampleSimple4(self):
        self.template_cluster_allocation('../Samples/SampleSimple4.txt', [15, 15, 15, 15, 15], 5);
        
    def testClusterAllocationSampleSimple5(self):
        self.template_cluster_allocation('../Samples/SampleSimple5.txt', [15, 15, 15, 15], 4);

    def testClusterAllocationSampleTwoDiamonds(self):
        self.template_cluster_allocation('../Samples/SampleTwoDiamonds.txt', [399, 401], 2);

    def testClusterAllocationSampleLsun(self):
        self.template_cluster_allocation('../Samples/SampleLsun.txt', [100, 101, 202], 3);


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
        self.template_queue_creation('../Samples/SampleSimple1.txt');
        self.template_queue_creation('../Samples/SampleSimple2.txt');
        self.template_queue_creation('../Samples/SampleSimple3.txt');
        self.template_queue_creation('../Samples/SampleSimple4.txt');
        self.template_queue_creation('../Samples/SampleSimple5.txt');
        

if __name__ == "__main__":
    unittest.main();