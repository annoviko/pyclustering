import unittest;

from pyclustering.nnet import *;
from pyclustering.nnet.sync import sync_network, phase_normalization;

from scipy import pi;


class Test(unittest.TestCase):
    def testCreate(self):
        network = sync_network(10, 1);
        assert network.num_osc == 10;
   
   
    def testCreationDeletionByCore(self):
        # Crash occurs in case of memory leak
        for iteration in range(0, 15):
            network = sync_network(4096, 1, type_conn = conn_type.ALL_TO_ALL, ccore = True);
            del network;
     
     
    def testPhaseNormalization(self):       
        "Check for phase normalization"
        assert phase_normalization(2 * math.pi + 1) == 1;
        assert phase_normalization(2 * math.pi) == 2 * math.pi;
        assert phase_normalization(0) == 0;
        assert phase_normalization(4 * math.pi) == 2 * math.pi;
        assert phase_normalization(-2 * math.pi) == 0;
     
     
    def testSyncOrderSingleOscillator(self):
        # Check for order parameter of network with one oscillator
        network = sync_network(1, 1);
        assert network.sync_order() == 1;
     
     
    def testSyncOrderNetwork(self):
        # Check for order parameter of network with several oscillators
        network = sync_network(20, 1);
         
        sync_state = 1;
        tolerance = 0.1;
         
        network.simulate(50, 20, solve_type.RK4);
        assert (abs(network.sync_order() - sync_state) < tolerance) == True;        
     
     
    def testSyncLocalOrderSingleOscillator(self):
        network = sync_network(1, 1);
        assert network.sync_local_order() == 0;   
     
     
    def templateSimulateTest(self, nodes = 10, weight = 1, solution = solve_type.FAST, ccore_flag = False):
        sim_time = 20;
        sim_steps = 50;
        tolerance = 0.01;
         
        network = sync_network(nodes, weight, ccore = ccore_flag);
               
        (t, dyn_phase) = network.simulate(sim_steps, sim_time, solution);
         
        index = len(dyn_phase) - 1;
        value = dyn_phase[index][0];
         
        for item in dyn_phase[index]:
            assert (abs(item - value) < tolerance) == True;
     
    def testFastSolution(self):
        # Check for convergence when solution using fast way of calculation of derivative
        self.templateSimulateTest(10, 1, solve_type.FAST);
         
    def testFastSolutionByCore(self):
        self.templateSimulateTest(10, 1, solve_type.FAST, ccore_flag = True);
     
    def testRK4Solution(self):
        # Check for convergence when solution using RK4 function of calculation of derivative
        self.templateSimulateTest(10, 1, solve_type.RK4);   
     
    def testRK4SolutionByCore(self):
        self.templateSimulateTest(10, 1, solve_type.RK4, ccore_flag = True);
     
    def testLargeNetwork(self):
        # Check for convergence of phases in large network - network that contains large number of oscillators
        self.templateSimulateTest(128, 1, solve_type.FAST);                      
     
     
     
    def templateDynamicSimulationConnectionTypeTest(self, num_osc, weight, connection_type):
        network = sync_network(num_osc, weight, type_conn = connection_type);
        network.simulate_dynamic(collect_dynamic = False);  # Just current state of network is required
         
        clusters = network.allocate_sync_ensembles(0.1);
        assert len(clusters) == 1;
         
    def testDynamicSimulationAllToAll(self):
        self.templateDynamicSimulationConnectionTypeTest(10, 1, conn_type.ALL_TO_ALL);
        self.templateDynamicSimulationConnectionTypeTest(50, 1, conn_type.ALL_TO_ALL);
         
    def testDynamicSimulationGridFour(self):
        self.templateDynamicSimulationConnectionTypeTest(9, 1, conn_type.GRID_FOUR);
        self.templateDynamicSimulationConnectionTypeTest(25, 1, conn_type.GRID_FOUR);
 
    def testDynamicSimulationGridEight(self):
        self.templateDynamicSimulationConnectionTypeTest(9, 1, conn_type.GRID_FOUR);
        self.templateDynamicSimulationConnectionTypeTest(25, 1, conn_type.GRID_FOUR);
 
    def testDynamicSimulationBidir(self):
        self.templateDynamicSimulationConnectionTypeTest(5, 1, conn_type.LIST_BIDIR);
        self.templateDynamicSimulationConnectionTypeTest(10, 1, conn_type.LIST_BIDIR);


    def templateDynamicSimulationConvergence(self, num_osc, weight, connection_type, ccore_flag):
        network = sync_network(num_osc, weight, type_conn = connection_type, initial_phases=initial_type.EQUIPARTITION, ccore = ccore_flag);
        (t, dyn) = network.simulate_dynamic(collect_dynamic = False);  # Just current state of network is required
        
        #import pyclustering.support;
        #pyclustering.support.draw_dynamics(t, dyn);
        
        clusters = network.allocate_sync_ensembles(0.1);
        assert len(clusters) == 1;
        
    def testTwoOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(2, 1, conn_type.ALL_TO_ALL, False);
        self.templateDynamicSimulationConvergence(2, 1, conn_type.ALL_TO_ALL, True);
        
    def testThreeOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(3, 1, conn_type.ALL_TO_ALL, False);
        self.templateDynamicSimulationConvergence(3, 1, conn_type.ALL_TO_ALL, True);

    def testFourOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(4, 1, conn_type.ALL_TO_ALL, False);
        self.templateDynamicSimulationConvergence(4, 1, conn_type.ALL_TO_ALL, True);
 
    def testFiveOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(5, 1, conn_type.ALL_TO_ALL, False);
        self.templateDynamicSimulationConvergence(5, 1, conn_type.ALL_TO_ALL, True);
         
    def testSixOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(6, 1, conn_type.ALL_TO_ALL, False);
        self.templateDynamicSimulationConvergence(6, 1, conn_type.ALL_TO_ALL, True);
 
    def testSevenOscillatorDynamic(self):
        self.templateDynamicSimulationConvergence(7, 1, conn_type.ALL_TO_ALL, False);
        self.templateDynamicSimulationConvergence(7, 1, conn_type.ALL_TO_ALL, True);
        

if __name__ == "__main__":
    unittest.main();
