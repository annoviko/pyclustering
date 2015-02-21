'''

Unit-tests for Hierarchical Sync (HSyncNet) algorithm.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import unittest;

from pyclustering.nnet import *;

from pyclustering.support import read_sample, read_image;

from pyclustering.cluster.hsyncnet import hsyncnet;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, IMAGE_MAP_SAMPLES;

class Test(unittest.TestCase):
    def templateClustering(self, path, number_clusters, expected_length_clusters, solver, ccore_flag):
        result_testing = False;
        
        # If phases crosses each other because of random part of the network then we should try again.
        for attempt in range(0, 3, 1):
            sample = read_sample(path);
            network = hsyncnet(sample, number_clusters, initial_type.EQUIPARTITION, ccore = ccore_flag); # EQUIPARTITION - makes test more stable.
            
            (t, d) = network.process(order = 0.997, solution = solver, collect_dynamic = True);
            clusters = network.get_clusters();
            
            if (sum([len(cluster) for cluster in clusters]) != sum(expected_length_clusters)):
                continue;
            
            if (sorted([len(cluster) for cluster in clusters]) != expected_length_clusters):
                if (sorted([len(cluster) for cluster in clusters]) != expected_length_clusters):
                    continue;
            
            # Unit-test is passed
            result_testing = True;
            break;
        
        assert result_testing;
        
    
    def testClusteringSampleSimple1(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.FAST, False);
        
    def testClusteringOneAllocationSampleSimple1(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10], solve_type.FAST, False);
        
    def testClusteringSampleSimple1ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.FAST, True);
        
    def testClusteringOneAllocationSampleSimple1ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, [10], solve_type.FAST, True);
        
    def testClusteringSampleSimple2(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [5, 8, 10], solve_type.FAST, False);
        
    def testClusteringOneAllocationSampleSimple2(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23], solve_type.FAST, False);    

    def testClusteringSampleSimple2ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, [5, 8, 10], solve_type.FAST, True);

    def testClusteringOneAllocationSampleSimple2ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, [23], solve_type.FAST, True);
    
    
    def testClusteringSolverRK4SampleSimple1(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.RK4, False);
        
    def testClusteringSolverRK4SampleSimple1ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.RK4, True);
        
    def testClusteringSolverRKF45SampleSimple1ByCore(self):
        self.templateClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, [5, 5], solve_type.RKF45, True);        
           
    
    def testCreationDeletionByCore(self):
        # Crash occurs in case of memory leak
        data = read_image(IMAGE_MAP_SAMPLES.IMAGE_WHITE_SEA_SMALL);
        
        for iteration in range(0, 15):
            network = hsyncnet(data, 2, ccore = True);
            del network;
        
        
if __name__ == "__main__":
    unittest.main();