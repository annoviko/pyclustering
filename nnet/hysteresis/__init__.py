import numpy;

from scipy.integrate import odeint;

from support import draw_dynamics;
from support.differential import *;

import matplotlib.pyplot as plt;

class solve_type:
    FAST = 1;                   # Usual calculation: x(k + 1) = x(k) + f(x(k)).
    ODEINT = 2;                 # Runge-Kutte method with fixed step.
    ODE = 3;

class hysteresis_network:
    _name = "Hysteresis Neural Network"
    _num_osc = 0;
    _states = None;
    __outputs_buffer = None;
    _outputs = None;
    _weight = None;
    #_time_constant = 0;
    
    @property
    def outputs(self):
        return self._outputs;
    
    @outputs.setter
    def outputs(self, values):
        self._outputs = [val for val in values];
        self.__outputs_buffer = [val for val in values];
    
    @property
    def states(self):
        return self._states;
    
    @states.setter
    def states(self, values):
        self._states = [val for val in values];
    
    
    def __init__(self, num_osc, own_weight = -4, neigh_weight = -1, time_constant = 1):
        self._num_osc = num_osc;
        
        self._states = [0] * self._num_osc;
        self._outputs = [-1] * self._num_osc;
        self.__outputs_buffer = [-1] * self._num_osc;
        self._time_contant = time_constant;
        
        self._weight = list();
        for index in range(0, self._num_osc, 1):
            self._weight.append( [neigh_weight] * self._num_osc);
            self._weight[index][index] = own_weight;

    
    def _scipy_neuron_state(self, inputs, t, argv):
        return self._neuron_states(t, inputs[0], [ argv ]);
    
    def _neuron_states(self, t, inputs, argv):
        xi = inputs;
        index = argv[0];
        impact = 0;
        
        for i in range(0, self._num_osc, 1):
            impact += self._weight[index][i] * self._outputs[i];

        x = -xi + impact;
        
        #if (xi > 1): self._outputs[index] = 1; 
        #if (xi < -1): self._outputs[index] = -1;
                
        if (xi > 1): self.__outputs_buffer[index] = 1; 
        if (xi < -1): self.__outputs_buffer[index] = -1;
        
        return x / self._time_contant;
        
    
    def simulate(self, steps, time, solution = diffsolver.DIFF_SOLVER_RK4, collect_dynamic = True):
        return self.simulate_static(steps, time, solution, collect_dynamic);
    
    
    def simulate_static(self, steps, time, solution = diffsolver.DIFF_SOLVER_RK4, collect_dynamic = False):
        "Simulate network during specified time and return dynamic of the network if it's required"
        dyn_state = None;
        dyn_time = None;
        
        if (collect_dynamic == True):
            dyn_state = [];
            dyn_time = [];
            
            dyn_state.append(self._states);
            dyn_time.append(0);
        
        step = time / steps;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._states = self._calculate_states(solution, t, step, 10);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_state.append(self._states);
                dyn_time.append(t);
            else:
                dyn_state = self._states;
                dyn_time = t;
        
        return (dyn_time, dyn_state);   
    
        
    def _calculate_states(self, solution, t, step, steps):
        "Return new states for neurons"
        next_states = [0] * self._num_osc;
        
        for index in range (0, self._num_osc, 1):            
            if (solution == diffsolver.DIFF_SOLVER_RK4):
                (times, values) = rk4(self._neuron_states, self._states[index], t - step, t, steps, (index, ));
                next_states[index] = values[len(values) - 1];
            elif (solution == diffsolver.DIFF_SOLVER_RKF45):
                (times, values) = rkf45(self._neuron_states, self._states[index], t - step, t, steps, argv = (index , ));
                next_states[index] = values[len(values) - 1];                
            elif (solution == diffsolver.UNDEFINED):
                result = odeint(self._scipy_neuron_state, self._states[index], numpy.arange(t - step, t, step / 10), (index , ));
                next_states[index] = result[len(result) - 1][0];
            else:
                assert(0);
        
        self._outputs = [val for val in self.__outputs_buffer];
        return next_states;
    
    
network = hysteresis_network(2, -3, -1);
network.states[0] = 1; network.outputs[0] = 1; network.states[1] = 0; network.outputs[1] = 1;
 
from support import timedcall;
 
(time, (t, x)) = timedcall(network.simulate, 1000, 10, diffsolver.DIFF_SOLVER_RKF45);
print("RKF45: ", time);
 
network = hysteresis_network(2, -3, -1);
network.states[0] = 1; network.outputs[0] = 1; network.states[1] = 0; network.outputs[1] = 1;
 
(time, (t, x)) = timedcall(network.simulate, 1000, 10, diffsolver.DIFF_SOLVER_RK4);
print("RK45: ", time);

network = hysteresis_network(2, -3, -1);
network.states[0] = 1; network.outputs[0] = 1; network.states[1] = 0; network.outputs[1] = 1;

(time, (t, x)) = timedcall(network.simulate, 1000, 10, diffsolver.UNDEFINED);
print("ODEINT: ", time);


draw_dynamics(t, x, x_title = "Time", y_title = "x(t)");