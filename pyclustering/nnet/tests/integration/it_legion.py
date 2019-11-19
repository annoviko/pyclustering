"""!

@brief Integration-tests for Local Excitatory Global Inhibitory Oscillatory Network (LEGION).

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


import unittest

from pyclustering.nnet.tests.legion_templates import LegionTestTemplates

from pyclustering.nnet.legion import legion_network, legion_parameters
from pyclustering.nnet import conn_type

from pyclustering.utils import extract_number_oscillations

from pyclustering.core.tests import remove_library


class LegionIntergrationTest(unittest.TestCase):   
    def testMixStimulatedThreeOscillatorsByCore(self):
        net = legion_network(3, type_conn = conn_type.LIST_BIDIR, ccore=True)
        dynamic = net.simulate(1000, 2000, [1, 0, 1])
          
        assert extract_number_oscillations(dynamic.output, 0) > 1; 
        assert extract_number_oscillations(dynamic.output, 2) > 1;

    def testStimulatedOscillatorListStructureByCore(self):
        LegionTestTemplates.templateOscillationsWithStructures(conn_type.LIST_BIDIR, True)

    def testStimulatedOscillatorGridFourStructureByCore(self):
        LegionTestTemplates.templateOscillationsWithStructures(conn_type.GRID_FOUR, True)

    def testStimulatedOscillatorGridEightStructureByCore(self):
        LegionTestTemplates.templateOscillationsWithStructures(conn_type.GRID_EIGHT, True)

    def testStimulatedOscillatorAllToAllStructureByCore(self):
        LegionTestTemplates.templateOscillationsWithStructures(conn_type.ALL_TO_ALL, True)


    def testSyncEnsembleAllocationOneStimulatedOscillatorByCore(self):
        params = legion_parameters()
        params.teta = 0 # due to no neighbors
        LegionTestTemplates.templateSyncEnsembleAllocation([1], params, conn_type.NONE, 2000, 500, [[0]], True)

    def testSyncEnsembleAllocationThreeStimulatedOscillatorsByCore(self):
        LegionTestTemplates.templateSyncEnsembleAllocation([1, 1, 1], None, conn_type.LIST_BIDIR, 1500, 1500, [[0, 1, 2]], True)

    def testSyncEnsembleAllocationThreeMixStimulatedOscillatorsByCore(self):
        parameters = legion_parameters()
        parameters.Wt = 4.0
        LegionTestTemplates.templateSyncEnsembleAllocation([1, 0, 1], None, conn_type.LIST_BIDIR, 1500, 1500, [[0, 2], [1]], True)


    def testOutputDynamicInformationByCore(self):
        LegionTestTemplates.templateOutputDynamicInformation([1, 0, 1], legion_parameters(), conn_type.LIST_BIDIR, 100, 100, True)


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        LegionTestTemplates.templateOscillationsWithStructures(conn_type.LIST_BIDIR, True)
