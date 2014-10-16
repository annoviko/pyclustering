import unittest;

from nnet import *;
from nnet.sync import sync_network, phase_normalization;

from scipy import pi;


class Test(unittest.TestCase):
    def test_create(self):
        network = sync_network(10, 1);
        assert network.num_osc == 10;
  
  
    def test_creation_deletion_by_core(self):
        # Crash occurs in case of memory leak
        for iteration in range(0, 15):
            network = sync_network(4096, 1, type_conn = conn_type.ALL_TO_ALL, ccore = True);
            del network;
    
    
    def test_phase_normalization(self):       
        "Check for phase normalization"
        assert phase_normalization(2 * math.pi + 1) == 1;
        assert phase_normalization(2 * math.pi) == 2 * math.pi;
        assert phase_normalization(0) == 0;
        assert phase_normalization(4 * math.pi) == 2 * math.pi;
        assert phase_normalization(-2 * math.pi) == 0;
    
    
    def test_sync_order_single_osc(self):
        # Check for order parameter of network with one oscillator
        network = sync_network(1, 1);
        assert network.sync_order() == 1;
    
    
    def test_sync_order_network(self):
        # Check for order parameter of network with several oscillators
        network = sync_network(20, 1);
        assert network.sync_order() < 0.5;
        
        sync_state = 1;
        tolerance = 0.1;
        
        network.simulate(50, 20, solve_type.RK4);
        assert (abs(network.sync_order() - sync_state) < tolerance) == True;        
    
    
    def test_sync_local_order_single_osc(self):
        network = sync_network(1, 1);
        assert network.sync_local_order() == 0;   
        
        
    def test_sync_local_order_network(self):
        network = sync_network(10, 1);
        network.cluster = 2;
        network.simulate(20, 10, solve_type.RK4); 

        # There are all-to-all connected network, but two clusters, so it means that we have half sync. state Rc ~ 0.5.
        assert (abs(network.sync_local_order() - 0.5) < 0.2) == True;
        
        network.cluster = 1;
        network.simulate(40, 15, solve_type.FAST);
        assert (abs(network.sync_local_order() - 1) < 0.1) == True;
    
    
    def test_fast_solution(self):
        # Check for convergence when solution using fast way of calculation of derivative
        self.template_simulate_test(10, 1, solve_type.FAST);
        
    
    def test_odeint_solution(self):
        # Check for convergence when solution using RK4 function of calculation of derivative
        self.template_simulate_test(10, 1, solve_type.RK4);   
    
    
    def test_large_network(self):
        # Check for convergence of phases in large network - network that contains large number of oscillators
        self.template_simulate_test(128, 1, solve_type.FAST);              
        
        
    def template_simulate_test(self, nodes = 10, weight = 1, solution = solve_type.FAST, ccore_flag = False):
        sim_time = 20;
        sim_steps = 50;
        tolerance = 0.01;
        
        network = sync_network(nodes, weight, ccore = ccore_flag);
              
        (t, dyn_phase) = network.simulate(sim_steps, sim_time, solution);
        
        index = len(dyn_phase) - 1;
        value = dyn_phase[index][0];
        
        for item in dyn_phase[index]:
            assert (abs(item - value) < tolerance) == True;        
    
    
    def test_cluster_parameter(self):
        # Check feature of oscillatory network to clustering oscillators using internal cluster parameter
        self.template_cluster_parameter_test(10, 1, 1);
        self.template_cluster_parameter_test(10, 1, 2);
        self.template_cluster_parameter_test(10, 5, 2);
        self.template_cluster_parameter_test(25, 1, 5);     # Unstable test
        
        
    def template_cluster_parameter_test(self, num_osc = 10, weight = 1, cluster_param = 2, tolerance = 0.1):
        network = sync_network(num_osc, weight);   
        network.cluster = cluster_param;
        
        network.simulate(50, 20, solve_type.RK4);
        clusters = network.allocate_sync_ensembles(0.1);
        
        assert len(clusters) == cluster_param;

    
    def test_all_to_all_connection(self):
        # Check creation of coupling between oscillator in all-to-all case
        network = sync_network(10, 1, type_conn = conn_type.ALL_TO_ALL);
        self.template_all_to_all_connection_test(network);


    def test_all_to_all_connection_list_represent(self):
        network = sync_network(10, 1, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.LIST);
        self.template_all_to_all_connection_test(network);        


    def template_all_to_all_connection_test(self, network):
        for i in range(0, network.num_osc, 1):
            for j in range(0, network.num_osc, 1):
                if (i != j):
                    assert network.has_connection(i, j) == True;
                else:
                    assert network.has_connection(i, j) == False; 
    

    def test_none_connection(self):
        network = sync_network(10, 1, type_conn = conn_type.NONE);
        self.template_none_connection_test(network);


    def test_none_connection_list_represent(self):
        network = sync_network(10, 1, type_conn = conn_type.NONE, conn_represent = conn_represent.LIST);
        self.template_none_connection_test(network);


    def template_none_connection_test(self, network):
        for i in range(0, network.num_osc, 1):
            for j in range(0, network.num_osc, 1):
                assert network.has_connection(i, j) == False;
        

    def test_bidir_list_connection(self):
        # Check creation of coupling between oscillator in bidirectional list case
        network = sync_network(10, 1, type_conn = conn_type.LIST_BIDIR);
        self.template_bidir_list_connection_test(network);
    
    
    def test_bidir_list_connection_list_represent(self):
        network = sync_network(10, 1, type_conn = conn_type.LIST_BIDIR, conn_represent = conn_represent.LIST);
        self.template_bidir_list_connection_test(network);
    
    
    def template_bidir_list_connection_test(self, network):
        for index in range(0, network.num_osc, 1):
            if (index > 0):
                assert network.has_connection(index, index - 1) == True;
            
            if (index < (network.num_osc - 1)):
                assert network.has_connection(index, index + 1) == True;        
    
    
    def test_grid_four_connection(self):
        # Check creation of coupling between oscillator in grid with four neighbors case
        network = sync_network(25, 1, type_conn = conn_type.GRID_FOUR);
        self.template_grid_four_connection_test(network);
    
    
    def test_grid_four_connection_list_represent(self):
        # Check creation of coupling between oscillator in grid with four neighbors case
        network = sync_network(25, 1, type_conn = conn_type.GRID_FOUR, conn_represent = conn_represent.LIST);        
        self.template_grid_four_connection_test(network);

    
    def template_grid_four_connection_test(self, network):
        for index in range(0, network.num_osc, 1):
            upper_index = index - 5;
            lower_index = index + 5;
            left_index = index - 1;
            right_index = index + 1;
            
            node_row_index = math.ceil(index / 5);
            if (upper_index >= 0):
                assert network.has_connection(index, upper_index) == True;
            
            if (lower_index < network.num_osc):
                assert network.has_connection(index, lower_index) == True;
            
            if ( (left_index >= 0) and (math.ceil(left_index / 5) == node_row_index) ):
                assert network.has_connection(index, left_index) == True;
            
            if ( (right_index < network.num_osc) and (math.ceil(right_index / 5) == node_row_index) ):
                assert network.has_connection(index, right_index) == True;
    
    
    def test_initial_phases_equipartition(self):
        network = sync_network(3, 1, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.MATRIX, initial_phases = initial_type.EQUIPARTITION);
        assert len(network.phases) == 3;
        assert network.phases == [0, pi, 2.0 * pi];
        
        network = sync_network(10, 1, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.MATRIX, initial_phases = initial_type.EQUIPARTITION);
        assert len(network.phases) == 10;
        assert network.phases[0] == 0;
        assert network.phases[9] == 2 * pi;
        
        for index in range(len(network.phases)):
            assert network.phases[index] == ( (2.0 * pi) / 9.0 ) * index;
    
    
    def template_dynamic_simulation_connection_type_test(self, num_osc, weight, connection_type):
        network = sync_network(num_osc, weight, type_conn = connection_type);
        network.simulate_dynamic(collect_dynamic = False);  # Just current state of network is required
        
        clusters = network.allocate_sync_ensembles(0.1);
        assert len(clusters) == 1;
        
    
    def test_dynamic_simulation_all_to_all(self):
        self.template_dynamic_simulation_connection_type_test(10, 1, conn_type.ALL_TO_ALL);
        self.template_dynamic_simulation_connection_type_test(50, 1, conn_type.ALL_TO_ALL);
        
        
    def test_dynamic_simulation_grid_four(self):
        self.template_dynamic_simulation_connection_type_test(9, 1, conn_type.GRID_FOUR);
        self.template_dynamic_simulation_connection_type_test(25, 1, conn_type.GRID_FOUR);

        
    def test_dynamic_simulation_grid_eight(self):
        self.template_dynamic_simulation_connection_type_test(9, 1, conn_type.GRID_FOUR);
        self.template_dynamic_simulation_connection_type_test(25, 1, conn_type.GRID_FOUR);

        
    def test_dynamic_simulation_bidir(self):
        self.template_dynamic_simulation_connection_type_test(5, 1, conn_type.LIST_BIDIR);
        self.template_dynamic_simulation_connection_type_test(10, 1, conn_type.LIST_BIDIR);


    def template_dynamic_simulation_cluster_parameter(self, num_osc, cluster_parameter, ccore_flag = False):
        network = sync_network(num_osc, 1, 0, cluster_parameter, conn_type.ALL_TO_ALL, ccore = ccore_flag);   
          
        network.simulate_dynamic(solution = solve_type.RK4);
        clusters = network.allocate_sync_ensembles(0.1);
        
        assert len(clusters) == cluster_parameter;
        assert sum([len(cluster) for cluster in clusters]) == num_osc;


    def test_dynamic_simulation_cluster_parameter_2(self):
        self.template_dynamic_simulation_cluster_parameter(20, 2);
        
        
    def test_dynamic_simulation_cluster_parameter_3(self):
        self.template_dynamic_simulation_cluster_parameter(20, 3);
        
    
    def test_dynamic_simulation_cluster_parameter_4(self):
        self.template_dynamic_simulation_cluster_parameter(20, 4);
    
    
    def test_dynamic_simulation_cluster_parameter_6(self):
        self.template_dynamic_simulation_cluster_parameter(20, 6);
    
    
    def test_static_simulation_by_core(self):
        self.template_simulate_test(10, 1, solve_type.FAST, True);
        

if __name__ == "__main__":
    unittest.main();
