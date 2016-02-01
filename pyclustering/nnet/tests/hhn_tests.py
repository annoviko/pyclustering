"""!

@brief Unit-tests for oscillatory network based on Hodgkin-Huxley model of neuron.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""

import unittest;

from pyclustering.utils import extract_number_oscillations;

from pyclustering.nnet.hhn import hhn_network, hhn_parameters;

class Test(unittest.TestCase):
    # Tests regarded to synchronous ensembles allocation.
    def templateSyncEnsembleAllocation(self, stimulus, params, sim_steps, sim_time, expected_clusters):
        result_testing = False;
        
        for attempt in range(0, 2, 1):
            net = hhn_network(len(stimulus), stimulus, params);
            (t, x) = net.simulate(sim_steps, sim_time);
            
            ensembles = net.allocate_sync_ensembles(1.0);
            if (ensembles != expected_clusters):
                continue;
            
            result_testing = True;
            break;
        
        assert result_testing;

    def testGlobalSyncWithSameStimulus(self):
        self.templateSyncEnsembleAllocation([27, 27, 27], None, 300, 50, [[0, 1, 2]]);
          
    def testGlobalSyncWithVariousStimulus(self):
        self.templateSyncEnsembleAllocation([26, 26, 27, 27, 26, 25], None, 300, 50, [[0, 1, 2, 3, 4, 5]]);
    
    def testPartialSync(self):
        self.templateSyncEnsembleAllocation([25, 25, 50, 50], None, 400, 200, [ [0, 1], [2, 3] ]);

if __name__ == "__main__":
    unittest.main();