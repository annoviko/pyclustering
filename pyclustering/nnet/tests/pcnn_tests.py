"""!

@brief Unit-tests for Pulse Coupled Neural Network.

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

from pyclustering.nnet.pcnn import pcnn_network, pcnn_parameters;
from pyclustering.nnet import *;

class Test(unittest.TestCase):
    def templateDynamicLength(self, num_osc, steps, type_conn, repr_type, stimulus, ccore):
        net = pcnn_network(num_osc, None, type_conn, repr_type, None, None, ccore);
        dynamic = net.simulate(steps, stimulus);
        
        assert steps == len(dynamic);
        assert num_osc == len(dynamic.output[0]);
        assert steps == len(dynamic.allocate_time_signal());
    
    def testDynamicLengthNoneConnection(self):
        self.templateDynamicLength(10, 20, conn_type.NONE, conn_represent.MATRIX, [0] * 10, False);
    
    def testDynamicLengthNoneConnectionByCore(self):
        self.templateDynamicLength(10, 20, conn_type.NONE, None, [0] * 10, True);
     
    def testDynamicLengthGridFourConnection(self):
        self.templateDynamicLength(25, 20, conn_type.GRID_FOUR, conn_represent.MATRIX, [0] * 25, False);
 
    def testDynamicLengthGridFourConnectionByCore(self):
        self.templateDynamicLength(25, 20, conn_type.GRID_FOUR, None, [0] * 25, True);        
 
    def testDynamicLengthGridEightConnection(self):
        self.templateDynamicLength(25, 20, conn_type.GRID_EIGHT, conn_represent.MATRIX, [0] * 25, False);
 
    def testDynamicLengthGridEightConnectionByCore(self):
        self.templateDynamicLength(25, 20, conn_type.GRID_EIGHT, None, [0] * 25, True); 
 
    def testDynamicLengthListBidirConnection(self):
        self.templateDynamicLength(10, 20, conn_type.LIST_BIDIR, conn_represent.MATRIX, [0] * 10, False);
 
    def testDynamicLengthListBidirConnectionByCore(self):
        self.templateDynamicLength(10, 20, conn_type.LIST_BIDIR, None, [0] * 10, True); 
 
    def testDynamicLengthAllToAllConnection(self):
        self.templateDynamicLength(10, 20, conn_type.ALL_TO_ALL, conn_represent.MATRIX, [0] * 10, False);
 
    def testDynamicLengthAllToAllConnectionByCore(self):
        self.templateDynamicLength(10, 20, conn_type.ALL_TO_ALL, None, [0] * 10, True); 
    
    def testDynamicLengthListRepresentation(self):
        self.templateDynamicLength(25, 30, conn_type.NONE, conn_represent.LIST, [0] * 25, False);
        self.templateDynamicLength(25, 30, conn_type.GRID_EIGHT, conn_represent.LIST, [0] * 25, False);
        self.templateDynamicLength(25, 30, conn_type.GRID_FOUR, conn_represent.LIST, [0] * 25, False);
        self.templateDynamicLength(25, 30, conn_type.LIST_BIDIR, conn_represent.LIST, [0] * 25, False);
        self.templateDynamicLength(25, 30, conn_type.ALL_TO_ALL, conn_represent.LIST, [0] * 25, False);
    
    
    def templateGridRectangleDynamicLength(self, num_osc, steps, type_conn, repr_type, height, width, stimulus, ccore):
        net = pcnn_network(num_osc, None, type_conn, repr_type, height, width, ccore);
        dynamic = net.simulate(steps, stimulus);
        
        assert steps == len(dynamic);
        assert num_osc == len(dynamic.output[0]);
        assert steps == len(dynamic.allocate_time_signal());
    
    def testDynamicLengthGridRectangle25FourConnection(self):
        self.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_FOUR, conn_represent.MATRIX, 1, 25, [0] * 25, False);
        self.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_FOUR, conn_represent.MATRIX, 25, 1, [0] * 25, False);
 
    def testDynamicLengthGridRectangle25FourConnectionByCore(self):
        self.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_FOUR, None, 1, 25, [0] * 25, True);
        self.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_FOUR, None, 25, 1, [0] * 25, True);   
 
    def testDynamicLengthGridRectangle25EightConnection(self):
        self.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_EIGHT, conn_represent.MATRIX, 1, 25, [0] * 25, False);
        self.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_EIGHT, conn_represent.MATRIX, 25, 1, [0] * 25, False);
 
    def testDynamicLengthGridRectangle25EightConnectionByCore(self):
        self.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_EIGHT, None, 1, 25, [0] * 25, True);
        self.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_EIGHT, None, 25, 1, [0] * 25, True); 
    
    
    def templateSyncEnsemblesAllocation(self, num_osc, type_conn, steps, stimulus, ccore, ensembles):
        net = pcnn_network(num_osc, None, type_conn, conn_represent.MATRIX, None, None, ccore);
        dynamic = net.simulate(steps, stimulus);
        
        assert steps == len(dynamic);
        
        sync_ensembles = dynamic.allocate_sync_ensembles();
        
        if (ensembles is not None):
            assert len(ensembles) == len(sync_ensembles);
            
            for expected_ensemble in ensembles:
                ensemble_correct = False;
                
                for index_ensemble in range(len(sync_ensembles)):
                    sorted_expected_ensemble = expected_ensemble.sort();
                    sorted_ensemble = sync_ensembles[index_ensemble].sort();
                    
                    if (sorted_expected_ensemble == sorted_ensemble):
                        ensemble_correct = True;
                        break;
                
                assert (True == ensemble_correct);
                
        unique_indexes = set();
        
        time_signal = dynamic.allocate_time_signal();
        spike_ensembles = dynamic.allocate_spike_ensembles();
        sync_ensembles = dynamic.allocate_sync_ensembles();
        
        for ensemble in spike_ensembles:
            assert len(ensemble) in time_signal;
        
        for ensemble in sync_ensembles:           
            spike_ensembles_exist = False;
            for index in range(len(spike_ensembles)): 
                if (ensemble == spike_ensembles[index]):
                    spike_ensembles_exist = True;
                    break;
            
            assert (True == spike_ensembles_exist);
            
            for index_oscillator in ensemble:
                assert index_oscillator not in unique_indexes;
                unique_indexes.add(index_oscillator);
    
    def testSyncEnsemblesAllStimulated(self):
        self.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, [1] * 25, False, [ list(range(25)) ]);
    
    def testSyncEnsemblesAllStimulatedByCore(self):
        self.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, [1] * 25, True, [ list(range(25)) ]);
    
    def testSyncEnsemblesAllUnstimulated(self):
        self.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, [0] * 25, False, []);

    def testSyncEnsemblesAllUnstimulatedByCore(self):
        self.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, [0] * 25, True, []);
    
    def testSyncEnsemblesPartialStimulation(self):
        stimulus = ([0] * 5) + ([1] * 5) + ([0] * 5) + ([1] * 5) + ([0] * 5);
        expected_ensemble = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19];
        
        self.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, stimulus, False, [ expected_ensemble ]);
    
    def testSyncEnsemblesPartialStimulationByCore(self):
        stimulus = ([0] * 5) + ([1] * 5) + ([0] * 5) + ([1] * 5) + ([0] * 5);
        expected_ensemble = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19];
        
        self.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, stimulus, True, [ expected_ensemble ]);
    
    def testSyncEnsemblesAllStimulatedWithVariousConnection(self):
        self.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 50, [20] * 25, False, None);
        self.templateSyncEnsemblesAllocation(25, conn_type.GRID_EIGHT, 50, [20] * 25, False, None);
        self.templateSyncEnsemblesAllocation(25, conn_type.GRID_FOUR, 50, [20] * 25, False, None);
        self.templateSyncEnsemblesAllocation(25, conn_type.LIST_BIDIR, 50, [20] * 25, False, None);
        self.templateSyncEnsemblesAllocation(25, conn_type.NONE, 50, [20] * 25, False, None);

    def testSyncEnsemblesAllStimulatedWithVariousConnectionByCore(self):
        self.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 50, [20] * 25, True, None);
        self.templateSyncEnsemblesAllocation(25, conn_type.GRID_EIGHT, 50, [20] * 25, True, None);
        self.templateSyncEnsemblesAllocation(25, conn_type.GRID_FOUR, 50, [20] * 25, True, None);
        self.templateSyncEnsemblesAllocation(25, conn_type.LIST_BIDIR, 50, [20] * 25, True, None);
        self.templateSyncEnsemblesAllocation(25, conn_type.NONE, 50, [20] * 25, True, None);
    
    
    def templateAllocationInRectangleStructure(self, num_osc, height, width, steps, type_conn, repr_type, stimulus, ccore):
        net = pcnn_network(num_osc, None, type_conn, repr_type, height, width, ccore);
        dynamic = net.simulate(steps, stimulus);
        
        assert steps == len(dynamic);
        assert num_osc == len(dynamic.output[0]);
        assert steps == len(dynamic.allocate_time_signal());
    
    def testAllocationInRectangleFourStructure(self):
        self.templateAllocationInRectangleStructure(20, 4, 5, 20, conn_type.GRID_FOUR, conn_represent.MATRIX, [0] * 20, False);

    def testAllocationInRectangleFourStructureByCore(self):
        self.templateAllocationInRectangleStructure(20, 4, 5, 20, conn_type.GRID_FOUR, None, [0] * 20, True);

    def testAllocationInRectangleEightStructure(self):
        self.templateAllocationInRectangleStructure(30, 6, 5, 20, conn_type.GRID_EIGHT, conn_represent.MATRIX, [0] * 30, False);
    
    def testAllocationInRectangleEightStructureByCore(self):
        self.templateAllocationInRectangleStructure(30, 6, 5, 20, conn_type.GRID_EIGHT, None, [0] * 30, True);


if __name__ == "__main__":
    unittest.main();