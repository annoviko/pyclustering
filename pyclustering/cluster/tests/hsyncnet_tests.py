"""!

@brief Unit-tests for Hierarchical Sync (HSyncNet) algorithm.

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

from pyclustering.nnet import *;

from pyclustering.utils import read_sample;

from pyclustering.cluster.hsyncnet import hsyncnet;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

class Test(unittest.TestCase):
    def templateClustering(self, path, number_clusters, expected_length_clusters, solver, initial_neighbors, increase_persent, collect_dynamic_flag, ccore_flag):
        result_testing = False;
        
        # If phases crosses each other because of random part of the network then we should try again.
        for _ in range(0, 3, 1):
            sample = read_sample(path);
            network = hsyncnet(sample, number_clusters, initial_type.EQUIPARTITION, initial_neighbors, increase_persent, ccore = ccore_flag);
            
            analyser = network.process(order = 0.997, solution = solver, collect_dynamic = collect_dynamic_flag);
            clusters = analyser.allocate_clusters(0.1);
            
            if (sum([len(cluster) for cluster in clusters]) != sum(expected_length_clusters)):
                continue;
            
            if (sorted([len(cluster) for cluster in clusters]) != expected_length_clusters):
                if (sorted([len(cluster) for cluster in clusters]) != sorted(expected_length_clusters)):
                    continue;
            
            # Unit-test is passed
            result_testing = True;
            break;
        
        assert result_testing;
        
    
    def testClusteringSampleSimple1(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.FAST, 5, 0.3, True, False);
         
    def testClusteringOneAllocationSampleSimple1(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10], solve_type.FAST, 5, 0.3, True, False);
    
    def testClusteringSampleSimple1WithoutCollecting(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.FAST, 5, 0.3, False, False);
    
    def testClusteringSampleSimple1WithoutCollectingByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.FAST, 5, 0.3, False, True);
    
    def testClusteringSampleSimple1ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.FAST, 5, 0.3, True, True);
         
    def testClusteringOneAllocationSampleSimple1ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10], solve_type.FAST, 5, 0.3, True, True);
    
    def testClusteringSampleSimple2(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [10, 5, 8], solve_type.FAST, 5, 0.2, True, False);
    
    def testClusteringSampleSimple2ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [10, 5, 8], solve_type.FAST, 5, 0.2, True, True);

    def testClusteringOneAllocationSampleSimple2(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23], solve_type.FAST, 5, 0.2, True, False);
    
    def testClusteringOneAllocationSampleSimple2ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23], solve_type.FAST, 5, 0.2, True, True);
    
    def testClusteringOneDimensionDataSampleSimple7(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, [10, 10], solve_type.FAST, 5, 0.3, True, False);

    def testClusteringOneDimensionDataSampleSimple7ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, [10, 10], solve_type.FAST, 5, 0.3, True, True);


if __name__ == "__main__":
    unittest.main();