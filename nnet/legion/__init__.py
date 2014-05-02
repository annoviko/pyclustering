import numpy;
import math;
import random;

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
    teta_xz     = 0.1;
    teta_zx     = 0.1;
    T           = 2.0;
    mu          = 0.01;
    Wz          = 1.5;
    Wt          = 8.0;
    fi          = 3.0;
    ro          = 0.02;


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
    
    _noise = None;
    
    def __init__(self, num_osc, stimulus = None, parameters = None, type_conn = conn_type.ALL_TO_ALL, conn_represent = conn_represent.MATRIX):
        super().__init__(num_osc, type_conn, conn_represent);
        
        # set parameters of the network
        if (parameters is not None):
            self._params = parameters;
        else:
            self._params = legion_parameters();
            
        # initial states
        self._excitatory = [0] * self._num_osc;
        self._inhibitory = [0] * self._num_osc;
        self._potential = [0] * self._num_osc;
        
        self._coupling_term = [0] * self._num_osc;
        self._buffer_coupling_term = [0] * self._num_osc;
        
        # set stimulus
        self.__create_stimulus(stimulus);
        
        # calculate dynamic weights
        self.__create_dynamic_connections();
            
        # generate first noises
        self._noise = [random.random() * -self._params.ro for i in range(self._num_osc)];
    
    def __create_stimulus(self, stimulus):
        if (stimulus is None):
            self._stimulus = [0] * self._num_osc;
        else:
            if (len(stimulus) != self._num_osc):
                raise NameError("Number of stimulus should be equal number of oscillators in the network");
            else:
                self._stimulus = stimulus;
    
    def __create_dynamic_connections(self):
        if (self._stimulus is None):
            raise NameError("Stimulus should initialed before creation of the dynamic connections in the network");
        
        self._dynamic_coupling = [ [0] * self._num_osc for i in range(self._num_osc)];
        
        for i in range(self._num_osc):
            neighbors = self.get_neighbors(i);
            
            if ( (len(neighbors) > 0) and (self._stimulus[i] > 0) ):
                number_stimulated_neighbors = 0;
                for j in neighbors:
                    if (self._stimulus[j] > 0):
                        number_stimulated_neighbors += 1;
                
                if (number_stimulated_neighbors > 0):
                    dynamic_weight = self._params.Wt / number_stimulated_neighbors;
                    
                    for j in neighbors:
                        self._dynamic_coupling[i][j] = dynamic_weight;    
    
    def simulate(self, steps, time, solution = solve_type.ODEINT, collect_dynamic = True):
        return self.simulate_static(steps, time, solution, collect_dynamic);
    
    def simulate_static(self, steps, time, solution = solve_type.ODEINT, collect_dynamic = False):       
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
        for index in range (0, self._num_osc, 1):
            if (solution == solve_type.FAST):
                assert 0;
                #[ next_excitatory[index], next_inhibitory[index], next_potential[index] ]  = self.legion_state([self._excitatory[index], self._inhibitory[index], self._potential[index]], 0, index);
                #next_excitatory[index] += self._excitatory[index];
                #next_inhibitory[index] += self._inhibitory[index];
                #next_potential[index] += self._potential[index];
                
            elif (solution == solve_type.ODEINT):
                result = odeint(self.legion_state, [self._excitatory[index], self._inhibitory[index], self._potential[index]], numpy.arange(t - step, t, int_step), (index , ));
                [ next_excitatory[index], next_inhibitory[index], next_potential[index] ] = result[len(result) - 1][0:3];
                
            else:
                assert 0;
        
        # Update state of global inhibitory
        if (solution == solve_type.FAST):
            assert 0;
            # z = self._global_inhibitor + self.global_inhibitor_state(self._global_inhibitor, t, None);
            
        elif (solution == solve_type.ODEINT):
            result = odeint(self.global_inhibitor_state, self._global_inhibitor, numpy.arange(t - step, t, int_step), (None, ));
            self._global_inhibitor = result[len(result) - 1][0];
            
        else:
            assert 0;
        
        self._noise = [random.random() * self._params.ro for i in range(self._num_osc)];
        self._coupling_term = [val for val in self._buffer_coupling_term];
        self._inhibitory = next_inhibitory;
        self._potential = next_potential;
        
        return next_excitatory;
    
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
        
        dx = 3 * x - x ** 3 + 2 - y + self._stimulus[index] + self._coupling_term[index] + self._noise[index];
        dy = self._params.eps * (self._params.gamma * (1 + math.tanh(x / self._params.betta)) - y);
        
        neighbors = self.get_neighbors(index);
        potential = 0;
        
        for index_neighbor in neighbors:
            potential += self._params.T * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
        
        dp = self._params.lamda * (1 - p) * heaviside(potential - self._params.teta_p) - self._params.mu * p;

        coupling = 0
        for index_neighbor in neighbors:
            coupling += self._dynamic_coupling[index][index_neighbor] * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
            
        self._buffer_coupling_term[index] = coupling - self._params.Wz * heaviside(self._global_inhibitor - self._params.teta_xz);
        
        return [dx, dy, dp];
