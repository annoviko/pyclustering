import unittest;

from nnet.pcnn import pcnn_network, pcnn_parameters;
from nnet import *;

class Test(unittest.TestCase):
    def testUnstimulatedOscillators(self):
        net = pcnn_network(9, [0] * 9, type_conn=conn_type.GRID_FOUR);
        net.simulate(100, collect_dynamic = True);
        
        assert [] == net.allocate_sync_ensembles();

    def testStimulatedOscillators(self):
        params = pcnn_parameters();
        params.AT = 0.6;
        
        net = pcnn_network(9, [1] * 9, params, type_conn = conn_type.GRID_FOUR);
        net.simulate(100, collect_dynamic = True);
        
        sync_ensebles = net.allocate_sync_ensembles();
        sync_ensebles.sort();

        assert [ [0, 1, 2, 3, 4, 5, 6, 7, 8] ] == sync_ensebles;

if __name__ == "__main__":
    unittest.main();