"""!

@brief Unit-tests for clustering result representor.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

from pyclustering.cluster.dbscan import dbscan;
from pyclustering.cluster.representor import cluster_result_representor;
from pyclustering.cluster.representor import type_cluster_result;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.cluster import representor


class Test(unittest.TestCase): 
    def getIndexRepresentor(self):
        clusters = [ [0, 1, 2, 3], [4, 5, 6, 7] ];
        data = [10, 11, 13, 12, 64, 65, 65, 68];
        
        return cluster_result_representor(type_cluster_result.CLUSTER_INDEX_LIST_SEPARATION, clusters, data);


    def testIndexToLabel(self):
        representor = self.getIndexRepresentor();
        
        representor.set_representation(type_cluster_result.CLUSTER_INDEX_LABELING);
        assert 8 == len(representor.get_clusters());
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters();


    def testIndexToObject(self):
        representor = self.getIndexRepresentor();
        representor.set_representation(type_cluster_result.CLUSTER_OBJECT_LIST_SEPARATION);
        
        assert 2 == len(representor.get_clusters());
        assert [ [10, 11, 13, 12 ], [64, 65, 65, 68] ] == representor.get_clusters();


    def testObjectToIndex(self):
        representor = self.getIndexRepresentor();
        representor.set_representation(type_cluster_result.CLUSTER_OBJECT_LIST_SEPARATION);
        
        representor.set_representation(type_cluster_result.CLUSTER_INDEX_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters();


    def testObjectToLabel(self):
        representor = self.getIndexRepresentor();
        representor.set_representation(type_cluster_result.CLUSTER_OBJECT_LIST_SEPARATION);
        
        representor.set_representation(type_cluster_result.CLUSTER_INDEX_LABELING);
        assert 8 == len(representor.get_clusters());
        assert [0, 0, 0, 0, 1, 1, 1, 1] == representor.get_clusters();


    def testLabelToIndex(self):
        representor = self.getIndexRepresentor();
        representor.set_representation(type_cluster_result.CLUSTER_INDEX_LABELING);
        
        representor.set_representation(type_cluster_result.CLUSTER_INDEX_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [0, 1, 2, 3], [4, 5, 6, 7] ] == representor.get_clusters();


    def testLabelToObject(self):
        representor = self.getIndexRepresentor();
        representor.set_representation(type_cluster_result.CLUSTER_INDEX_LABELING);
        
        representor.set_representation(type_cluster_result.CLUSTER_OBJECT_LIST_SEPARATION);
        assert 2 == len(representor.get_clusters());
        assert [ [10, 11, 13, 12 ], [64, 65, 65, 68] ] == representor.get_clusters();


if __name__ == "__main__":
    unittest.main();