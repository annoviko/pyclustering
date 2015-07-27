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

from pyclustering.nnet import *;
from pyclustering.nnet.syncpr import syncpr, syncpr_dynamic;

class Test(unittest.TestCase):
    def testCreateTenOscillatorsNetwork(self):
        net = syncpr(10, 0.1, 0.1);
        assert len(net) == 10;
    
    
    def testCreateHundredOscillatorsNetwork(self):
        net = syncpr(100, 0.1, 0.1);
        assert len(net) == 100;
        
        
    def testOutputDynamic(self):
        net = syncpr(5, 0.1, 0.1);
        output_dynamic = net.simulate(10, 10, [-1, 1, -1, 1, -1], solve_type.RK4, True);
        
        assert len(output_dynamic) == 10;
        
        
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
    
    
    def testIncorrectPatternValues(self):
        net = syncpr(10, 0.1, 0.1);
        
        patterns =  [];
        patterns += [ [2, 1, 1, 1, 1, -1, -1, -1, -1, -1] ];
        patterns += [ [-1, -2, -1, -1, -1, 1, 1, 1, 1, 1] ];
        
        self.assertRaises(Exception, net.train, patterns);
        
        
    def testIncorrectSmallPatternSize(self):
        net = syncpr(10, 0.1, 0.1);
        
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1] ];
        
        self.assertRaises(Exception, net.train, patterns);
        
        
    def testIncorrectLargePatternSize(self):
        net = syncpr(10, 0.1, 0.1);
        
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1] ];
        
        self.assertRaises(Exception, net.train, patterns);
        
        
    def testIncorrectSmallPatternSizeSimulation(self):
        net = syncpr(10, 0.1, 0.1);
        
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1] ];
        
        self.assertRaises(Exception, net.simulate, 10, 10, patterns[0]);
    
    
    def testIncorrectLargePatternSizeSimulation(self):
        net = syncpr(10, 0.1, 0.1);
        
        patterns =  [];
        patterns += [ [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1] ];
        
        self.assertRaises(Exception, net.simulate, 10, 10, patterns[0]);
    
    
if __name__ == "__main__":
    unittest.main();

        