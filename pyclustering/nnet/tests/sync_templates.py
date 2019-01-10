"""!

@brief Templates for tests of Sync (oscillatory network based on Kuramoto model).

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


# Generate images without having a window appear.
import matplotlib;
matplotlib.use('Agg');

from pyclustering.nnet import conn_type, solve_type, initial_type;
from pyclustering.nnet.sync import sync_network, sync_visualizer;


class SyncTestTemplates:
    @staticmethod
    def templateCreateNetwork(size, ccore_flag):
        network = sync_network(size, 1, ccore = ccore_flag);
        assert len(network) == size;


    @staticmethod
    def templateConnectionsApi(size, ccore_flag):
        network = sync_network(size, 1, type_conn = conn_type.ALL_TO_ALL, ccore = ccore_flag);
        for i in range(len(network)):
            for j in range(len(network)):
                if (i != j):
                    assert network.has_connection(i, j) == True;
                    assert len(network.get_neighbors(i)) == size - 1, str(network.get_neighbors(i));
                    assert len(network.get_neighbors(j)) == size - 1;


    @staticmethod
    def templateSimulateTest(nodes, weight, solution, ccore_flag):
        sim_time = 20;
        sim_steps = 50;
        tolerance = 0.01;
           
        network = sync_network(nodes, weight, ccore = ccore_flag);
                 
        output_dynamic = network.simulate(sim_steps, sim_time, solution);
         
        dyn_phase = output_dynamic.output;
         
        index = len(dyn_phase) - 1;
        value = dyn_phase[index][0];
           
        for item in dyn_phase[index]:
            if ((abs(item - value) < tolerance) != True):
                print(dyn_phase[:][0]);
                 
            assert (abs(item - value) < tolerance) == True;


    @staticmethod
    def templateDynamicSimulationConnectionTypeTest(num_osc, weight, connection_type, ccore_flag):
        testing_result = False;
        
        for _ in range(3):
            network = sync_network(num_osc, weight, type_conn = connection_type, ccore = ccore_flag);
            output_dynamic = network.simulate_dynamic(collect_dynamic = False);  # Just current state of network is required
            
            clusters = output_dynamic.allocate_sync_ensembles(0.1);
            
            if (len(clusters) != 1):
                continue;
            
            testing_result = True;
            break;
        
        assert testing_result == True;


    @staticmethod
    def templateDynamicSimulationConvergence(num_osc, weight, connection_type, ccore_flag):
        network = sync_network(num_osc, weight, type_conn = connection_type, initial_phases=initial_type.EQUIPARTITION, ccore = ccore_flag);
        output_dynamic = network.simulate_dynamic(collect_dynamic = False);  # Just current state of network is required
         
        clusters = output_dynamic.allocate_sync_ensembles(0.1);
        assert len(clusters) == 1;


    @staticmethod
    def templateOutputDynamicCalculateOrderParameter(ccore_flag):
        net = sync_network(5, ccore = ccore_flag);
        output_dynamic = net.simulate_static(20, 10, solution = solve_type.FAST, collect_dynamic = True);
        
        assert len(output_dynamic.calculate_order_parameter(0, 20)) == 20;
        assert len(output_dynamic.calculate_order_parameter()) == 1;
        assert len(output_dynamic.calculate_order_parameter(5)) == 1;
        assert len(output_dynamic.calculate_order_parameter(5, 10)) == 5;
        assert output_dynamic.calculate_order_parameter(20)[0] > 0.9;


    @staticmethod
    def templateOutputDynamicCalculateLocalOrderParameter(ccore_flag):
        net = sync_network(5, ccore = ccore_flag);
        output_dynamic = net.simulate_static(20, 10, solution = solve_type.FAST, collect_dynamic = True);
        
        assert len(output_dynamic.calculate_local_order_parameter(net, 0, 20)) == 20;
        assert len(output_dynamic.calculate_local_order_parameter(net)) == 1;
        assert len(output_dynamic.calculate_local_order_parameter(net, 5)) == 1;
        assert len(output_dynamic.calculate_local_order_parameter(net, 5, 10)) == 5;
        assert output_dynamic.calculate_local_order_parameter(net, 20)[0] > 0.9;


    @staticmethod
    def templateVisualizerNoFailures(size, velocity, ccore_flag):
        net = sync_network(size, ccore = ccore_flag);
        output_dynamic = net.simulate_dynamic(solution = solve_type.FAST, collect_dynamic = True);
        
        sync_visualizer.animate(output_dynamic);
        sync_visualizer.animate_correlation_matrix(output_dynamic, velocity);
        sync_visualizer.animate_output_dynamic(output_dynamic, velocity);
        sync_visualizer.animate_phase_matrix(output_dynamic, 1, size, velocity);
        sync_visualizer.show_correlation_matrix(output_dynamic);
        sync_visualizer.show_output_dynamic(output_dynamic);
        sync_visualizer.show_phase_matrix(output_dynamic, 1, size);
        sync_visualizer.show_order_parameter(output_dynamic);
        sync_visualizer.show_local_order_parameter(output_dynamic, net);


