"""!

@brief Abstract network representation that is used as a basic class.

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

import math;

from pyclustering.nnet import network, conn_type, conn_represent;


class NnetUnitTest(unittest.TestCase):
    # All to All connection suite
    def templateAllToAllConnectionsTest(self, network):
        assert network.structure == conn_type.ALL_TO_ALL;
        
        for i in range(0, len(network), 1):
            for j in range(0, len(network), 1):
                if (i != j):
                    assert network.has_connection(i, j) == True;
                    assert network.has_connection(j, i) == True;
                else:
                    assert network.has_connection(i, j) == False;
                    assert network.has_connection(j, i) == False;
    
    def testAllToAll1Connections(self):
        net = network(1, type_conn = conn_type.ALL_TO_ALL);
        self.templateAllToAllConnectionsTest(net);
           
    def testAllToAll10Connections(self):
        net = network(10, type_conn = conn_type.ALL_TO_ALL);
        self.templateAllToAllConnectionsTest(net);

    def testAllToAll25Connections(self):
        net = network(25, type_conn = conn_type.ALL_TO_ALL);
        self.templateAllToAllConnectionsTest(net);

    def testAllToAll1ConnectionsListRepresentation(self):
        net = network(1, type_conn = conn_type.ALL_TO_ALL, conn_repr = conn_represent.LIST);
        self.templateAllToAllConnectionsTest(net);      

    def testAllToAll10ConnectionsListRepresentation(self):
        net = network(10, type_conn = conn_type.ALL_TO_ALL, conn_repr = conn_represent.LIST);
        self.templateAllToAllConnectionsTest(net);

    def testAllToAll25ConnectionsListRepresentation(self):
        net = network(25, type_conn = conn_type.ALL_TO_ALL, conn_repr = conn_represent.LIST);
        self.templateAllToAllConnectionsTest(net);


    # None connection suite
    def templateNoneConnectionsTest(self, network):
        assert network.structure == conn_type.NONE;
        
        for i in range(0, len(network), 1):
            for j in range(0, len(network), 1):
                assert network.has_connection(i, j) == False;
                assert network.has_connection(j, i) == False;

    def testNoneConnections(self):
        net = network(10, type_conn = conn_type.NONE);
        self.templateNoneConnectionsTest(net);

    def testNoneConnectionsListRepresentation(self):
        net = network(10, type_conn = conn_type.NONE, conn_repr = conn_represent.LIST);
        self.templateNoneConnectionsTest(net);

    
    # Bidirectional list connection suite
    def templateBidirListConnectionsTest(self, network):
        assert network.structure == conn_type.LIST_BIDIR;
        
        for index in range(0, len(network), 1):
            if (index > 0):
                assert network.has_connection(index, index - 1) == True;
                assert network.has_connection(index - 1, index) == True;
            
            if (index < (len(network) - 1)):
                assert network.has_connection(index, index + 1) == True;
                assert network.has_connection(index + 1, index) == True;
                
    def testBidirListConnections(self):
        net = network(10, type_conn = conn_type.LIST_BIDIR);
        self.templateBidirListConnectionsTest(net);
    
    def testBidirListConnectionsListRepresentation(self):
        net = network(10, type_conn = conn_type.LIST_BIDIR, conn_repr = conn_represent.LIST);
        self.templateBidirListConnectionsTest(net);     


    # Grid four connection suite
    def templateGridFourConnectionsTest(self, network):
        assert network.structure == conn_type.GRID_FOUR;
        
        for index in range(0, len(network), 1):
            upper_index = index - network.width;
            lower_index = index + network.width;
            left_index = index - 1;
            right_index = index + 1;
            
            node_row_index = math.ceil(index / network.width);
            if (upper_index >= 0):
                assert network.has_connection(index, upper_index) == True;
                assert network.has_connection(upper_index, index) == True;
            
            if (lower_index < len(network)):
                assert network.has_connection(index, lower_index) == True;
                assert network.has_connection(lower_index, index) == True;
            
            if ( (left_index >= 0) and (math.ceil(left_index / network.width) == node_row_index) ):
                assert network.has_connection(index, left_index) == True;
                assert network.has_connection(left_index, index) == True;
            
            if ( (right_index < network._num_osc) and (math.ceil(right_index / network.width) == node_row_index) ):
                assert network.has_connection(index, right_index) == True;
                assert network.has_connection(right_index, index) == True;
                
    def testGridFourConnectionsMatrixRepresentation(self):
        net = network(25, type_conn = conn_type.GRID_FOUR);
        self.templateGridFourConnectionsTest(net);
    
    def testGridFourConnectionsListRepresentation(self):
        net = network(25, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST);
        self.templateGridFourConnectionsTest(net);

    def testGridFourConnections1MatrixRepresentation(self):
        net = network(1, type_conn = conn_type.GRID_FOUR);
        self.templateGridFourConnectionsTest(net);
    
    def testGridFourConnections1ListRepresentation(self):
        net = network(1, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST);
        self.templateGridFourConnectionsTest(net);

    def testGridFourConnectionsRectange40MatrixRepresentation(self):
        net = network(40, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.MATRIX, height = 4, width = 10);
        self.templateGridFourConnectionsTest(net);
        
        net = network(40, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.MATRIX, height = 10, width = 4);
        self.templateGridFourConnectionsTest(net);
        
    def testGridFourConnectionsRectangeList40Representation(self):
        net = network(40, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST, height = 4, width = 10);        
        self.templateGridFourConnectionsTest(net);
        
        net = network(40, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST, height = 10, width = 4);
        self.templateGridFourConnectionsTest(net);        

    def testGridFourConnectionsRectange10MatrixRepresentation(self):
        net = network(10, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.MATRIX, height = 1, width = 10);
        self.templateGridFourConnectionsTest(net);
        
        net = network(10, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.MATRIX, height = 10, width = 1);
        self.templateGridFourConnectionsTest(net);
        
    def testGridFourConnectionsRectangeList10Representation(self):
        net = network(10, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST, height = 1, width = 10);
        self.templateGridFourConnectionsTest(net);
        
        net = network(10, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST, height = 10, width = 1);
        self.templateGridFourConnectionsTest(net);

    def testGridFourConnectionsRectange1MatrixRepresentation(self):
        net = network(1, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.MATRIX, height = 1, width = 1);
        self.templateGridFourConnectionsTest(net);
        
        net = network(1, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.MATRIX, height = 1, width = 1);
        self.templateGridFourConnectionsTest(net);
        
    def testGridFourConnectionsRectangeList1Representation(self):
        net = network(1, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST, height = 1, width = 1);
        self.templateGridFourConnectionsTest(net);
        
        net = network(1, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST, height = 1, width = 1);
        self.templateGridFourConnectionsTest(net);
    
    # Grid four connection suite
    def templateGridEightConnectionsTest(self, network):
        assert network.structure == conn_type.GRID_EIGHT;
        
        for index in range(0, len(network), 1):
            upper_index = index - network.width;
            lower_index = index + network.width;
            left_index = index - 1;
            right_index = index + 1;
            
            node_row_index = math.ceil(index / network.width);
            if (upper_index >= 0):
                assert network.has_connection(index, upper_index) == True;
                assert network.has_connection(upper_index, index) == True;
            
            if (lower_index < len(network)):
                assert network.has_connection(index, lower_index) == True;
                assert network.has_connection(lower_index, index) == True;
            
            if ( (left_index >= 0) and (math.ceil(left_index / network.width) == node_row_index) ):
                assert network.has_connection(index, left_index) == True;
                assert network.has_connection(left_index, index) == True;
            
            if ( (right_index < len(network)) and (math.ceil(right_index / network.width) == node_row_index) ):
                assert network.has_connection(index, right_index) == True;
                assert network.has_connection(right_index, index) == True;
    
            side_size = network.width;

            upper_left_index = index - side_size - 1;
            upper_right_index = index - side_size + 1;
            
            lower_left_index = index + side_size - 1;
            lower_right_index = index + side_size + 1;
            
            node_row_index = math.floor(index / side_size);
            upper_row_index = node_row_index - 1;
            lower_row_index = node_row_index + 1;
            
            if ( (upper_left_index >= 0) and (math.floor(upper_left_index / side_size) == upper_row_index) ):
                assert network.has_connection(index, upper_left_index) == True;
                assert network.has_connection(upper_left_index, index) == True;
            
            if ( (upper_right_index >= 0) and (math.floor(upper_right_index / side_size) == upper_row_index) ):
                assert network.has_connection(index, upper_right_index) == True;
                assert network.has_connection(upper_right_index, index) == True;
                
            if ( (lower_left_index < len(network)) and (math.floor(lower_left_index / side_size) == lower_row_index) ):
                assert network.has_connection(index, lower_left_index) == True;
                assert network.has_connection(lower_left_index, index) == True;
                
            if ( (lower_right_index < len(network)) and (math.floor(lower_right_index / side_size) == lower_row_index) ):
                assert network.has_connection(index, lower_right_index) == True;
                assert network.has_connection(lower_right_index, index) == True;
    
    def testGridEightConnectionsMatrixRepresentation(self):
        net = network(25, type_conn = conn_type.GRID_EIGHT);
        self.templateGridEightConnectionsTest(net);
    
    def testGridEightConnectionsListRepresentation(self):
        net = network(25, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST);
        self.templateGridEightConnectionsTest(net);

    def testGridEightConnections1MatrixRepresentation(self):
        net = network(1, type_conn = conn_type.GRID_EIGHT);
        self.templateGridEightConnectionsTest(net);
    
    def testGridEightConnections1ListRepresentation(self):
        net = network(1, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST);
        self.templateGridEightConnectionsTest(net);

    def testGridEightConnectionsRectange40MatrixRepresentation(self):
        net = network(40, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.MATRIX, height = 4, width = 10);
        self.templateGridEightConnectionsTest(net);
        
        net = network(40, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.MATRIX, height = 10, width = 4);
        self.templateGridEightConnectionsTest(net);
        
    def testGridEightConnectionsRectangeList40Representation(self):
        net = network(40, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST, height = 4, width = 10);
        self.templateGridEightConnectionsTest(net);
        
        net = network(40, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST, height = 10, width = 4);
        self.templateGridEightConnectionsTest(net);        

    def testGridEightConnectionsRectange10MatrixRepresentation(self):
        net = network(10, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.MATRIX, height = 1, width = 10);
        self.templateGridEightConnectionsTest(net);
        
        net = network(10, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.MATRIX, height = 10, width = 1);
        self.templateGridEightConnectionsTest(net);
        
    def testGridEightConnectionsRectangeList10Representation(self):
        net = network(10, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST, height = 1, width = 10);
        self.templateGridEightConnectionsTest(net);
        
        net = network(10, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST, height = 10, width = 1);
        self.templateGridEightConnectionsTest(net);

    def testGridEightConnectionsRectange1MatrixRepresentation(self):
        net = network(1, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.MATRIX, height = 1, width = 1);
        self.templateGridEightConnectionsTest(net);
        
        net = network(1, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.MATRIX, height = 1, width = 1);
        self.templateGridEightConnectionsTest(net);
        
    def testGridEightConnectionsRectangeList1Representation(self):
        net = network(1, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST, height = 1, width = 1);
        self.templateGridEightConnectionsTest(net);
        
        net = network(1, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST, height = 1, width = 1);
        self.templateGridEightConnectionsTest(net);
    
    
    def testGridFourStructure1GridProperty(self):
        net = network(1, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST, height = 1, width = 1);
        assert(net.height == 1);
        assert(net.width == 1);
        
    def testGridEightStructure1GridProperty(self):
        net = network(1, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST, height = 1, width = 1);
        assert(net.height == 1);
        assert(net.width == 1);
    
    def testGridFourStructure40GridProperty(self):
        net = network(40, type_conn = conn_type.GRID_FOUR, conn_repr = conn_represent.LIST, height = 20, width = 2);
        assert(net.height == 20);
        assert(net.width == 2);
        
    def testGridEightStructure40GridProperty(self):
        net = network(40, type_conn = conn_type.GRID_EIGHT, conn_repr = conn_represent.LIST, height = 20, width = 2);
        assert(net.height == 20);
        assert(net.width == 2);
    
    def templateAssertRaises(self, size, type_conn, height, width):
        try:
            network(size, type_conn, height, width);
            assert(False); # assert must occure
            
        except:
            pass;
    
    def testInvalidGridFourDescription(self):
        self.templateAssertRaises(10, type_conn = conn_type.GRID_FOUR, height = 10, width = 5);
        self.templateAssertRaises(10, type_conn = conn_type.GRID_FOUR, height = 6, width = 2);
        self.templateAssertRaises(10, type_conn = conn_type.GRID_FOUR, height = 1, width = 11);
        self.templateAssertRaises(10, type_conn = conn_type.GRID_FOUR, height = 0, width = 0);
        
    def testInvalidGridEightDescription(self):
        self.templateAssertRaises(10, type_conn = conn_type.GRID_EIGHT, height = 5, width = 8);
        self.templateAssertRaises(10, type_conn = conn_type.GRID_EIGHT, height = 1, width = 2);
        self.templateAssertRaises(10, type_conn = conn_type.GRID_EIGHT, height = 1, width = 1);
        self.templateAssertRaises(10, type_conn = conn_type.GRID_EIGHT, height = 0, width = 0);
