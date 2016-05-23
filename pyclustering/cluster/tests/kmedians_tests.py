"""!

@brief Unit-tests for K-Medians algorithm.

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

from pyclustering.cluster.kmedians import kmedians;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from random import random;


class Test(unittest.TestCase):
    def templateLengthProcessData(self, path_to_file, start_centers, expected_cluster_length, ccore = False):
        sample = read_sample(path_to_file);
        
        kmedians_instance = kmedians(sample, start_centers, 0.025, ccore);
        kmedians_instance.process();
        
        clusters = kmedians_instance.get_clusters();
        
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        assert len(sample) == sum(obtained_cluster_sizes);
        
        if (expected_cluster_length is not None):
            obtained_cluster_sizes.sort();
            expected_cluster_length.sort();
            if (obtained_cluster_sizes != expected_cluster_length):
                print(obtained_cluster_sizes);
            assert obtained_cluster_sizes == expected_cluster_length;
    
    def testClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5]);
     
    def testClusterAllocationSampleSimple1Core(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True);
     
    def testClusterOneAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10]);
 
    def testClusterOneAllocationSampleSimple1Core(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10], True);
 
    def testClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8]);
 
    def testClusterAllocationSampleSimple2Core(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], True);
 
    def testClusterOneAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23]);
     
    def testClusterOneAllocationSampleSimple2Core(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23], True);
 
    def testClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30]);
 
    def testClusterAllocationSampleSimple3Core(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], True);
 
    def testClusterOneAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60]);
 
    def testClusterOneAllocationSampleSimple3Core(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60], True);
 
    def testClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15]);
 
    def testClusterAllocationSampleSimple5Core(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], True);
 
    def testClusterOneAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60]);
 
    def testClusterOneAllocationSampleSimple5Core(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60], True);
 
    def testClusterAllocationSample1WrongInitialNumberCenters(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.8, 9.5], [3.5, 6.6], [1.3, 4.0]], None);
 
    def testClusterAllocationSample1WrongInitialNumberCentersCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.8, 9.5], [3.5, 6.6], [1.3, 4.0]], None, True);
 
    def testClusterAllocationSample2WrongInitialNumberCenters(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5], [7.3, 4.5], [3.1, 5.4]], None);
 
    def testClusterAllocationSample2WrongInitialNumberCentersCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5], [7.3, 4.5], [3.1, 5.4]], None, True);
 
    def testDifferentDimensions(self):
        kmedians_instance = kmedians([ [0, 1, 5], [0, 2, 3] ], [ [0, 3] ]);
        self.assertRaises(NameError, kmedians_instance.process);
 
 
    def templateClusterAllocationOneDimensionData(self, ccore = False):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ];
         
        kmedians_instance = kmedians(input_data, [ [0.0], [3.0], [5.0], [8.0] ], 0.025, ccore);
        kmedians_instance.process();
        clusters = kmedians_instance.get_clusters();
         
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;
                 
    def testClusterAllocationOneDimensionData(self):
        self.templateClusterAllocationOneDimensionData();
     
    def testClusterAllocationOneDimensionDataCore(self):
        self.templateClusterAllocationOneDimensionData(True);
     
     
    def templateClusterAllocationTheSameObjects(self, number_objects, number_clusters, ccore_flag = False):
        value = random();
        input_data = [ [value] ] * number_objects;
         
        initial_centers = [];
        for i in range(number_clusters):
            initial_centers.append([ random() ]);
         
        kmedians_instance = kmedians(input_data, initial_centers, ccore_flag);
        kmedians_instance.process();
        clusters = kmedians_instance.get_clusters();
         
        object_mark = [False] * number_objects;
        allocated_number_objects = 0;
         
        for cluster in clusters:
            for index_object in cluster: 
                assert (object_mark[index_object] == False);    # one object can be in only one cluster.
                 
                object_mark[index_object] = True;
                allocated_number_objects += 1;
             
        assert (number_objects == allocated_number_objects);    # number of allocated objects should be the same.
 
    def testClusterAllocationTheSameObjectsOneInitialCenter(self):
        self.templateClusterAllocationTheSameObjects(20, 1, False);
     
    def testClusterAllocationTheSameObjectsOneInitialCenterCore(self):
        self.templateClusterAllocationTheSameObjects(20, 1, True);
 
    def testClusterAllocationTheSameObjectsTwoInitialCenters(self):
        self.templateClusterAllocationTheSameObjects(15, 2, False);
 
    def testClusterAllocationTheSameObjectsTwoInitialCentersCore(self):
        self.templateClusterAllocationTheSameObjects(15, 2, True);
 
    def testClusterAllocationTheSameObjectsThreeInitialCenters(self):
        self.templateClusterAllocationTheSameObjects(25, 3, False);
 
    def testClusterAllocationTheSameObjectsThreeInitialCentersCore(self):
        self.templateClusterAllocationTheSameObjects(25, 3, True);
    
    def testClusterAllocationSampleRoughMediansSimple10(self):
        initial_medians = [[0.0772944481804071, 0.05224990900863469], [1.6021689021213712, 1.0347579135245601], [2.3341008076636096, 1.280022869739064]];
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, initial_medians, None);

    def testClusterAllocationSampleRoughMediansSimple10ByCore(self):
        initial_medians = [[0.0772944481804071, 0.05224990900863469], [1.6021689021213712, 1.0347579135245601], [2.3341008076636096, 1.280022869739064]];
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, initial_medians, None, True);


if __name__ == "__main__":
    unittest.main();