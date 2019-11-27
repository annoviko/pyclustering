"""!

@brief Unit-tests for CF-tree container.

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
import numpy
import math

from random import random

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.container.cftree import cfentry, cftree
from pyclustering.container.cftree import measurement_type

from pyclustering.utils import linear_sum, square_sum, read_sample
from pyclustering.utils import euclidean_distance_square, manhattan_distance, average_inter_cluster_distance, average_intra_cluster_distance, variance_increase_distance


class CftreeUnitTest(unittest.TestCase):
    def templateCfClusterRepresentation(self, cluster, centroid, radius, diameter, tolerance):
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster))
           
        assertion_centroid = centroid
        if type(centroid) != list:
            assertion_centroid = [centroid]
           
        if type(centroid) == list:
            for dimension in range(0, len(assertion_centroid)):
                self.assertAlmostEqual(assertion_centroid[dimension], (entry.get_centroid())[dimension], tolerance)

        self.assertAlmostEqual(radius, entry.get_radius(), tolerance)
        self.assertAlmostEqual(diameter, entry.get_diameter(), tolerance)

    def testCfClusterRepresentationOneDimension2(self):
        cluster = [[0.1], [0.2], [0.5], [0.4], [0.6]]
        self.templateCfClusterRepresentation(cluster, 0.36, 0.18547, 0.29326, 5)
       
    def testCfClusterRepresentationTwoDimension(self):
        cluster = [[0.1, 0.1], [0.2, 0.2], [0.5, 0.5], [0.4, 0.4], [0.6, 0.6]]
        self.templateCfClusterRepresentation(cluster, [0.36, 0.36], 0.26230, 0.41473, 5)


    def testGetNearestEntry(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        tree = cftree(10, 100, 0.2, measurement_type.CENTROID_EUCLIDEAN_DISTANCE)

        self.assertEqual(10, tree.branch_factor)
        self.assertEqual(100, tree.max_entries)
        self.assertEqual(0.2, tree.threshold)
        self.assertEqual(measurement_type.CENTROID_EUCLIDEAN_DISTANCE, tree.type_measurement)

        for index_point in range(len(sample)):
            tree.insert_point(sample[index_point])

        cluster = [[0.1, 0.1], [0.2, 0.2]]
        entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster))

        leaf = tree.find_nearest_leaf(entry)
        found_entry = leaf.get_nearest_entry(entry, measurement_type.CENTROID_EUCLIDEAN_DISTANCE)
        found_index_entry = leaf.get_nearest_index_entry(entry, measurement_type.CENTROID_EUCLIDEAN_DISTANCE)

        self.assertEqual(leaf.entries[found_index_entry], found_entry)


    def templateCfEntryValueDistance(self, cluster1, cluster2, value, tolerance, type_measurment):
        entry1 = cfentry(len(cluster1), linear_sum(cluster1), square_sum(cluster1))
        entry2 = cfentry(len(cluster2), linear_sum(cluster2), square_sum(cluster2))
           
        distance = entry1.get_distance(entry2, type_measurment)
        assert ((value - tolerance < distance) and (value + tolerance > distance))
           
    def testCfEntryTwoPoints1(self):
        self.templateCfEntryValueDistance([[0.0]], [[1.0]], 1.0, 0.0000001, measurement_type.CENTROID_EUCLIDEAN_DISTANCE)
   
    def testCfEntryTwoPoints2(self):
        self.templateCfEntryValueDistance([[0.0]], [[0.0]], 0.0, 0.0000001, measurement_type.CENTROID_EUCLIDEAN_DISTANCE)
           
    def testCfEntryTwoPoints3(self):
        self.templateCfEntryValueDistance([[-1.0]], [[0.0]], 1.0, 0.0000001, measurement_type.CENTROID_EUCLIDEAN_DISTANCE)
           
    def testCfEntryTwoPoints4(self):
        self.templateCfEntryValueDistance([[1.0, 0.0]], [[0.0, 1.0]], 2.0, 0.0000001, measurement_type.CENTROID_EUCLIDEAN_DISTANCE)


    def testCfEntryIncrease(self):
        cluster = [[0.1, 0.1], [0.2, 0.2], [0.5, 0.5], [0.4, 0.4], [0.6, 0.6]]
           
        entry1 = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster))
        entry2 = entry1 + entry1
           
        assert cfentry(10, [3.6, 3.6], 3.28) == entry2
           
        entry2 = entry2 + entry2
        assert cfentry(20, [7.2, 7.2], 6.56) == entry2


    def templateCfEntryDistance(self, type_measurement):
        cluster1 = [[0.1, 0.1], [0.1, 0.2], [0.2, 0.1], [0.2, 0.2]]
        cluster2 = [[0.4, 0.4], [0.4, 0.5], [0.5, 0.4], [0.5, 0.5]]
        cluster3 = [[0.9, 0.9], [0.9, 1.0], [1.0, 0.9], [1.0, 1.0]]
           
        entry1 = cfentry(len(cluster1), linear_sum(cluster1), square_sum(cluster1))
        entry2 = cfentry(len(cluster2), linear_sum(cluster2), square_sum(cluster2))
        entry3 = cfentry(len(cluster3), linear_sum(cluster3), square_sum(cluster3))
           
        distance12 = entry1.get_distance(entry2, type_measurement)
        distance23 = entry2.get_distance(entry3, type_measurement)
        distance13 = entry1.get_distance(entry3, type_measurement)
        
        assert distance12 < distance23;
        assert distance23 < distance13;
       
    def testCfDistanceCentroidEuclidian(self):
        self.templateCfEntryDistance(measurement_type.CENTROID_EUCLIDEAN_DISTANCE)
           
    def testCfDistanceCentroidManhatten(self):
        self.templateCfEntryDistance(measurement_type.CENTROID_MANHATTAN_DISTANCE)
           
    def testCfDistanceAverageInterCluster(self):
        self.templateCfEntryDistance(measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE)
   
    def testCfDistanceAverageIntraCluster(self):
        self.templateCfEntryDistance(measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE)
           
    def testCfDistanceVarianceIncrease(self):
        self.templateCfEntryDistance(measurement_type.VARIANCE_INCREASE_DISTANCE)
    
    
    def templateDistanceCalculation(self, cluster1, cluster2, type_measurement):
        entry1 = cfentry(len(cluster1), linear_sum(cluster1), square_sum(cluster1))
        entry2 = cfentry(len(cluster2), linear_sum(cluster2), square_sum(cluster2))
        
        # check that the same distance from 1 to 2 and from 2 to 1.
        distance12 = entry1.get_distance(entry2, type_measurement)
        distance21 = entry2.get_distance(entry1, type_measurement)
        
        assert distance12 == distance21;
        
        # check with utils calculation
        float_delta = 0.0000001
        if (type_measurement == measurement_type.CENTROID_EUCLIDEAN_DISTANCE):
            assert distance12 == euclidean_distance_square(entry1.get_centroid(), entry2.get_centroid());
        
        elif (type_measurement == measurement_type.CENTROID_MANHATTAN_DISTANCE):
            assert distance12 == manhattan_distance(entry1.get_centroid(), entry2.get_centroid());
        
        elif (type_measurement == measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE):
            assert numpy.isclose(distance12, average_inter_cluster_distance(cluster1, cluster2)) == True;
        
        elif (type_measurement == measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE):
            assert numpy.isclose(distance12, average_intra_cluster_distance(cluster1, cluster2)) == True;
        
        elif (type_measurement == measurement_type.VARIANCE_INCREASE_DISTANCE):
            assert numpy.isclose(distance12, variance_increase_distance(cluster1, cluster2)) == True;
    
    def templateDistanceCalculationTheSimplestSample(self, type_measurement):
        cluster1 = [[0.1, 0.1], [0.1, 0.2], [0.2, 0.1], [0.2, 0.2]]
        cluster2 = [[0.4, 0.4], [0.4, 0.5], [0.5, 0.4], [0.5, 0.5]]
        
        self.templateDistanceCalculation(cluster1, cluster2, type_measurement)
    
    def testDistanceCalculationTheSimplestSampleCentroidEuclidian(self):
        self.templateDistanceCalculationTheSimplestSample(measurement_type.CENTROID_EUCLIDEAN_DISTANCE)

    def testDistanceCalculationTheSimplestSampleCentroidManhattan(self):
        self.templateDistanceCalculationTheSimplestSample(measurement_type.CENTROID_MANHATTAN_DISTANCE)

    def testDistanceCalculationTheSimplestSampleAverageInterClusterDistance(self):
        self.templateDistanceCalculationTheSimplestSample(measurement_type.AVERAGE_INTER_CLUSTER_DISTANCE)

    def testDistanceCalculationTheSimplestSampleAverageIntraClusterDistance(self):
        self.templateDistanceCalculationTheSimplestSample(measurement_type.AVERAGE_INTRA_CLUSTER_DISTANCE)

    def testDistanceCalculationTheSimplestSampleVarianceIncreaseDistance(self):
        self.templateDistanceCalculationTheSimplestSample(measurement_type.VARIANCE_INCREASE_DISTANCE)


    def testCfTreeCreationWithOneEntry(self):
        tree = cftree(2, 1, 1.0)
        entry = cfentry(5, [0.0, 0.1], 0.05)
           
        tree.insert(entry)
           
        assert 1 == tree.amount_nodes;
        assert 1 == tree.height;
        assert 1 == tree.amount_entries;
           
        assert entry == tree.root.feature;
        assert None == tree.root.parent;


    def testCfTreeCreationWithoutMerging(self):
        clusters = [[[random() + j, random() + j] for _ in range(10)] for j in range(10)]
        tree = cftree(2, 1, 0.0)
           
        for cluster in clusters:
            for point in cluster:
                tree.insert_point(point)
           
        assert tree.height >= 4
        self.assertEqual(tree.amount_entries, 100)
        self.assertEqual(len(tree.leafes), 100)


    def templateCfTreeLeafIntegrity(self, number_clusters, branching_factor, max_entries, threshold):
        clusters = [ [ [random() + j, random() + j] for i in range(10) ] for j in range(number_clusters) ]
        tree = cftree(branching_factor, max_entries, threshold)
           
        for index_cluster in range(0, len(clusters)):
            for point in clusters[index_cluster]:
                tree.insert_point(point)
               
            result_searching = False
            for leaf in tree.leafes:
                for node_entry in leaf.entries:
                    result_searching |= (node_entry == node_entry)
       
            assert True == result_searching;
                   
    def testCfTreeLeafIntegrity10_2_1(self):
        self.templateCfTreeLeafIntegrity(10, 2, 1, 0.0)
            
    def testCfTreeLeafIntegrity10_3_1(self):
        self.templateCfTreeLeafIntegrity(10, 3, 1, 0.0)
            
    def testCfTreeLeafIntegrity20_4_1(self):
        self.templateCfTreeLeafIntegrity(20, 4, 1, 0.0)
       
    def testCfTreeLeafIntegrity20_4_2(self):
        self.templateCfTreeLeafIntegrity(20, 4, 2, 0.0)
           
    def testCfTreeLeafIntegrity40_10_5(self):
        self.templateCfTreeLeafIntegrity(40, 10, 5, 0.0)
          
          
    def testCfTreeEntryAbsorbing(self):
        tree = cftree(2, 1, 10000.0)
        absorbing_entry = cfentry(0, [0.0, 0.0], 0.0)
          
        for offset in range(0, 10):
            cluster = [[random() + offset, random() + offset] for i in range(10)]
            entry = cfentry(len(cluster), linear_sum(cluster), square_sum(cluster))

            absorbing_entry += entry

            tree.insert(entry)

            assert 1 == tree.amount_entries
            assert 1 == tree.amount_nodes
            assert 1 == tree.height
              
            assert None == tree.root.parent
            assert absorbing_entry == tree.root.feature
    
    
    def templateCfTreeTotalNumberPoints(self, number_points, dimension, branching_factor, number_entries, diameter):
        tree = cftree(branching_factor, number_entries, diameter)
         
        for index_point in range(0, number_points):
            point = [index_point for i in range(0, dimension)]
             
            tree.insert_point(point)
             
            number_points = 0
            for leaf in tree.leafes:
                number_points += leaf.feature.number_points
                 
            assert (index_point + 1) == number_points;
         
        number_leaf_points = 0
        for leaf in tree.leafes:
            number_leaf_points += leaf.feature.number_points
         
        assert number_points == tree.root.feature.number_points
         
        if number_points != number_leaf_points:
            print(number_points, number_leaf_points)
             
        assert number_points == number_leaf_points;
    
    def testCfTreeTotalNumberPoints10_1_5_5_NoDiameter(self):
        self.templateCfTreeTotalNumberPoints(10, 1, 5, 5, 0.0)
 
    def testCfTreeTotalNumberPoints10_1_5_5_WithDiameter(self):
        self.templateCfTreeTotalNumberPoints(10, 1, 5, 5, 100.0)
        
    def testCfTreeTotalNumberPoints10_1_5_5_WithSmallDiameter(self):
        self.templateCfTreeTotalNumberPoints(10, 1, 5, 5, 2.5)
         
    def testCfTreeTotalNumberPoints10_2_5_5_NoDiameter(self):
        self.templateCfTreeTotalNumberPoints(10, 2, 5, 5, 0.0)
  
    def testCfTreeTotalNumberPoints10_2_5_5_WithDiameter(self):
        self.templateCfTreeTotalNumberPoints(10, 2, 5, 5, 100.0)
  
    def testCfTreeTotalNumberPoints50_3_5_5_NoDiameter(self):
        self.templateCfTreeTotalNumberPoints(50, 3, 5, 5, 0.0)
          
    def testCfTreeTotalNumberPoints50_3_5_5_WithDiameter(self):
        self.templateCfTreeTotalNumberPoints(50, 3, 5, 5, 100.0)
          
    def testCfTreeTotalNumberPoints100_2_2_1_NoDiameter(self):
        self.templateCfTreeTotalNumberPoints(100, 2, 2, 1, 0.0)
    
    def testCfTreeTotalNumberPoints100_2_2_1_WithDiameter(self):
        self.templateCfTreeTotalNumberPoints(100, 2, 2, 1, 100.0)
         
    def testCfTreeTotalNumberPoints100_2_5_5_WithSmallDiameter(self):
        self.templateCfTreeTotalNumberPoints(100, 2, 5, 5, 10.0)


    def templateTreeHeight(self, number_points, branching_factor):
        tree = cftree(branching_factor, 1, 0.1)
         
        for index_point in range(0, number_points):
            point = [index_point]
            tree.insert_point(point)
        
        assert math.floor(math.log(number_points, branching_factor)) <= tree.height;
    
    
    def testObtainNodesFromTheLevel_7_2(self):
        self.templateTreeHeight(7, 2)
    
    def testObtainNodesFromTheLevel_63_2(self):
        self.templateTreeHeight(63, 2)
    
    def testObtainNodesFromTheLevel_40_3(self):
        self.templateTreeHeight(40, 3)
    
    def testObtainNodesFromTheLevel_21_4(self):
        self.templateTreeHeight(21, 4)
    
    def testObtainNodesFromTheLevel_156_5(self):
        self.templateTreeHeight(156, 5)


    def templateLevelNodeObtaining(self, number_points, branching_factor):
        tree = cftree(branching_factor, 1, 0.1)
         
        for index_point in range(0, number_points):
            point = [index_point]
            tree.insert_point(point)
        
        total_node_amount = 0
        for level in range(0, tree.height):
            nodes = tree.get_level_nodes(level)
            total_node_amount += len(nodes)
        
        assert tree.amount_nodes == total_node_amount;

    def testLevelNodeObtaining_7_2(self):
        self.templateLevelNodeObtaining(7, 2)

    def testLevelNodeObtaining_10_2(self):
        self.templateLevelNodeObtaining(10, 2)

    def testLevelNodeObtaining_7_3(self):
        self.templateLevelNodeObtaining(7, 3)

    def testLevelNodeObtaining_20_3(self):
        self.templateLevelNodeObtaining(20, 3)

    def testLevelNodeObtaining_26_3(self):
        self.templateLevelNodeObtaining(26, 3)

    def testLevelNodeObtaining_16_4(self):
        self.templateLevelNodeObtaining(16, 4)

    def testLevelNodeObtaining_34_4(self):
        self.templateLevelNodeObtaining(34, 4)


    def templateLeafNodeAndEntriesAmount(self, number_points, branching_factor):
        tree = cftree(branching_factor, 1, 0.1)
        
        current_size = 0
        for index_point in range(0, number_points):
            point = [index_point]
            tree.insert_point(point)
            
            current_size += 1
            
            assert current_size == tree.amount_entries
            assert current_size == len(tree.leafes)
        
        assert number_points == tree.amount_entries
        assert number_points == len(tree.leafes)
    
    def testLeafNodeAndEntriesAmount_5_2(self):
        self.templateLeafNodeAndEntriesAmount(5, 2)

    def testLeafNodeAndEntriesAmount_10_2(self):
        self.templateLeafNodeAndEntriesAmount(10, 2)

    def testLeafNodeAndEntriesAmount_6_3(self):
        self.templateLeafNodeAndEntriesAmount(6, 3)

    def testLeafNodeAndEntriesAmount_18_3(self):
        self.templateLeafNodeAndEntriesAmount(18, 3)

    def testLeafNodeAndEntriesAmount_16_4(self):
        self.templateLeafNodeAndEntriesAmount(16, 4)


    def templateCorrectEntryDiameter(self, sample_path, branching_factor, diameter):
        sample = read_sample(sample_path)
        tree = cftree(branching_factor, 100, diameter)
        for index_point in range(len(sample)):
            tree.insert_point(sample[index_point])

        leaf_nodes = tree.leafes
        for node in leaf_nodes:
            for entry in node.entries:
                self.assertLessEqual(entry.get_diameter(), diameter)

    def testCorrectEntryDiameterSimple1(self):
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 0.01)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 0.1)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 0.5)

    def testCorrectEntryDiameterSimple2(self):
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 0.01)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 0.1)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 0.5)

    def testCorrectEntryDiameterSimple3(self):
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0.01)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0.1)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 1.0)

    def testCorrectEntryDiameterSimple4(self):
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, 0.01)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, 0.1)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, 1.0)

    def testCorrectEntryDiameterSimple5(self):
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 5, 0.01)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 5, 0.1)
        self.templateCorrectEntryDiameter(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 5, 1.0)

    def testCorrectEntryDiameterLsun(self):
        self.templateCorrectEntryDiameter(FCPS_SAMPLES.SAMPLE_LSUN, 200, 0.01)
        self.templateCorrectEntryDiameter(FCPS_SAMPLES.SAMPLE_LSUN, 200, 0.1)
        self.templateCorrectEntryDiameter(FCPS_SAMPLES.SAMPLE_LSUN, 200, 1.0)

    def testCorrectEntryDiameterTarget(self):
        self.templateCorrectEntryDiameter(FCPS_SAMPLES.SAMPLE_TARGET, 200, 0.5)
