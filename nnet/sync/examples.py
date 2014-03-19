from nnet import sync;

def trivial_dynamic_sync():
    network = sync.net(100, 1);
    (t, dyn_phase) = network.simulate(50, 10);
    sync.draw_dynamics(t, dyn_phase);
    

def weight_5_dynamic_sync():
    network = sync.net(10, 10);
    (t, dyn_phase) = network.simulate(100, 10, solution = sync.solve_type.ODEINT);
    sync.draw_dynamics(t, dyn_phase);
    

def cluster_2_dynamic_sync():
    network = sync.net(10, 1);
    network._cluster = 2;
    
    (t, dyn_phase) = network.simulate(20, 10, solution = sync.solve_type.ODEINT);
    sync.draw_dynamics(t, dyn_phase);


def cluster_5_dynamic_sync():
    network = sync.net(50, 1);
    network._cluster = 5;
    
    (t, dyn_phase) = network.simulate(20, 10, solution = sync.solve_type.ODEINT);
    sync.draw_dynamics(t, dyn_phase);


def bidir_struct_dynamic_sync():
    network = sync.net(10, 100, type_conn = sync.conn_type.LIST_BIDIR);
    (t, dyn_phase) = network.simulate(100, 10, solution = sync.solve_type.ODEINT);
    sync.draw_dynamics(t, dyn_phase);
    
    
def grid_four_struct_dynamic_sync():
    network = sync.net(25, 50, type_conn = sync.conn_type.GRID_FOUR);
    (t, dyn_phase) = network.simulate(50, 10, solution = sync.solve_type.ODEINT);
    sync.draw_dynamics(t, dyn_phase);
    
    
def time_dependence_grid_struct():
    number_oscillator = range(5, 100, 5);
    time_dependence = [];
    
    for num_osc in number_oscillator:
        network = sync.net(num_osc, 1, type_conn = sync.conn_type.GRID_FOUR, initial_phases = sync.initial_type.EQUIPARTITION);
        (t, dyn_phase) = network.simulate(50, 10, solution = sync.solve_type.ODEINT);
        
        
def negative_connection_5_oscillators():
    network = sync.net(5, -1);
    (t, dyn_phase) = network.simulate_dynamic(collect_dynamic = True, solution = sync.solve_type.FAST);
    sync.draw_dynamics(t, dyn_phase); 
       
    
def negative_connection_10_oscillators():
    "Comment: It is not full desynchronization"
    network = sync.net(10, -5);
    (t, dyn_phase) = network.simulate_dynamic(collect_dynamic = True, solution = sync.solve_type.FAST);
    sync.draw_dynamics(t, dyn_phase);
    
    
def negative_connection_9_grid_struct():
    "Comment: Right coloring"
    network = sync.net(9, -2, type_conn = sync.conn_type.GRID_FOUR);
    (t, dyn_phase) = network.simulate_dynamic(collect_dynamic = True, solution = sync.solve_type.FAST);
    sync.draw_dynamics(t, dyn_phase);
    
    print(network.allocate_sync_ensembles(0.1));
    
    
def negative_connection_16_grid_struct():
    "Comment: Wrong coloring"
    network = sync.net(16, -3, type_conn = sync.conn_type.GRID_FOUR);
    (t, dyn_phase) = network.simulate_dynamic(collect_dynamic = True, solution = sync.solve_type.FAST);
    sync.draw_dynamics(t, dyn_phase);
    
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