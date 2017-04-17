"""!

@brief Unit-tests for OPTICS algorithm.

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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.cluster.optics import optics, ordering_analyser, ordering_visualizer;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

class Test(unittest.TestCase):
    def templateClusteringResults(self, path, radius, neighbors, amount_clusters, expected_length_clusters, ccore):
        sample = read_sample(path);
        
        optics_instance = optics(sample, radius, neighbors, amount_clusters, ccore);
        optics_instance.process();
        
        clusters = optics_instance.get_clusters();
        noise = optics_instance.get_noise();
        
        assert sum([len(cluster) for cluster in clusters]) + len(noise) == len(sample);
        assert len(clusters) == len(expected_length_clusters);
        assert sum([len(cluster) for cluster in clusters]) == sum(expected_length_clusters);
        assert sorted([len(cluster) for cluster in clusters]) == sorted(expected_length_clusters);
        
        if (amount_clusters is not None):
            analyser = ordering_analyser(optics_instance.get_ordering());
            assert len(analyser) > 0;
            
            amount_clusters, borders = analyser.extract_cluster_amount(optics_instance.get_radius());
            assert amount_clusters == len(expected_length_clusters);
            assert len(borders) == amount_clusters - 1;


    def testClusteringSampleSimple1(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, None, [5, 5], False);
      
    def testClusteringSampleSimple1ByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.4, 2, None, [5, 5], True);

    def testClusteringSampleSimple2(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, None, [5, 8, 10], False);
  
    def testClusteringSampleSimple2ByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 2, None, [5, 8, 10], True);
  
    def testClusteringSampleSimple3(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, None, [10, 10, 10, 30], False);
  
    def testClusteringSampleSimple3ByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3, None, [10, 10, 10, 30], True);
  
    def testClusteringSampleSimple4(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, None, [15, 15, 15, 15, 15], False);
  
    def testClusteringSampleSimple4ByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3, None, [15, 15, 15, 15, 15], True);
  
    def testClusteringSampleSimple5(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, None, [15, 15, 15, 15], False);
  
    def testClusteringSampleSimple5ByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3, None, [15, 15, 15, 15], True);
  
    def testClusteringHepta(self):
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3, None, [30, 30, 30, 30, 30, 30, 32], False);
  
    def testClusteringOneDimensionDataSampleSimple7(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2.0, 2, None, [10, 10], False);
  
    def testClusteringHeptaByCore(self):
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3, None, [30, 30, 30, 30, 30, 30, 32], True);
  
    def testClusteringOneDimensionDataSampleSimple9(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 3.0, 3, None, [10, 20], False);
  
    def testClusteringOneDimensionDataSampleSimple9ByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 3.0, 3, None, [10, 20], True);
  
    def testClusteringSampleSimple2RadiusGreater(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5.0, 2, 3, [5, 8, 10], False);
  
    def testClusteringSampleSimple2RadiusGreaterByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5.0, 2, 3, [5, 8, 10], True);
  
    def testClusteringSampleSimple3RadiusGreater(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5.0, 3, 4, [10, 10, 10, 30], False);
  
    def testClusteringSampleSimple3RadiusGreaterByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5.0, 3, 4, [10, 10, 10, 30], True);
  
    def testClusteringSampleSimple4RadiusGreater(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 6.0, 3, 5, [15, 15, 15, 15, 15], False);
  
    def testClusteringSampleSimple4RadiusGreaterByCore(self):
        self.templateClusteringResults(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 6.0, 3, 5, [15, 15, 15, 15, 15], True);
  
    def testClusteringLsunRadiusGreater(self):
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_LSUN, 1.0, 3, 3, [99, 100, 202], False);
  
    def testClusteringLsunRadiusGreaterByCore(self):
        self.templateClusteringResults(FCPS_SAMPLES.SAMPLE_LSUN, 1.0, 3, 3, [99, 100, 202], True);
  
    def testClusteringOrderVisualizer(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4);
           
        optics_instance = optics(sample, 6.0, 3, 5);
        optics_instance.process();
           
        analyser = ordering_analyser(optics_instance.get_ordering());
        ordering_visualizer.show_ordering_diagram(analyser, 5);
     
    def testClusterOrderingOneClusterExtraction(self):
        analyser = ordering_analyser([5.0, 5.0, 5.0, 5.0, 5.0, 5.0]);
        
        amount_clusters, borders = analyser.extract_cluster_amount(6.5);
        assert 1 == amount_clusters;
        assert 0 == len(borders);
        
        amount_clusters, borders = analyser.extract_cluster_amount(4.5);
        assert 0 == amount_clusters;
        assert 0 == len(borders);
      
    def testImpossibleClusterOrderingAllocationHomogeneous(self):
        analyser = ordering_analyser([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]);
        amount_clusters, borders = analyser.calculate_connvectivity_radius(2);
        assert None == amount_clusters;
        assert 0 == len(borders);
      
    def testImpossibleClusterOrderingAllocationGeterogeneous(self):
        analyser = ordering_analyser([5.0, 5.0, 5.0, 5.0, 6.0, 8.0, 6.0, 5.0, 5.0, 5.0]);
        amount_clusters, borders = analyser.calculate_connvectivity_radius(3);
        assert None == amount_clusters;
        assert 0 == len(borders);


if __name__ == "__main__":
    unittest.main();