"""!

@brief Unit-tests for Phase Oscillatory Neural Network for Pattern Recognition based on Kuramoto model.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

from pyclustering.nnet import *;
from pyclustering.nnet.syncpr import syncpr, syncpr_dynamic, syncpr_visualizer;

class Test(unittest.TestCase):
    def testCreateTenOscillatorsNetwork(self):
        net = syncpr(10, 0.1, 0.1);
        assert len(net) == 10;
         
     
    def testCreateTenOscillatorsNetworkByCore(self):
        net = syncpr(10, 0.1, 0.1, True);
        assert len(net) == 10;
     
     
    def testCreateHundredOscillatorsNetwork(self):
        net = syncpr(100, 0.1, 0.1);
        assert len(net) == 100;
         
     
    def testCreateHundredOscillatorsNetworkByCore(self):
        net = syncpr(100, 0.1, 0.1, True);
        assert len(net) == 100;
     
     
    def templateOutputDynamic(self, solver, ccore = False):    
        net = syncpr(5, 0.1, 0.1, ccore);
        output_dynamic = net.simulate(10, 10, [-1, 1, -1, 1, -1], solver, True);
         
        assert len(output_dynamic) == 11; # 10 steps without initial values.
             
     
    def testOutputDynamicFastSolver(self):
        self.templateOutputDynamic(solve_type.FAST);
 
 
    def testOutputDynamicFastSolverByCore(self):
        self.templateOutputDynamic(solve_type.FAST, True);
 
 
    def testOutputDynamicRK4Solver(self):
        self.templateOutputDynamic(solve_type.RK4);
  
  
    def testOutputDynamicRK4SolverByCore(self):
        self.templateOutputDynamic(solve_type.RK4, True);
         
     
    def testOutputDinamicLengthSimulation(self):
        net = syncpr(5, 0.1, 0.1);
        output_dynamic = net.simulate(10, 10, [-1, 1, -1, 1, -1], solution = solve_type.FAST, collect_dynamic = True);
         
        assert len(output_dynamic) == 11; # 10 steps without initial values.
     
     
    def templateOutputDynamicLengthStaticSimulation(self, collect_flag, ccore_flag):
        net = syncpr(5, 0.1, 0.1, ccore_flag);
        output_dynamic = net.simulate_static(10, 10, [-1, 1, -1, 1, -1], solution = solve_type.FAST, collect_dynamic = collect_flag);
         
        if (collect_flag is True):
            assert len(output_dynamic) == 11; # 10 steps without initial values.
        else:
            assert len(output_dynamic) == 1;
     
     
    def testOutputDynamicLengthStaticSimulation(self):
        self.templateOutputDynamicLengthStaticSimulation(True, False);    
 
 
    def testOutputDynamicLengthStaticSimulationWithouCollecting(self):
        self.templateOutputDynamicLengthStaticSimulation(False, False);   
 
 
    def testOutputDynamicLengthStaticSimulationByCore(self):
        self.templateOutputDynamicLengthStaticSimulation(True, True);    
 
 
    def testOutputDynamicLengthStaticSimulationWithouCollectingByCore(self):
        self.templateOutputDynamicLengthStaticSimulation(False, True);   
    
     
    def templateOutputDynamicLengthDynamicSimulation(self, collect_flag, ccore_flag):
        net = syncpr(5, 0.1, 0.1, ccore_flag);
        output_dynamic = net.simulate_dynamic([-1, 1, -1, 1, -1], solution = solve_type.FAST, collect_dynamic = collect_flag);
         
        if (collect_flag is True):
            assert len(output_dynamic) > 1;
        else:
            assert len(output_dynamic) == 1;
                
         
    def testOutputDynamicLengthDynamicSimulation(self):
        self.templateOutputDynamicLengthDynamicSimulation(True, False);
 
 
    def testOutputDynamicLengthDynamicSimulationByCore(self):
        self.templateOutputDynamicLengthDynamicSimulation(True, True);
 
 
    def testOutputDynamicLengthDynamicSimulationWithoutCollecting(self):
        self.templateOutputDynamicLengthDynamicSimulation(False, False);
 
 
    def testOutputDynamicLengthDynamicSimulationWithoutCollectingByCore(self):
        self.templateOutputDynamicLengthDynamicSimulation(False, True);
 
     
    def templateTrainNetworkAndRecognizePattern(self, ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
         
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
         
        net.train(patterns);
         
        # recognize it
        for i in range(len(patterns)):
            output_dynamic = net.simulate(10, 10, patterns[i], solve_type.RK4, True);
             
            ensembles = output_dynamic.allocate_sync_ensembles(0.5);
            assert len(ensembles) == 2;
            assert len(ensembles[0]) == len(ensembles[1]);
             
            # sort results
            ensembles[0].sort();
            ensembles[1].sort();
             
            assert (ensembles[0] == [0, 1, 2, 3, 4]) or (ensembles[0] == [5, 6, 7, 8, 9]);
            assert (ensembles[1] == [0, 1, 2, 3, 4]) or (ensembles[1] == [5, 6, 7, 8, 9]);
     
     
    def testTrainNetworkAndRecognizePattern(self):
        self.templateTrainNetworkAndRecognizePattern(False);
         
     
    def testTrainNetworkAndRecognizePatternByCore(self):
        self.templateTrainNetworkAndRecognizePattern(True); 
         
     
    def templateIncorrectPatternForTraining(self, patterns, ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
         
        self.assertRaises(Exception, net.train, patterns);        
         
 
    def templateIncorrectPatternValues(self, ccore_flag):
        patterns =  [];
        patterns += [ [2, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -2, -1, -1, -1, 1, 1, 1, 1, 1] ];
         
        self.templateIncorrectPatternForTraining(patterns, ccore_flag);
 
 
    def testIncorrectPatternValues(self):
        self.templateIncorrectPatternValues(False);
 
 
    def testIncorrectPatternValuesByCore(self):
        self.templateIncorrectPatternValues(True);
     
     
    def testIncorrectSmallPatternSize(self):
        patterns = [ [1, 1, 1, 1, 1, -1] ];
        self.templateIncorrectPatternForTraining(patterns, False);
 
 
    def testIncorrectSmallPatternSizeByCore(self):
        patterns = [ [1, 1, 1, 1, 1, -1] ];
        self.templateIncorrectPatternForTraining(patterns, True);
         
         
    def testIncorrectLargePatternSize(self):
        patterns = [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1] ];
        self.templateIncorrectPatternForTraining(patterns, False);
 
 
    def testIncorrectLargePatternSizeByCore(self):
        patterns = [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1] ];
        self.templateIncorrectPatternForTraining(patterns, True);
         
 
    def templateIncorrectPatternForSimulation(self, pattern):
        net = syncpr(10, 0.1, 0.1);
         
        self.assertRaises(Exception, net.simulate, 10, 10, pattern);
 
         
    def testIncorrectSmallPatternSizeSimulation(self):
        pattern = [1, 1, 1, 1, 1, -1];
         
        self.templateIncorrectPatternForSimulation(pattern);
     
     
    def testIncorrectLargePatternSizeSimulation(self):
        pattern = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1];
         
        self.templateIncorrectPatternForSimulation(pattern);
     
     
    def templatePatternVisualizer(self, collect_dynamic):
        net = syncpr(5, 0.1, 0.1);
        output_dynamic = net.simulate(10, 10, [-1, 1, -1, 1, -1], solve_type.RK4, collect_dynamic);
         
        # test that we don't have any exception during vizualization.
        syncpr_visualizer.show_pattern(output_dynamic, 5, 2);
             
     
    def testPatternVisualizerCollectDynamic(self):
        self.templatePatternVisualizer(True);
     
     
    def testPatternVisualizerWithoutCollectDynamic(self):
        self.templatePatternVisualizer(False);
        
    
    def templateMemoryOrder(self, ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
        
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
        
        net.train(patterns);
        assert net.memory_order(patterns[0]) < 0.8;
        assert net.memory_order(patterns[1]) < 0.8;
        
        for pattern in patterns:
            net.simulate(20, 10, pattern, solve_type.RK4);
            memory_order = net.memory_order(pattern);
            assert (memory_order > 0.95) and (memory_order <= 1.000005);
    
    
    def testMemoryOrder(self):
        self.templateMemoryOrder(False);


    def testMemoryOrderByCore(self):
        self.templateMemoryOrder(True);
    
    
    def templateStaticSimulation(self, ccore_falg):
        net = syncpr(10, 0.1, 0.1, ccore_falg);
         
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
         
        net.train(patterns);
        net.simulate_static(20, 10, patterns[0], solve_type.RK4);
        memory_order = net.memory_order(patterns[0]);
         
        assert (memory_order > 0.95) and (memory_order <= 1.000005);


    def testStaticSimulation(self):
        self.templateStaticSimulation(False);


    def testStaticSimulationByCore(self):
        self.templateStaticSimulation(True);


    def templateDynamicSimulation(self, ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
         
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
         
        net.train(patterns);
        net.simulate_dynamic(patterns[0], order = 0.998, solution = solve_type.RK4);
        memory_order = net.memory_order(patterns[0]);
         
        assert (memory_order > 0.998) and (memory_order <= 1.0);


    def testDynamicSimulation(self):
        self.templateDynamicSimulation(False);


    def testDynamicSimulationByCore(self):
        self.templateDynamicSimulation(True);
        
    
    def templateGlobalSyncOrder(self, ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
        
        patterns =  [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
        
        global_sync_order = net.sync_order();
        assert (global_sync_order < 1.0) and (global_sync_order > 0.0);
        
        net.train(patterns);
        
        global_sync_order = net.sync_order();
        assert (global_sync_order < 1.0) and (global_sync_order > 0.0);


    def testGlobalSyncOrder(self):
        self.templateGlobalSyncOrder(False);


    def testGlobalSyncOrderByCore(self):
        self.templateGlobalSyncOrder(True);
        

    def templateLocalSyncOrder(self, ccore_flag):
        net = syncpr(10, 0.1, 0.1, ccore_flag);
        
        patterns =  [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1] ];
        
        local_sync_order = net.sync_local_order();
        assert (local_sync_order < 1.0) and (local_sync_order > 0.0);
        
        net.train(patterns);
        
        local_sync_order = net.sync_local_order();
        assert (local_sync_order < 1.0) and (local_sync_order > 0.0);


    def testLocalSyncOrder(self):
        self.templateLocalSyncOrder(False);


    def testLocalSyncOrderByCore(self):
        self.templateLocalSyncOrder(True);


if __name__ == "__main__":
    unittest.main();

        