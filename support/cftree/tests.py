import unittest;

from support.cftree import cfentry;

from support import list_math_multiplication;
from support import linear_sum, square_sum;

class Test(unittest.TestCase):
    def templateCfClusterRepresentation(self, cluster, centroid, radius, diameter, tolerance):
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster));
        
        assert centroid == entry.get_centroid();
        assert radius - tolerance < entry.get_radius() < radius + tolerance;
        assert diameter - tolerance < entry.get_diameter() < diameter + tolerance;
        
    def testCfClusterRepresentationOneDimension(self):
        cluster = [0.1, 0.2, 0.5, 0.4, 0.6];
        self.templateCfClusterRepresentation(cluster, 0.36, 0.18547, 0.29326, 0.0001);
        
        
if __name__ == "__main__":
    unittest.main();