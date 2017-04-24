"""!

@brief Unit-tests for SOM-SC algorithm.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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

from pyclustering.cluster.somsc import somsc;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from random import random;


class Test(unittest.TestCase):
    def templateLengthProcessData(self, path_to_file, amount_clusters, expected_cluster_length, ccore = False):
        sample = read_sample(path_to_file);
        
        somsc_instance = somsc(sample, amount_clusters, 100, ccore);
        somsc_instance.process();
        
        clusters = somsc_instance.get_clusters();

        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        assert len(sample) == sum(obtained_cluster_sizes);
        
        if (expected_cluster_length != None):
            obtained_cluster_sizes.sort();
            expected_cluster_length.sort();
            if (obtained_cluster_sizes != expected_cluster_length):
                print 
            assert obtained_cluster_sizes == expected_cluster_length;

    def testClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5]);

    def testClusterAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], True);

    def testClusterOneAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10]);

    def testClusterOneAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10], True);

    def testClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [10, 5, 8]);

    def testClusterAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [10, 5, 8], True);

    def testClusterOneAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23]);

    def testClusterOneAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23], True);

    def testClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [10, 10, 10, 30]);

    def testClusterAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, [10, 10, 10, 30], True); 

    def testClusterOneAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, [60]);

    def testClusterOneAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, [60], True); 

    def testClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, [15, 15, 15, 15, 15]);

    def testClusterAllocationSampleSimple4ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, [15, 15, 15, 15, 15], True);

    def testClusterOneAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, [75]);

    def testClusterOneAllocationSampleSimple4ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, [75], True);

    def testClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, [15, 15, 15, 15]);

    def testClusterAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, [15, 15, 15, 15], True);

    def testClusterOneAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, [60]);

    def testClusterOneAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, [60], True);

    def testClusterOneDimensionSampleSimple7(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, [10, 10]);

    def testClusterOneDimensionSampleSimple7ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, [10, 10], True);

    def testClusterOneDimensionSampleSimple8(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 4, None);

    def testClusterOneDimensionSampleSimple8ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 4, None, True);

    def testWrongNumberOfCentersSimpleSample1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, None);

    def testWrongNumberOfCentersSimpleSample1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3, None, True);

    def testWrongNumberOfCentersSimpleSample2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 4, None);

    def testWrongNumberOfCentersSimpleSample2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 4, None, True);

    def templateClusterAllocationOneDimensionData(self, ccore_flag):
        input_data = [ [random()] for i in range(10) ] + [ [random() + 3] for i in range(10) ] + [ [random() + 5] for i in range(10) ] + [ [random() + 8] for i in range(10) ];

        somsc_instance = somsc(input_data, 4, 100, ccore_flag);
        somsc_instance.process();
        clusters = somsc_instance.get_clusters();

        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;

    def testClusterAllocationOneDimensionData(self):
        self.templateClusterAllocationOneDimensionData(False);

    def testClusterAllocationOneDimensionDataByCore(self):
        self.templateClusterAllocationOneDimensionData(True);


if __name__ == "__main__":
    unittest.main();