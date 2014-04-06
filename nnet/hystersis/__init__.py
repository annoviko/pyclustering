import numpy;

from scipy.integrate import odeint;

from support import draw_dynamics;

import matplotlib.pyplot as plt;

class solve_type:
    FAST = 1;                   # Usual calculation: x(k + 1) = x(k) + f(x(k)).
    ODEINT = 2;                 # Runge-Kutte method with fixed step.
    ODE = 3;


class net:
    _name = "Hysteresis Neural Network"
    _num_osc = 0;
    _states = None;
    _hysters = None;
    _outputs = None;
    _weight = None;
    
    @property
    def outputs(self):
        return self._outputs;
    
    def __init__(self, num_osc):
        self._num_osc = num_osc;
        
        self._states = [0] * self._num_osc;
        self._outputs = [-1] * self._num_osc;
        self._hysters = [False] * self._num_osc;
        
        self._weight = list();
        for index in range(0, self._num_osc, 1):
            self._weight.append([-1] * self._num_osc);
            self._weight[index][index] = -4;

    
    def neuron_states(self, inputs, t, argv):
        xi = inputs[0];
        
        index = argv;
        
        impact = 0;
        for i in range(0, self._num_osc, 1):
            impact += self._weight[index][i] * self._outputs[i];
        
        x = -xi + impact;
        
        if (xi > -1):
            pass;
        
        if (xi > 1):
            self._outputs[index] = 1;
        
        if (xi < -1):
            self._outputs[index] = -1;
            
        return x;
        
    
    def simulate(self, steps, time, solution = solve_type.FAST, collect_dynamic = True):
        return self.simulate_static(steps, time, solution, collect_dynamic);
    
    
    def simulate_static(self, steps, time, solution = solve_type.FAST, collect_dynamic = False):
        "Simulate network during specified time and return dynamic of the network if it's required"
        dyn_state = None;
        dyn_time = None;
        
        if (collect_dynamic == True):
            dyn_state = [];
            dyn_time = [];
            
            dyn_state.append(self._states);
            dyn_time.append(0);
        
        step = time / steps;
        int_step = step / 10;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._states = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_state.append(self._states);
                dyn_time.append(t);
            else:
                dyn_state = self._states;
                dyn_time = t;
        
        return (dyn_time, dyn_state);   
    
        
    def _calculate_states(self, solution, t, step, int_step):
        "Return new states for neurons"
        next_states = [0] * self._num_osc;
        
        for index in range (0, self._num_osc, 1):
            if (solution == solve_type.FAST):
                next_states[index] = self.neuron_states([ self._states[index] ], 0, index);
                next_states[index] = next_states[index] / 100;
                next_states[index] += self._states[index];
                
            elif (solution == solve_type.ODEINT):
                result = odeint(self.neuron_states, self._states[index], numpy.arange(t - step, t, int_step), (index , ));
                next_states[index] = result[len(result) - 1][0];
                
            else:
                assert 0;
        
        return next_states;
    
    
network = net(1);

(t, x) = network.simulate(1000, 1);
#(t, x) = network.simulate(1000, 10, solve_type.ODEINT);
draw_dynamics(t, x, x_title = "Time", y_title = "x(t)");