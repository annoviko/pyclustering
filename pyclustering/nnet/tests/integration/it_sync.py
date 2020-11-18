"""!

@brief Integration-tests for Oscillatory Neural Network based on Kuramoto model.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest;

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.nnet.tests.sync_templates import SyncTestTemplates;

from pyclustering.nnet import conn_type, solve_type;
from pyclustering.nnet.sync import sync_network;

from pyclustering.core.tests import remove_library;


class SyncIntegrationTest(unittest.TestCase):
    def testCreateNetworkByCore(self):
        SyncTestTemplates.templateCreateNetwork(1, True);
        SyncTestTemplates.templateCreateNetwork(10, True);
        SyncTestTemplates.templateCreateNetwork(55, True);

    def testCreationDeletionByCore(self):
        # Crash occurs in case of memory leak
        for _ in range(0, 15):
            network = sync_network(4096, 1, type_conn = conn_type.ALL_TO_ALL, ccore = True);
            del network;


    def testConnectionsApiByCore(self):
        SyncTestTemplates.templateConnectionsApi(1, True);
        SyncTestTemplates.templateConnectionsApi(5, True);
        SyncTestTemplates.templateConnectionsApi(10, True);


    def testFastSolutionByCore(self):
        SyncTestTemplates.templateSimulateTest(10, 1, solve_type.FAST, ccore_flag = True);

    def testRK4SolutionByCore(self):
        SyncTestTemplates.templateSimulateTest(10, 1, solve_type.RK4, ccore_flag = True);

    def testRKF45SolutionByCore(self):
        SyncTestTemplates.templateSimulateTest(10, 1, solve_type.RKF45, ccore_flag = True);


    def testTwoOscillatorDynamicByCore(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(2, 1, conn_type.ALL_TO_ALL, True);

    def testThreeOscillatorDynamicByCore(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(3, 1, conn_type.ALL_TO_ALL, True);

    def testFourOscillatorDynamicByCore(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(4, 1, conn_type.ALL_TO_ALL, True);

    def testFiveOscillatorDynamicByCore(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(5, 1, conn_type.ALL_TO_ALL, True);

    def testSixOscillatorDynamicByCore(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(6, 1, conn_type.ALL_TO_ALL, True);

    def testSevenOscillatorDynamicByCore(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(7, 1, conn_type.ALL_TO_ALL, True);


    def testOutputDynamicCalculateOrderParameterByCore(self):
        SyncTestTemplates.templateOutputDynamicCalculateOrderParameter(True);


    def testOutputDynamicCalculateLocalOrderParameterByCore(self):
        SyncTestTemplates.templateOutputDynamicCalculateLocalOrderParameter(True);


    def testVisualizerNoFailuresByCore(self):
        SyncTestTemplates.templateVisualizerNoFailures(5, 10, True);


    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        SyncTestTemplates.templateSimulateTest(10, 1, solve_type.FAST, ccore_flag = True);
