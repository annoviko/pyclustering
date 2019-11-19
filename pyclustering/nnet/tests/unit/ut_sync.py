"""!

@brief Unit-tests for Oscillatory Neural Network based on Kuramoto model.

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

from pyclustering.nnet.tests.sync_templates import SyncTestTemplates;

from pyclustering.nnet import solve_type, conn_type;
from pyclustering.nnet.sync import sync_network, sync_dynamic, sync_visualizer;
from pyclustering.utils import pi;


class SyncUnitTest(unittest.TestCase):
    def testCreateNetwork(self):
        SyncTestTemplates.templateCreateNetwork(1, False);
        SyncTestTemplates.templateCreateNetwork(10, False);
        SyncTestTemplates.templateCreateNetwork(55, False);


    def testConnectionsApi(self):
        SyncTestTemplates.templateConnectionsApi(1, False);
        SyncTestTemplates.templateConnectionsApi(5, False);
        SyncTestTemplates.templateConnectionsApi(10, False);


    def testSyncOrderSingleOscillator(self):
        # Check for order parameter of network with one oscillator
        network = sync_network(1, 1, ccore=False);
        assert network.sync_order() == 1;

    def testSyncOrderNetwork(self):
        # Check for order parameter of network with several oscillators
        network = sync_network(2, 1, ccore=False);
            
        sync_state = 1;
        tolerance = 0.1;
            
        network.simulate(50, 20, solve_type.RK4);
        assert (abs(network.sync_order() - sync_state) < tolerance) == True;

    def testSyncLocalOrderSingleOscillator(self):
        network = sync_network(1, 1);
        assert network.sync_local_order() == 0;


    def testOutputNormalization(self):
        network = sync_network(20, 1, ccore=False);
          
        output_dynamic = network.simulate(50, 20, solve_type.RK4);
         
        t = output_dynamic.time;
        dyn = output_dynamic.output;
         
        for iteration in range(len(dyn)):
            for index_oscillator in range(len(dyn[iteration])):
                assert (dyn[iteration][index_oscillator] >= 0);
                assert (dyn[iteration][index_oscillator] <= 2.0 * pi);



    def testFastSolution(self):
        # Check for convergence when solution using fast way of calculation of derivative
        SyncTestTemplates.templateSimulateTest(10, 1, solve_type.FAST, False);

    def testRK4Solution(self):
        # Check for convergence when solution using RK4 function of calculation of derivative
        SyncTestTemplates.templateSimulateTest(10, 1, solve_type.RK4, False);

    def testLargeNetwork(self):
        # Check for convergence of phases in large network - network that contains large number of oscillators
        SyncTestTemplates.templateSimulateTest(128, 1, solve_type.FAST, False);

    def testOutputDynamicAroundZero(self):
        phases = [ [ 0.01, 0.02, 0.04, 6.27, 6.28, 6.25, 0.03] ];
        time = [ 10.0 ];
        
        output_sync_dynamic = sync_dynamic(phases, time, None);

        assert len(output_sync_dynamic.allocate_sync_ensembles(0.2)) == 1;
        assert len(output_sync_dynamic.allocate_sync_ensembles(0.1)) == 1;
        
        phases = [ [ 1.02, 1.05, 1.52, 5.87, 5.98, 5.14] ];
        
        output_sync_dynamic = sync_dynamic(phases, time, None);
        
        assert len(output_sync_dynamic.allocate_sync_ensembles(3.0)) == 1;
        assert len(output_sync_dynamic.allocate_sync_ensembles(2.0)) == 1;


    def testDynamicSimulationAllToAll(self):
        SyncTestTemplates.templateDynamicSimulationConnectionTypeTest(10, 1, conn_type.ALL_TO_ALL, False);
        SyncTestTemplates.templateDynamicSimulationConnectionTypeTest(50, 1, conn_type.ALL_TO_ALL, False);
           
    def testDynamicSimulationGridFour(self):
        SyncTestTemplates.templateDynamicSimulationConnectionTypeTest(9, 1, conn_type.GRID_FOUR, False);
        SyncTestTemplates.templateDynamicSimulationConnectionTypeTest(25, 1, conn_type.GRID_FOUR, False);
   
    def testDynamicSimulationGridEight(self):
        SyncTestTemplates.templateDynamicSimulationConnectionTypeTest(9, 1, conn_type.GRID_FOUR, False);
        SyncTestTemplates.templateDynamicSimulationConnectionTypeTest(25, 1, conn_type.GRID_FOUR, False);
   
    def testDynamicSimulationBidir(self):
        SyncTestTemplates.templateDynamicSimulationConnectionTypeTest(5, 1, conn_type.LIST_BIDIR, False);
        SyncTestTemplates.templateDynamicSimulationConnectionTypeTest(10, 1, conn_type.LIST_BIDIR, False);


    def testTwoOscillatorDynamic(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(2, 1, conn_type.ALL_TO_ALL, False);

    def testThreeOscillatorDynamic(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(3, 1, conn_type.ALL_TO_ALL, False);

    def testFourOscillatorDynamic(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(4, 1, conn_type.ALL_TO_ALL, False);

    def testFiveOscillatorDynamic(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(5, 1, conn_type.ALL_TO_ALL, False);

    def testSixOscillatorDynamic(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(6, 1, conn_type.ALL_TO_ALL, False);

    def testSevenOscillatorDynamic(self):
        SyncTestTemplates.templateDynamicSimulationConvergence(7, 1, conn_type.ALL_TO_ALL, False);


    def testOutputDynamicLengthSimulation(self):
        net = sync_network(5, ccore=False);
        output_dynamic = net.simulate(10, 10, solution = solve_type.FAST, collect_dynamic = True);
         
        assert len(output_dynamic) == 11; # 10 steps without initial values.

    def testOutputDynamicLengthStaticSimulation(self):
        net = sync_network(5, ccore=False);
        output_dynamic = net.simulate_static(10, 10, solution = solve_type.FAST, collect_dynamic = True);
         
        assert len(output_dynamic) == 11; # 10 steps without initial values.    

    def testOutputDynamicLengthStaticSimulationWithouCollecting(self):
        net = sync_network(5, ccore=False);
        output_dynamic = net.simulate_static(10, 10, solution = solve_type.FAST, collect_dynamic = False);
         
        assert len(output_dynamic) == 1; # 10 steps without initial values.    

    def testOutputDynamicLengthDynamicSimulation(self):
        net = sync_network(5, ccore=False);
        output_dynamic = net.simulate_dynamic(solution = solve_type.FAST, collect_dynamic = True);
         
        assert len(output_dynamic) > 1; 

    def testOutputDynamicLengthDynamicSimulationWithoutCollecting(self):
        net = sync_network(5, ccore=False);
        output_dynamic = net.simulate_dynamic(solution = solve_type.FAST, collect_dynamic = False);
         
        assert len(output_dynamic) == 1;

    def testInfoAllicationWithNoSimulation(self):
        output_dynamic = sync_dynamic(None, None, None);
        ensembles = output_dynamic.allocate_sync_ensembles();
        assert ensembles == [];
        
        matrix = output_dynamic.allocate_correlation_matrix();
        assert matrix == [];


    def testOutputDynamicCalculateOrderParameter(self):
        SyncTestTemplates.templateOutputDynamicCalculateOrderParameter(False);


    def testOutputDynamicCalculateLocalOrderParameter(self):
        SyncTestTemplates.templateOutputDynamicCalculateLocalOrderParameter(False);


    def testVisualizerOrderParameterNoFailures(self):
        net = sync_network(10, ccore = False);
        output_dynamic = net.simulate_static(20, 10, solution = solve_type.FAST, collect_dynamic = True);
        
        sync_visualizer.show_order_parameter(output_dynamic);
        sync_visualizer.show_order_parameter(output_dynamic, 0);
        sync_visualizer.show_order_parameter(output_dynamic, 5);
        sync_visualizer.show_order_parameter(output_dynamic, 5, 20);

    def testVisualizeLocalOrderParameterNoFailures(self):
        net = sync_network(10, ccore = False);
        output_dynamic = net.simulate_static(20, 10, solution = solve_type.FAST, collect_dynamic = True);

        sync_visualizer.show_local_order_parameter(output_dynamic, net);
        sync_visualizer.show_local_order_parameter(output_dynamic, net, 0);
        sync_visualizer.show_local_order_parameter(output_dynamic, net, 5);
        sync_visualizer.show_local_order_parameter(output_dynamic, net, 5, 20);


    def testVisualizerNoFailures(self):
        SyncTestTemplates.templateVisualizerNoFailures(5, 10, False);
