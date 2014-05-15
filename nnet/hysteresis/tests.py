import unittest;

from nnet.hysteresis import hysteresis_network;

from support import extract_number_oscillations;

class Test(unittest.TestCase):
    def templateOscillationExistance(self, num_osc, own_weight, neigh_weight, steps, time, initial_states = None, initial_outputs = None):
        network = hysteresis_network(num_osc, own_weight, neigh_weight);
        
        if (initial_states is not None):
            network.states = initial_states;
            
        if (initial_outputs is not None):
            network.outputs = initial_outputs;
        
        (t, x) = network.simulate(steps, time);
        
        for index in range(num_osc):
            assert extract_number_oscillations(x, index, 0.9) > 1;
    
    def testOscillationsOneOscillator(self):
        self.templateOscillationExistance(1, -2, -1, 1000, 10);
        self.templateOscillationExistance(1, -4, -1, 1000, 10);
        
    def testOscillationsTwoOscillators(self):
        self.templateOscillationExistance(2, -4, 1, 1000, 10, [1, 0], [1, 1]);
        self.templateOscillationExistance(2, -4, -1, 1000, 10, [1, 0], [1, 1]);
        
    def testOscillationsFiveOscillators(self):
        self.templateOscillationExistance(5, -4, -1, 1000, 10, [1, 0.5, 0, -0.5, -1], [1, 1, 1, 1, 1]);
        
    

if __name__ == "__main__":
    unittest.main();