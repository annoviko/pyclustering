import unittest;

from nnet.legion import legion_network, legion_parameters, extract_number_oscillations;
from nnet import *;


class Test(unittest.TestCase):   
    def testUstimulatedOscillatorWithoutLateralPotential(self):
        params = legion_parameters();
        params.teta = 0;    # because no neighbors at all
    
        net = legion_network(1, [0], type_conn = conn_type.NONE, parameters = params);
        (t, x, z) = net.simulate(1000, 200);
        
        assert extract_number_oscillations(x) == 1;
        
        
    def testStimulatedOscillatorWithoutLateralPotential(self):
        params = legion_parameters();
        params.teta = 0;    # because no neighbors at all
        
        net = legion_network(1, [1], type_conn = conn_type.NONE, parameters = params);
        (t, x, z) = net.simulate(1000, 200);
        
        assert extract_number_oscillations(x) > 1;      


    def testStimulatedOscillatorWithLateralPotential(self):
        net = legion_network(1, [1], type_conn = conn_type.NONE);
        (t, x, z) = net.simulate(1000, 200);
        
        assert extract_number_oscillations(x) == 1;
        
    
    def testStimulatedTwoOscillators(self):
        net = legion_network(2, [1, 1], type_conn = conn_type.LIST_BIDIR);
        (t, x, z) = net.simulate(1000, 2000);
        
        assert extract_number_oscillations(x, 0) > 1;
        assert extract_number_oscillations(x, 1) > 1;


    def testUnstimulatedTwoOscillators(self):
        params = legion_parameters();
        params.teta_p = 2.5;
        
        net = legion_network(2, [0, 0], type_conn = conn_type.LIST_BIDIR, parameters = params);
        (t, x, z) = net.simulate(1000, 1000);
        
        assert extract_number_oscillations(x, 0) == 1;
        assert extract_number_oscillations(x, 1) == 1;
        
        
    def testMixStimulatedThreeOscillators(self):
        net = legion_network(3, [1, 0, 1], type_conn = conn_type.LIST_BIDIR);
        (t, x, z) = net.simulate(1000, 2000);
        
        assert extract_number_oscillations(x, 0) > 1;
        assert extract_number_oscillations(x, 1) == 1;   
        assert extract_number_oscillations(x, 2) > 1;       


if __name__ == "__main__":
    unittest.main();