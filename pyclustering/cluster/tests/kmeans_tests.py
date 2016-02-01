"""!

@brief Unit-tests for K-Means algorithm.

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

from pyclustering.cluster.kmeans import kmeans;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from random import random;

class Test(unittest.TestCase):
    def templateLengthProcessData(self, path_to_file, start_centers, expected_cluster_length, ccore = False):
        sample = read_sample(path_to_file);
        
        kmeans_instance = kmeans(sample, start_centers, 0.025, ccore);
        kmeans_instance.process();
        
        clusters = kmeans_instance.get_clusters();
    
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        assert len(sample) == sum(obtained_cluster_sizes);
        
        if (expected_cluster_length != None):
            obtained_cluster_sizes.sort();
            expected_cluster_length.sort();
            assert obtained_cluster_sizes == expected_cluster_length;
    
    def testClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5]);
    
    def testClusterAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], True);
    
    def testClusterOneAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10]);
        
    def testClusterOneAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[1.0, 2.5]], [10], True);

    def testClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8]);

    def testClusterAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], True);

    def testClusterOneAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23]);

    def testClusterOneAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[0.5, 0.2]], [23], True);

    def testClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30]);    

    def testClusterAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], True); 

    def testClusterOneAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60]);   

    def testClusterOneAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1]], [60], True); 

    def testClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15]);

    def testClusterAllocationSampleSimple4ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], True);

    def testClusterOneAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[2.0, 5.0]], [75]);

    def testClusterOneAllocationSampleSimple4ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[2.0, 5.0]], [75], True);

    def testClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15]);

    def testClusterAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], True);
  
    def testClusterOneAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60]);

    def testClusterOneAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 0.0]], [60], True);

    def testClusterOneDimensionSampleSimple7(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [[-3.0], [2.0]], [10, 10]);

    def testClusterOneDimensionSampleSimple7ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [[-3.0], [2.0]], [10, 10], True);

    def testClusterOneDimensionSampleSimple8(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-4.0], [3.1], [6.1], [12.0]], [15, 30, 20, 80]);

    def testClusterOneDimensionSampleSimple8ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, [[-4.0], [3.1], [6.1], [12.0]], [15, 30, 20, 80], True);

    def testWrongNumberOfCentersSimpleSample1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.0, 4.5], [3.3, 6.5], [5.0, 7.8]], None);

    def testWrongNumberOfCentersSimpleSample1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[2.0, 4.5], [3.3, 6.5], [5.0, 7.8]], None, True);

    def testWrongNumberOfCentersSimpleSample2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[1.3, 1.5], [5.2, 8.5], [5.0, 7.8], [11.0, -3.0]], None);

    def testWrongNumberOfCentersSimpleSample2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[1.3, 1.5], [5.2, 8.5], [5.0, 7.8], [11.0, -3.0]], None, True);

    def testDifferentDimensions(self):
        kmeans_instance = kmeans([ [0, 1, 5], [0, 2, 3] ], [ [0, 3] ]);
        self.assertRaises(NameError, kmeans_instance.process);
        
        
    def templateClusterAllocationOneDimensionData(self, ccore_flag):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ];
        
        kmeans_instance = kmeans(input_data, [ [0.0], [3.0], [5.0], [8.0] ], 0.025, ccore_flag);
        kmeans_instance.process();
        clusters = kmeans_instance.get_clusters();
        
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;
                
    def testClusterAllocationOneDimensionData(self):
        self.templateClusterAllocationOneDimensionData(False);
        
    def testClusterAllocationOneDimensionDataByCore(self):
        self.templateClusterAllocationOneDimensionData(True);



if __name__ == "__main__":
    unittest.main();
