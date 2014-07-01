import unittest;

import support;

import clustering.dbscan as dbscan;

from samples.definitions import SIMPLE_SAMPLES;
from samples.definitions import FCPS_SAMPLES;

class Test(unittest.TestCase):  
        
    def testNeighborIndexes(self):
        # Tests for neighbor_indexes
        data = [[1, 2], [1, 3], [4, 6]];
        assert dbscan.neighbor_indexes(data, 0, 0.5) == [];
        assert dbscan.neighbor_indexes(data, 0, 1) == [1];
        assert dbscan.neighbor_indexes(data, 0, 6) == [1, 2];
    
        
    def testExpandCluster(self):
        data = [[0, 0], [0, 1], [1, 0], [1, 1], [3, 5]];
        visited = [False] * len(data);
        belong = [False] * len(data);
        
        # Tests for expand_cluster
        cluster = dbscan.expand_cluster(data, visited, belong, 0, 1.5, 3);
        cluster.sort();
        assert cluster == [0, 1, 2, 3];
        
        visited = [False] * len(data);
        belong = [False] * len(data);
        cluster = dbscan.expand_cluster(data, visited, belong, 2, 1.5, 3);
        cluster.sort();
        assert cluster == [0, 1, 2, 3];
        
        data = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2]];
        visited = [False] * len(data);
        belong = [False] * len(data);
        cluster = dbscan.expand_cluster(data, visited, belong, 2, 1.5, 3);
        cluster.sort();
        assert cluster == [0, 1, 2, 3, 4];
        
        data = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [0, 5], [1, 5], [0, 6], [1, 6]];
        visited = [False] * len(data);   
        belong = [False] * len(data);
        cluster = dbscan.expand_cluster(data, visited, belong, 0, 1.5, 3);
        cluster.sort();
        assert cluster == [0, 1, 2, 3, 4, 5];
        
        cluster = dbscan.expand_cluster(data, visited, belong, 9, 1.5, 3);
        cluster.sort();
        assert cluster == [6, 7, 8, 9, 10];     # without [5] because it should be included to another cluster in previous call.

        
    def testClustering(self):
        data = [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [0, 5], [1, 5], [0, 6], [1, 6]];
        
        clusters = dbscan.dbscan(data, 1.5, 3);
        assert len(clusters) == 2;
        [cluster.sort() for cluster in clusters];
        assert (clusters[0] == [0, 1, 2, 3, 4, 5] and clusters[1] == [6, 7, 8, 9, 10]);
        
        clusters = dbscan.dbscan(data, 0.5, 3);
        assert len(clusters) == 0;
        
        clusters = dbscan.dbscan(data, 3, 3);
        assert len(clusters) == 1;
        [cluster.sort() for cluster in clusters];
        assert (clusters[0] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
        
        data = [[0, 0], [0, 1], [1, 0], [1, 1], [5, 5], [5, 6], [6, 5], [6, 6], [9, 0], [9, 1], [10, 0], [10, 1]];
        clusters = dbscan.dbscan(data, 1.5, 3);
        assert len(clusters) == 3;
        [cluster.sort() for cluster in clusters];
        assert (clusters[0] == [0, 1, 2, 3] and clusters[1] == [4, 5, 6, 7] and clusters[2] == [8, 9, 10, 11]);


    def templateLengthProcessData(self, path_to_file, radius, min_number_neighbors, max_number_neighbors, ccore = False):
        for number_neighbors in range(min_number_neighbors, max_number_neighbors, 1):
            sample = support.read_sample(path_to_file);
            (clusters, noise) = dbscan.dbscan(sample, radius, number_neighbors, True, ccore);
            
            length = len(noise);
            length += sum([len(cluster) for cluster in clusters]);
        
            assert len(sample) == length;


    def testLengthProcessedSampleSimple1(self):    
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.7, 0, 10);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.7, 0, 10, True);     
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 0, 10); 
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 0, 10, True);

    def testLengthProcessedSampleSimple2(self):    
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.3, 0, 15);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.3, 0, 15, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0, 15);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0, 15, True);
        
    def testLengthProcessedSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.1, 0, 20);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.1, 0, 20, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0, 20);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0, 20, True);
        
    def testLengthProcessedSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.1, 0, 10);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.1, 0, 10, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 65, 75);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 65, 75, True);
    
    def testLengthProcessedSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.1, 0, 10);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.1, 0, 10, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.3, 0, 10);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.3, 0, 10, True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.6, 0, 10);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.6, 0, 10, True);
        
    
    def testResultDataClusteringSample1(self):
        sample = support.read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
        (clusters, noise) = dbscan.dbscan(sample, 0.5, 3, True);
        
        assert noise == [];
        assert sorted(clusters[0]) == [0, 1, 2, 3, 4];
        assert sorted(clusters[1]) == [5, 6, 7, 8, 9];
        
    
    def testResultDataClusteringSample2(self):
        sample = support.read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        (clusters, noise) = dbscan.dbscan(sample, 0.7, 3, True);
        
        assert noise == [];
        assert sorted(clusters[0]) == [i for i in range(0, 10)];
        assert sorted(clusters[1]) == [i for i in range(10, 15)];
        assert sorted(clusters[2]) == [i for i in range(15, 23)];
        
        
    def testResultDataClusteringHepta(self):
        sample = support.read_sample(FCPS_SAMPLES.SAMPLE_HEPTA);
        (clusters, noise) = dbscan.dbscan(sample, 1, 3, True);
        
        assert noise == [];
        
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        total_length = sum(obtained_cluster_sizes);
        assert total_length == len(sample);
        
        obtained_cluster_sizes.sort();
        
        assert obtained_cluster_sizes == [30, 30, 30, 30, 30, 30, 32]; 


if __name__ == "__main__":
    unittest.main();