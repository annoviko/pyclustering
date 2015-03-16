"""!

@brief Unit-tests for self-organized feature map.

@authors Andrei Novikov (spb.andr@yandex.ru)
@date 2014-2015
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

from pyclustering.nnet.som import som;
from pyclustering.nnet.som import type_conn;

from pyclustering.support import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;
from pyclustering.nnet.som import som_parameters

class Test(unittest.TestCase):   
    
    def templateTestAwardNeurons(self, file, rows, cols, time, expected_result, autostop = False, ccore_flag = False):
        types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb];
        sample = read_sample(file);
        
        for stucture in types:
            network = som(rows, cols, sample, time, stucture, ccore = ccore_flag); 
            network.train(autostop);
                
            assert sorted(network.awards) == expected_result;
            
            total_capture_points = 0;
            for points in network.capture_objects:
                total_capture_points += len(points);
                
            assert total_capture_points == sum(expected_result);
        
            del network;
    
    def testTwoNeuronsTwoClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5]);        
 
 
    def testTwoNeuronsTwoClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], False, True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], False, True);         
      
      
    def testAutostopTwoNeuronsTwoClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], True);        
       
       
    def testAutostopTwoNeuronsTwoClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], True, True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], True, True);   
            
           
    def testThreeNeuronsThreeClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10]);
        
                
    def testThreeNeuronsThreeClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10], False, True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10], False, True);    
        
        
    def testAutostopThreeNeuronsThreeClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10], True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10], True);        
        
        
    def testAutostopThreeNeuronsThreeClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10], True, True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10], True, True);    
            
        
    def testFourNeuronsFourClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30]);
      
      
    def testFourNeuronsFourClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30], False, True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30], False, True);
        
        
    def testAutostopFourNeuronsFourClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30], True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30], True);
  
  
    def testAutostopFourNeuronsFourClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30], True, True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30], True, True);
  
        
    def testTwoNeuronsFourClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30]); 
        
        
    def testTwoNeuronsFourClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30], False, True); 
          
          
    def testAutostopTwoNeuronsFourClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30], True); 
      
      
    def testAutostopTwoNeuronsFourClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30], True, True); 
        
      
    def testSevenNeuronsHeptaClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32]); 
        
      
    def testSevenNeuronsHeptaClustersByCore(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32], False, True); 
      
        
    def testAutostopSevenNeuronsHeptaClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32], True); 
      
      
    def testAutostopSevenNeuronsHeptaClustersByCore(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32], True, True);
        
        
    def testFourNeuronsTetraClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100]);
      
      
    def testFourNeuronsTetraClustersByCore(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100], False, True); 
        
      
    def testAutostopFourNeuronsTetraClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100], True);
      
      
    def testAutostopFourNeuronsTetraClustersByCore(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100], True, True);
        
        
    def testTwoNeuronsTwoDiamondsClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400]);
        
        
    def testTwoNeuronsTwoDiamondsClustersByCore(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400], False, True);
           
           
    def testAutostopTwoNeuronsTwoDiamondsClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400], True);
      
      
    def testAutostopTwoNeuronsTwoDiamondsClustersByCore(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400], True, True);
        
      
    def testFiveNeuronsFiveClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15]);      
      
      
    def testFiveNeuronsFiveClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15], False, True);  
      
      
    def testAutostopFiveNeuronsFiveClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15], True);
  
  
    def testAutostopFiveNeuronsFiveClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15], True, True);      
  
        
    def testFourNeuronsSquareClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15]);
      
      
    def testFourNeuronsSquareClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15], False, True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15], False, True);    
        
      
    def testAutostopFourNeuronsSquareClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15], True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15], True);
      
      
    def testAutostopFourNeuronsSquareClustersByCore(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15], True, True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15], True, True);
      
      
    def testHighEpochs(self):
        # This test requires too much time for execution
        epochs = 1000;
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, epochs, [5, 5]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, epochs, [5, 5]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, epochs, [10, 10, 10, 30]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, epochs, [10, 10, 10, 30]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, epochs, [15, 15, 15, 15, 15]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, epochs, [15, 15, 15, 15]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, epochs, [15, 15, 15, 15]);
        
      
    def templateTestWinners(self, ccore_flag):
        types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb];
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
            
        for stucture in types:
            network = som(5, 5, sample, 100, stucture, ccore = ccore_flag);
            network.train();
                
            assert sum(network.awards) == 60;
                
            points = list();
            for i in range(network.size):
                if (network.awards[i] > 0):
                    points += network.capture_objects[i];
                
            assert len(points) == len(sample);
                
            points = sorted(points);
            for i in range(len(points)):
                assert points[i] == i;
      
    def testWinners(self):
        self.templateTestWinners(False);
      
    def testWinnersByCore(self):
        self.templateTestWinners(True);
             
         
if __name__ == "__main__":
    unittest.main();
    