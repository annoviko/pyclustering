import unittest;

from support.cftree import cfentry;

from support import list_math_multiplication;
from support import linear_sum, square_sum;

class Test(unittest.TestCase):
    def templateCfClusterRepresentation(self, cluster, centroid, radius, diameter, tolerance):
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster));
        print(len(cluster), linear_sum(cluster), square_sum(cluster));
        print(entry.number_points, entry.linear_sum, entry.square_sum);
        
        print(centroid, entry.get_centroid());
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
        
        
if __name__ == "__main__":
    unittest.main();