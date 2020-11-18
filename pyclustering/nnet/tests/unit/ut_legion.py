"""!

@brief Unit-tests for Local Excitatory Global Inhibitory Oscillatory Network (LEGION).

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import unittest;

from pyclustering.nnet.tests.legion_templates import LegionTestTemplates;

from pyclustering.nnet.legion import legion_network, legion_parameters;
from pyclustering.nnet import conn_type, conn_represent;

from pyclustering.utils import extract_number_oscillations;


class LegionUnitTest(unittest.TestCase):   
    def testUstimulatedOscillatorWithoutLateralPotential(self):
        params = legion_parameters();
        params.teta = 0;    # because no neighbors at all
      
        net = legion_network(1, type_conn = conn_type.NONE, parameters = params, ccore = False);
        dynamic = net.simulate(1000, 200, [0]);
         
        assert extract_number_oscillations(dynamic.output, amplitude_threshold = 0.0) == 0;


    def testStimulatedOscillatorWithoutLateralPotential(self):
        params = legion_parameters();
        params.teta = 0;    # because no neighbors at all
         
        net = legion_network(1, type_conn = conn_type.NONE, parameters = params, ccore = False);
        dynamic = net.simulate(2000, 400, [1]);
         
        assert extract_number_oscillations(dynamic.output) > 1;


    def testStimulatedOscillatorWithLateralPotential(self):
        net = legion_network(1, type_conn = conn_type.NONE, ccore = False);
        dynamic = net.simulate(2000, 400, [1]);
         
        assert extract_number_oscillations(dynamic.output, amplitude_threshold = 0.0) >= 1;

    def testStimulatedTwoOscillators(self):
        net = legion_network(2, type_conn = conn_type.LIST_BIDIR, ccore = False);
        dynamic = net.simulate(1000, 2000, [1, 1]);
           
        assert extract_number_oscillations(dynamic.output, 0) > 1;
        assert extract_number_oscillations(dynamic.output, 1) > 1;


    def testMixStimulatedThreeOscillators(self):
        net = legion_network(3, type_conn = conn_type.LIST_BIDIR, ccore = False);
        dynamic = net.simulate(1000, 2000, [1, 0, 1]);
          
        assert extract_number_oscillations(dynamic.output, 0) > 1; 
        assert extract_number_oscillations(dynamic.output, 2) > 1;


    def testListConnectionRepresentation(self):
        net = legion_network(3, type_conn = conn_type.LIST_BIDIR, type_conn_represent = conn_represent.LIST, ccore = False);
        dynamic = net.simulate(1000, 2000, [1, 0, 1]);
  
        assert extract_number_oscillations(dynamic.output, 0) > 1;  
        assert extract_number_oscillations(dynamic.output, 2) > 1;  



    def testStimulatedOscillatorListStructure(self):
        LegionTestTemplates.templateOscillationsWithStructures(conn_type.LIST_BIDIR, False);


    def testStimulatedOscillatorGridFourStructure(self):
        LegionTestTemplates.templateOscillationsWithStructures(conn_type.GRID_FOUR, False);


    def testStimulatedOscillatorGridEightStructure(self):
        LegionTestTemplates.templateOscillationsWithStructures(conn_type.GRID_EIGHT, False);


    def testStimulatedOscillatorAllToAllStructure(self):
        LegionTestTemplates.templateOscillationsWithStructures(conn_type.ALL_TO_ALL, False);



    def testSyncEnsembleAllocationOneStimulatedOscillator(self):
        params = legion_parameters();
        params.teta = 0; # due to no neighbors
        LegionTestTemplates.templateSyncEnsembleAllocation([1], params, conn_type.NONE, 2000, 500, [[0]], False);


    def testSyncEnsembleAllocationThreeStimulatedOscillators(self):
        LegionTestTemplates.templateSyncEnsembleAllocation([1, 1, 1], None, conn_type.LIST_BIDIR, 1500, 1500, [[0, 1, 2]], False);
 
 
    def testSyncEnsembleAllocationThreeMixStimulatedOscillators(self):
        parameters = legion_parameters();
        parameters.Wt = 4.0;
        LegionTestTemplates.templateSyncEnsembleAllocation([1, 0, 1], None, conn_type.LIST_BIDIR, 1500, 1500, [[0, 2], [1]], False);



    def testOutputDynamicInformation(self):
        LegionTestTemplates.templateOutputDynamicInformation([1, 0, 1], legion_parameters(), conn_type.LIST_BIDIR, 100, 100, False);
