"""!

@brief Unit-tests for Oscillatory Neural Network based on Kuramoto model and Landau-Stuart.

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

# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');


from pyclustering.nnet import conn_type, conn_represent;
from pyclustering.nnet.fsync import fsync_network, fsync_visualizer;


class FsyncUnitTest(unittest.TestCase):
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
        output_dynamic = oscillatory_network.simulate(steps, time, collect_dynamic);
        
        if (collect_dynamic is True):
            assert len(output_dynamic) == steps + 1;
            assert output_dynamic.time[0] == 0;
        else:
            assert len(output_dynamic) == 1;
        
        assert output_dynamic.time[len(output_dynamic) - 1] == time;

    def testSimulateStatic10StepsTime10(self):
        self.templateSimulateStaticOutputDynamic(10, 10, 10, True);

    def testSimulateStatic100StepsTime10(self):
        self.templateSimulateStaticOutputDynamic(3, 100, 10, True);

    def testSimulateStatic100StepsTime1(self):
        self.templateSimulateStaticOutputDynamic(3, 100, 1, True);

    def testSimulateStatic50StepsTime10WithoutCollecting(self):
        self.templateSimulateStaticOutputDynamic(3, 50, 10, False);

    def testSimulateStatic100StepsTime10WithoutCollecting(self):
        self.templateSimulateStaticOutputDynamic(1, 100, 10, False);


    def templateGlobalSynchronization(self, size, steps, time, frequency, radius, coupling, amplitude_threshold, connections, representation):
        oscillatory_network = fsync_network(size, frequency, radius, coupling, connections, representation);
        output_dynamic = oscillatory_network.simulate(steps, time, True);
        
        for index_oscillator in range(len(oscillatory_network)):
            assert output_dynamic.extract_number_oscillations(index_oscillator, amplitude_threshold) > 0;

        sync_ensembles = output_dynamic.allocate_sync_ensembles(amplitude_threshold);
        assert len(sync_ensembles) == 1;
        assert len(sync_ensembles[0]) == size;

    def testGlobalSyncOneOscillatorAllToAll(self):
        self.templateGlobalSynchronization(1, 50, 10, 1.0, 1.0, 1.0, 0.8, conn_type.ALL_TO_ALL, conn_represent.MATRIX);

    def testGlobalSyncGroupOscillatorAllToAll(self):
        self.templateGlobalSynchronization(5, 50, 10, 1.0, 1.0, 1.0, 0.8, conn_type.ALL_TO_ALL, conn_represent.MATRIX);

    def testGlobalSyncOneOscillatorGridFour(self):
        self.templateGlobalSynchronization(1, 50, 10, 1.0, 1.0, 1.0, 0.8, conn_type.GRID_FOUR, conn_represent.MATRIX);

    def testGlobalSyncGroupOscillatorGridFour(self):
        self.templateGlobalSynchronization(9, 50, 10, 1.0, 1.0, 1.0, 0.8, conn_type.GRID_FOUR, conn_represent.MATRIX);

    def testGlobalSyncOneOscillatorGridEight(self):
        self.templateGlobalSynchronization(1, 50, 10, 1.0, 1.0, 1.0, 0.8, conn_type.GRID_EIGHT, conn_represent.MATRIX);

    def testGlobalSyncGroupOscillatorGridEight(self):
        self.templateGlobalSynchronization(9, 50, 10, 1.0, 1.0, 1.0, 0.8, conn_type.GRID_EIGHT, conn_represent.MATRIX);

    def testGlobalSyncOneOscillatorBidir(self):
        self.templateGlobalSynchronization(1, 50, 10, 1.0, 1.0, 1.0, 0.8, conn_type.LIST_BIDIR, conn_represent.MATRIX);

    def testGlobalSyncGroupOscillatorBidir(self):
        self.templateGlobalSynchronization(5, 50, 10, 1.0, 1.0, 1.0, 0.8, conn_type.LIST_BIDIR, conn_represent.MATRIX);

    def testGlobalSyncOneOscillatorDifferentFrequency(self):
        self.templateGlobalSynchronization(1, 50, 10, [ 1.0 ], 1.0, 1.0, 0.8, conn_type.ALL_TO_ALL, conn_represent.MATRIX);

    def testGlobalSyncGroupOscillatorDifferentFrequency(self):
        self.templateGlobalSynchronization(5, 100, 20, [ 1.0, 1.1, 1.1, 1.2, 1.15 ], 1.0, 1.0, 0.8, conn_type.ALL_TO_ALL, conn_represent.MATRIX);

    def testGlobalSyncOneOscillatorDifferentRadius(self):
        self.templateGlobalSynchronization(1, 50, 10, 1.0, [ 1.0 ], 1.0, 0.8, conn_type.ALL_TO_ALL, conn_represent.MATRIX);

    def testGlobalSyncGroupOscillatorDifferentRadius(self):
        self.templateGlobalSynchronization(5, 50, 10, 1.0, [ 1.0, 2.0, 3.0, 4.0, 5.0 ], 1.0, 0.8, conn_type.ALL_TO_ALL, conn_represent.MATRIX);

    def testGlobalSyncOneOscillatorDifferentProperty(self):
        self.templateGlobalSynchronization(1, 50, 10, [ 1.0 ], [ 1.0 ], 1.0, 0.8, conn_type.ALL_TO_ALL, conn_represent.MATRIX);

    def testGlobalSyncGroupOscillatorDifferentProperty(self):
        self.templateGlobalSynchronization(5, 100, 20, [ 1.0, 1.1, 1.1, 1.2, 1.15 ], [ 1.0, 2.0, 3.0, 4.0, 5.0 ], 1.0, 0.8, conn_type.ALL_TO_ALL, conn_represent.MATRIX);


    def templateNoOscillations(self, size, steps, time, frequency, radius, amplitude_threshold):
        oscillatory_network = fsync_network(size, frequency, radius);
        output_dynamic = oscillatory_network.simulate(steps, time, True);
        
        for index_oscillator in range(len(oscillatory_network)):
            assert output_dynamic.extract_number_oscillations(index_oscillator, amplitude_threshold) == 0;

    def testNoOscillationsZeroFrequency(self):
        self.templateNoOscillations(5, 50, 10, 0.0, 1.0, 0.5);

    def testNoOscillationsZeroRadius(self):
        self.templateNoOscillations(5, 50, 10, 1.0, 0.0, 0.5);


    def testLackCrashGraphics(self):
        oscillatory_network = fsync_network(5);
        
        output_dynamic = oscillatory_network.simulate(50, 10, True);
        
        fsync_visualizer.show_output_dynamic(output_dynamic);
        fsync_visualizer.show_output_dynamics([output_dynamic]);

    def testLackCrashGraphicsDynamicSet(self):
        oscillatory_network_1 = fsync_network(2);
        oscillatory_network_2 = fsync_network(3);
        
        output_dynamic_1 = oscillatory_network_1.simulate(50, 10, True);
        output_dynamic_2 = oscillatory_network_2.simulate(50, 10, True);

        fsync_visualizer.show_output_dynamics([output_dynamic_1, output_dynamic_2]);
