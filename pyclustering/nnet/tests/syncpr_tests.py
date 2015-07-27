"""!

@brief Unit-tests for Phase Oscillatory Neural Network for Pattern Recognition based on Kuramoto model.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2015
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
matplotlib.use('agg');

from pyclustering.nnet import *;
from pyclustering.nnet.syncpr import syncpr, syncpr_dynamic, syncpr_visualizer;

class Test(unittest.TestCase):
    def testCreateTenOscillatorsNetwork(self):
        net = syncpr(10, 0.1, 0.1);
        assert len(net) == 10;
    
    
    def testCreateHundredOscillatorsNetwork(self):
        net = syncpr(100, 0.1, 0.1);
        assert len(net) == 100;
    
    
    def templateOutputDynamic(self, solver):    
        net = syncpr(5, 0.1, 0.1);
        output_dynamic = net.simulate(10, 10, [-1, 1, -1, 1, -1], solver, True);
        
        assert len(output_dynamic) == 11; # 10 steps without initial values.
            
    
    def testOutputDynamicFastSolver(self):
        self.templateOutputDynamic(solve_type.FAST);


    def testOutputDynamicRK4Solver(self):
        self.templateOutputDynamic(solve_type.RK4);
        
        
    def testTrainNetworkAndRecognizePattern(self):
        net = syncpr(10, 0.1, 0.1);
        
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
        
    
    def templateIncorrectPatternForTraining(self, patterns):
        net = syncpr(10, 0.1, 0.1);
        
        self.assertRaises(Exception, net.train, patterns);        
        

    def testIncorrectPatternValues(self):
        patterns =  [];
        patterns += [ [2, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -2, -1, -1, -1, 1, 1, 1, 1, 1] ];
        
        self.templateIncorrectPatternForTraining(patterns);

        
    def testIncorrectSmallPatternSize(self):
        patterns = [ [1, 1, 1, 1, 1, -1] ];
        
        self.templateIncorrectPatternForTraining(patterns);
        
        
    def testIncorrectLargePatternSize(self):
        patterns = [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1] ];
        
        self.templateIncorrectPatternForTraining(patterns);
        

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
        
            
if __name__ == "__main__":
    unittest.main();

        