"""!

@brief Unit-tests for KD-tree container.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest
import numpy
import matplotlib
import random

matplotlib.use('Agg')

from pyclustering.container.kdtree import kdtree, kdtree_balanced, kdtree_visualizer

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.utils import read_sample


class KDTreeUnitTest(unittest.TestCase):
    def templateCreateWithPayloadAndFindNode(self, array, payload, kdtree_class):
        tree = kdtree_class(array, payload)
        self.assertEqual(len(array), len(tree))
        for index in range(len(array)):
            node = tree.find_node(array[index])

            self.assertIsNotNone(node)
            self.assertEqual(node.payload, payload[index])
            self.assertEqual(node.data, array[index])
            self.assertGreater(len(str(node)), 1)


    def testKDTreeCreateWithPayload01(self):
        array = [[4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9]]
        payload = ['q', 'w', 'e', 'r', 't', 'y', 'u']
        self.templateCreateWithPayloadAndFindNode(array, payload, kdtree)

    def testKDTreeBalancedWithPayload01(self):
        array = [[4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9]]
        payload = ['q', 'w', 'e', 'r', 't', 'y', 'u']
        self.templateCreateWithPayloadAndFindNode(array, payload, kdtree_balanced)

    def testKDTreeCreateWithPayload02(self):
        array = [[3, 4], [5, 6], [9, 8], [7, 3], [1, 2], [2, 4], [2, 5], [3, 2]]
        payload = ['q', 'w', 'a', 's', 'z', 'x', 't', 'y']
        self.templateCreateWithPayloadAndFindNode(array, payload, kdtree)

    def testKDTreeBalancedWithPayload02(self):
        array = [[3, 4], [5, 6], [9, 8], [7, 3], [1, 2], [2, 4], [2, 5], [3, 2]]
        payload = ['q', 'w', 'a', 's', 'z', 'x', 't', 'y']
        self.templateCreateWithPayloadAndFindNode(array, payload, kdtree_balanced)

    def testKDTreeWithPayload03(self):
        array = [[3, 4], [3, 2]]
        payload = ['q', 'y']
        self.templateCreateWithPayloadAndFindNode(array, payload, kdtree)

    def testKDTreeBalancedWithPayload03(self):
        array = [[3, 4], [3, 2]]
        payload = ['q', 'y']
        self.templateCreateWithPayloadAndFindNode(array, payload, kdtree_balanced)

    def testKDTreeCreateWithPayloadSample01(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        possible_payload = ["qwe", "asd", "zxc", "rty", "fgh", "vbn", "yui", "ghj", "bnm"]
        payload = [possible_payload[random.randint(0, len(possible_payload) - 1)] for _ in range(len(array))]
        self.templateCreateWithPayloadAndFindNode(array, payload, kdtree)

    def testKDTreeBalancedWithPayloadSample01(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        possible_payload = ["qwe", "asd", "zxc", "rty", "fgh", "vbn", "yui", "ghj", "bnm"]
        payload = [possible_payload[random.randint(0, len(possible_payload) - 1)] for _ in range(len(array))]
        self.templateCreateWithPayloadAndFindNode(array, payload, kdtree_balanced)


    def templateCreateWithoutPayloadAndFindNode(self, array, kdtree_class):
        tree = kdtree_class(array)
        self.assertEqual(len(array), len(tree))
        for item in array:
            found_node = tree.find_node(item)
            self.assertIsNotNone(found_node, "Point '%s' is not found." % str(item))
            self.assertEqual(found_node.data, item)
            self.assertIsNone(found_node.payload)

    def testKDTreeCreateWithoutPayloadOneNode(self):
        self.templateCreateWithoutPayloadAndFindNode([[3, 4]], kdtree)

    def testKDTreeBalancedCreateWithoutPayloadOneNode(self):
        self.templateCreateWithoutPayloadAndFindNode([[3, 4]], kdtree_balanced)

    def testKDTreeCreateWithoutPayloadTwoNode(self):
        self.templateCreateWithoutPayloadAndFindNode([[3, 4], [5, 6]], kdtree)

    def testKDTreeBalancedCreateWithoutPayloadTwoNode(self):
        self.templateCreateWithoutPayloadAndFindNode([[3, 4], [5, 6]], kdtree_balanced)

    def testKDTreeCreateWithoutPayload(self):
        array = [[3, 4], [5, 6], [9, 8], [7, 3], [1, 2], [2, 4], [2, 5], [3, 2]]
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree)

    def testKDTreeBalancedCreateWithoutPayload(self):
        array = [[3, 4], [5, 6], [9, 8], [7, 3], [1, 2], [2, 4], [2, 5], [3, 2]]
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree_balanced)

    def testKDTreeCreateWithoutPayloadSample01(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree)

    def testKDTreeBalancedCreateWithoutPayloadSample01(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree_balanced)

    def testKDTreeCreateWithoutPayloadSample02(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree)

    def testKDTreeBalancedCreateWithoutPayloadSample02(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree_balanced)

    def testKDTreeCreateWithoutPayloadSample03(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree)

    def testKDTreeBalancedCreateWithoutPayloadSample03(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree_balanced)

    def testKDTreeCreateWithoutPayloadSample04(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree)

    def testKDTreeBalancedCreateWithoutPayloadSample04(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree_balanced)

    def testKDTreeCreateWithoutPayloadSample05(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE5)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree)

    def testKDTreeBalancedCreateWithoutPayloadSample05(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE5)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree_balanced)

    def testKDTreeCreateWithoutPayloadSample06(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE6)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree)

    def testKDTreeBalancedCreateWithoutPayloadSample06(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE6)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree_balanced)

    def testKDTreeCreateWithoutPayloadSample07(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE7)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree)

    def testKDTreeBalancedCreateWithoutPayloadSample07(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE7)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree_balanced)

    def testKDTreeCreateWithoutPayloadSample08(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE8)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree)

    def testKDTreeBalancedCreateWithoutPayloadSample08(self):
        array = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE8)
        self.templateCreateWithoutPayloadAndFindNode(array, kdtree_balanced)


    def templateInsertNodes(self):
        array = [[4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9]]
        payload = ['q', 'w', 'e', 'r', 't', 'y', 'u']

        tree = kdtree()
        self.assertEqual(len(tree), 0)
        for index in range(len(array)):
            node = tree.insert(array[index], payload[index])

            self.assertEqual(len(tree), index + 1)

            self.assertIsNotNone(node)
            self.assertEqual(node.payload, payload[index])
            self.assertEqual(node.data, array[index])

    def testKDTreeInsertNodes(self):
        array = [[4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9]]
        payload = ['q', 'w', 'e', 'r', 't', 'y', 'u']
        
        tree = kdtree()
        self.assertEqual(len(tree), 0)
        for index in range(len(array)):
            node = tree.insert(array[index], payload[index])
            
            self.assertEqual(len(tree), index + 1)

            self.assertIsNotNone(node)
            self.assertEqual(node.payload, payload[index])
            self.assertEqual(node.data, array[index])


    def testKDTreeParentSearch(self):
        array = [[4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9]]
        tree = kdtree(array)
        
        node = tree.find_node([4, 3])
        assert node.parent is None
        
        node = tree.find_node([3, 4])
        assert node.parent.data == [4, 3]
        
        node = tree.find_node([5, 8])
        assert node.parent.data == [4, 3]
    
        node = tree.find_node([6, 4])
        assert node.parent.data == [5, 8]
        
        node = tree.find_node([3, 3])
        assert node.parent.data == [3, 4]
        
        node = tree.find_node([5, 9])
        assert node.parent.data == [5, 8]
        
        node = tree.find_node([3, 9])
        assert node.parent.data == [3, 4]


    def testKDTreeInsertRemoveNode1(self):
        array = [[4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [5, 9]]
        payload = ['q', 'w', 'e', 'r', 't', 'y', 'u']
        
        tree = kdtree()
        for index in range(len(array)):
            removed_node = tree.remove(array[index])
            self.assertIsNone(removed_node, "The point '%s' shouldn't be found in the tree - it wasn't added yet." %
                              str(array[index]))

            node = tree.insert(array[index], payload[index])
            self.assertIsNotNone(node)
            self.assertEqual(node.data, array[index])
        
        length = len(array)
        for index in range(0, length):
            node = tree.remove(array[index])
            assert len(tree) == length - index - 1
            
            if index + 1 < length:    # When root is removed then None will be returned
                assert node is not None
            else:
                assert node is None

            # Check other nodes are located in the tree
            for k in range(index + 1, length):
                node = tree.find_node(array[k])
                
                assert node.data == array[k];
                assert node.payload == payload[k];


    def testKDTreeInsertRemoveNode2(self):
        array = [[9, 9], [3, 3], [4, 4]]
        tree = kdtree(array)
        
        assert None is not tree.remove([9, 9])
        assert len(tree) == 2
        
        assert None is not tree.remove([4, 4])
        assert len(tree) == 1
        
        assert None is tree.remove([3, 3])
        assert len(tree) == 0


    def testKDTreeInsertFindNode(self):
        suite_array = [[[9, 9], [3, 3], [4, 4]],
                       [[9, 9], [3, 3]],
                       [[9, 9], [4, 4], [10, 10]],
                       [[5, 5]],
                       [[5, 5], [2, 2], [7, 7]],
                       [[5, 5], [2, 2], [7, 7], [1, 1], [8, 8]]]

        for array in suite_array:
            tree = kdtree(array)
            for point in array:
                node = tree.find_node(point)
                self.assertIsNotNone(node)
                self.assertEqual(node.data, point)


    def testKDTreeRemoveLongBranch(self):
        # Create only one branch - worth case and remove it
        array = [[5, 5], [6, 5], [6, 6], [7, 6], [7, 7]]
        tree = kdtree(array)
        
        self.assertEqual(len(tree), len(array))
        
        for index in range(len(array)):
            node = tree.remove(array[index])
            if len(tree) != 0:
                self.assertIsNotNone(node)
            self.assertEqual(len(tree), len(array) - index - 1)
        
        # Remove from other end
        tree = kdtree(array)
        for index in range(len(array)):
            node = tree.remove(array[len(array) - index - 1])
            if len(tree) != 0:
                self.assertIsNotNone(node)
            self.assertEqual(len(tree), len(array) - index - 1)


    def templateKDTreeNearestNodeTrivial1(self, kdtree_class):
        array = [ [4, 3], [3, 4], [5, 8], [3, 3], [3, 9], [6, 4], [6, 9], [4, 9] ]
        tree = kdtree_class(array)
        
        for item in array:
            assert tree.find_nearest_dist_node(item, 0).data == item;
            assert tree.find_nearest_dist_node(item, 0.5).data == item;
            assert tree.find_nearest_dist_node(item, 1).data == item;
            assert tree.find_nearest_dist_node(item, 3).data == item;
            assert tree.find_nearest_dist_node(item, 10).data == item;
        
        assert tree.find_nearest_dist_node([6.1, 4.1], 0.5).data == [6, 4]
        assert tree.find_nearest_dist_node([6, 12], 0) is None
        assert tree.find_nearest_dist_node([6, 12], 1) is None
        assert tree.find_nearest_dist_node([6, 12], 3).data == [6, 9]

    def testKDTreeNearestNodeTrivial1(self):
        self.templateKDTreeNearestNodeTrivial1(kdtree)

    def testKDTreeBalancedNearestNodeTrivial1(self):
        self.templateKDTreeNearestNodeTrivial1(kdtree_balanced)


    def testKDTreeNearestNodeTrivial2(self):
        arrays = [
                    [ [3, 4], [5, 6], [9, 8], [7, 3], [1, 2], [2, 4], [2, 5], [3, 2], [3, 3] ],
                    [ [5, 6], [1, 3], [7, 3], [1, 1], [9, 9], [4, 7], [0, 3], [3, 5], [1, 2], [9, 3], [9, 8], [5, 5], [6, 6], [0, 0], [-4, -5], [-1, 5], [-8, 3] ]
                 ]

        distances = [0.0, 0.5, 1.0, 3.0, 10.0]

        for array in arrays:
            tree = kdtree(array)
            
            for item in array:
                for distance in distances:
                    assert tree.find_nearest_dist_node(item, distance).data == item;


    def templateSeachNearestNodeInTree(self, sample_path, **kwargs):
        numpy_usage = kwargs.get('numpy_usage', False)

        sample = read_sample(sample_path)
        if numpy_usage is True:
            sample = numpy.array(sample)

        tree = kdtree()
        
        for point in sample:
            node = tree.find_nearest_dist_node(point, 0.0)
            self.assertIsNone(node)

            tree.insert(point, None)

            node = tree.find_nearest_dist_node(point, 0.0)
            self.assertIsNotNone(node)
            self.assertIs(node.data, point)

            distance_and_node = tree.find_nearest_dist_node(point, 0.0, True)
            self.assertIsNotNone(distance_and_node)
            self.assertIs(distance_and_node[1].data, point)
            self.assertEqual(distance_and_node[0], 0.0)


    def testSearchNearestNodeInSampleSimple01(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)

    def testSearchNearestNodeInSampleSimple01NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, numpy_usage=True)

    def testSearchNearestNodeInSampleSimple02(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)

    def testSearchNearestNodeInSampleSimple02NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, numpy_usage=True)

    def testSearchNearestNodeInSampleSimple03(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

    def testSearchNearestNodeInSampleSimple03NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, numpy_usage=True)

    def testSearchNearestNodeInSampleSimple04(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)

    def testSearchNearestNodeInSampleSimple04NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, numpy_usage=True)

    def testSearchNearestNodeInSampleSimple05(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE5)

    def testSearchNearestNodeInSampleSimple05NumPy(self):
        self.templateSeachNearestNodeInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, numpy_usage=True)

    def testSearchNearestNodeInLsun(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_LSUN)

    def testSearchNearestNodeInLsunNumPy(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_LSUN, numpy_usage=True)

    def testSearchNearestNodeInTetra(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_TETRA)

    def testSearchNearestNodeInTetraNumPy(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_TETRA, numpy_usage=True)

    def testSearchNearestNodeInHepta(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_HEPTA)

    def testSearchNearestNodeInHeptaNumPy(self):
        self.templateSeachNearestNodeInTree(FCPS_SAMPLES.SAMPLE_HEPTA, numpy_usage=True)


    def templateSeachNearestNodeInBalancedTree(self, sample_path, generate_payload=False, **kwargs):
        numpy_usage = kwargs.get('numpy_usage', False)

        sample = read_sample(sample_path)
        if numpy_usage is True:
            sample = numpy.array(sample)

        payloads = None
        if generate_payload is True:
            payloads = [random.randint(1, 1000) for _ in range(len(sample))]

        tree = kdtree_balanced(sample, payloads)

        for i in range(len(sample)):
            node = tree.find_nearest_dist_node(sample[i], 0.0)
            self.assertIsNotNone(node)

            if numpy_usage is False:
                self.assertIs(node.data, sample[i])
            else:
                self.assertTrue((node.data == sample[i]).all())

            if payloads is not None:
                self.assertEqual(node.payload, payloads[i])


    def testKDTreeBalancedSearchNearestSimple01(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)

    def testKDTreeBalancedSearchNearestSimple01Payload(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, True)

    def testKDTreeBalancedSearchNearestSimple01NumPy(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, numpy_usage=True)

    def testKDTreeBalancedSearchNearestSimple01PayloadNumPy(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, True, numpy_usage=True)

    def testKDTreeBalancedSearchNearestSimple02(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)

    def testKDTreeBalancedSearchNearestSimple02Payload(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, True)

    def testKDTreeBalancedSearchNearestSimple02NumPy(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, numpy_usage=True)

    def testKDTreeBalancedSearchNearestSimple02PayloadNumPy(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, True, numpy_usage=True)

    def testKDTreeBalancedSearchNearestSimple03(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

    def testKDTreeBalancedSearchNearestSimple03Payload(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, True)

    def testKDTreeBalancedSearchNearestSimple03NumPy(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, numpy_usage=True)

    def testKDTreeBalancedSearchNearestSimple04(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)

    def testKDTreeBalancedSearchNearestSimple04Payload(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, True)

    def testKDTreeBalancedSearchNearestSimple04NumPy(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, numpy_usage=True)

    def testKDTreeBalancedSearchNearestSimple05(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE5)

    def testKDTreeBalancedSearchNearestSimple05Payload(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, True)

    def testKDTreeBalancedSearchNearestSimple05NumPy(self):
        self.templateSeachNearestNodeInBalancedTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, numpy_usage=True)

    def testKDTreeBalancedSearchNearestLsun(self):
        self.templateSeachNearestNodeInBalancedTree(FCPS_SAMPLES.SAMPLE_LSUN)

    def testKDTreeBalancedSearchNearestLsunNumPy(self):
        self.templateSeachNearestNodeInBalancedTree(FCPS_SAMPLES.SAMPLE_LSUN, numpy_usage=True)

    def testKDTreeBalancedSearchNearestHepta(self):
        self.templateSeachNearestNodeInBalancedTree(FCPS_SAMPLES.SAMPLE_HEPTA)

    def testKDTreeBalancedSearchNearestHeptaNumPy(self):
        self.templateSeachNearestNodeInBalancedTree(FCPS_SAMPLES.SAMPLE_HEPTA, numpy_usage=True)


    def templateSeachNearestNodesInTree(self, sample_path, search_radius, length=None, numpy_usage=False, **kwargs):
        kdtree_class = kwargs.get('kdtree_class', kdtree)

        sample = read_sample(sample_path)
        if numpy_usage is True:
            sample = numpy.array(sample)

        tree = kdtree_class(sample)
        
        for point in sample:
            nodes = tree.find_nearest_dist_nodes(point, search_radius)
            self.assertNotEqual(len(nodes), 0)
            
            if length is None:
                self.assertGreater(len(nodes), 1)
            else:
                self.assertEqual(len(nodes), length)


    def testSeachNearestNodesInSampleSimple01(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5)

    def testSeachNearestNodesInSampleSimple01Balanced(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, kdtree_class=kdtree_balanced)

    def testSeachNearestNodesInSampleSimple01NumPy(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, numpy_usage=True)

    def testSeachNearestNodesInSampleSimple02(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.5)

    def testSeachNearestNodesInSampleSimple02Balanced(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.5, kdtree_class=kdtree_balanced)

    def testSeachNearestNodesInSampleSimple02NumPy(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 0.5, numpy_usage=True)

    def testSeachNearestNodesInSampleSimple03(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.5)

    def testSeachNearestNodesInSampleSimple03Balanced(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.5, kdtree_class=kdtree_balanced)

    def testSeachNearestNodesInSampleSimple03NumPy(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.5, numpy_usage=True)

    def testSeachNearestNodesInSampleSimple03OneNode(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.0, 1)

    def testSeachNearestNodesInSampleSimple03OneNodeBalanced(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.0, 1, kdtree_class=kdtree_balanced)

    def testSeachNearestNodesInSampleSimple03OneNodeNumPy(self):
        self.templateSeachNearestNodesInTree(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.0, 1, numpy_usage=True)


    def templateTreeVisualization(self, path, **kwargs):
        sample = None
        if path is not None:
            sample = read_sample(path)

        exception = kwargs.get('exception', None)

        if exception is not None:
            self.assertRaises(exception, kdtree_visualizer, kdtree(sample))
            self.assertRaises(exception, kdtree_visualizer, kdtree_balanced(sample))
        else:
            kdtree_visualizer(kdtree(sample)).visualize()
            kdtree_visualizer(kdtree_balanced(sample)).visualize()

    def testVisualizeNoData(self):
        self.templateTreeVisualization(None, exception=ValueError)

    def testVisualizeSampleSimple01(self):
        self.templateTreeVisualization(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)

    def testVisualizeSampleSimple01NumPy(self):
        self.templateTreeVisualization(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, numpy_usage=True)

    def testVisualizeSampleSimple02(self):
        self.templateTreeVisualization(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)

    def testVisualizeSampleSimple02NumPy(self):
        self.templateTreeVisualization(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, numpy_usage=True)

    def testVisualizeSampleSimple05(self):
        self.templateTreeVisualization(SIMPLE_SAMPLES.SAMPLE_SIMPLE5)

    def testVisualizeOneDimensional(self):
        self.templateTreeVisualization(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, exception=NotImplementedError)

    def testVisualizeThreeDimensional(self):
        self.templateTreeVisualization(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, exception=NotImplementedError)


    def templateTheSameDataSearchAndRemove(self, points, payloads):
        tree = kdtree()
        
        inserted_node = []
        for i in range(len(points)):
            inserted_node.append(tree.insert(points[i], payloads[i]))
        
        for node in inserted_node:
            found_node = tree.find_node_with_payload(node.data, node.payload)
            self.assertEqual(node, found_node)
        
        for i in range(len(inserted_node)):
            tree.remove(inserted_node[i].data, payload=inserted_node[i].payload)
            found_node = tree.find_node_with_payload(inserted_node[i].data, inserted_node[i].payload)
            self.assertIsNone(found_node)
            
            for j in range(i + 1, len(inserted_node)):
                found_node = tree.find_node_with_payload(inserted_node[j].data, inserted_node[j].payload)
                self.assertEqual(inserted_node[j], found_node)
    
    def testTheSameDataSearchAndRemove1(self):
        self.templateTheSameDataSearchAndRemove([[2], [2], [2], [2], [2]], [1, 2, 3, 4, 5])

    def testTheSameDataSearchAndRemove1NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([[2], [2], [2], [2], [2]]), [1, 2, 3, 4, 5])

    def testTheSameDataSearchAndRemove2(self):
        self.templateTheSameDataSearchAndRemove([[-2.3], [-2.3], [-2.3], [-2.3], [-2.3]], [10, 11, 12, 13, 14])

    def testTheSameDataSearchAndRemove2NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([[-2.3], [-2.3], [-2.3], [-2.3], [-2.3]]),
                                                [10, 11, 12, 13, 14])

    def testTheSameDataSearchAndRemove3(self):
        self.templateTheSameDataSearchAndRemove([[1.1, 2.1], [1.1, 2.1], [1.1, 2.1]], ['qwe', 'asd', 'zxc'])

    def testTheSameDataSearchAndRemove3NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([[1.1, 2.1], [1.1, 2.1], [1.1, 2.1]]),
                                                ['qwe', 'asd', 'zxc'])

    def testTheSameDataSearchAndRemove4(self):
        self.templateTheSameDataSearchAndRemove([[1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 4.0]], ['qwe', None])

    def testTheSameDataSearchAndRemove4NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([[1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 4.0]]),
                                                ['qwe', None])

    def testTheSameDataSearchAndRemove5(self):
        self.templateTheSameDataSearchAndRemove([[2]], [None])

    def testTheSameDataSearchAndRemove5NumPy(self):
        self.templateTheSameDataSearchAndRemove(numpy.array([[2]]), [None])
