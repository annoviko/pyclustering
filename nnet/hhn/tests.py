import unittest;

from support import extract_number_oscillations;

from nnet.hhn import hhn_network, hhn_parameters;

class Test(unittest.TestCase):
    # Tests regarded to synchronous ensembles allocation.
    def templateSyncEnsembleAllocation(self, stimulus, params, sim_steps, sim_time, expected_clusters):
        net = hhn_network(len(stimulus), stimulus, params);
        (t, x) = net.simulate(sim_steps, sim_time);
        
        ensembles = net.allocate_sync_ensembles(0.2);
        assert ensembles == expected_clusters;

    def testGlobalSyncWithSameStimulus(self):        
        self.templateSyncEnsembleAllocation([27, 27, 27], None, 300, 50, [[0, 1, 2]]);
         
    def testGlobalSyncWithVariousStimulus(self):
        self.templateSyncEnsembleAllocation([26, 26, 27, 27, 26, 25], None, 300, 50, [[0, 1, 2, 3, 4, 5]]);
    
    def testPartialSync(self):
        self.templateSyncEnsembleAllocation([25, 25, 45, 45], None, 400, 200, [ [0, 1], [2, 3] ]);

if __name__ == "__main__":
    unittest.main();