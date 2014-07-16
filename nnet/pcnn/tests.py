import unittest;

from nnet.pcnn import pcnn_network, pcnn_parameters;
from nnet import *;

class Test(unittest.TestCase):
    def testUnstimulatedOscillators(self):
        net = pcnn_network(9, [0] * 9, type_conn=conn_type.GRID_FOUR);
        net.simulate(100, collect_dynamic = True);
        
        assert [] == net.allocate_sync_ensembles();

    def testStimulatedOscillators(self):
        net = pcnn_network(9, [1] * 9, type_conn=conn_type.GRID_FOUR);
        net.simulate(100, collect_dynamic = True);
        
        print(net.allocate_sync_ensembles());
        #assert [] == net.allocate_sync_ensembles();

if __name__ == "__main__":
    unittest.main();