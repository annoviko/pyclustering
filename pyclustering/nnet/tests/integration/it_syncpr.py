"""!

@brief Integration-tests for Phase Oscillatory Neural Network for Pattern Recognition based on Kuramoto model.

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

import matplotlib;
matplotlib.use('Agg');

from pyclustering.nnet.tests.syncpr_templates import SyncprTestTemplates;

from pyclustering.nnet import solve_type;
from pyclustering.nnet.syncpr import syncpr;

from pyclustering.core.tests import remove_library;


class SyncprIntegrationTest(unittest.TestCase):
    def testCreateTenOscillatorsNetworkByCore(self):
        net = syncpr(10, 0.1, 0.1, True);
        assert len(net) == 10;

    def testCreateHundredOscillatorsNetworkByCore(self):
        net = syncpr(100, 0.1, 0.1, True);
        assert len(net) == 100;


    def testOutputDynamicFastSolverByCore(self):
        SyncprTestTemplates.templateOutputDynamic(solve_type.FAST, True);

    def testOutputDynamicRK4SolverByCore(self):
        SyncprTestTemplates.templateOutputDynamic(solve_type.RK4, True);


    def testOutputDynamicLengthStaticSimulationByCore(self):
        SyncprTestTemplates.templateOutputDynamicLengthStaticSimulation(True, True);


    def testOutputDynamicLengthDynamicSimulationByCore(self):
        SyncprTestTemplates.templateOutputDynamicLengthDynamicSimulation(True, True);

    def testOutputDynamicLengthDynamicSimulationWithoutCollectingByCore(self):
        SyncprTestTemplates.templateOutputDynamicLengthDynamicSimulation(False, True);


    def testTrainNetworkAndRecognizePatternByCore(self):
        SyncprTestTemplates.templateTrainNetworkAndRecognizePattern(True); 


    def testIncorrectPatternValuesByCore(self):
        SyncprTestTemplates.templateIncorrectPatternValues(True);

    def testIncorrectSmallPatternSizeByCore(self):
        patterns = [ [1, 1, 1, 1, 1, -1] ];
        SyncprTestTemplates.templateIncorrectPatternForTraining(patterns, True);

    def testIncorrectLargePatternSizeByCore(self):
        patterns = [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1] ];
        SyncprTestTemplates.templateIncorrectPatternForTraining(patterns, True);


    def testPatternVisualizerCollectDynamicByCore(self):
        SyncprTestTemplates.templatePatternVisualizer(True, True);

    def testPatternVisualizerWithoutCollectDynamicByCore(self):
        SyncprTestTemplates.templatePatternVisualizer(False, True);


    def testMemoryOrderByCore(self):
        SyncprTestTemplates.templateMemoryOrder(True);


    def testStaticSimulationByCore(self):
        SyncprTestTemplates.templateStaticSimulation(True);


    def testDynamicSimulationByCore(self):
        SyncprTestTemplates.templateDynamicSimulation(True);


    def testGlobalSyncOrderByCore(self):
        SyncprTestTemplates.templateGlobalSyncOrder(True);


    def testLocalSyncOrderByCore(self):
        SyncprTestTemplates.templateLocalSyncOrder(True);


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        SyncprTestTemplates.templateOutputDynamic(solve_type.FAST, True);
