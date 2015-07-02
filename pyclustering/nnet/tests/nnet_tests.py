"""!

@brief Abstract network representation that is used as a basic class.

@authors Andrei Novikov (spb.andr@yandex.ru)
@date 2014-2015
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

import math;

from pyclustering.nnet import network, conn_type, conn_represent;

class Test(unittest.TestCase):
    # All to All connection suite
    def templateAllToAllConnectionsTest(self, network):
        for i in range(0, len(network), 1):
            for j in range(0, len(network), 1):
                if (i != j):
                    assert network.has_connection(i, j) == True;
                else:
                    assert network.has_connection(i, j) == False; 
                    
    def testAllToAllConnections(self):
        # Check creation of coupling between oscillator in all-to-all case
        net = network(10, type_conn = conn_type.ALL_TO_ALL);
        self.templateAllToAllConnectionsTest(net);

    def testAllToAllConnectionsListRepresentation(self):
        net = network(10, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.LIST);
        self.templateAllToAllConnectionsTest(net);        

    # None connection suite
    def templateNoneConnectionsTest(self, network):
        for i in range(0, len(network), 1):
            for j in range(0, len(network), 1):
                assert network.has_connection(i, j) == False;

    def testNoneConnections(self):
        net = network(10, type_conn = conn_type.NONE);
        self.templateNoneConnectionsTest(net);

    def testNoneConnectionsListRepresentation(self):
        net = network(10, type_conn = conn_type.NONE, conn_represent = conn_represent.LIST);
        self.templateNoneConnectionsTest(net);

    
    # Bidirectional list connection suite
    def templateBidirListConnectionsTest(self, network):
        for index in range(0, len(network), 1):
            if (index > 0):
                assert network.has_connection(index, index - 1) == True;
            
            if (index < (len(network) - 1)):
                assert network.has_connection(index, index + 1) == True;   
                
    def testBidirListConnections(self):
        # Check creation of coupling between oscillator in bidirectional list case
        net = network(10, type_conn = conn_type.LIST_BIDIR);
        self.templateBidirListConnectionsTest(net);
    
    def testBidirListConnectionsListRepresentation(self):
        net = network(10, type_conn = conn_type.LIST_BIDIR, conn_represent = conn_represent.LIST);
        self.templateBidirListConnectionsTest(net);     


    # Grid four connection suite
    def templateGridFourConnectionsTest(self, network):
        for index in range(0, len(network), 1):
            upper_index = index - 5;
            lower_index = index + 5;
            left_index = index - 1;
            right_index = index + 1;
            
            node_row_index = math.ceil(index / 5);
            if (upper_index >= 0):
                assert network.has_connection(index, upper_index) == True;
            
            if (lower_index < len(network)):
                assert network.has_connection(index, lower_index) == True;
            
            if ( (left_index >= 0) and (math.ceil(left_index / 5) == node_row_index) ):
                assert network.has_connection(index, left_index) == True;
            
            if ( (right_index < network._num_osc) and (math.ceil(right_index / 5) == node_row_index) ):
                assert network.has_connection(index, right_index) == True;
                
    def testGridFourConnections(self):
        # Check creation of coupling between oscillator in grid with four neighbors case
        net = network(25, type_conn = conn_type.GRID_FOUR);
        self.templateGridFourConnectionsTest(net);
    
    def testGridFourConnectionsListRepresentation(self):
        # Check creation of coupling between oscillator in grid with four neighbors case
        net = network(25, type_conn = conn_type.GRID_FOUR, conn_represent = conn_represent.LIST);        
        self.templateGridFourConnectionsTest(net);


if __name__ == "__main__":
    unittest.main();