"""!

@brief Unit-tests for clustering result representation.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest
import math

import matplotlib
matplotlib.use('Agg')

from pyclustering.cluster.encoder import cluster_encoder
from pyclustering.cluster.encoder import type_encoding


class Test(unittest.TestCase): 
    def getIndexRepresentor(self):
        clusters = [ [0, 1, 2, 3], [4, 5, 6, 7] ]
        data = [10, 11, 13, 12, 64, 65, 65, 68]
        
        return cluster_encoder(type_encoding.CLUSTER_INDEX_LIST_SEPARATION, clusters, data)


    def testIndexToLabel(self):
        representor = self.getIndexRepresentor()
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        assert 8 == len(representor.get_clusters())
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters()


    def testIndexToObject(self):
        representor = self.getIndexRepresentor()
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        
        assert 2 == len(representor.get_clusters());
        assert [ [10, 11, 13, 12 ], [64, 65, 65, 68] ] == representor.get_clusters()


    def testObjectToIndex(self):
        representor = self.getIndexRepresentor()
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        assert 2 == len(representor.get_clusters())
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters()


    def testObjectToLabel(self):
        representor = self.getIndexRepresentor()
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        assert 8 == len(representor.get_clusters())
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters()


    def testLabelToIndex(self):
        representor = self.getIndexRepresentor()
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        assert 2 == len(representor.get_clusters())
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters()


    def testLabelToObject(self):
        representor = self.getIndexRepresentor()
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        assert 2 == len(representor.get_clusters())
        assert [ [10, 11, 13, 12 ], [64, 65, 65, 68] ] == representor.get_clusters()


    def testLabelToLabel(self):
        representor = self.getIndexRepresentor()
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        
        assert 8 == len(representor.get_clusters())
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters()


    def testObjectToObject(self):
        representor = self.getIndexRepresentor()
        
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        
        assert 2 == len(representor.get_clusters())
        assert [ [10, 11, 13, 12 ], [64, 65, 65, 68] ] == representor.get_clusters()


    def testIndexToIndex(self):
        representor = self.getIndexRepresentor()
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        
        assert 2 == len(representor.get_clusters())
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters()


    def getIndexRepresentorDoubleData(self):
        clusters = [ [0, 1, 2, 3], [4, 5, 6, 7] ]
        data = [5.4562, 5.1235, 4.9235, 4.8712, 8.3451, 8.4215, 8.6535, 8.7345]
        
        return cluster_encoder(type_encoding.CLUSTER_INDEX_LIST_SEPARATION, clusters, data)
    
    
    def testDoubleObjectToIndex(self):
        representor = self.getIndexRepresentorDoubleData()
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        assert 2 == len(representor.get_clusters());
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters()


    def testDoubleObjectToLabel(self):
        representor = self.getIndexRepresentorDoubleData()
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        assert 8 == len(representor.get_clusters())
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters()


    def testOverAllTypes(self):
        representor = self.getIndexRepresentorDoubleData()
        
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        
        assert 8 == len(representor.get_clusters())
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters()


    def getIndexRepresentorTwoDimensionData(self):
        clusters = [ [0, 1, 2, 3], [4, 5, 6, 7] ]
        data = [ [5.1, 5.2], [5.2, 5.1], [5.4, 5.2], [5.1, 5.0], [8.1, 8.0], [8.4, 8.2], [8.3, 8.4], [8.5, 8.5]]
        
        return cluster_encoder(type_encoding.CLUSTER_INDEX_LIST_SEPARATION, clusters, data)


    def testIndexToLabelTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData()
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        assert 8 == len(representor.get_clusters())
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters()


    def testIndexToObjectTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData()
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        
        assert 2 == len(representor.get_clusters())
        assert [ [[5.1, 5.2], [5.2, 5.1], [5.4, 5.2], [5.1, 5.0]], [[8.1, 8.0], [8.4, 8.2], [8.3, 8.4], [8.5, 8.5]] ] == representor.get_clusters()


    def testObjectToIndexTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData()
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        assert 2 == len(representor.get_clusters())
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters()


    def testObjectToLabelTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData()
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        assert 8 == len(representor.get_clusters())
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters()


    def testLabelToIndexTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData()
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        assert 2 == len(representor.get_clusters())
        assert [[0, 1, 2, 3], [4, 5, 6, 7]] == representor.get_clusters()


    def testLabelToObjectTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData()
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)
        
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        assert 2 == len(representor.get_clusters())
        assert [ [[5.1, 5.2], [5.2, 5.1], [5.4, 5.2], [5.1, 5.0]], [[8.1, 8.0], [8.4, 8.2], [8.3, 8.4], [8.5, 8.5]] ] == representor.get_clusters()


    def testIndexListToLabelsMissedPoint(self):
        clusters = [[0, 1, 2, 3], [4, 5, 6]]    # the last point is missed
        data = [[5.1, 5.2], [5.2, 5.1], [5.4, 5.2], [5.1, 5.0], [8.1, 8.0], [8.4, 8.2], [8.3, 8.4], [8.5, 8.5]]

        encoder = cluster_encoder(type_encoding.CLUSTER_INDEX_LIST_SEPARATION, clusters, data)
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)

        expected = [0, 0, 0, 0, 1, 1, 1, float('NaN')]
        actual = encoder.get_clusters()

        self.assertEqual(len(expected), len(actual))

        for i in range(len(expected)):
            if math.isnan(expected[i]) is True:
                self.assertTrue(math.isnan(actual[i]))
            else:
                self.assertEqual(expected[i], actual[i])

    def testObjectListToLabelsMissedPoint(self):
        clusters = [[[5.1, 5.2], [5.2, 5.1]], [[8.1, 8.0], [8.4, 8.2]]]
        data = [[5.1, 5.2], [5.2, 5.1], [14.1, 76.0], [8.1, 8.0], [8.4, 8.2]]

        encoder = cluster_encoder(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION, clusters, data)
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LABELING)

        expected = [0, 0, float('NaN'), 1, 1]
        actual = encoder.get_clusters()

        self.assertEqual(len(expected), len(actual))

        for i in range(len(expected)):
            if math.isnan(expected[i]) is True:
                self.assertTrue(math.isnan(actual[i]))
            else:
                self.assertEqual(expected[i], actual[i])

    def testLabelsToIndexListAndObjectListMissedPoint(self):
        clusters = [0, 0, float('NaN'), 1, 1]
        data = [[5.1, 5.2], [5.2, 5.1], [14.1, 76.0], [8.1, 8.0], [8.4, 8.2]]

        encoder = cluster_encoder(type_encoding.CLUSTER_INDEX_LABELING, clusters, data)
        encoder.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION)
        expected = [[0, 1], [3, 4]]
        actual = encoder.get_clusters()

        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected, actual)

        encoder = cluster_encoder(type_encoding.CLUSTER_INDEX_LABELING, clusters, data)
        encoder.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION)
        expected = [[[5.1, 5.2], [5.2, 5.1]], [[8.1, 8.0], [8.4, 8.2]]]
        actual = encoder.get_clusters()

        self.assertEqual(len(expected), len(actual))
        self.assertEqual(expected, actual)
