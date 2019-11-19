"""!

@brief Integration-tests for Pulse Coupled Neural Network.

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

from pyclustering.nnet.tests.pcnn_templates import PcnnTestTemplates;

from pyclustering.nnet import conn_type, conn_represent;

from pyclustering.core.tests import remove_library;


class PcnnIntegrationTest(unittest.TestCase):
    def testDynamicLengthNoneConnectionByCore(self):
        PcnnTestTemplates.templateDynamicLength(10, 20, conn_type.NONE, None, [0] * 10, True);

    def testDynamicLengthGridFourConnectionByCore(self):
        PcnnTestTemplates.templateDynamicLength(25, 20, conn_type.GRID_FOUR, None, [0] * 25, True);

    def testDynamicLengthGridEightConnectionByCore(self):
        PcnnTestTemplates.templateDynamicLength(25, 20, conn_type.GRID_EIGHT, None, [0] * 25, True); 

    def testDynamicLengthListBidirConnectionByCore(self):
        PcnnTestTemplates.templateDynamicLength(10, 20, conn_type.LIST_BIDIR, None, [0] * 10, True); 

    def testDynamicLengthAllToAllConnectionByCore(self):
        PcnnTestTemplates.templateDynamicLength(10, 20, conn_type.ALL_TO_ALL, None, [0] * 10, True); 


    def testDynamicLengthGridRectangle25FourConnectionByCore(self):
        PcnnTestTemplates.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_FOUR, None, 1, 25, [0] * 25, True);
        PcnnTestTemplates.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_FOUR, None, 25, 1, [0] * 25, True);

    def testDynamicLengthGridRectangle25EightConnectionByCore(self):
        PcnnTestTemplates.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_EIGHT, None, 1, 25, [0] * 25, True);
        PcnnTestTemplates.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_EIGHT, None, 25, 1, [0] * 25, True); 


    def testSyncEnsemblesAllStimulatedByCore(self):
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, [1] * 25, True, [ list(range(25)) ]);

    def testSyncEnsemblesAllUnstimulatedByCore(self):
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, [0] * 25, True, []);

    def testSyncEnsemblesPartialStimulationByCore(self):
        stimulus = ([0] * 5) + ([1] * 5) + ([0] * 5) + ([1] * 5) + ([0] * 5);
        expected_ensemble = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19];
        
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, stimulus, True, [ expected_ensemble ]);

    def testSyncEnsemblesAllStimulatedWithVariousConnectionByCore(self):
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 50, [20] * 25, True, None);
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.GRID_EIGHT, 50, [20] * 25, True, None);
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.GRID_FOUR, 50, [20] * 25, True, None);
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.LIST_BIDIR, 50, [20] * 25, True, None);
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.NONE, 50, [20] * 25, True, None);


    def testAllocationInRectangleFourStructureByCore(self):
        PcnnTestTemplates.templateAllocationInRectangleStructure(20, 4, 5, 20, conn_type.GRID_FOUR, None, [0] * 20, True);

    def testAllocationInRectangleEightStructureByCore(self):
        PcnnTestTemplates.templateAllocationInRectangleStructure(30, 6, 5, 20, conn_type.GRID_EIGHT, None, [0] * 30, True);


    def testVisualizerNoFailureByCore(self):
        stimulus = [ 5, 5, 5, 5, 10, 10, 10, 10, 15, 15, 15, 15, 20, 20, 20, 20 ];
        PcnnTestTemplates.visualize(16, 20, conn_type.ALL_TO_ALL, conn_represent.MATRIX, stimulus, 4, 4, True);


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        PcnnTestTemplates.templateDynamicLength(10, 20, conn_type.NONE, None, [0] * 10, True);
