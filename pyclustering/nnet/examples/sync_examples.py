"""!

@brief Examples of usage and demonstration of abilities of Oscillatory Neural Network based on Kuramoto model.

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


from pyclustering.nnet import solve_type, conn_type;
from pyclustering.nnet.sync import sync_network, sync_visualizer;


def template_dynamic_sync(num_osc, k = 1, sim_arg = None, conn = conn_type.ALL_TO_ALL, type_solution = solve_type.FAST, collect_dyn = True, ccore_flag = False):
    network = sync_network(num_osc, k, type_conn = conn, ccore = ccore_flag);

    if (sim_arg is not None):
        sync_output_dynamic = network.simulate(sim_arg[0], sim_arg[1], solution = type_solution, collect_dynamic = collect_dyn);
    else:
        sync_output_dynamic = network.simulate_dynamic(collect_dynamic = collect_dyn, solution = type_solution);

    sync_visualizer.show_output_dynamic(sync_output_dynamic);
    sync_visualizer.show_order_parameter(sync_output_dynamic);
    sync_visualizer.animate_output_dynamic(sync_output_dynamic);
    sync_visualizer.animate_correlation_matrix(sync_output_dynamic);

    return network;


# Positive connections
def trivial_dynamic_sync():
    template_dynamic_sync(100, 1, sim_arg = [50, 10]);
    template_dynamic_sync(100, 1, sim_arg = [50, 10], ccore_flag = True);

def weight_5_dynamic_sync():
    template_dynamic_sync(10, 10, sim_arg = [100, 10], type_solution = solve_type.RK4);

def bidir_struct_dynamic_sync():
    template_dynamic_sync(10, 100, sim_arg = [100, 10], conn = conn_type.LIST_BIDIR, type_solution = solve_type.RK4);    
    
def grid_four_struct_dynamic_sync():
    template_dynamic_sync(25, 50, sim_arg = [50, 10], conn = conn_type.GRID_FOUR, type_solution = solve_type.RK4);


def dynamic_simulation_all_to_all_structure():
    template_dynamic_sync(25, 1, conn = conn_type.ALL_TO_ALL, ccore_flag = True);

def dynamic_simulation_grid_four_structure():
    template_dynamic_sync(25, 1, conn = conn_type.GRID_FOUR, ccore_flag = True);

def dynamic_simulation_bidir_list_structure():
    template_dynamic_sync(25, 1, conn = conn_type.LIST_BIDIR, ccore_flag = True);

# Negative connections        
def negative_connection_5_oscillators():
    template_dynamic_sync(5, -1); 
    template_dynamic_sync(5, -1, ccore_flag = True);
    
def negative_connection_10_oscillators():
    "Comment: It is not full desynchronization"
    template_dynamic_sync(10, -3);
    
def negative_connection_9_grid_struct():
    "Comment: Right coloring"
    _ = template_dynamic_sync(9, -2, conn = conn_type.GRID_FOUR);
    
    
def negative_connection_16_grid_struct():
    "Comment: Wrong coloring"
    _ = template_dynamic_sync(16, -3, conn = conn_type.GRID_FOUR);


def template_animate_output_dynamic(title, amount_oscillators, coupling_stregth, frequency, order):
    network = sync_network(amount_oscillators, coupling_stregth, frequency, ccore = True);
    sync_output_dynamic = network.simulate_dynamic(order, solution = solve_type.RK4, collect_dynamic = True);
    
    sync_visualizer.animate(sync_output_dynamic, title);
    #sync_visualizer.animate(sync_output_dynamic, title);

def animate_phase_locking():
    template_animate_output_dynamic("Phase locking", 300, 1.0, 1.0, 0.995);

def animate_global_synchronization():
    template_animate_output_dynamic("Global synchronization", 300, 0.5, 0.0, 0.9999);


def template_animate_phase_matrix(num_osc, strength = 1.0, steps = None, time = None, conn = conn_type.ALL_TO_ALL, type_solution = solve_type.FAST, ccore_flag = True):
    network = sync_network(num_osc, strength, type_conn = conn, ccore = ccore_flag);

    if ( (steps is not None) and (time is not None) ):
        sync_output_dynamic = network.simulate(steps, time, solution = type_solution, collect_dynamic = True);
    else:
        sync_output_dynamic = network.simulate_dynamic(collect_dynamic = True, order = 0.999, solution = type_solution);

    sync_visualizer.animate_phase_matrix(sync_output_dynamic);
    return network;

def animate_phase_matrix_400_all_to_all():
    template_animate_phase_matrix(400, 0.4, None, None, conn = conn_type.ALL_TO_ALL, type_solution = solve_type.FAST);

def animate_phase_matrix_400_grid_four():
    template_animate_phase_matrix(400, 2.0, conn = conn_type.GRID_FOUR);

def animate_phase_matrix_400_grid_eight():
    template_animate_phase_matrix(400, 1.0, conn = conn_type.GRID_EIGHT);

# Examples of global synchronization.
trivial_dynamic_sync();
weight_5_dynamic_sync();
bidir_struct_dynamic_sync();
grid_four_struct_dynamic_sync();

# Examples of global synchronization for various network structures
dynamic_simulation_all_to_all_structure();
dynamic_simulation_grid_four_structure();
dynamic_simulation_bidir_list_structure();

# Examples with negative connection
negative_connection_5_oscillators();        # Almost full desynchronization
negative_connection_10_oscillators();       # It's not full desynchronization
negative_connection_9_grid_struct();        # Right coloring
negative_connection_16_grid_struct();       # Wrong coloring
   
   
animate_phase_locking();
animate_global_synchronization();

animate_phase_matrix_400_all_to_all();
animate_phase_matrix_400_grid_four();
animate_phase_matrix_400_grid_eight();