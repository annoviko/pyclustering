"""!

@brief Unit-tests for Phase Oscillatory Neural Network for Pattern Recognition based on Kuramoto model.

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


class SyncprUnitTest(unittest.TestCase):
    def testCreateTenOscillatorsNetwork(self):
        net = syncpr(10, 0.1, 0.1, ccore=False);
        assert len(net) == 10;


    def testCreateHundredOscillatorsNetwork(self):
        net = syncpr(100, 0.1, 0.1, ccore=False);
        assert len(net) == 100;


    def testOutputDynamicFastSolver(self):
        SyncprTestTemplates.templateOutputDynamic(solve_type.FAST, False);


    def testOutputDynamicRK4Solver(self):
        SyncprTestTemplates.templateOutputDynamic(solve_type.RK4, False);

    def testOutputDinamicLengthSimulation(self):
        net = syncpr(5, 0.1, 0.1, ccore=False);
        output_dynamic = net.simulate(10, 10, [-1, 1, -1, 1, -1], solution = solve_type.FAST, collect_dynamic = True);
         
        assert len(output_dynamic) == 11; # 10 steps without initial values.


    def testOutputDynamicLengthStaticSimulation(self):
        SyncprTestTemplates.templateOutputDynamicLengthStaticSimulation(True, False);

    def testOutputDynamicLengthStaticSimulationWithouCollecting(self):
        SyncprTestTemplates.templateOutputDynamicLengthStaticSimulation(False, False);


    def testOutputDynamicLengthDynamicSimulation(self):
        SyncprTestTemplates.templateOutputDynamicLengthDynamicSimulation(True, False);

    def testOutputDynamicLengthDynamicSimulationWithoutCollecting(self):
        SyncprTestTemplates.templateOutputDynamicLengthDynamicSimulation(False, False);


    def testTrainNetworkAndRecognizePattern(self):
        SyncprTestTemplates.templateTrainNetworkAndRecognizePattern(False);


    def testIncorrectPatternValues(self):
        SyncprTestTemplates.templateIncorrectPatternValues(False);

    def testIncorrectSmallPatternSize(self):
        patterns = [ [1, 1, 1, 1, 1, -1] ];
        SyncprTestTemplates.templateIncorrectPatternForTraining(patterns, False);

    def testIncorrectLargePatternSize(self):
        patterns = [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1] ];
        SyncprTestTemplates.templateIncorrectPatternForTraining(patterns, False);


    def testIncorrectSmallPatternSizeSimulation(self):
        pattern = [1, 1, 1, 1, 1, -1];
         
        SyncprTestTemplates.templateIncorrectPatternForSimulation(pattern, False);

    def testIncorrectLargePatternSizeSimulation(self):
        pattern = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1];
         
        SyncprTestTemplates.templateIncorrectPatternForSimulation(pattern, False);


    def testPatternVisualizerCollectDynamic(self):
        SyncprTestTemplates.templatePatternVisualizer(True);

    def testPatternVisualizerWithoutCollectDynamic(self):
        SyncprTestTemplates.templatePatternVisualizer(False);


    def testMemoryOrder(self):
        SyncprTestTemplates.templateMemoryOrder(False);


    def testStaticSimulation(self):
        SyncprTestTemplates.templateStaticSimulation(False);


    def testDynamicSimulation(self):
        SyncprTestTemplates.templateDynamicSimulation(False);


    def testGlobalSyncOrder(self):
        SyncprTestTemplates.templateGlobalSyncOrder(False);


    def testLocalSyncOrder(self):
        SyncprTestTemplates.templateLocalSyncOrder(False);
