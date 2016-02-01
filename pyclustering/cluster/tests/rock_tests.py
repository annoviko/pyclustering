"""!

@brief Unit-tests for ROCK algorithm.

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

from pyclustering.cluster.rock import rock;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from random import random;

class Test(unittest.TestCase):  
    def templateLengthProcessData(self, path_to_file, radius, cluster_numbers, threshold, expected_cluster_length, ccore = False):
        sample = read_sample(path_to_file);
        
        rock_instance = rock(sample, radius, cluster_numbers, threshold, ccore);
        rock_instance.process();
        clusters = rock_instance.get_clusters();
        
        length = sum([len(cluster) for cluster in clusters]);
        assert len(sample) == length;
        
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        obtained_cluster_sizes.sort();
        expected_cluster_length.sort();
        
        assert obtained_cluster_sizes == expected_cluster_length;


    def testClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 0.5, [5, 5]);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 1, 0.5, [10]);
        
    def testClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 0.5, [10, 5, 8]);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 1, 0.5, [23]);
        
    def testClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 0.5, [10, 10, 10, 30]);
        
    def testClusterAllocationSampleSimple3WrongRadius(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.7, 4, 0.5, [10, 10, 10, 30]);
        
    def testClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 0.5, [15, 15, 15, 15, 15]);    

    def testClusterAllocationSampleSimple4WrongRadius(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1.5, 5, 0.5, [15, 15, 15, 15, 15]);  

    def testClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 0.5, [15, 15, 15, 15]);    
        
    def testClusterAllocationByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 0.5, [5, 5], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 1, 0.5, [10], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 0.5, [10, 5, 8], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 1, 0.5, [23], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 0.5, [10, 10, 10, 30], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.7, 4, 0.5, [10, 10, 10, 30], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 0.5, [15, 15, 15, 15, 15], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1.5, 5, 0.5, [15, 15, 15, 15, 15], True);
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 0.5, [15, 15, 15, 15], True); 
    
    def testClusterAllocationIncorrectNumberClusters(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 4, 0.5, [15, 15, 15, 15, 15]);
    
    def testClusterAllocationByCoreIncorrectNumberOfClusters(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 4, 0.5, [15, 15, 15, 15, 15], True);
    
    
    def templateClusterAllocationOneDimensionData(self, ccore_flag):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ];
        
        rock_instance = rock(input_data, 1, 4, 0.5, ccore_flag);
        rock_instance.process();
        clusters = rock_instance.get_clusters();
        
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;
                
    def testClusterAllocationOneDimensionData(self):
        self.templateClusterAllocationOneDimensionData(False);
        
    def testClusterAllocationOneDimensionDataByCore(self):
        self.templateClusterAllocationOneDimensionData(True);
        

if __name__ == "__main__":
    unittest.main();