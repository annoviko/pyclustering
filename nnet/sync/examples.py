from nnet import sync;
from support import draw_dynamics;
import support;

def template_dynamic_sync(num_osc, k = 1, q = 1, sim_arg = None, conn = sync.conn_type.ALL_TO_ALL, type_solution = sync.solve_type.FAST, collect_dyn = True):
    network = sync.net(num_osc, k, type_conn = conn);
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

def weight_5_dynamic_sync():
    template_dynamic_sync(10, 10, sim_arg = [100, 10], type_solution = sync.solve_type.ODEINT);
    
def cluster_2_dynamic_sync():
    template_dynamic_sync(10, 1, q = 2, sim_arg = [20, 10], type_solution = sync.solve_type.ODEINT);

def cluster_5_dynamic_sync():
    template_dynamic_sync(50, 1, q = 5, sim_arg = [20, 10], type_solution = sync.solve_type.ODEINT);

def bidir_struct_dynamic_sync():
    template_dynamic_sync(10, 100, sim_arg = [100, 10], conn = sync.conn_type.LIST_BIDIR, type_solution = sync.solve_type.ODEINT);    
    
def grid_four_struct_dynamic_sync():
    template_dynamic_sync(25, 50, sim_arg = [50, 10], conn = sync.conn_type.GRID_FOUR, type_solution = sync.solve_type.ODEINT);
    
        
# Negative connections        
def negative_connection_5_oscillators():
    template_dynamic_sync(5, -1);       
    
def negative_connection_10_oscillators():
    "Comment: It is not full desynchronization"
    template_dynamic_sync(10, -3);     
    
def negative_connection_9_grid_struct():
    "Comment: Right coloring"
    network = template_dynamic_sync(9, -2, conn = sync.conn_type.GRID_FOUR);      
    print(network.allocate_sync_ensembles(0.1));
    
    
def negative_connection_16_grid_struct():
    "Comment: Wrong coloring"
    network = template_dynamic_sync(16, -3, conn = sync.conn_type.GRID_FOUR);    
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