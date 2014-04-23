import unittest

from nnet.sync import initial_type, conn_represent;

from syncnet import syncnet;

from support import read_sample;

from numpy import pi;

from samples.definitions import SIMPLE_SAMPLES;


class Test(unittest.TestCase):
    def templateClustering(self, file, radius, order, connection_representation, expected_cluster_length):
        sample = read_sample(file);
        network = syncnet(sample, initial_phases = initial_type.EQUIPARTITION, conn_repr = connection_representation); # EQUIPARTITION - makes test more stable.
        network.process(radius, order);
        
        clusters = network.get_clusters(0.05);
        
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        
        assert len(obtained_cluster_sizes) == len(expected_cluster_length);
        
        obtained_cluster_sizes.sort();
        expected_cluster_length.sort();
        
        assert obtained_cluster_sizes == expected_cluster_length;
        
    
    def testClusteringSampleSimple1(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.998, conn_represent.MATRIX, [5, 5]);
        
    
    def testClusteringSampleSimple1ListRepr(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.998, conn_represent.LIST, [5, 5]);
        
        
    def testClusteringSampleSimple2(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.998, conn_represent.MATRIX, [5, 8, 10]);
        
    
    def testClusteringSampleSimple2ListRepr(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.998, conn_represent.LIST, [5, 8, 10]);     

    
    def testClusteringSampleSimple3(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.998, conn_represent.MATRIX, [10, 10, 10, 30]);
 
 
    def testClusteringSampleSimple3ListRepr(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.998, conn_represent.LIST, [10, 10, 10, 30]);
    
    
    def testClusteringSampleSimple4(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0.998, conn_represent.MATRIX, [15, 15, 15, 15, 15]); 
    
    
    def testClusteringSampleSimple5(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0.998, conn_represent.MATRIX, [15, 15, 15, 15]);
        
        
    
    def templateClusterAllocationHighTolerance(self, file, radius, order):
        sample = read_sample(file);
        network = syncnet(sample);
        network.process(radius, order);
        clusters = network.get_clusters(2 * pi);
        
        assert sum([len(cluster) for cluster in clusters]) == network.num_osc;
                
    
    def testClusterAllocationHighToleranceSampleSimple1(self):
        self.templateClusterAllocationHighTolerance(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.998);
        
        
    def testClusterAllocationHighToleranceSampleSimple2(self):
        self.templateClusterAllocationHighTolerance(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.998);
        
        
    def testClusterAllocationHighToleranceSampleSimple3(self):
        self.templateClusterAllocationHighTolerance(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.998);
    
    
    def testClusterAllocationHighToleranceSampleSimple4(self):
        self.templateClusterAllocationHighTolerance(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 0.998);
    
    
    def testClusterAllocationHighToleranceSampleSimple5(self):
        self.templateClusterAllocationHighTolerance(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0.998);



    def templateClusterAllocationConnWeights(self, file, radius, order, expected_cluster_length):
        sample = read_sample(file);
        network = syncnet(sample, enable_conn_weight = True);
        network.process(radius, order);
        
        clusters = network.get_clusters(0.05);
        
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        
        assert len(obtained_cluster_sizes) == len(expected_cluster_length);
        
        obtained_cluster_sizes.sort();
        expected_cluster_length.sort();
        
        assert obtained_cluster_sizes == expected_cluster_length;
        
    def testClusterAllocationConnWeightSampleSimple1(self):
        self.templateClusterAllocationConnWeights(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 0.998, [5, 5]);
        self.templateClusterAllocationConnWeights(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 0.998, [10]);
    
    def testClusterAllocationConnWeightSampleSimple2(self):
        self.templateClusterAllocationConnWeights(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, 0.998, [5, 8, 10]);
        self.templateClusterAllocationConnWeights(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 10, 0.998, [23]);
    
if __name__ == "__main__":
    unittest.main()