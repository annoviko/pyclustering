"""!

@brief Integration-tests for Phase Oscillatory Neural Network for Pattern Recognition based on Kuramoto model.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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
