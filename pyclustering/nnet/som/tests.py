import unittest;

from pyclustering.nnet.som import som;
from pyclustering.nnet.som import type_conn;

from pyclustering.support import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

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
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30], True, True); 
        
        
    def testAutostopTwoNeuronsFourClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30], True); 
      
      
    def testSevenNeuronsHeptaClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32]); 
      
      
    def testAutostopSevenNeuronsHeptaClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 7, 100, [30, 30, 30, 30, 30, 30, 32], True); 
      
      
    def testFourNeuronsTetraClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100]);
      
      
    def testAutostopFourNeuronsTetraClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TETRA, 1, 4, 100, [100, 100, 100, 100], True);
      
      
    def testTwoNeuronsTwoDiamondsClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400]);
      
      
    def testAutostopTwoNeuronsTwoDiamondsClusters(self):
        self.templateTestAwardNeurons(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1, 2, 100, [400, 400], True);
      
      
    def testFiveNeuronsFiveClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15]);      
      
      
    def testAutostopFiveNeuronsFiveClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 5, 100, [15, 15, 15, 15, 15], True);
      
      
    def testFourNeuronsSquareClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15]);
      
      
    def testAutostopFourNeuronsSquareClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 2, 2, 100, [15, 15, 15, 15], True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 4, 100, [15, 15, 15, 15], True);
      
      
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
      
      
    def testWinners(self):
        types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb];
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
          
        for stucture in types:
            network = som(5, 5, sample, 100, stucture);
            network.train();
              
            assert sum(network._award) == 60;
              
            points = list();
            for i in range(network.size):
                if (network._award[i] > 0):
                    points += network._capture_objects[i];
              
            assert len(points) == len(sample);
              
            points = sorted(points);
            for i in range(len(points)):
                assert points[i] == i;
             
         
if __name__ == "__main__":
    unittest.main();
    