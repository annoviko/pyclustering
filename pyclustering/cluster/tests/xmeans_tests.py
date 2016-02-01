"""!

@brief Unit-tests for X-Means algorithm.

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

from pyclustering.cluster.xmeans import xmeans, splitting_type;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;


class Test(unittest.TestCase):
    def templateLengthProcessData(self, path_to_file, start_centers, expected_cluster_length, type_splitting, ccore = False):
        sample = read_sample(path_to_file);
        
        #clusters = xmeans(sample, start_centers, 20, ccore);
        xmeans_instance = xmeans(sample, start_centers, 20, 0.025, type_splitting, ccore);
        xmeans_instance.process();
         
        clusters = xmeans_instance.get_clusters();
    
        obtained_cluster_sizes = [len(cluster) for cluster in clusters];
        assert len(sample) == sum(obtained_cluster_sizes);
        
        obtained_cluster_sizes.sort();
        expected_cluster_length.sort();
        assert obtained_cluster_sizes == expected_cluster_length;
    
    def testBicClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION);
  
    def testBicClusterAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
          
    def testBicWrongStartClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION);
   
    def testBicWrongStartClusterAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
     
    def testMndlClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
   
    def testMndlClusterAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5], [6.7, 7.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True);
    
    def testMndlWrongStartClusterAllocationSampleSimple1(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
 
    def testMndlWrongStartClusterAllocationSampleSimple1ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [[3.7, 5.5]], [5, 5], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True);
  
    def testBicClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION);
 
    def testBicClusterAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
   
    def testBicWrongStartClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION);
 
    def testBicWrongStartClusterAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
   
    def testMndlClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
 
    def testMndlClusterAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7], [7.5, 0.5]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True);
  
    def testMndlWrongStartClusterAllocationSampleSimple2(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);  
 
    def testMndlWrongStartClusterAllocationSampleSimple2ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [[3.5, 4.8], [6.9, 7]], [10, 5, 8], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True); 
  
    def testBicClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION);    
 
    def testBicClusterAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION, True); 
   
    def testBicWrongStartClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [5.9, 5.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION); 
 
    def testBicWrongStartClusterAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [5.9, 5.9]], [10, 10, 10, 30], splitting_type.BAYESIAN_INFORMATION_CRITERION, True); 
  
    def testMndlClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);    
 
    def testMndlClusterAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]], [10, 10, 10, 30], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True);
   
    def testMndlWrongStartClusterAllocationSampleSimple3(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [5.9, 5.9]], [10, 10, 10, 30], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);   
 
    def testMndlWrongStartClusterAllocationSampleSimple3ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [[0.2, 0.1], [4.0, 1.0], [5.9, 5.9]], [10, 10, 10, 30], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True); 
   
    def testBicClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION);
 
    def testBicClusterAllocationSampleSimple4ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
   
    def testBicWrongStartClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION);
 
    def testBicWrongStartClusterAllocationSampleSimple4ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
   
    def testMndlClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
 
    def testMndlClusterAllocationSampleSimple4ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]], [15, 15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True);
   
    def testMndlWrongStartClusterAllocationSampleSimple4(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);  
 
    def testMndlWrongStartClusterAllocationSampleSimple4ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0]], [15, 15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True); 
   
    def testBicClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION);
 
    def testBicClusterAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
           
    def testBicWrongStartClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION);
 
    def testBicWrongStartClusterAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
   
    def testMndlClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
 
    def testMndlClusterAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True);
           
    def testMndlWrongStartClusterAllocationSampleSimple5(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);  
 
    def testMndlWrongStartClusterAllocationSampleSimple5ByCore(self):
        self.templateLengthProcessData(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [[0.0, 1.0], [0.0, 0.0]], [15, 15, 15, 15], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True);
  
    def testBicClusterAllocationSampleTwoDiamonds(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400], splitting_type.BAYESIAN_INFORMATION_CRITERION);
 
    def testBicClusterAllocationSampleTwoDiamondsByCore(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
  
    def testBicWrongStartClusterAllocationSampleTwoDiamonds(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2]], [400, 400], splitting_type.BAYESIAN_INFORMATION_CRITERION);
 
    def testBicWrongStartClusterAllocationSampleTwoDiamondsByCore(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2]], [400, 400], splitting_type.BAYESIAN_INFORMATION_CRITERION, True);
 
    def testMndlClusterAllocationSampleTwoDiamonds(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
 
    def testMndlClusterAllocationSampleTwoDiamondsByCore(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2], [3.0, 0.0]], [400, 400], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True);
 
    def testMndlWrongStartClusterAllocationSampleTwoDiamonds(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2]], [400, 400], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH);
 
    def testMndlWrongStartClusterAllocationSampleTwoDiamondsByCore(self):
        self.templateLengthProcessData(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [[0.8, 0.2]], [400, 400], splitting_type.MINIMUM_NOISELESS_DESCRIPTION_LENGTH, True);
           
       
    def templateClusterAllocationOneDimensionData(self, ccore_flag):
        input_data = [ [0.0] for i in range(10) ] + [ [5.0] for i in range(10) ] + [ [10.0] for i in range(10) ] + [ [15.0] for i in range(10) ];
           
        xmeans_instance = xmeans(input_data, [ [0.5], [5.5], [10.5], [15.5] ], 20, 0.025, splitting_type.BAYESIAN_INFORMATION_CRITERION, ccore_flag);
        xmeans_instance.process();
        clusters = xmeans_instance.get_clusters();
           
        assert len(clusters) == 4;
        for cluster in clusters:
            assert len(cluster) == 10;
                   
    def testClusterAllocationOneDimensionData(self):
        self.templateClusterAllocationOneDimensionData(False);
           
    def testClusterAllocationOneDimensionDataByCore(self):
        self.templateClusterAllocationOneDimensionData(True);


if __name__ == "__main__":
    unittest.main();