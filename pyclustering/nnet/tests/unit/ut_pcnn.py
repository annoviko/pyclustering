"""!

@brief Unit-tests for Pulse Coupled Neural Network.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest

from pyclustering.nnet.tests.pcnn_templates import PcnnTestTemplates

from pyclustering.nnet import conn_type, conn_represent


class PcnnUnitTest(unittest.TestCase):
    def testDynamicLengthNoneConnection(self):
        PcnnTestTemplates.templateDynamicLength(10, 20, conn_type.NONE, conn_represent.MATRIX, [0] * 10, False)

    def testDynamicLengthNoneConnectionFastLinking(self):
        PcnnTestTemplates.templateDynamicLengthFastLinking(10, 20, conn_type.NONE, conn_represent.MATRIX, [0] * 10, False)

    def testDynamicLengthGridFourConnection(self):
        PcnnTestTemplates.templateDynamicLength(25, 20, conn_type.GRID_FOUR, conn_represent.MATRIX, [0] * 25, False)

    def testDynamicLengthGridFourConnectionFastLinking(self):
        PcnnTestTemplates.templateDynamicLengthFastLinking(25, 20, conn_type.GRID_FOUR, conn_represent.MATRIX, [0] * 25, False)

    def testDynamicLengthGridEightConnection(self):
        PcnnTestTemplates.templateDynamicLength(25, 20, conn_type.GRID_EIGHT, conn_represent.MATRIX, [0] * 25, False)

    def testDynamicLengthGridEightConnectionFastLinking(self):
        PcnnTestTemplates.templateDynamicLengthFastLinking(25, 20, conn_type.GRID_EIGHT, conn_represent.MATRIX, [0] * 25, False)

    def testDynamicLengthListBidirConnection(self):
        PcnnTestTemplates.templateDynamicLength(10, 20, conn_type.LIST_BIDIR, conn_represent.MATRIX, [0] * 10, False)

    def testDynamicLengthListBidirConnectionFastLinking(self):
        PcnnTestTemplates.templateDynamicLengthFastLinking(10, 20, conn_type.LIST_BIDIR, conn_represent.MATRIX, [0] * 10, False)

    def testDynamicLengthAllToAllConnection(self):
        PcnnTestTemplates.templateDynamicLength(10, 20, conn_type.ALL_TO_ALL, conn_represent.MATRIX, [0] * 10, False)

    def testDynamicLengthAllToAllConnectionFastLinking(self):
        PcnnTestTemplates.templateDynamicLengthFastLinking(10, 20, conn_type.ALL_TO_ALL, conn_represent.MATRIX, [0] * 10, False)

    def testDynamicLengthListRepresentation(self):
        PcnnTestTemplates.templateDynamicLength(25, 30, conn_type.NONE, conn_represent.LIST, [0] * 25, False)
        PcnnTestTemplates.templateDynamicLength(25, 30, conn_type.GRID_EIGHT, conn_represent.LIST, [0] * 25, False)
        PcnnTestTemplates.templateDynamicLength(25, 30, conn_type.GRID_FOUR, conn_represent.LIST, [0] * 25, False)
        PcnnTestTemplates.templateDynamicLength(25, 30, conn_type.LIST_BIDIR, conn_represent.LIST, [0] * 25, False)
        PcnnTestTemplates.templateDynamicLength(25, 30, conn_type.ALL_TO_ALL, conn_represent.LIST, [0] * 25, False)
    
    
    def testDynamicLengthGridRectangle25FourConnection(self):
        PcnnTestTemplates.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_FOUR, conn_represent.MATRIX, 1, 25, [0] * 25, False)
        PcnnTestTemplates.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_FOUR, conn_represent.MATRIX, 25, 1, [0] * 25, False)
 
    def testDynamicLengthGridRectangle25EightConnection(self):
        PcnnTestTemplates.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_EIGHT, conn_represent.MATRIX, 1, 25, [0] * 25, False)
        PcnnTestTemplates.templateGridRectangleDynamicLength(25, 20, conn_type.GRID_EIGHT, conn_represent.MATRIX, 25, 1, [0] * 25, False)


    def testSyncEnsemblesAllStimulated(self):
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, [1] * 25, False, [ list(range(25)) ])

    def testSyncEnsemblesAllUnstimulated(self):
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, [0] * 25, False, [])

    def testSyncEnsemblesPartialStimulation(self):
        stimulus = ([0] * 5) + ([1] * 5) + ([0] * 5) + ([1] * 5) + ([0] * 5)
        expected_ensemble = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19]
        
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 20, stimulus, False, [ expected_ensemble ])


    def testSyncEnsemblesAllStimulatedWithVariousConnection(self):
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.ALL_TO_ALL, 50, [20] * 25, False, None)
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.GRID_EIGHT, 50, [20] * 25, False, None)
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.GRID_FOUR, 50, [20] * 25, False, None)
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.LIST_BIDIR, 50, [20] * 25, False, None)
        PcnnTestTemplates.templateSyncEnsemblesAllocation(25, conn_type.NONE, 50, [20] * 25, False, None)


    def testAllocationInRectangleFourStructure(self):
        PcnnTestTemplates.templateAllocationInRectangleStructure(20, 4, 5, 20, conn_type.GRID_FOUR, conn_represent.MATRIX, [0] * 20, False)

    def testAllocationInRectangleEightStructure(self):
        PcnnTestTemplates.templateAllocationInRectangleStructure(30, 6, 5, 20, conn_type.GRID_EIGHT, conn_represent.MATRIX, [0] * 30, False)

    def testVisualizerNoFailure(self):
        stimulus = [ 5, 5, 5, 5, 10, 10, 10, 10, 15, 15, 15, 15, 20, 20, 20, 20 ]
        PcnnTestTemplates.visualize(16, 20, conn_type.ALL_TO_ALL, conn_represent.MATRIX, stimulus, 4, 4, False)
