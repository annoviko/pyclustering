"""!

@brief Unit-tests for K-Medoids algorithm.

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

import math;

from pyclustering.cluster.kmedoids import kmedoids;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from random import random;

class Test(unittest.TestCase):
    def templateLengthProcessData(self, path_to_file, initial_medoids, expected_cluster_length, ccore_flag = False):
        sample = read_sample(path_to_file);
         
        kmedoids_instance = kmedoids(sample, initial_medoids, 0.025, ccore_flag);
        kmedoids_instance.process();
         
        clusters = kmedoids_instance.get_clusters();
     
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        assert len(sample) == sum(obtained_cluster_sizes);
         
        obtained_cluster_sizes.sort();
        expected_cluster_length.sort();
        assert obtained_cluster_sizes == expected_cluster_length;
     
    def testClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5]);

    def testClusterAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 9], [5, 5], True);

    def testClusterOneAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10]);

    def testClusterOneAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5], [10], True);

    def testClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8]);

    def testClusterAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [3, 12, 20], [10, 5, 8], True);

    def testClusterOneAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23]);

    def testClusterOneAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [10], [23], True);

    def testClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 12, 25, 37], [10, 10, 10, 30]);

    def testClusterAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [4, 12, 25, 37], [10, 10, 10, 30], True);

    def testClusterOneAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [30], [60]);

    def testClusterOneAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [30], [60], True);

    def testClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 18, 34, 55], [15, 15, 15, 15]);

    def testClusterAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [4, 18, 34, 55], [15, 15, 15, 15], True);

    def testClusterOneAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [35], [60]);

    def testClusterOneAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [35], [60], True);


    def templateClusterAllocationOneDimensionData(self):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ];
         
        kmedoids_instance = kmedoids(input_data, [ 5, 15, 25, 35 ], 0.025);
        kmedoids_instance.process();
        clusters = kmedoids_instance.get_clusters();
         
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;
                 
    def testClusterAllocationOneDimensionData(self):
        self.templateClusterAllocationOneDimensionData();


    def templateClusterAllocationTheSameObjects(self, number_objects, number_clusters, ccore_flag = False):
        value = random();
        input_data = [ [value] ] * number_objects;
        
        initial_medoids = [];
        step = math.floor(number_objects / number_clusters);
        for i in range(number_clusters):
            initial_medoids.append(i * step);
        
        kmedoids_instance = kmedoids(input_data, initial_medoids);
        kmedoids_instance.process();
        clusters = kmedoids_instance.get_clusters();
        
        object_mark = [False] * number_objects;
        allocated_number_objects = 0;
        
        for cluster in clusters:
            for index_object in cluster: 
                assert (object_mark[index_object] == False);    # one object can be in only one cluster.
                
                object_mark[index_object] = True;
                allocated_number_objects += 1;
            
        assert (number_objects == allocated_number_objects);    # number of allocated objects should be the same.

    def testClusterAllocationTheSameObjectsOneInitialMedoid(self):
        self.templateClusterAllocationTheSameObjects(20, 1, False);

    def testClusterAllocationTheSameObjectsOneInitialMedoidByCore(self):
        self.templateClusterAllocationTheSameObjects(20, 1, True);

    def testClusterAllocationTheSameObjectsTwoInitialMedoids(self):
        self.templateClusterAllocationTheSameObjects(15, 2, False);

    def testClusterAllocationTheSameObjectsTwoInitialMedoidsByCore(self):
        self.templateClusterAllocationTheSameObjects(15, 2, True);

    def testClusterAllocationTheSameObjectsThreeInitialMedoids(self):
        self.templateClusterAllocationTheSameObjects(25, 3, False);

    def testClusterAllocationTheSameObjectsThreeInitialMedoidsByCore(self):
        self.templateClusterAllocationTheSameObjects(25, 3, True);


if __name__ == "__main__":
    unittest.main();
