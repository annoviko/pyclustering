"""!

@brief Unit-tests for Oscillatory Neural Network based on Kuramoto model and Landau-Stuart.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2017
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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');


from pyclustering.nnet.fsync import fsync_network;


class Test(unittest.TestCase):
    def templateCreateNetwork(self, network_size):
        oscillatory_network = fsync_network(network_size);
        assert len(oscillatory_network) == network_size;
    
    
    def testCreateNetworkSize1(self):
        self.templateCreateNetwork(1);

    def testCreateNetworkSize20(self):
        self.templateCreateNetwork(20);

    def testCreateNetworkSize100(self):
        self.templateCreateNetwork(100);


    def templateSimulateStaticOutputDynamic(self, num_osc, steps, time, collect_dynamic):
        oscillatory_network = fsync_network(num_osc);
        output_dynamic = oscillatory_network.simulate_static(steps, time, collect_dynamic);
        
        if (collect_dynamic is True):
            assert len(output_dynamic) == steps + 1;
        else:
            assert len(output_dynamic) == 1;

    def testSimulateStatic10StepsTime10(self):
        self.templateSimulateStaticOutputDynamic(10, 10, 10, True);

    def testSimulateStatic100StepsTime10(self):
        self.templateSimulateStaticOutputDynamic(3, 100, 10, True);

    def testSimulateStatic100StepsTime1(self):
        self.templateSimulateStaticOutputDynamic(3, 100, 1, True);

    def testSimulateStatic50StepsTime10WithoutCollecting(self):
        self.templateSimulateStaticOutputDynamic(3, 50, 10, True);

    def testSimulateStatic100StepsTime10WithoutCollecting(self):
        self.templateSimulateStaticOutputDynamic(1, 100, 10, True);


if __name__ == "__main__":
    unittest.main();