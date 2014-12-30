import unittest;

from pyclustering.support import euclidean_distance;
from pyclustering.support import average_neighbor_distance;

class Test(unittest.TestCase):

    def testEuclideanDistance(self):
        point1 = [1, 2];
        point2 = [1, 3];
        point3 = [4, 6];
        
        # Tests for euclidean_distance
        assert euclidean_distance(point1, point2) == 1;
        assert euclidean_distance(point1, point1) == 0;
        assert euclidean_distance(point1, point3) == 5;

    
    def testFloatEuclideanDistance(self):
        assert euclidean_distance(0.5, 1.5) == 1;
        assert self.float_comparasion(euclidean_distance(1.6, 1.4), 0.2);
        assert self.float_comparasion(euclidean_distance(4.23, 2.14), 2.09);
    
    
    def testAverageNeighborDistance(self):
        points = [[0, 0], [0, 1], [1, 1], [1, 0]];
        
        assert average_neighbor_distance(points, 1) == 1.0;
        assert average_neighbor_distance(points, 2) == 1.0;
        assert self.float_comparasion(average_neighbor_distance(points, 3), 1.1381);
            
    
    def float_comparasion(self, float1, float2, eps = 0.001):
        return ( (float1 + eps) > float2 and (float1 - eps) < float2 );
        
        

if __name__ == "__main__":
    unittest.main();