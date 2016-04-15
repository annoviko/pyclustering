"""!

@brief Unit-tests for KD-tree container.

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
import itertools;

from pyclustering.container.kdtree import kdtree;

class Test(unittest.TestCase):
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
        #tree.show();
        
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
    
    # Verification test, so it is required too much time for testing.
    #def testVerificationKdTree1(self):
    #    array = [ [5, 5], [4, 5], [4, 4], [3, 4], [3, 3], [6, 6], [8, 8], [7, 7], [9, 9]];
    #    self.template_verification_insert_remove_kdtree_test(array);
                    
    def templateVerificationInsertRemoveKDTreeTest(self, array):
        for perm_array in itertools.permutations(array):
            tree = kdtree(array);
            length = len(array);
            
            for index in range(len(perm_array)):
                #tree.show();
                
                node = tree.remove(perm_array[index]);

                if ( index + 1 < length ):
                    assert node is not None;
                    
                assert len(tree.traverse()) == length - index - 1;


if __name__ == "__main__":
    unittest.main();