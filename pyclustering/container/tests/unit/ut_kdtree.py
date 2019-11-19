"""!

@brief Unit-tests for KD-tree container.

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


import unittest

import math

import numpy

from pyclustering.container.kdtree import kdtree, kdtree_text_visualizer

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.utils import read_sample


class KDTreeUnitTest(unittest.TestCase):
    def testKDTreeCreateWithoutPayload(self):
        # Create k-d tree without any payload
        array = [ [4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9] ];
        tree = kdtree(array);
        
        assert len(tree.traverse()) == len(array);
        for item in array:
            node = tree.find_node(item);
            
            assert node != None;            # node should exist in the tree.
            assert node.payload == None;    # because we have created tree without any payloads.
            assert node.data == item;       # check for valid data.


    def testKDTreeCreateWithPayload(self):
        # Create k-d tree with payload
        array = [ [4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9] ];
        payload = ['q', 'w', 'e', 'r', 't', 'y', 'u'];
        
        tree = kdtree(array, payload);
        assert len(tree.traverse()) == len(array);
        for index in range(len(array)):
            node = tree.find_node(array[index]);
            
            assert node != None;
            assert node.payload == payload[index];
            assert node.data == array[index];


    def testKDTreeCreateTrivial(self):
        "Create k-d tree"
        array = [ [3, 4], [5, 6], [9, 8], [7, 3], [1, 2], [2, 4], [2, 5], [3, 2] ];
        tree = kdtree(array);
        
        assert len(tree.traverse()) == len(array);
        for item in array:
            assert tree.find_node(item).data == item;


    def testKDTreeInsertNodes(self):
        "Create empty k-d tree and insert nodes"
        array = [ [4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9] ];
        payload = ['q', 'w', 'e', 'r', 't', 'y', 'u'];
        
        tree = kdtree();
        assert len(tree.traverse()) == 0;
        for index in range(len(array)):
            node = tree.insert(array[index], payload[index]);
            
            assert len(tree.traverse()) == index + 1;
                        
            assert node != None;
            assert node.payload == payload[index];
            assert node.data == array[index];


    def testKDTreeParentSearch(self):
        "Check for right parents"
        array = [ [4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9] ];
        tree = kdtree(array);
        
        node = tree.find_node([4, 3]);
        assert node.parent == None;
        
        node = tree.find_node([3, 4]);
        assert node.parent.data == [4, 3];
        
        node = tree.find_node([5, 8]);
        assert node.parent.data == [4, 3];
    
        node = tree.find_node([6, 4]);
        assert node.parent.data == [5, 8];
        
        node = tree.find_node([3, 3]);
        assert node.parent.data == [3, 4];
        
        node = tree.find_node([5, 9]);
        assert node.parent.data == [5, 8];
        
        node = tree.find_node([3, 9]);
        assert node.parent.data == [3, 4];


    def testKDTreeInsertRemoveNode1(self):
        "Create empty k-d tree and insert nodes and after that remove all nodes"
        array = [ [4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9] ];
        payload = ['q', 'w', 'e', 'r', 't', 'y', 'u'];
        
        tree = kdtree();
        for index in range(len(array)):
            node = tree.insert(array[index], payload[index]);
        
        length = len(array);
        for index in range(0, length):
            node = tree.remove(array[index]);
            assert len(tree.traverse()) == length - index - 1;
            
            if (index + 1 < length):    # When root is removed then None will be returned
                assert node != None;
            else:
                assert node == None;

            # Check other nodes are located in the tree
            for k in range(index + 1, length):
                node = tree.find_node(array[k]);
                
                assert node.data == array[k];
                assert node.payload == payload[k];


    def testKDTreeInsertRemoveNode2(self):
        # This test simulates situation when a bug (16.01.2014) with removing was occuring
        array = [ [9, 9], [3, 3], [4, 4] ];
        tree = kdtree(array);
        
        assert None != tree.remove([9, 9]);
        assert len(tree.traverse()) == 2;
        
        assert None != tree.remove([4, 4]);
        assert len(tree.traverse()) == 1;
        
        assert None == tree.remove([3, 3]);
        assert len(tree.traverse()) == 0;


    def testKDTreeRemoveLongBranch(self):
        # Create only one branch - worth case and remove it
        array = [ [5, 5], [6, 5], [6, 6], [7, 6], [7, 7] ];
        tree = kdtree(array);
        
        assert len(tree.traverse()) == len(array);
        
        for index in range(len(array)):
            node = tree.remove(array[index]);
            assert len(tree.traverse()) == len(array) - index - 1;
        
        # Remove from other end
        tree = kdtree(array);
        for index in range(len(array)):
            node = tree.remove(array[len(array) - index - 1]);
            assert len(tree.traverse()) == len(array) - index - 1;


    def testKDTreeNearestNodeTrivial1(self):
        array = [ [4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [6, 9], [4, 9] ];
        tree = kdtree(array);
        
        for item in array:
            assert tree.find_nearest_dist_node(item, 0).data == item;
            assert tree.find_nearest_dist_node(item, 0.5).data == item;
            assert tree.find_nearest_dist_node(item, 1).data == item;
            assert tree.find_nearest_dist_node(item, 3).data == item;
            assert tree.find_nearest_dist_node(item, 10).data == item;
        
        assert tree.find_nearest_dist_node([6.1, 4.1], 0.5).data == [6, 4];
        assert tree.find_nearest_dist_node([6, 12], 0) == None;
        assert tree.find_nearest_dist_node([6, 12], 1) == None;
        assert tree.find_nearest_dist_node([6, 12], 3).data == [6, 9];


    def testKDTreeNearestNodeTrivial2(self):
        arrays = [ 
                    [ [3, 4], [5, 6], [9, 8], [7, 3], [1, 2], [2, 4], [2, 5], [3, 2], [3, 3] ],
                    [ [5, 6], [1, 3], [7, 3], [1, 1], [9, 9], [4, 7], [0, 3], [3, 5], [1, 2], [9, 3], [9, 8], [5, 5], [6, 6], [0, 0], [-4, -5], [-1, 5], [-8, 3] ] 
                 ];
                 
        distances = [0.0, 0.5, 1.0, 3.0, 10.0];
        
        for array in arrays:
            tree = kdtree(array);
            
            for item in array:
                for distance in distances:
                    assert tree.find_nearest_dist_node(item, distance).data == item;


    def templateSeachNearestNodeInTree(self, sample_path, **kwargs):
        numpy_usage = kwargs.get('numpy_usage', False)

        sample = read_sample(sample_path);
        if numpy_usage is True:
            sample = numpy.array(sample)

        tree = kdtree();
        
        for point in sample:
            node = tree.find_nearest_dist_node(point, 0.0);
            assert node == None;

            tree.insert(point, None);

            node = tree.find_nearest_dist_node(point, 0.0);
            assert node != None;
            assert node.data is point;


    def testSearchNearestNodeInSampleSimple01(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);

    def testSearchNearestNodeInSampleSimple01NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, numpy_usage=True);

    def testSearchNearestNodeInSampleSimple02(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);

    def testSearchNearestNodeInSampleSimple02NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, numpy_usage=True);

    def testSearchNearestNodeInSampleSimple03(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);

    def testSearchNearestNodeInSampleSimple03NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, numpy_usage=True);

    def testSearchNearestNodeInSampleSimple04(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE4);

    def testSearchNearestNodeInSampleSimple04NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, numpy_usage=True)

    def testSearchNearestNodeInSampleSimple05(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE5);

    def testSearchNearestNodeInSampleSimple05NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, numpy_usage=True);

    def testSearchNearestNodeInLsun(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_LSUN);

    def testSearchNearestNodeInLsunNumPy(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_LSUN, numpy_usage=True);

    def testSearchNearestNodeInTetra(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_TETRA);

    def testSearchNearestNodeInTetraNumPy(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_TETRA, numpy_usage=True);

    def testSearchNearestNodeInHepta(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_HEPTA);

    def testSearchNearestNodeInHeptaNumPy(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_HEPTA, numpy_usage=True);


    def templateSeachNearestNodesInTree(self, sample_path, search_radius, length=None, numpy_usage=False):
        sample = read_sample(sample_path);
        if numpy_usage is True:
            sample = numpy.array(sample)

        tree = kdtree(sample);
        
        for point in sample:
            nodes = tree.find_nearest_dist_nodes(point, search_radius);
            assert nodes != [];
            
            if (length is None):
                assert len(nodes) > 1;
            else:
                assert len(nodes) == length;


    def testSeachNearestNodesInSampleSimple01(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5);

    def testSeachNearestNodesInSampleSimple01NumPy(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, numpy_usage=True);

    def testSeachNearestNodesInSampleSimple02(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.5);

    def testSeachNearestNodesInSampleSimple02NumPy(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.5, numpy_usage=True);

    def testSeachNearestNodesInSampleSimple03(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.5);

    def testSeachNearestNodesInSampleSimple03NumPy(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.5, numpy_usage=True);

    def testSeachNearestNodesInSampleSimple03OneNode(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.0, 1);

    def testSeachNearestNodesInSampleSimple03OneNodeNumPy(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.0, 1, numpy_usage=True);


    def templateTextTreeRepresentation(self, sample_path, numpy_usage=False):
        sample = read_sample(sample_path);
        if numpy_usage is True:
            sample = numpy.array(sample)

        tree = kdtree(sample);
        
        representation = kdtree_text_visualizer(tree).visualize(False);
        assert representation != None;
        assert len(representation) > 0;
        
        amount_lines = representation.count("\n");
        expected_lower_edge = math.log2(len(sample)) * len(sample[0]);
        
        assert expected_lower_edge <= amount_lines;


    def testVisualizeSampleSimple01(self):
        self.templateTextTreeRepresentation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);

    def testVisualizeSampleSimple01NumPy(self):
        self.templateTextTreeRepresentation(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, numpy_usage=True);

    def testVisualizeSampleSimple02(self):
        self.templateTextTreeRepresentation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);

    def testVisualizeSampleSimple02NumPy(self):
        self.templateTextTreeRepresentation(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, numpy_usage=True);

    def testVisualizeSampleSimple05(self):
        self.templateTextTreeRepresentation(SIMPLE_SAMPLES.SAMPLE_SIMPLE5);

    def testVisualizeOneDimensional(self):
        self.templateTextTreeRepresentation(SIMPLE_SAMPLES.SAMPLE_SIMPLE7);

    def testVisualizeThreeDimensional(self):
        self.templateTextTreeRepresentation(SIMPLE_SAMPLES.SAMPLE_SIMPLE11);


    def templateTheSameDataSearchAndRemove(self, points, payloads):
        tree = kdtree();
        
        inserted_node = [];
        for i in range(len(points)):
            inserted_node.append( tree.insert(points[i], payloads[i]) );
        
        for node in inserted_node:
            found_node = tree.find_node_with_payload(node.data, node.payload);
            assert node == found_node;
        
        for i in range(len(inserted_node)):
            tree.remove(inserted_node[i].data, payload=inserted_node[i].payload);
            found_node = tree.find_node_with_payload(inserted_node[i].data, inserted_node[i].payload);
            assert None == found_node;
            
            for j in range(i + 1, len(inserted_node)):
                found_node = tree.find_node_with_payload(inserted_node[j].data, inserted_node[j].payload);
                assert inserted_node[j] == found_node;
    
    def testTheSameDataSearchAndRemove1(self):
        self.templateTheSameDataSearchAndRemove([ [2], [2], [2], [2], [2] ], [ 1, 2, 3, 4, 5 ]);

    def testTheSameDataSearchAndRemove1NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([ [2], [2], [2], [2], [2] ]), [ 1, 2, 3, 4, 5 ]);

    def testTheSameDataSearchAndRemove2(self):
        self.templateTheSameDataSearchAndRemove([ [-2.3], [-2.3], [-2.3], [-2.3], [-2.3] ], [ 10, 11, 12, 13, 14 ]);

    def testTheSameDataSearchAndRemove2NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([ [-2.3], [-2.3], [-2.3], [-2.3], [-2.3] ]), [ 10, 11, 12, 13, 14 ]);

    def testTheSameDataSearchAndRemove3(self):
        self.templateTheSameDataSearchAndRemove([ [1.1, 2.1], [1.1, 2.1], [1.1, 2.1] ], [ 'qwe', 'asd', 'zxc' ]);

    def testTheSameDataSearchAndRemove3NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([ [1.1, 2.1], [1.1, 2.1], [1.1, 2.1] ]), [ 'qwe', 'asd', 'zxc' ]);

    def testTheSameDataSearchAndRemove4(self):
        self.templateTheSameDataSearchAndRemove([ [1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 4.0] ], [ 'qwe', None ]);

    def testTheSameDataSearchAndRemove4NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([ [1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 4.0] ]), [ 'qwe', None ]);

    def testTheSameDataSearchAndRemove5(self):
        self.templateTheSameDataSearchAndRemove([ [2] ], [ None ]);

    def testTheSameDataSearchAndRemove5NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([ [2] ]), [ None ]);
