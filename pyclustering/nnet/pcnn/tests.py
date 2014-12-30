import unittest;

from pyclustering.nnet.pcnn import pcnn_network, pcnn_parameters;
from pyclustering.nnet import *;

class Test(unittest.TestCase):
    def testUnstimulatedOscillators(self):
        net = pcnn_network(9, [0] * 9, type_conn=conn_type.GRID_FOUR);
        net.simulate(100, collect_dynamic = True);
        
        assert [] == net.allocate_sync_ensembles();

    def testStimulatedOscillators(self):
        params = pcnn_parameters();
        
        net = pcnn_network(9, [1.0] * 9, params, type_conn = conn_type.GRID_FOUR);
        net.simulate(100, collect_dynamic = True);
        
        sync_ensebles = net.allocate_sync_ensembles(5);
        sync_ensebles.sort();

        assert [ [0, 1, 2, 3, 4, 5, 6, 7, 8] ] == sync_ensebles;

    def testStimulatedTwoAreas(self):
        params = pcnn_parameters();
        params.M = 0.0;
        
        net = pcnn_network(25, [0, 0, 0, 0, 0,
                                0, 1, 1, 1, 0,
                                0, 1, 1, 1, 0,
                                0, 1, 1, 1, 0,
                                0, 0, 0, 0, 0], params, type_conn = conn_type.GRID_EIGHT);
                               
        net.simulate(100, collect_dynamic = True);
        
        sync_ensebles = net.allocate_sync_ensembles(5);
        sync_ensebles.sort();

        assert [ [6, 7, 8, 11, 12, 13, 16, 17, 18] ] == sync_ensebles;


if __name__ == "__main__":
    unittest.main();