"""!

@brief Unit-tests for Local Excitatory Global Inhibitory Oscillatory Network (LEGION).

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

from pyclustering.nnet.legion import legion_network, legion_parameters;
from pyclustering.nnet import *;

from pyclustering.utils import extract_number_oscillations;


class Test(unittest.TestCase):   
    def testUstimulatedOscillatorWithoutLateralPotential(self):
        params = legion_parameters();
        params.teta = 0;    # because no neighbors at all
     
        net = legion_network(1, type_conn = conn_type.NONE, parameters = params);
        dynamic = net.simulate(1000, 200, [0]);
         
        assert extract_number_oscillations(dynamic.output) == 1;
         
         
    def testStimulatedOscillatorWithoutLateralPotential(self):
        params = legion_parameters();
        params.teta = 0;    # because no neighbors at all
         
        net = legion_network(1, type_conn = conn_type.NONE, parameters = params);
        dynamic = net.simulate(1000, 200, [1]);
         
        assert extract_number_oscillations(dynamic.output) > 1;
 
 
    def testStimulatedOscillatorWithLateralPotential(self):
        net = legion_network(1, type_conn = conn_type.NONE);
        dynamic = net.simulate(1000, 200, [1]);
         
        assert extract_number_oscillations(dynamic.output) == 1;
         
     
    def testStimulatedTwoOscillators(self):
        net = legion_network(2, type_conn = conn_type.LIST_BIDIR);
        dynamic = net.simulate(1000, 2000, [1, 1]);
         
        assert extract_number_oscillations(dynamic.output, 0) > 1;
        assert extract_number_oscillations(dynamic.output, 1) > 1;
        
         
    def testMixStimulatedThreeOscillators(self):
        net = legion_network(3, type_conn = conn_type.LIST_BIDIR);
        dynamic = net.simulate(1000, 2000, [1, 0, 1]);
         
        assert extract_number_oscillations(dynamic.output, 0) > 1; 
        assert extract_number_oscillations(dynamic.output, 2) > 1;
    
    
    def testMixStimulatedThreeOscillatorsByCore(self):
        net = legion_network(3, type_conn = conn_type.LIST_BIDIR, ccore = True);
        dynamic = net.simulate(1000, 2000, [1, 0, 1]);
         
        assert extract_number_oscillations(dynamic.output, 0) > 1; 
        assert extract_number_oscillations(dynamic.output, 2) > 1;
 
 
    def testListConnectionRepresentation(self):
        net = legion_network(3, type_conn = conn_type.LIST_BIDIR, type_conn_represent = conn_represent.LIST);
        dynamic = net.simulate(1000, 2000, [1, 0, 1]);
 
        assert extract_number_oscillations(dynamic.output, 0) > 1;  
        assert extract_number_oscillations(dynamic.output, 2) > 1;  
         
         
    # Tests regarded to various structures that can be used.
    def templateOscillationsWithStructures(self, type_conn, ccore_flag = False):
        net = legion_network(4, type_conn = conn_type.LIST_BIDIR, ccore = ccore_flag);
        dynamic = net.simulate(500, 1000, [1, 1, 1, 1]);
         
        for i in range(len(net)):
            assert extract_number_oscillations(dynamic.output, i) > 1;
 
 
    def testStimulatedOscillatorListStructure(self):
        self.templateOscillationsWithStructures(conn_type.LIST_BIDIR);


    def testStimulatedOscillatorGridFourStructure(self):
        self.templateOscillationsWithStructures(conn_type.GRID_FOUR);


    def testStimulatedOscillatorGridEightStructure(self):
        self.templateOscillationsWithStructures(conn_type.GRID_EIGHT);


    def testStimulatedOscillatorAllToAllStructure(self):
        self.templateOscillationsWithStructures(conn_type.ALL_TO_ALL);


    def testStimulatedOscillatorListStructureByCore(self):
        self.templateOscillationsWithStructures(conn_type.LIST_BIDIR, True);


    def testStimulatedOscillatorGridFourStructureByCore(self):
        self.templateOscillationsWithStructures(conn_type.GRID_FOUR, True);


    def testStimulatedOscillatorGridEightStructureByCore(self):
        self.templateOscillationsWithStructures(conn_type.GRID_EIGHT, True);


    def testStimulatedOscillatorAllToAllStructureByCore(self):
        self.templateOscillationsWithStructures(conn_type.ALL_TO_ALL, True);


    # Tests regarded to synchronous ensembles allocation.
    def templateSyncEnsembleAllocation(self, stimulus, params, type_conn, sim_steps, sim_time, expected_clusters, ccore_flag = False):
        result_testing = False;
        
        for _ in range(0, 3, 1):
            net = legion_network(len(stimulus), params, type_conn, ccore = ccore_flag);
            dynamic = net.simulate(sim_steps, sim_time, stimulus);
            
            ensembles = dynamic.allocate_sync_ensembles(0.1);
            if (ensembles != expected_clusters):
                continue;
            
            result_testing = True;
            break;
        
        assert result_testing;


    def testSyncEnsembleAllocationOneStimulatedOscillator(self):
        params = legion_parameters();
        params.teta = 0; # due to no neighbors
        self.templateSyncEnsembleAllocation([1], params, conn_type.NONE, 2000, 500, [[0]]);


    def testSyncEnsembleAllocationOneStimulatedOscillatorByCore(self):
        params = legion_parameters();
        params.teta = 0; # due to no neighbors
        self.templateSyncEnsembleAllocation([1], params, conn_type.NONE, 2000, 500, [[0]], True);


    def testSyncEnsembleAllocationThreeStimulatedOscillators(self):
        self.templateSyncEnsembleAllocation([1, 1, 1], None, conn_type.LIST_BIDIR, 1500, 1500, [[0, 1, 2]]);


    def testSyncEnsembleAllocationThreeStimulatedOscillatorsByCore(self):
        self.templateSyncEnsembleAllocation([1, 1, 1], None, conn_type.LIST_BIDIR, 1500, 1500, [[0, 1, 2]], True);


    def testSyncEnsembleAllocationThreeMixStimulatedOscillators(self):
        parameters = legion_parameters();
        parameters.Wt = 4.0;
        self.templateSyncEnsembleAllocation([1, 0, 1], None, conn_type.LIST_BIDIR, 1500, 1500, [[0, 2], [1]]);


    def testSyncEnsembleAllocationThreeMixStimulatedOscillatorsByCore(self):
        parameters = legion_parameters();
        parameters.Wt = 4.0;
        self.templateSyncEnsembleAllocation([1, 0, 1], None, conn_type.LIST_BIDIR, 1500, 1500, [[0, 2], [1]], True);


if __name__ == "__main__":
    unittest.main();