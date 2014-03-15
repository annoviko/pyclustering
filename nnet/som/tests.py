import unittest

from nnet.som import som;
from nnet.som import type_conn;

from support import read_sample;

from samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

class Test(unittest.TestCase):

    def testHoneycombStruct(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
        network = som(3, 4, sample, 200, type_conn.honeycomb);
        
        assert sorted(network.neighbors[0]) == sorted([1, 4, 5]);
        assert sorted(network.neighbors[6]) == sorted([1, 2, 7, 10, 9, 5]);
        assert sorted(network.neighbors[3]) == sorted([2, 7]);
        assert sorted(network.neighbors[11]) == sorted([7, 10]);
        assert sorted(network.neighbors[9]) == sorted([8, 5, 6, 10]);
        
        
        network = som(4, 4, sample, 200, type_conn.honeycomb);
        assert sorted(network.neighbors[11]) == sorted([7, 10, 15]);
        assert sorted(network.neighbors[9]) == sorted([8, 5, 6, 10, 13, 14]);
        
        
        network = som(2, 2, sample, 200, type_conn.honeycomb);
        assert sorted(network.neighbors[0]) == sorted([1, 3, 2]);
        assert sorted(network.neighbors[1]) == sorted([0, 3]);
        assert sorted(network.neighbors[2]) == sorted([0, 3]);
        assert sorted(network.neighbors[3]) == sorted([2, 0, 1]);
        
        
    def testGridFourStruct(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
        network = som(4, 4, sample, 200, type_conn.grid_four);
         
        assert sorted(network.neighbors[0]) == sorted([1, 4]);
        assert sorted(network.neighbors[2]) == sorted([1, 6, 3]);
        assert sorted(network.neighbors[10]) == sorted([9, 6, 11, 14]);
        assert sorted(network.neighbors[11]) == sorted([7, 10, 15]);
         
        network = som(1, 4, sample, 200, type_conn.grid_four);
        assert network.neighbors[0] == [1];
        assert sorted(network.neighbors[1]) == sorted([0, 2]); 
        assert sorted(network.neighbors[2]) == sorted([1, 3]); 
        assert network.neighbors[3] == [2];
    
    
    def templateTestAwardNeurons(self, file, rows, cols, time, expected_result, autostop = False):
        types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb];
        sample = read_sample(file);
        
        for stucture in types:
            network = som(rows, cols, sample, time, stucture);
            network.train(autostop);
            
            #print(sorted(network._award));
            
            assert sorted(network._award) == expected_result;
            
            total_capture_points = 0;
            for points in network._capture_objects:
                total_capture_points += len(points);
                
            assert total_capture_points == sum(expected_result);
    
    
    def testTwoNeuronsTwoClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5]);
        
    
    def testAutostopTwoNeuronsTwoClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 2, 100, [5, 5], True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1, 100, [5, 5], True);        
        
        
    def testThreeNeuronsThreeClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10]);
        
    
    def testAutostopThreeNeuronsThreeClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 3, 100, [5, 8, 10], True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1, 100, [5, 8, 10], True);        
    
    
    def testFourNeuronsFourClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30]);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30]);
    
    
    def testAutostopFourNeuronsFourClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 4, 100, [10, 10, 10, 30], True);
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 2, 100, [10, 10, 10, 30], True);
    
    
    def testTwoNeuronsFourClusters(self):
        self.templateTestAwardNeurons(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 2, 100, [30, 30]); 
    
    
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
    