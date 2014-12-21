import unittest;

from support.cftree import cfentry;
from support.cftree import measurement_type;

from support import list_math_multiplication;
from support import linear_sum, square_sum;

class Test(unittest.TestCase):
    def templateCfClusterRepresentation(self, cluster, centroid, radius, diameter, tolerance):
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster));
        
        if (type(centroid) == list):
            for dimension in range(0, len(centroid)):
                assert (centroid[dimension] - tolerance < ( entry.get_centroid() )[dimension]) and (( entry.get_centroid() )[dimension] < centroid[dimension] + tolerance);
        else:
            assert (centroid - tolerance < entry.get_centroid()) and (entry.get_centroid() < centroid + tolerance);
        
        assert (radius - tolerance < entry.get_radius()) and (entry.get_radius() < radius + tolerance);
        assert (diameter - tolerance < entry.get_diameter()) and (entry.get_diameter() < diameter + tolerance);
        
    def testCfClusterRepresentationOneDimension(self):
        cluster = [0.1, 0.2, 0.5, 0.4, 0.6];
        self.templateCfClusterRepresentation(cluster, 0.36, 0.18547, 0.29326, 0.0001);
    
    def testCfClusterRepresentationTwoDimension(self):
        cluster = [ [0.1, 0.1], [0.2, 0.2], [0.5, 0.5], [0.4, 0.4], [0.6, 0.6] ];
        self.templateCfClusterRepresentation(cluster, [0.36, 0.36], 0.26230, 0.41473, 0.0001);
    
    
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
        
        
        
if __name__ == "__main__":
    unittest.main();