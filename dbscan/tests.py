import unittest;
import dbscan;
import support;

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


    def templateLengthProcessData(self, path_to_file, radius, min_number_neighbors, max_number_neighbors):
        for number_neighbors in range(min_number_neighbors, max_number_neighbors, 1):
            sample = support.read_sample(path_to_file);
            (clusters, noise) = dbscan.dbscan(sample, radius, number_neighbors, False, True);
            
            length = len(noise);
            length += sum([len(cluster) for cluster in clusters]);
        
            assert len(sample) == length;


    def testLengthProcessedSampleSimple1(self):    
        self.templateLengthProcessData('../samples/SampleSimple1.txt', 0.7, 0, 10);       
        self.templateLengthProcessData('../samples/SampleSimple1.txt', 0.5, 0, 10); 

    def testLengthProcessedSampleSimple2(self):    
        self.templateLengthProcessData('../samples/SampleSimple2.txt', 0.3, 0, 15);
        self.templateLengthProcessData('../samples/SampleSimple2.txt', 1, 0, 15);
        
    def testLengthProcessedSampleSimple3(self):
        self.templateLengthProcessData('../samples/SampleSimple3.txt', 0.1, 0, 20);
        self.templateLengthProcessData('../samples/SampleSimple3.txt', 5, 0, 20);
        
    def testLengthProcessedSampleSimple4(self):
        self.templateLengthProcessData('../samples/SampleSimple4.txt', 0.1, 0, 10);
        self.templateLengthProcessData('../samples/SampleSimple4.txt', 10, 65, 75);
    
    def testLengthProcessedSampleSimple5(self):
        self.templateLengthProcessData('../samples/SampleSimple5.txt', 0.1, 0, 10);
        self.templateLengthProcessData('../samples/SampleSimple5.txt', 0.3, 0, 10);
        self.templateLengthProcessData('../samples/SampleSimple5.txt', 0.6, 0, 10);
        
    
    def testResultDataClusteringSample1(self):
        sample = support.read_sample('../samples/SampleSimple1.txt');
        (clusters, noise) = dbscan.dbscan(sample, 0.5, 3, False, True);
        
        assert noise == [];
        assert sorted(clusters[0]) == [0, 1, 2, 3, 4];
        assert sorted(clusters[1]) == [5, 6, 7, 8, 9];
        
    
    def testResultDataClusteringSample2(self):
        sample = support.read_sample('../samples/SampleSimple2.txt');
        (clusters, noise) = dbscan.dbscan(sample, 0.7, 3, False, True);
        
        assert noise == [];
        assert sorted(clusters[0]) == [i for i in range(0, 10)];
        assert sorted(clusters[1]) == [i for i in range(10, 15)];
        assert sorted(clusters[2]) == [i for i in range(15, 23)];
        


if __name__ == "__main__":
    unittest.main()