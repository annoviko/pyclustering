"""!

@brief Unit-tests for clustering result representation.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""

import unittest;

import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.encoder import cluster_encoder;
from pyclustering.cluster.encoder import type_encoding;


class Test(unittest.TestCase): 
    def getIndexRepresentor(self):
        clusters = [ [0, 1, 2, 3], [4, 5, 6, 7] ];
        data = [10, 11, 13, 12, 64, 65, 65, 68];
        
        return cluster_encoder(type_encoding.CLUSTER_INDEX_LIST_SEPARATION, clusters, data);


    def testIndexToLabel(self):
        representor = self.getIndexRepresentor();
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        assert 8 == len(representor.get_clusters());
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters();


    def testIndexToObject(self):
        representor = self.getIndexRepresentor();
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        
        assert 2 == len(representor.get_clusters());
        assert [ [10, 11, 13, 12 ], [64, 65, 65, 68] ] == representor.get_clusters();


    def testObjectToIndex(self):
        representor = self.getIndexRepresentor();
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters();


    def testObjectToLabel(self):
        representor = self.getIndexRepresentor();
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        assert 8 == len(representor.get_clusters());
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters();


    def testLabelToIndex(self):
        representor = self.getIndexRepresentor();
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters();


    def testLabelToObject(self):
        representor = self.getIndexRepresentor();
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [10, 11, 13, 12 ], [64, 65, 65, 68] ] == representor.get_clusters();


    def testLabelToLabel(self):
        representor = self.getIndexRepresentor();
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        
        assert 8 == len(representor.get_clusters());
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters();


    def testObjectToObject(self):
        representor = self.getIndexRepresentor();
        
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        
        assert 2 == len(representor.get_clusters());
        assert [ [10, 11, 13, 12 ], [64, 65, 65, 68] ] == representor.get_clusters();


    def testIndexToIndex(self):
        representor = self.getIndexRepresentor();
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        
        assert 2 == len(representor.get_clusters());
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters();


    def getIndexRepresentorDoubleData(self):
        clusters = [ [0, 1, 2, 3], [4, 5, 6, 7] ];
        data = [5.4562, 5.1235, 4.9235, 4.8712, 8.3451, 8.4215, 8.6535, 8.7345];
        
        return cluster_encoder(type_encoding.CLUSTER_INDEX_LIST_SEPARATION, clusters, data);
    
    
    def testDoubleObjectToIndex(self):
        representor = self.getIndexRepresentorDoubleData();
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters();


    def testDoubleObjectToLabel(self):
        representor = self.getIndexRepresentorDoubleData();
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        assert 8 == len(representor.get_clusters());
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters();


    def testOverAllTypes(self):
        representor = self.getIndexRepresentorDoubleData();
        
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        
        assert 8 == len(representor.get_clusters());
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters();


    def getIndexRepresentorTwoDimensionData(self):
        clusters = [ [0, 1, 2, 3], [4, 5, 6, 7] ];
        data = [ [5.1, 5.2], [5.2, 5.1], [5.4, 5.2], [5.1, 5.0], [8.1, 8.0], [8.4, 8.2], [8.3, 8.4], [8.5, 8.5]];
        
        return cluster_encoder(type_encoding.CLUSTER_INDEX_LIST_SEPARATION, clusters, data);


    def testIndexToLabelTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData();
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        assert 8 == len(representor.get_clusters());
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters();


    def testIndexToObjectTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData();
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        
        assert 2 == len(representor.get_clusters());
        assert [ [[5.1, 5.2], [5.2, 5.1], [5.4, 5.2], [5.1, 5.0]], [[8.1, 8.0], [8.4, 8.2], [8.3, 8.4], [8.5, 8.5]] ] == representor.get_clusters();


    def testObjectToIndexTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData();
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters();


    def testObjectToLabelTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData();
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        assert 8 == len(representor.get_clusters());
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters();


    def testLabelToIndexTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData();
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters();


    def testLabelToObjectTwoDimension(self):
        representor = self.getIndexRepresentorTwoDimensionData();
        representor.set_encoding(type_encoding.CLUSTER_INDEX_LABELING);
        
        representor.set_encoding(type_encoding.CLUSTER_OBJECT_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [[5.1, 5.2], [5.2, 5.1], [5.4, 5.2], [5.1, 5.0]], [[8.1, 8.0], [8.4, 8.2], [8.3, 8.4], [8.5, 8.5]] ] == representor.get_clusters();
