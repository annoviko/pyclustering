import unittest;

from nnet.legion import legion_network, legion_parameters;
from nnet import *;

from support import extract_number_oscillations;


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

    def testListConnectionRepresentation(self):
        net = legion_network(3, [1, 0, 1], type_conn = conn_type.LIST_BIDIR, conn_represent=conn_represent.LIST);
        (t, x, z) = net.simulate(1000, 2000);

        assert extract_number_oscillations(x, 0) > 1;
        assert extract_number_oscillations(x, 1) == 1;   
        assert extract_number_oscillations(x, 2) > 1;  
        
        
        

    def templateOscillationsWithStructures(self, type_conn):
        net = legion_network(4, [1, 1, 1, 1], type_conn = conn_type.LIST_BIDIR);
        (t, x, z) = net.simulate(500, 1000);
        
        for i in range(net.num_osc):
            assert extract_number_oscillations(x, i) > 1;


    def testStimulatedOscillatorListStructure(self):
        self.templateOscillationsWithStructures(conn_type.LIST_BIDIR);

    def testStimulatedOscillatorGridFourStructure(self):
        self.templateOscillationsWithStructures(conn_type.GRID_FOUR);
        
    def testStimulatedOscillatorGridEightStructure(self):
        self.templateOscillationsWithStructures(conn_type.GRID_EIGHT);

    def testStimulatedOscillatorAllToAllStructure(self):
        self.templateOscillationsWithStructures(conn_type.ALL_TO_ALL);
          


if __name__ == "__main__":
    unittest.main();