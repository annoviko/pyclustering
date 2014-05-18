import unittest;

from nnet.hysteresis import hysteresis_network;
from nnet import *;

from support import extract_number_oscillations;

class Test(unittest.TestCase):
    def templateOscillationExistance(self, num_osc, own_weight, neigh_weight, steps, time, initial_states = None, initial_outputs = None, conn_repr = conn_represent.MATRIX):
        network = hysteresis_network(num_osc, own_weight, neigh_weight, conn_represent = conn_repr);
        
        if (initial_states is not None):
            network.states = initial_states;
            
        if (initial_outputs is not None):
            network.outputs = initial_outputs;
        
        (t, x) = network.simulate(steps, time);
        
        oscillations = [];
        for index in range(num_osc):
            number_oscillations = extract_number_oscillations(x, index, 0.9);
            oscillations.append(number_oscillations)
            
            assert number_oscillations > 1;
            
        return oscillations;
    
    def testOscillationsOneOscillator(self):
        self.templateOscillationExistance(1, -2, -1, 1000, 10);
        self.templateOscillationExistance(1, -4, -1, 1000, 10);
        
    def testOscillationsTwoOscillators(self):
        self.templateOscillationExistance(2, -4, 1, 1000, 10, [1, 0], [1, 1]);
        self.templateOscillationExistance(2, -4, -1, 1000, 10, [1, 0], [1, 1]);
        
    def testOscillationsFiveOscillators(self):
        self.templateOscillationExistance(5, -4, -1, 1000, 10, [1, 0.5, 0, -0.5, -1], [1, 1, 1, 1, 1]);
        
    def testListConnectionRepresentation(self):
        self.templateOscillationExistance(1, -2, -1, 1000, 10, conn_repr = conn_represent.LIST);
        self.templateOscillationExistance(2, -4, -1, 1000, 10, [1, 0], [1, 1], conn_repr = conn_represent.LIST);
        self.templateOscillationExistance(5, -4, -1, 1000, 10, [1, 0.5, 0, -0.5, -1], [1, 1, 1, 1, 1], conn_repr = conn_represent.LIST);
        
    

if __name__ == "__main__":
    unittest.main();