'''

Neural Network: Oscillatory Neural Network based on Hodgkin-Huxley Neuron Model

Based on article description:
 - D.Chik, R.Borisyuk, Y.Kazanovich. "Selective attention model with spiking elements" - Nov. 2009.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from nnet import *;

from scipy.integrate import odeint;

import numpy;
import random;

class hhn_params:    
    nu = random.random() * 2.0 - 1.0;
    
    gNa = 120.0 * (1 + 0.02 * nu);
    gK = 0.3 * (1 + 0.02 * nu);
    gL = -1.1;
    
    vNa = 50.0;
    vK = -77.0;
    vL = -54.4;
    
    Icn1 = 5.0;
    Icn2 = 30.0;


class hhn_network(network, network_interface):
    _name = "Oscillatory Neural Network based on Hodgkin-Huxley Neuron Model"
    
    _membrane_potential = None;          # membrane potential of neuron (V)
    
    _active_cond_sodium = None;          # activation conductance of the sodium channel (h).
    _inactive_cond_sodium = None;        # inactivaton conductance of the sodium channel (m).
    _active_cond_potassium = None;       # activation conductance of the potassium channel (n).
    
    _stimulus = None;               # stimulus of each oscillator
    
    _params = None;                 # parameters of the network
    _noise = None;
    
    def __init__(self, num_osc, stimulus = None, parameters = None, type_conn = conn_type.NONE, conn_represent = conn_represent.MATRIX):
        super().__init__(num_osc, type_conn, conn_represent);
        
        self._active_cond_sodium = [0.0] * self._num_osc;
        self._inactive_cond_sodium = [0.0] * self._num_osc;
        self._active_cond_potassium = [0.0] * self._num_osc;
        
        self._membrane_potential = [0.0] * self._num_osc;
        self._noise = [random.random() * 2.0 - 1.0 for i in range(self._num_osc)];
        
        if (stimulus is None):
            self._stimulus = [0.0] * self._num_osc;
        else:
            self._stimulus = stimulus;
        
        if (parameters is not None):
            self._params = parameters;
        else:
            self._params = hhn_params();
    
    
    def simulate(self, steps, time, solution = solve_type.RK4, collect_dynamic = True):
        "Performs static simulation of oscillatory network based on Hodgkin-Huxley neuron model."
        
        "(in) steps            - number steps of simulations during simulation."
        "(in) time             - time of simulation."
        "(in) solution         - type of solution (solving)."
        "(in) collect_dynamic  - if True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics."
        
        "Returns dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,"
        "otherwise returns only last values (last step of simulation) of dynamic."
        
        return self.simulate_static(steps, time, solution, collect_dynamic);


    def simulate_dynamic(self, order, solution, collect_dynamic, step, int_step, threshold_changes):
        "Performs dynamic simulation, when time simulation is not specified, only stop condition."
        "The method is not supported."
        
        raise NameError("Dynamic simulation is not supported due to lack of stop conditions for the model.");

    
    def simulate_static(self, steps, time, solution = solve_type.RK4, collect_dynamic = False):  
        "Performs static simulation of oscillatory network based on Hodgkin-Huxley neuron model."
        
        "(in) steps            - number steps of simulations during simulation."
        "(in) time             - time of simulation."
        "(in) solution         - type of solution (only RK4 is supported for python implementation)."
        "(in) collect_dynamic  - if True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics."
        
        "Returns dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,"
        "otherwise returns only last values (last step of simulation) of dynamic."        
        
        # Check solver before simulation
        if (solution == solve_type.FAST):
            raise NameError("Solver FAST is not support due to low accuracy that leads to huge error.");
        elif (solution == solve_type.RKF45):
            raise NameError("Solver RKF45 is not support in python version.");
        
        if (self._dyn_exc is not None):
            del self._dyn_exc;
            self._dyn_exc = None;
        
        dyn_memb = None;
        dyn_time = None;
        
        # Store only excitatory of the oscillator
        if (collect_dynamic == True):
            dyn_memb = [];
            dyn_time = [];
            
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._excitatory = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_memb.append(self._excitatory);
                dyn_time.append(t);
            else:
                dyn_memb = self._membrane_potential;
                dyn_time = t;
        
        self._membrane_potential = dyn_memb;
        return (dyn_time, dyn_memb);
    
    
    def _calculate_states(self, solution, t, step, int_step):
        "Caclculates new state of each oscillator in the network. Returns only excitatory state of oscillators."
        
        "(in) solution        - type solver of the differential equation."
        "(in) t               - current time of simulation."
        "(in) step            - step of solution at the end of which states of oscillators should be calculated."
        "(in) int_step        - step differentiation that is used for solving differential equation."
        
        "Returns new state of excitatory parts of oscillators."
        
        next_membrane = [0.0] * self._num_osc;
        
        # Update states of oscillators
        for index in range (0, self._num_osc, 1):
            result = odeint(self.hhn_state, self._membrane_potential[index], numpy.arange(t - step, t, int_step), (index , ));
            next_membrane[index] = result[len(result) - 1];
        
        return next_membrane;
    
    
    def hnn_state(self, inputs, t, argv):
        "Returns new values of excitatory and inhibitory parts of oscillator and potential of oscillator."
        
        "(in) t             - current time of simulation."
        "(in) argv          - extra arguments that are not used for integration - index of oscillator."
        
        "Returns new values of excitatoty and inhibitory part of oscillator and new value of potential (not assign)."
        
        index = argv;
        
        # Calculate ion current
        # gNa * m[i]^3 * h * (v[i] - vNa) + gK * n[i]^4 * (v[i] - vK) + gL  (v[i] - vL)
        active_sodium_part = self._params.gNa * (self._active_cond_sodium[index] ** 3) * (self._membrane_potential[index] - self._params.vNa);
        inactive_sodium_part = self._params.gK * (self._inactive_cond_sodium[index] ** 4) * (self._membrane_potential[index] - self._params.vK);
        active_potassium_part = self._params.gL * (self._membrane_potential - self._params.vL);
        
        Iion = active_sodium_part + inactive_sodium_part + active_potassium_part;
        
        # Caclulation states
        Iext = 0;
        Isyn = 0;
        
        dv = -Iion + Iext - Isyn;
        dh = 0;
        dk = 0;
        dl = 0;
        
        return [dv, dh, dk, dl];
        