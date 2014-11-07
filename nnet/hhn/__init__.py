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
    nu      = random.random() * 2.0 - 1.0;
    
    gNa     = 120.0 * (1 + 0.02 * nu);
    gK      = 0.3 * (1 + 0.02 * nu);
    gL      = -1.1;
    
    vNa     = 50.0;
    vK      = -77.0;
    vL      = -54.4;
    vRest   = -60.0;
    
    Icn1    = 5.0;
    Icn2    = 30.0;
    
    Vsyninh = -80.0;    # [mV] synaptic reversal potential for inhibitory effects
    Vsynexc = 0.0;      # [mV] synaptic reversal potential for exciting effects
    
    alfa_inhibitory     = 6.0;
    betta_inhibitory    = 0.3;
    
    alfa_excitatory     = 40.0;
    betta_excitatory    = 2.0;
    
    w1 = 0.1;   # strength of the synaptic connection from PN to CN1
    w2 = 9.0;   # strength of the synaptic connection from CN1 to PN
    w3 = 5.0;   # strength of the synaptic connection from CN2 to PN
    
    deltah = 650; # period of time when high strength value of synaptic connection exists from CN2 to PN.


class central_element:
    "Central element consist of two central neurons that are described by a little bit different dynamic"
    membrane_potential      = 0.0;        # membrane potential of cenral neuron (V)
    active_cond_sodium      = 0.0;        # activation conductance of the sodium channel (m)
    inactive_cond_sodium    = 0.0;        # inactivaton conductance of the sodium channel (h)
    active_cond_potassium   = 0.0;        # inactivaton conductance of the sodium channel (h)
    
    pulse_generation_time = [];     # times of pulse generation by central neuron
    pulse_generation = False;       # spike generation of central neuron


