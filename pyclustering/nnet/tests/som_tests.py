"""!

@brief Unit-tests for self-organized feature map.

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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.nnet.som import som, type_conn, type_init;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;
from pyclustering.nnet.som import som_parameters;

class Test(unittest.TestCase):   
    def templateTestAwardNeurons(self, file, rows, cols, time, expected_result, autostop = False, ccore_flag = False, parameters = None):
        types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb];
        sample = read_sample(file);
         
        if (parameters is None):
            parameters = som_parameters();
         
        for stucture in types:
            network = som(rows, cols, stucture, parameters, ccore = ccore_flag);
            network.train(sample, time, autostop);
             
            if (sorted(network.awards) != expected_result):
                network.show_network(awards = True);
                print(sorted(network.awards));
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
         
         
    def testOneDimensionSampleSimple7Cluster(self):
        parameters = som_parameters();
        parameters.init_type = type_init.random_surface;
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 1, 100, [10, 10], True, False, parameters);
   
   
    def testOneDimensionSampleSimple7ClusterByCore(self):
        parameters = som_parameters();
        parameters.init_type = type_init.random_surface;
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 1, 100, [10, 10], True, True, parameters);
           
         
    def testHighEpochs(self):
        # This test requires too much time for execution
        epochs = 1000;
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, epochs, [5, 5]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, epochs, [5, 5]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, epochs, [10, 10, 10, 30]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, epochs, [10, 10, 10, 30]);
 
 
    def templateTestWinners(self, ccore_flag):
        types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb];
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
                
        for stucture in types:
            network = som(5, 5, stucture, ccore = ccore_flag);
            network.train(sample, 100);
                    
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
         
    def testDoubleTrain(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
         
        parameters = som_parameters();
        network = som(2, 2, type_conn.grid_eight, parameters, ccore = False);
         
        network.train(sample, 100, False);
        network.train(sample, 100, False);
         
        assert sum(network.awards) == len(sample);
         
        total_capture_points = 0;
        for points in network.capture_objects:
            total_capture_points += len(points);
         
        assert total_capture_points == len(sample);

    def testSomVisualization(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4);
        
        parameters = som_parameters();
        network = som(5, 5, type_conn.grid_eight, parameters, ccore = True);
        network.train(sample, 100, True);
        
        network.show_network();
        network.show_winner_matrix();
        network.show_distance_matrix();
        network.show_density_matrix();

if __name__ == "__main__":
    unittest.main();
    