import unittest

from nnet.som import type_conn;

from nnet.plsom import plsom;

from support import read_sample;

# NOTE! This suite of tests has been developed for SOM. And 

class Test(unittest.TestCase):

    def testHoneycombStruct(self):
        sample = read_sample('../../Samples/SampleSimple3.txt');
        network = plsom(3, 4, sample, type_conn.honeycomb);
        
        assert sorted(network.neighbors[0]) == sorted([1, 4, 5]);
        assert sorted(network.neighbors[6]) == sorted([1, 2, 7, 10, 9, 5]);
        assert sorted(network.neighbors[3]) == sorted([2, 7]);
        assert sorted(network.neighbors[11]) == sorted([7, 10]);
        assert sorted(network.neighbors[9]) == sorted([8, 5, 6, 10]);
        
        
        network = plsom(4, 4, sample, type_conn.honeycomb);
        assert sorted(network.neighbors[11]) == sorted([7, 10, 15]);
        assert sorted(network.neighbors[9]) == sorted([8, 5, 6, 10, 13, 14]);
        
        
        network = plsom(2, 2, sample, type_conn.honeycomb);
        assert sorted(network.neighbors[0]) == sorted([1, 3, 2]);
        assert sorted(network.neighbors[1]) == sorted([0, 3]);
        assert sorted(network.neighbors[2]) == sorted([0, 3]);
        assert sorted(network.neighbors[3]) == sorted([2, 0, 1]);
        
        
    def testGridFourStruct(self):
        sample = read_sample('../../Samples/SampleSimple2.txt');
        network = plsom(4, 4, sample, type_conn.grid_four);
         
        assert sorted(network.neighbors[0]) == sorted([1, 4]);
        assert sorted(network.neighbors[2]) == sorted([1, 6, 3]);
        assert sorted(network.neighbors[10]) == sorted([9, 6, 11, 14]);
        assert sorted(network.neighbors[11]) == sorted([7, 10, 15]);
         
        network = plsom(1, 4, sample, type_conn.grid_four);
        assert network.neighbors[0] == [1];
        assert sorted(network.neighbors[1]) == sorted([0, 2]); 
        assert sorted(network.neighbors[2]) == sorted([1, 3]); 
        assert network.neighbors[3] == [2];
    
    
    def templateTestAwardNeurons(self, file, rows, cols, expected_result):
        types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb];
        sample = read_sample(file);
        
        for stucture in types:
            network = plsom(rows, cols, sample, stucture);
            network.train();
            
#             if (sorted(network._award) != expected_result):
#                 print("Awards: ", sorted(network._award), "Expect: ", expected_result);
#                 network.show_network(belongs = True);
#                 assert 0;
                
            assert sorted(network._award) == expected_result;
            
            total_capture_points = 0;
            for points in network._capture_objects:
                total_capture_points += len(points);
                
            assert total_capture_points == sum(expected_result);
    
    
    def testTwoNeuronsTwoClusters(self):
        self.templateTestAwardNeurons('../../Samples/SampleSimple1.txt', 1, 2, [5, 5]);
        self.templateTestAwardNeurons('../../Samples/SampleSimple1.txt', 2, 1, [5, 5]);
        
        
    def testThreeNeuronsThreeClusters(self):
        self.templateTestAwardNeurons('../../Samples/SampleSimple2.txt', 1, 3, [5, 8, 10]);
        self.templateTestAwardNeurons('../../Samples/SampleSimple2.txt', 3, 1, [5, 8, 10]);
        
    
    # TODO: This test is fail. Is this test applicable for PLSOM?
    def testFourNeuronsFourClusters(self):
        self.templateTestAwardNeurons('../../Samples/SampleSimple3.txt', 1, 4, [10, 10, 10, 30]);
        self.templateTestAwardNeurons('../../Samples/SampleSimple3.txt', 2, 2, [10, 10, 10, 30]);
        
    
    def testTwoNeuronsFourClusters(self):
        self.templateTestAwardNeurons('../../Samples/SampleSimple3.txt', 1, 2, [30, 30]); 
        
    
    # TODO: This test is fail. Is this test applicable for PLSOM (implementation in line with the article)?
    def testSevenNeuronsHeptaClusters(self):
        self.templateTestAwardNeurons('../../Samples/SampleHepta.txt', 1, 7, [30, 30, 30, 30, 30, 30, 32]); 
    
    # TODO: Infinite loop. Is this test applicable for PLSOM (implementation in line with the article)?
#     def testFourNeuronsTetraClusters(self):
#         self.templateTestAwardNeurons('../../../Samples/SampleTetra.txt', 1, 4, [100, 100, 100, 100]);
        
    
    # TODO: This test is fail. Is this test applicable for PLSOM (implementation in line with the article)?
    def testTwoNeuronsTwoDiamondsClusters(self):
        self.templateTestAwardNeurons('../../Samples/SampleTwoDiamonds.txt', 1, 2, [400, 400]);
    
    
    def testFiveNeuronsFiveClusters(self):
        self.templateTestAwardNeurons('../../Samples/SampleSimple4.txt', 1, 5, [15, 15, 15, 15, 15]);      
    
    
    def testFourNeuronsSquareClusters(self):
        self.templateTestAwardNeurons('../../Samples/SampleSimple5.txt', 2, 2, [15, 15, 15, 15]);
        self.templateTestAwardNeurons('../../Samples/SampleSimple5.txt', 1, 4, [15, 15, 15, 15]);
    
    
    # TODO: Infinite loop. Is this test applicable for PLSOM (implementation in line with the article)?
#     def testWinners(self):
#         types = [type_conn.func_neighbor, type_conn.grid_eight, type_conn.grid_four, type_conn.honeycomb];
#         sample = read_sample('../../../Samples/SampleSimple3.txt');
#         
#         for stucture in types:
#             network = plsom(5, 5, sample, stucture);
#             network.train();
#             
#             assert sum(network._award) == 60;
#             
#             points = list();
#             for i in range(network.size):
#                 if (network._award[i] > 0):
#                     points += network._capture_objects[i];
#             
#             assert len(points) == len(sample);
#             
#             points = sorted(points);
#             for i in range(len(points)):
#                 assert points[i] == i;
            
         

if __name__ == "__main__":
    unittest.main();