class hhn_network(network, network_interface):
    _name = "Oscillatory Neural Network based on Hodgkin-Huxley Neuron Model"
    
    # States of peripheral oscillators
    _membrane_potential     = None;          # membrane potential of neuron (V)
    _active_cond_sodium     = None;          # activation conductance of the sodium channel (m)
    _inactive_cond_sodium   = None;          # inactivaton conductance of the sodium channel (h)
    _active_cond_potassium  = None;          # inactivaton conductance of the sodium channel (h)
    _link_activation_time   = None;          # time of set w3 - connection from CN2 to PN for each oscillator.
    _link_deactivation_time = None;          # time of reset w3 - connection from CN2 to PN for each oscillator.
    _link_weight3           = None;          # connection strength for each oscillator from CN2 to PN.
    
    _pulse_generation_time  = None;          # time of spike generation for each oscillator.
    _pulse_generation       = None;          # spike generation for each oscillator.
    
    _stimulus = None;               # stimulus of each oscillator
    _noise = None;                  # Noise for each oscillator
    
    _central_element = None;        # Central element description
    
    _params = None;                 # parameters of the network
    
    _alfa_inhibitory = None;        # inhibitory potential
    _alfa_excitatory = None;        # excitatory potential
    
    def __init__(self, num_osc, stimulus = None, parameters = None, type_conn = conn_type.NONE, conn_represent = conn_represent.MATRIX):
        super().__init__(num_osc, type_conn, conn_represent);
        
        self._membrane_potential        = [0.0] * self._num_osc;
        self._active_cond_sodium        = [0.0] * self._num_osc;
        self._inactive_cond_sodium      = [0.0] * self._num_osc;
        self._active_cond_potassium     = [0.0] * self._num_osc;
        self._link_activation_time      = [0.0] * self._num_osc;
        self._link_deactivation_time    = [0.0] * self.num_osc;
        self._link_weight3              = [0.0] * self._num_osc;
        self._pulse_generation_time     = [ [] ] * self._num_osc;
        self._pulse_generation          = [False] * self._num_osc;
        
        self._alfa_inh = 0.0;       # alfa-function for excitatory
        
        self._noise = [random.random() * 2.0 - 1.0 for i in range(self._num_osc)];
        
        self._central_element = [central_element(), central_element()];
        
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
            self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_memb.append(self._membrane_potential);
                dyn_time.append(t);
            else:
                dyn_memb = self._membrane_potential;
                dyn_time = t;
        
        return (dyn_time, dyn_memb);
    
    
    def _calculate_states(self, solution, t, step, int_step):
        "Caclculates new state of each oscillator in the network. Returns only excitatory state of oscillators."
        
        "(in) solution        - type solver of the differential equation."
        "(in) t               - current time of simulation."
        "(in) step            - step of solution at the end of which states of oscillators should be calculated."
        "(in) int_step        - step differentiation that is used for solving differential equation."
        
        "Returns new state of excitatory parts of oscillators."
        
        next_membrane           = [0.0] * self._num_osc;
        next_active_sodium      = [0.0] * self._num_osc;
        next_inactive_sodium    = [0.0] * self._num_osc;
        next_active_potassium   = [0.0] * self._num_osc;
        
        # Update states of oscillators
        for index in range (0, self._num_osc, 1):
            result = odeint(self.hnn_state, 
                            [ self._membrane_potential[index], self._active_cond_sodium[index], self._inactive_cond_sodium[index], self._active_cond_potassium[index] ], 
                            numpy.arange(t - step, t, int_step), 
                            (index , ));
                            
            [ next_membrane[index], next_active_sodium[index], next_inactive_sodium[index], next_active_potassium[index] ] = result[len(result) - 1][0:4];        
        
        next_cn_membrane            = [0.0, 0.0];
        next_cn_active_sodium       = [0.0, 0.0];
        next_cn_inactive_sodium     = [0.0, 0.0];
        next_cn_active_potassium    = [0.0, 0.0];
        
        # Update states of central elements
        for index in range(0, len(self._central_element)):
            result = odeint(self.hnn_state, 
                            [ self._central_element[0].membrane_potential, self._central_element[0].active_cond_sodium, self._central_element[0].inactive_cond_sodium, self._central_element[0].active_cond_potassium ], 
                            numpy.arange(t - step, t, int_step), 
                            (self._num_osc + index , ));
                            
            [ next_cn_membrane[index], next_cn_active_sodium[index], next_cn_inactive_sodium[index], next_cn_active_potassium[index] ] = result[len(result) - 1][0:4];
        
        # Noise generation
        self._noise = [ 1.0 + 0.01 * (random.random() * 2.0 - 1.0) for i in range(self._num_osc)];
        self._alfa_inhibitory = self._params.alfa_inhibitory * t * math.exp(-self._params.betta_inhibitory * t);
        self._alfa_excitatory = self._params.alfa_excitatory * t * math.exp(-self._params.betta_excitatory * t);
        
        # Updating states of PNs
        for index in range(0, self._num_osc):
            if (self._pulse_generation is False):
                if (next_membrane[index] > 0):
                    self._pulse_generation[index] = True;
                    self._pulse_generation_time[index].append(t);
            else:
                if (next_membrane[index] < 0):
                    self._pulse_generation[index] = False;
            
            # Update connection from CN2 to PN
            if ( (self._link_activation_time[index] < t) and (t < self._link_activation_time[index] + self._params.deltah) ):
                if (self._link_weight3[index] == 0):
                    self._link_activation_time[index] = t;
                    
                self._link_weight3[index] = self._params.w3;
            else:
                if (self._link_weight3[index] != 0):
                    self._link_deactivation_time[index] = t;
                
                self._link_weight3[index] = 0.0;            
        
        
        # Updation states of CN
        for index in range(0, len(self._central_element)):
            if (self._central_element[index].pulse_generation is False):
                if (next_cn_membrane[index] > 0):
                    self._central_element[index].pulse_generation = True;
                    self._central_element[index].pulse_generation_time.append(t);
                else:
                    if (next_cn_membrane[index] < 0):
                        self._central_element[index].pulse_generation = False;
            
            self._central_element[index].membrane_potential = next_cn_membrane[index];
            self._central_element[index].active_cond_sodium = next_cn_active_sodium[index];
            self._central_element[index].inactive_cond_sodium = next_cn_inactive_sodium[index];
            self._central_element[index].active_cond_potassium = next_cn_active_potassium[index];
        
        self._membrane_potential = next_membrane[:];
        self._active_cond_sodium = next_active_sodium[:];
        self._inactive_cond_sodium = next_inactive_sodium[:];
        self._active_cond_potassium = next_cn_active_potassium[:];
        
        return next_membrane;
    
    
    def hnn_state(self, inputs, t, argv):
        "Returns new values of excitatory and inhibitory parts of oscillator and potential of oscillator."
        
        "(in) t             - current time of simulation."
        "(in) argv          - extra arguments that are not used for integration - index of oscillator."
        
        "Returns new values of excitatoty and inhibitory part of oscillator and new value of potential (not assign)."
        
        index = argv;
        
        v = inputs[0]; # membrane potential (v).
        m = inputs[1]; # activation conductance of the sodium channel (m).
        h = inputs[2]; # inactivaton conductance of the sodium channel (h).
        n = inputs[3]; # activation conductance of the potassium channel (n).
        
        # Calculate ion current
        # gNa * m[i]^3 * h * (v[i] - vNa) + gK * n[i]^4 * (v[i] - vK) + gL  (v[i] - vL)
        active_sodium_part = self._params.gNa * (m ** 3) * h * (v - self._params.vNa);
        inactive_sodium_part = self._params.gK * (n ** 4) * (v - self._params.vK);
        active_potassium_part = self._params.gL * (v - self._params.vL);
        
        Iion = active_sodium_part + inactive_sodium_part + active_potassium_part;
        
        Iext = 0;
        Isyn = 0;
        if (index < self._num_osc): 
            # PN - peripheral neuron - calculation of external current and synaptic current.
            Iext = self._stimulus[index] * self._noise[index];    # probably noise can be pre-defined for reducting compexity
            
            memory_impact1 = 0.0;
            for i in range(0, len(self._central_element[0].pulse_generation_time)):
                memory_impact1 += self._alfa_inhibitory * (t - self._central_element[0].pulse_generation_time[i]);
            
            memory_impact2 = 0.0;
            for i in range(0, len(self._central_element[1].pulse_generation_time)):
                memory_impact2 += self._alfa_inhibitory * (t - self._central_element[1].pulse_generation_time[i]);        
    
            Isyn = self._params.w2 * (v - self._params.Vsyninh) * memory_impact1 + self._link_weight3[index] * (v - self._params.Vsyninh) * memory_impact2;            
        else:
            # CN - central element.
            central_index = index - self._num_osc;
            if (central_index == 0):
                Iext = self._params.Icn1;   # CN1
                
                memory_impact = 0;
                for index_oscillator in range(0, self._num_osc):
                    for index_generation in range(0, len(self._pulse_generation_time[index_oscillator])):
                        memory_impact += self._alfa_excitatory * (t - self._pulse_generation_time[index_oscillator][index_generation]);
                
                Isyn = self._params.w1 * (v - self._params.Vsynexc) * memory_impact;
                
                
            elif (central_index == 1):
                Iext = self._params.Icn2;   # CN2
                Isyn = 0.0;
            else:
                assert 0;
        
        
        # Membrane potential
        dv = -Iion + Iext - Isyn;
        
        # Calculate variables
        potential = v - self._params.vRest;
        am = (2.5 - 0.1 * potential) / (math.exp(2.5 - 0.1 * potential) - 1.0);
        ah = 0.07 * math.exp(-potential / 20.0);
        an = (0.1 - 0.01 * potential) / (math.exp(1 - 0.1 * potential) - 1.0);
        
        bm = 4.0 * math.exp(-potential / 18.0);
        bh = 1.0 / (math.exp(3.0 - 0.1 * potential) + 1.0);
        bn = 0.125 * math.exp(-potential / 80.0);
        
        dm = am * (1.0 - m) - bm * m;
        dh = ah * (1.0 - h) - bh * h;
        dn = an * (1.0 - n) - bn * n;
        
        return [dv, dm, dh, dn];
        
        
    def allocate_sync_ensembles(self, tolerance = 0.1):
        "Allocate clusters in line with ensembles of synchronous oscillators where each." 
        "synchronous ensemble corresponds to only one cluster."
        
        "(in) tolerance        - maximum error for allocation of synchronous ensemble oscillators."
        
        "Returns list of grours (lists) of indexes of synchronous oscillators."
        "For example [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ]."
        pass;
    