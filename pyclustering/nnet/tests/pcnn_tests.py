'''

Unit-tests for Pulse Coupled Neural Network.

Copyright (C) 2015    Andrei Novikov (spb.andr@yandex.ru)

pyclustering is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyclustering is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import unittest;

from pyclustering.nnet.pcnn import pcnn_network, pcnn_parameters;
from pyclustering.nnet import *;

class Test(unittest.TestCase):
    def testUnstimulatedOscillators(self):
        net = pcnn_network(9, [0] * 9, type_conn=conn_type.GRID_FOUR);
        net.simulate(100);
        
        assert [] == net.allocate_sync_ensembles();

    def testStimulatedOscillators(self):
        params = pcnn_parameters();
        
        net = pcnn_network(9, [1.0] * 9, params, type_conn = conn_type.GRID_FOUR);
        net.simulate(100);
        
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
                               
        net.simulate(100);
        
        sync_ensebles = net.allocate_sync_ensembles(5);
        sync_ensebles.sort();

        assert [ [6, 7, 8, 11, 12, 13, 16, 17, 18] ] == sync_ensebles;


if __name__ == "__main__":
    unittest.main();