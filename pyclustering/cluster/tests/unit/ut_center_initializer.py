"""

@brief Unit-tests for Center Initialization

"""


import unittest

from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer


class CenterInitializationKmeansPlusPlusTest(unittest.TestCase):

    def testEuclideanDistance(self):

        # Create Test data
        point_1 = [0.21312, -1.214214]
        point_2 = [198237.1231, 3231.1231]
        point_3 = [-312.3213, 312.3213]
        point_4 = [-32131, -31231]

        # Asserts
        self.assertAlmostEqual(kmeans_plusplus_initializer.get_euclidean_distance(point_1, point_2),
                               198263.26054,
                               places=4)
        self.assertAlmostEqual(kmeans_plusplus_initializer.get_euclidean_distance(point_2, point_3),
                               198570.89735,
                               places=4)
        self.assertAlmostEqual(kmeans_plusplus_initializer.get_euclidean_distance(point_3, point_4),
                               44804.122944,
                               places=4)
        self.assertAlmostEqual(kmeans_plusplus_initializer.get_euclidean_distance(point_4, point_4),
                               0.0,
                               places=4)

    def testUniformRandom(self):

        # Create Test Data
        prob_1 = [i / 10.0 for i in range(1, 11)]
        prob_2 = [0.1, 0.5, 1.0]

        # Init result
        res_1 = [0] * 10
        res_2 = [0] * 3

        # Run uniform
        for _ in range(10000):
            res_1[kmeans_plusplus_initializer.get_uniform(prob_1)] += 1
            res_2[kmeans_plusplus_initializer.get_uniform(prob_2)] += 1

        # Asserts

        # Data Set 1
        for _idx in range(10):
            self.assertGreater(res_1[_idx], 900)
            self.assertLess(res_1[_idx], 1100)

        # Data Set 2
        self.assertGreater(res_2[0], 900)
        self.assertLess(res_2[0], 1100)

        self.assertGreater(res_2[1], 3900)
        self.assertLess(res_2[1], 4100)

        self.assertGreater(res_2[2], 4900)
        self.assertLess(res_2[2], 5100)

    def testCalcDistanceToNearestCenter(self):

        # Test Data
        points_1 = [[0, 0], [1, 0], [0, 1], [1, 1]]
        points_2 = [[5, 0], [6, 0], [5, 1], [6, 1]]
        points_3 = [[0, 5], [1, 5], [0, 6], [1, 6]]
        points_4 = [[4, 4], [7, 4], [4, 7], [7, 7]]

        data_set_1 = [*points_1, *points_2, *points_3, *points_4]

        # Centers
        centers = [[0.5, 0.5], [5.5, 0.5], [0.5, 5.5], [5.5, 5.5]]

        # Result
        res_1 = kmeans_plusplus_initializer.calc_distance_to_nearest_center(data_set_1, centers)

        # Asserts
        for _idx in range(12):
            self.assertAlmostEqual(res_1[_idx], 0.7071067, places=4)

        for _idx in range(12, 16):
            self.assertAlmostEqual(res_1[_idx], 2.12132034, places=4)

