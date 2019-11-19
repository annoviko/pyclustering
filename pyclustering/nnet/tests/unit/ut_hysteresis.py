"""!

@brief Unit-tests for Hysteresis Oscillatory Network.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
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

from pyclustering.nnet.hysteresis import hysteresis_network;
from pyclustering.nnet import *;

from pyclustering.utils import extract_number_oscillations;


class HysteresisUnitTest(unittest.TestCase):
    def templateOscillationExistance(self, num_osc, own_weight, neigh_weight, steps, time, initial_states = None, initial_outputs = None, conn_repr = conn_represent.MATRIX):
        network = hysteresis_network(num_osc, own_weight, neigh_weight, type_conn_represent = conn_repr);
        
        if (initial_states is not None):
            network.states = initial_states;
            
        if (initial_outputs is not None):
            network.outputs = initial_outputs;
        
        output_dynamic = network.simulate(steps, time);
        
        oscillations = [];
        for index in range(num_osc):
            number_oscillations = extract_number_oscillations(output_dynamic.output, index, 0.9);
            oscillations.append(number_oscillations)
            
            assert number_oscillations > 1;


    def testOscillationsOneOscillator(self):
        self.templateOscillationExistance(1, -2, -1, 1000, 10);
        self.templateOscillationExistance(1, -4, -1, 1000, 10);
        
    def testOscillationsTwoOscillators(self):
        self.templateOscillationExistance(2, -4, 1, 1000, 10, [1, 0], [1, 1]);
        self.templateOscillationExistance(2, -4, -1, 1000, 10, [1, 0], [1, 1]);
        
    def testOscillationsFiveOscillators(self):
        self.templateOscillationExistance(5, -4, -1, 1000, 10, [1, 0.5, 0, -0.5, -1], [1, 1, 1, 1, 1]);
        
    def testListConnectionRepresentation(self):
        self.templateOscillationExistance(1, -2, -1, 1000, 10, conn_repr = conn_represent.LIST);
        self.templateOscillationExistance(2, -4, -1, 1000, 10, [1, 0], [1, 1], conn_repr = conn_represent.LIST);
        self.templateOscillationExistance(5, -4, -1, 1000, 10, [1, 0.5, 0, -0.5, -1], [1, 1, 1, 1, 1], conn_repr = conn_represent.LIST);
    
    
    def templateSynchronousEnsemblesAllocation(self, num_osc, own_weight, neigh_weight, steps, time, initial_states, initial_outputs, sync_ensembles_sizes):
        network = hysteresis_network(num_osc, own_weight, neigh_weight);
        
        if (initial_states is not None):
            network.states = initial_states;
            
        if (initial_outputs is not None):
            network.outputs = initial_outputs;
        
        output_dynamic = network.simulate(steps, time, collect_dynamic = True);
        ensembles = output_dynamic.allocate_sync_ensembles(0.5, 5);
        
        assert len(ensembles) == len(sync_ensembles_sizes);
        
        obtained_ensembles_sizes = [len(cluster) for cluster in ensembles];
        total_length = sum(obtained_ensembles_sizes);
        
        assert total_length == len(network);
        
        obtained_ensembles_sizes.sort();
        sync_ensembles_sizes.sort();
        
        assert obtained_ensembles_sizes == sync_ensembles_sizes;


    def testOneSyncEnsemblesAllocation(self):
        self.templateSynchronousEnsemblesAllocation(2, -4, 1, 1000, 10, [1, 0], [1, 1], [2]);
    
    def testTwoSyncEnsemblesAllocation(self):
        self.templateSynchronousEnsemblesAllocation(2, -4, -1, 1000, 10, [1, 0], [1, 1], [1, 1]);
