import unittest;

from support.cftree import cfentry, cftree, cfnode;
from support.cftree import measurement_type;

from support import list_math_multiplication;
from support import linear_sum, square_sum;

from random import random;
from math import ceil

class Test(unittest.TestCase):
    def templateCfClusterRepresentation(self, cluster, centroid, radius, diameter, tolerance):
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster));
        
        assertion_centroid = centroid;
        if (type(centroid) != list):
            assertion_centroid = [ centroid ];
        
        if (type(centroid) == list):
            for dimension in range(0, len(assertion_centroid)):
                assert (assertion_centroid[dimension] - tolerance < ( entry.get_centroid() )[dimension]) and (( entry.get_centroid() )[dimension] < assertion_centroid[dimension] + tolerance);
        
        assert (radius - tolerance < entry.get_radius()) and (entry.get_radius() < radius + tolerance);
        assert (diameter - tolerance < entry.get_diameter()) and (entry.get_diameter() < diameter + tolerance);
        
    def testCfClusterRepresentationOneDimension2(self):
        cluster = [ [0.1], [0.2], [0.5], [0.4], [0.6] ];
        self.templateCfClusterRepresentation(cluster, 0.36, 0.18547, 0.29326, 0.0001);        
    
    def testCfClusterRepresentationTwoDimension(self):
        cluster = [ [0.1, 0.1], [0.2, 0.2], [0.5, 0.5], [0.4, 0.4], [0.6, 0.6] ];
        self.templateCfClusterRepresentation(cluster, [0.36, 0.36], 0.26230, 0.41473, 0.0001);
    
    
    def templateCfEntryValueDistance(self, cluster1, cluster2, value, tolerance, type_measurment):
        entry1 = cfentry(len(cluster1), linear_sum(cluster1), square_sum(cluster1));
        entry2 = cfentry(len(cluster2), linear_sum(cluster2), square_sum(cluster2));
        
        distance = entry1.get_distance(entry2, type_measurment);
        assert ( (value - tolerance < distance) and (value + tolerance > distance) );
        
    def testCfEntryTwoPoints1(self):
        self.templateCfEntryValueDistance([[0.0]], [[1.0]], 1.0, 0.0000001, measurement_type.CENTROID_EUCLIDIAN_DISTANCE);

    def testCfEntryTwoPoints2(self):
        self.templateCfEntryValueDistance([[0.0]], [[0.0]], 0.0, 0.0000001, measurement_type.CENTROID_EUCLIDIAN_DISTANCE);
        
    def testCfEntryTwoPoints3(self):
        self.templateCfEntryValueDistance([[-1.0]], [[0.0]], 1.0, 0.0000001, measurement_type.CENTROID_EUCLIDIAN_DISTANCE);
        
    def testCfEntryTwoPoints4(self):
        self.templateCfEntryValueDistance([[1.0, 0.0]], [[0.0, 1.0]], 2.0, 0.0000001, measurement_type.CENTROID_EUCLIDIAN_DISTANCE);
        
    
    def templateCfEntryDistance(self, type_measurement):
        cluster1 = [[0.1, 0.1], [0.1, 0.2], [0.2, 0.1], [0.2, 0.2]];
        cluster2 = [[0.4, 0.4], [0.4, 0.5], [0.5, 0.4], [0.5, 0.5]];
        cluster3 = [[0.9, 0.9], [0.9, 1.0], [1.0, 0.9], [1.0, 1.0]];
        
        entry1 = cfentry(len(cluster1), linear_sum(cluster1), square_sum(cluster1));
        entry2 = cfentry(len(cluster2), linear_sum(cluster2), square_sum(cluster2));
        entry3 = cfentry(len(cluster3), linear_sum(cluster3), square_sum(cluster3));
        
        distance12 = entry1.get_distance(entry2, type_measurement);
        distance23 = entry2.get_distance(entry3, type_measurement);
        distance13 = entry1.get_distance(entry3, type_measurement);
        
        assert distance12 < distance23;
        assert distance23 < distance13;  
    
    def testCfDistanceCentroidEuclidian(self):
        self.templateCfEntryDistance(measurement_type.CENTROID_EUCLIDIAN_DISTANCE);
        
    def testCfDistanceCentroidManhatten(self):
        self.templateCfEntryDistance(measurement_type.CENTROID_MANHATTAN_DISTANCE);
        
    def testCfDistanceAverageInterCluster(self):
        self.templateCfEntryDistance(measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE);

    def testCfDistanceAverageIntraCluster(self):
        self.templateCfEntryDistance(measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE);
        
    def testCfDistanceVarianceIncrease(self):
        self.templateCfEntryDistance(measurement_type.VARIANCE_INCREASE_DISTANCE);
    
    
    
    def testCfTreeCreationWithoutMerging(self):
        clusters = [ [ [random() + j, random() + j] for i in range(10) ] for j in range(10) ];
        tree = cftree(2, 1, 0.0);
        
        for cluster in clusters:
            tree.insert(cluster);
        
        assert tree.height >= 4;
        assert tree.amount_entries == 10;
        assert len(tree.leafes) == 10;
        
    def testCfTreeInserionOneLeafThreeEntries(self):
        cluster1 = [[0.1, 0.1], [0.1, 0.2], [0.2, 0.1], [0.2, 0.2]];
        cluster2 = [[0.4, 0.4], [0.4, 0.5], [0.5, 0.4], [0.5, 0.5]];
        cluster3 = [[0.9, 0.9], [0.9, 1.0], [1.0, 0.9], [1.0, 1.0]];
         
        tree = cftree(3, 4, 0.0);
        tree.insert(cluster1);
        tree.insert(cluster2);
        tree.insert(cluster3);
         
        entry1 = cfentry(len(cluster1), linear_sum(cluster1), square_sum(cluster1));
        entry2 = cfentry(len(cluster2), linear_sum(cluster2), square_sum(cluster2));
        entry3 = cfentry(len(cluster3), linear_sum(cluster3), square_sum(cluster3));
         
        assert tree.find_nearest_leaf(entry1) == tree.find_nearest_leaf(entry2);
        assert tree.find_nearest_leaf(entry2) == tree.find_nearest_leaf(entry3);
    
    
    def templateCfTreeLeafIntegrity(self, number_clusters, branching_factor, max_entries, threshold):
        clusters = [ [ [random() + j, random() + j] for i in range(10) ] for j in range(number_clusters) ];
        tree = cftree(branching_factor, max_entries, threshold);
        
        for index_cluster in range(0, len(clusters)):
            tree.insert(clusters[index_cluster]);
            
            result_searching = False;
            for leaf in tree.leafes:
                for node_entry in leaf.entries:
                    result_searching |= (node_entry == node_entry);
    
            assert True == result_searching;
                
    def testCfTreeLeafIntegrity10_2_1(self):
        self.templateCfTreeLeafIntegrity(10, 2, 1, 0.0);
         
    def testCfTreeLeafIntegrity10_3_1(self):
        self.templateCfTreeLeafIntegrity(10, 3, 1, 0.0);
         
    def testCfTreeLeafIntegrity20_4_1(self):
        self.templateCfTreeLeafIntegrity(20, 4, 1, 0.0);
    
    def testCfTreeLeafIntegrity20_4_2(self):
        self.templateCfTreeLeafIntegrity(20, 4, 2, 0.0);
        
    def testCfTreeLeafIntegrity40_10_5(self):
        self.templateCfTreeLeafIntegrity(40, 10, 5, 0.0);
        
        
if __name__ == "__main__":
    unittest.main();