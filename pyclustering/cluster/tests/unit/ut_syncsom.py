"""!

@brief Unit-tests for SYNC-SOM algorithm.

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


import unittest;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.syncsom import syncsom;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class SyncsomUnitTest(unittest.TestCase):
    def templateLengthSomCluster(self, file, som_map_size, radius, eps):
        sample = read_sample(file);
        
        network = syncsom(sample, som_map_size[0], som_map_size[1], radius);
        network.process(collect_dynamic = False, order = eps);

        # Check unique
        som_clusters = network.get_som_clusters();
        indexes = set();
        
        for som_cluster in som_clusters:
            for index in som_cluster:
                assert (index in indexes) is False;
                indexes.add(index);

    def testSomClusterAllocationSampleSimple1(self):
        self.templateLengthSomCluster(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [3, 3], 1.0, 0.99);

    def testSomClusterAllocationSampleSimple3(self):
        self.templateLengthSomCluster(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [3, 3], 1.0, 0.99);
  
    def testSomClusterAllocationSampleSimple4(self):
        self.templateLengthSomCluster(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [3, 3], 1.0, 0.99);

    def testSomClusterAllocationSampleSimple5(self):
        self.templateLengthSomCluster(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [3, 3], 1.0, 0.99);



    def templateLengthProcessData(self, file, som_map_size, radius, eps, expected_cluster_length):
        result_testing = False;
        
        # If phases crosses each other because of random part of the network then we should try again.
        for _ in range(0, 5, 1):
            sample = read_sample(file);
            network = syncsom(sample, som_map_size[0], som_map_size[1], radius);
            network.process(collect_dynamic = False, order = eps);
            
            clusters = network.get_clusters();
            
            obtained_cluster_sizes = [len(cluster) for cluster in clusters];
            if (len(sample) != sum(obtained_cluster_sizes)):
                continue;
            
            obtained_cluster_sizes.sort();
            expected_cluster_length.sort();
            #print(obtained_cluster_sizes, expected_cluster_length);
            if (obtained_cluster_sizes != expected_cluster_length):
                continue;
            
            # Unit-test is passed
            result_testing = True;
            break;
            
        assert result_testing;
    
    def testClusterAllocationSampleSimple1ByGeaterAmoutNeurons(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [5, 5], 1.0, 0.999, [5, 5]);

    def testClusterAllocationSampleSimple1AsSom(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [1, 2], 1.0, 0.999, [5, 5]);

    def testClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [2, 2], 1.0, 0.999, [5, 5]);

    def testClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [5, 5], 1.0, 0.999, [10, 5, 8]);

    def testClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [5, 5], 1.0, 0.999, [10, 10, 10, 30]);

    def testClusterAllocationOneDimensionDataSampleSimple7AsSom(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [1, 2], 1.0, 0.999, [10, 10]);

    def testClusterAllocationOneDimensionDataSampleSimple7(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, [3, 3], 1.0, 0.999, [10, 10]);

    def testClusterAllocationOneDimensionDataSampleSimple9AsSom(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [1, 2], 1.0, 0.999, [20, 10]);

    def testClusterAllocationOneDimensionDataSampleSimple9(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, [3, 3], 1.0, 0.999, [20, 10]);


    def testShowLayersProcessing(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
        
        network = syncsom(sample, 4, 4, 1.0);
        network.process(collect_dynamic = False, order = 0.99);
        
        network.show_som_layer();
        network.show_sync_layer();
