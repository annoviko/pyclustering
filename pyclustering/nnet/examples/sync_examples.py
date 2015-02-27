"""!

@brief Examples of usage and demonstration of abilities of Oscillatory Neural  Network based on Kuramoto model.

@authors Andrei Novikov (spb.andr@yandex.ru)
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

from pyclustering.support import draw_dynamics;

from pyclustering.nnet import solve_type, conn_type;
from pyclustering.nnet.sync import sync_network;

def template_dynamic_sync(num_osc, k = 1, q = 1, sim_arg = None, conn = conn_type.ALL_TO_ALL, type_solution = solve_type.FAST, collect_dyn = True, ccore_flag = False):
    network = sync_network(num_osc, k, type_conn = conn, ccore = ccore_flag);
    network.cluster = q;

    if (sim_arg is not None):
        (t, dyn_phase) = network.simulate(sim_arg[0], sim_arg[1], solution = type_solution, collect_dynamic = collect_dyn);
    else:
        (t, dyn_phase) = network.simulate_dynamic(collect_dynamic = collect_dyn, solution = type_solution);
        
    draw_dynamics(t, dyn_phase, x_title = "Time", y_title = "Phase", y_lim = [0, 2 * 3.14]);
    return network;
    

# Positive connections
def trivial_dynamic_sync():
    template_dynamic_sync(100, 1, sim_arg = [50, 10]);
    template_dynamic_sync(100, 1, sim_arg = [50, 10], ccore_flag = True);

def weight_5_dynamic_sync():
    template_dynamic_sync(10, 10, sim_arg = [100, 10], type_solution = solve_type.RK4);
    
def cluster_2_dynamic_sync():
    template_dynamic_sync(10, 1, q = 2, sim_arg = [20, 10], type_solution = solve_type.RK4);

def cluster_5_dynamic_sync():
    template_dynamic_sync(50, 1, q = 5, sim_arg = [20, 10], type_solution = solve_type.RK4);

def bidir_struct_dynamic_sync():
    template_dynamic_sync(10, 100, sim_arg = [100, 10], conn = conn_type.LIST_BIDIR, type_solution = solve_type.RK4);    
    
def grid_four_struct_dynamic_sync():
    template_dynamic_sync(25, 50, sim_arg = [50, 10], conn = conn_type.GRID_FOUR, type_solution = solve_type.RK4);
    
        
# Negative connections        
def negative_connection_5_oscillators():
    template_dynamic_sync(5, -1); 
    template_dynamic_sync(5, -1, ccore_flag = True);    
    
def negative_connection_10_oscillators():
    "Comment: It is not full desynchronization"
    template_dynamic_sync(10, -3);     
    
def negative_connection_9_grid_struct():
    "Comment: Right coloring"
    network = template_dynamic_sync(9, -2, conn = conn_type.GRID_FOUR);      
    print(network.allocate_sync_ensembles(0.1));
    
    
def negative_connection_16_grid_struct():
    "Comment: Wrong coloring"
    network = template_dynamic_sync(16, -3, conn = conn_type.GRID_FOUR);    
    print(network.allocate_sync_ensembles(0.1));
    

# Examples of global synchronization and local (via q parameter).
trivial_dynamic_sync();
weight_5_dynamic_sync();
cluster_2_dynamic_sync();
cluster_5_dynamic_sync();
bidir_struct_dynamic_sync();
grid_four_struct_dynamic_sync();

# Examples with negative connection
negative_connection_5_oscillators();        # Almost full desynchronization
negative_connection_10_oscillators();       # It's not full desynchronization
negative_connection_9_grid_struct();        # Right coloring
negative_connection_16_grid_struct();       # Wrong coloring