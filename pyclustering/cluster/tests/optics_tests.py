"""!

@brief Unit-tests for OPTICS algorithm.

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

from pyclustering.cluster.optics import optics;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

class Test(unittest.TestCase):
    def templateClusteringResults(self, path, radius, neighbors, expected_length_clusters, ccore):
        sample = read_sample(path);
        
        optics_instance = optics(sample, radius, neighbors);
        optics_instance.process();
        
        clusters = optics_instance.get_clusters();
        noise = optics_instance.get_noise();
        
        assert sum([len(cluster) for cluster in clusters]) + len(noise) == len(sample);
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        assert sorted([len(cluster) for cluster in clusters]) == sorted(expected_length_clusters);
    
    def testClusteringSampleSimple1(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, [5, 5], False);
    
    def testClusteringSampleSimple2(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, [5, 8, 10], False);

    def testClusteringSampleSimple3(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, [10, 10, 10, 30], False);
        
    def testClusteringSampleSimple4(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, [15, 15, 15, 15, 15], False);

    def testClusteringSampleSimple5(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, [15, 15, 15, 15], False);
        
    def testClusteringHepta(self):
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3, [30, 30, 30, 30, 30, 30, 32], False);
    
    
    def testClusteringOneDimensionDataSampleSimple7(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2.0, 2, [10, 10], False);
    
    def testClusteringOneDimensionDataSampleSimple9(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 3.0, 3, [10, 20], False);
    
    
if __name__ == "__main__":
    unittest.main();