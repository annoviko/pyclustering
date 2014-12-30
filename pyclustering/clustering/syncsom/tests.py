import unittest;

from pyclustering.clustering.syncsom import syncsom;

from pyclustering.support import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

class Test(unittest.TestCase):
    def templateLengthSomCluster(self, file, som_map_size, avg_num_conn, eps):
        sample = read_sample(file);
        network = syncsom(sample, som_map_size[0], som_map_size[1]);   
        network.process(avg_num_conn, collect_dynamic = False, order = eps);
        
        # Check unique
        som_clusters = network.get_som_clusters();
        indexes = set();
        
        for som_cluster in som_clusters:
            for index in som_cluster:
                assert (index in indexes) is False;
                indexes.add(index);    
    
    def testSomClusterAllocationSampleSimple3(self):
        self.templateLengthSomCluster(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 4], 3, 0.999);
        
    def testSomClusterAllocationSampleSimple4(self):
        self.templateLengthSomCluster(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [5, 5], 3, 0.999);
         
    def testSomClusterAllocationSampleSimple5(self):
        self.templateLengthSomCluster(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 4], 3, 0.999);
        
    
    
    def templateLengthProcessData(self, file, som_map_size, avg_num_conn, eps, expected_cluster_length):
        result_testing = False;
        
        # If phases crosses each other because of random part of the network then we should try again.
        for attempt in range(0, 3, 1):
            sample = read_sample(file);
            network = syncsom(sample, som_map_size[0], som_map_size[1]);
            network.process(avg_num_conn, collect_dynamic = False, order = eps);
            
            clusters = network.get_clusters();
            
            obtained_cluster_sizes = [len(cluster) for cluster in clusters];
            if (len(sample) != sum(obtained_cluster_sizes)):
                continue;
            
            obtained_cluster_sizes.sort();
            expected_cluster_length.sort();
            #print(obtained_cluster_sizes, expected_cluster_length);
            if (obtained_cluster_sizes != expected_cluster_length):
                continue;
            
            # Unit-test is passed
            result_testing = True;
            break;
            
        assert result_testing;
       
    def testClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 4, 0.999, [5, 5]);   
        
    def testClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [5, 5], 4, 0.999, [10, 5, 8]);
        
    def testClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [5, 5], 4, 0.999, [10, 10, 10, 30]);
         
    def testClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [7, 7], 5, 0.999, [15, 15, 15, 15]);
        

if __name__ == "__main__":
    unittest.main();