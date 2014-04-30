import numpy;
import math;

from nnet import *;  

from support import heaviside;

from scipy.integrate import odeint;


class legion_parameters:
    eps         = 0.02;
    alpha       = 0.005;
    gamma       = 6.0;
    betta       = 0.1;
    lamda       = 0.1;
    teta        = 0.9;
    teta_x      = -0.5;
    teta_p      = 7.0;
    tate_xz     = 0.1;
    T           = 2.0;
    mu          = 0.01;
    Wz          = 1.5;
    fi          = 3.0;


class legion_network(network):
    _name = "Local excitatory global inhibitory oscillatory network (LEGION)"
    
    _excitatory = None;
    _inhibitory = None;
    _potential = None;
    
    _stimulus = None;
    _coupling_term = None;
    _global_inhibitor = 0;
    
    _buffer_coupling_term = None;
    _dynamic_coupling = None;
    
    _params = None;
    
    def __init__(self, num_osc, parameters = None, conn_type = conn_type.ALL_TO_ALL):
        self._num_osc = num_osc;
        self._create_structure(conn_type);
        
        # set parameters of the network
        if (parameters is not None):
            self._params = parameters;
        else:
            self._params = legion_parameters();
        
        # calculate dynamic weights
        
    def simulate(self, steps, time, solution = solve_type.FAST, collect_dynamic = True):
        self.simulate_static(steps, time, solution, collect_dynamic);
    
    def simulate_static(self, steps, time, solution = solve_type.FAST, collect_dynamic = False):
        dyn_exc = None;
        dyn_time = None;
        
        # Store only excitatory of the oscillator
        if (collect_dynamic == True):
            dyn_exc = [];
            dyn_time = [];
            
        step = time / steps;
        int_step = step / 10;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._excitatory = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_exc.append(self._excitatory);
                dyn_time.append(t);
            else:
                dyn_exc = self._excitatory;
                dyn_time = t;
        
        return (dyn_time, dyn_exc); 
    
    
    def _calculate_states(self, solution, t, step, int_step):
        next_excitatory = [0] * self._num_osc;
        next_inhibitory = [0] * self._num_osc;
        next_potential = [0] * self._num_osc;
        
        # Update states of oscillators
        for index in range (0, self.num_osc, 1):
            if (solution == solve_type.FAST):
                [ next_excitatory[index], next_inhibitory[index], next_potential[index] ]  = self._states[index] + self.legion_state(self._states[index], 0, index);
                
            elif (solution == solve_type.ODEINT):
                result = odeint(self.legion_state, [self._excitatory[index], self._inhibitory[index], self._potential[index]], numpy.arange(t - step, t, int_step), (index , ));
                [ next_excitatory[index], next_inhibitory[index], next_potential[index] ] = result[len(result) - 1][0:3];
                
            else:
                assert 0;
        
        # Update state of global inhibitory
        if (solution == solve_type.FAST):
            z = self._global_inhibitor + self.global_inhibitor_state(self._global_inhibitor, t, None);
            
        elif (solution == solve_type.ODEINT):
            result = odeint(self.global_inhibitor_state, self._global_inhibitor, numpy.arange(t - step, t, int_step), None);
            
        else:
            assert 0;
        
        
        self._coupling_term = [val for val in self._buffer_coupling_term];
        self._inhibitory = next_inhibitory;
        self._potential = next_potential;
        
        return next_excitatory;
    
    
    def get_neighbors(self, index):
        "Return list of neighbors of a oscillator with sequence number 'index'"
        
        "(in) index    - index of oscillator in the network"
        
        "Return list of neighbors"
        if (self._conn_represent == conn_represent.LIST):
            return self._osc_conn[index];      # connections are represented by list.
        elif (self._conn_represent == conn_represent.MATRIX):
            return [neigh_index for neigh_index in range(self._num_osc) if self._osc_conn[index][neigh_index] == True];
        else:
            raise NameError("Unknown type of representation of connections");
    
    def global_inhibitor_state(self, z, t, argv):
        sigma = 0;
        
        for x in self._excitatory:
            if (x > self._params.teta_zx):
                sigma = 1;
                break;
        
        return self._params.fi * (sigma - z);
    
    def legion_state(self, inputs, t, argv):
        index = argv;
        
        x = inputs[0];
        y = inputs[1];
        p = inputs[2];
        
        dx = 3 * x - x ** 3 + 2 - y + self._stimulus[index] + self._coupling_term[index];
        dy = self._params.eps * (self._params.gamma * (1 + math.atanh(x / self._params.betta)) - y);
        
        neighbors = self.get_neighbors(index);
        potential = 0;
        
        for index_neighbor in neighbors:
            potential += self._params.T * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
        
        dp = self._params.lamda * (1 - p) * heaviside(potential - self._params.teta_p) - self._params.mu * p;

        coupling = 0
        for index_neighbor in neighbors:
            coupling += self._dynamic_coupling[index_neighbor][index] * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
            
        self._buffer_coupling_term[index] = self._dynamic_coupling[index_neighbor][index] * self._params.Wz * heaviside(self._global_inhibitor - self._params.teta_xz);
        
        return [dx, dy, dp];
    
        