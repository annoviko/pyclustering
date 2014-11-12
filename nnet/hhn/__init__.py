'''

Neural Network: Oscillatory Neural Network based on Hodgkin-Huxley Neuron Model

Based on article description:
 - D.Chik, R.Borisyuk, Y.Kazanovich. "Selective attention model with spiking elements" - Nov. 2009.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from nnet import *;

from scipy.integrate import odeint;

from support import allocate_sync_ensembles;

import numpy;
import random;

class hhn_parameters:    
    nu      = random.random() * 2.0 - 1.0;
    
    gNa     = 120.0 * (1 + 0.02 * nu);  # maximal conductivity for sodium current
    gK      = 36.0 * (1 + 0.02 * nu);   # maximal conductivity for potassium current
    gL      = 0.3 * (1 + 0.02 * nu);    # maximal conductivity for leakage current
    
    vNa     = 50.0;     # [mV] reverse potential of sodium current
    vK      = -77.0;    # [mV] reverse potential of potassium current
    vL      = -54.4;    # [mV] reverse potantial of leakage current
    vRest   = -65.0;    # [mV] rest potential
    
    Icn1    = 5.0;      # [mV] external current for central element 1
    Icn2    = 30.0;     # [mV] external current for central element 2
    
    Vsyninh = -80.0;    # [mV] synaptic reversal potential for inhibitory effects
    Vsynexc = 0.0;      # [mV] synaptic reversal potential for exciting effects
    
    alfa_inhibitory     = 6.0;      # alfa-parameter for alfa-function for inhibitory effect
    betta_inhibitory    = 0.3;      # betta-parameter for alfa-function for inhibitory effect
    
    alfa_excitatory     = 40.0;     # alfa-parameter for alfa-function for excitatoty effect
    betta_excitatory    = 2.0;      # betta-parameter for alfa-function for excitatoty effect
    
    w1 = 0.1;   # strength of the synaptic connection from PN to CN1
    w2 = 9.0;   # strength of the synaptic connection from CN1 to PN
    w3 = 5.0;   # strength of the synaptic connection from CN2 to PN
    
    deltah = 650.0;     # [ms] period of time when high strength value of synaptic connection exists from CN2 to PN.
    threshold = -10;
    eps = 0.16;


class central_element:
    "Central element consist of two central neurons that are described by a little bit different dynamic"
    membrane_potential      = 0.0;        # membrane potential of cenral neuron (V)
    active_cond_sodium      = 0.0;        # activation conductance of the sodium channel (m)
    inactive_cond_sodium    = 0.0;        # inactivaton conductance of the sodium channel (h)
    active_cond_potassium   = 0.0;        # inactivaton conductance of the sodium channel (h)
    
    pulse_generation_time = None;         # times of pulse generation by central neuron
    pulse_generation = False;             # spike generation of central neuron
    
    def __init__(self):
        self.pulse_generation_time = [];
    
    def __repr__(self):
        return "%s, %s" % (self.membrane_potential, self.pulse_generation_time);


class hhn_network(network, network_interface):
    _name = "Oscillatory Neural Network based on Hodgkin-Huxley Neuron Model"
    
    # States of peripheral oscillators
    _membrane_potential     = None;          # membrane potential of neuron (V)
    _active_cond_sodium     = None;          # activation conductance of the sodium channel (m)
    _inactive_cond_sodium   = None;          # inactivaton conductance of the sodium channel (h)
    _active_cond_potassium  = None;          # activation conductance of the potassium channel (n)
    _link_activation_time   = None;          # time of set w3 - connection from CN2 to PN for each oscillator.
    _link_weight3           = None;          # connection strength for each oscillator from CN2 to PN.
    
    _pulse_generation_time  = None;          # time of spike generation for each oscillator.
    _pulse_generation       = None;          # spike generation for each oscillator.
    
    _stimulus = None;               # stimulus of each oscillator
    _noise = None;                  # Noise for each oscillator
    
    _central_element = None;        # Central element description
    
    _params = None;                 # parameters of the network
    
    _membrane_dynamic_pointer = None;        # final result is stored here.
    
    def __init__(self, num_osc, stimulus = None, parameters = None, type_conn = None, conn_represent = conn_represent.MATRIX):
        "Constructor of oscillatory network based on Hodgkin-Huxley meuron model."
        
        "(in) num_osc             - number of peripheral oscillators in the network."
        "(in) stimulus            - list of stimulus for oscillators, number of stimulus should be equal to number of peripheral oscillators."
        "(in) parameters          - parameters of the network that are defined by structure 'hhn_parameters'."
        "(in) type_conn           - type of connection between oscillators in the network (ignored for this type of network)."
        "(in) conn_represent      - internal representation of connection in the network: matrix or list."      
          
        super().__init__(num_osc, conn_type.NONE, conn_represent);
        
        self._membrane_potential        = [0.0] * self._num_osc;
        self._active_cond_sodium        = [0.0] * self._num_osc;
        self._inactive_cond_sodium      = [0.0] * self._num_osc;
        self._active_cond_potassium     = [0.0] * self._num_osc;
        self._link_activation_time      = [0.0] * self._num_osc;
        self._link_pulse_counter        = [0.0] * self._num_osc;
        self._link_deactivation_time    = [0.0] * self.num_osc;
        self._link_weight3              = [0.0] * self._num_osc;
        self._pulse_generation_time     = [ [] for i in range(self._num_osc) ];
        self._pulse_generation          = [False] * self._num_osc;
        
        self._noise = [random.random() * 2.0 - 1.0 for i in range(self._num_osc)];
        
        self._central_element = [central_element(), central_element()];
        
        if (stimulus is None):
            self._stimulus = [0.0] * self._num_osc;
        else:
            self._stimulus = stimulus;
        
        if (parameters is not None):
            self._params = parameters;
        else:
            self._params = hhn_parameters();
    
    
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
        
        self._membrane_dynamic_pointer = None;
        
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
            memb = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_memb.append(memb);
                dyn_time.append(t);
            else:
                dyn_memb = memb;
                dyn_time = t;
        
        self._membrane_dynamic_pointer = dyn_memb;
        return (dyn_time, dyn_memb);
    
    
    def _calculate_states(self, solution, t, step, int_step):
        "Caclculates new state of each oscillator in the network. Returns only excitatory state of oscillators."
        
        "(in) solution        - type solver of the differential equation."
        "(in) t               - current time of simulation."
        "(in) step            - step of solution at the end of which states of oscillators should be calculated."
        "(in) int_step        - step differentiation that is used for solving differential equation."
        
        "Returns new state of membrance potential for peripheral oscillators and for cental elements as a list where"
        "the last two values correspond to central element 1 and 2."
        
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
                            [ self._central_element[index].membrane_potential, self._central_element[index].active_cond_sodium, self._central_element[index].inactive_cond_sodium, self._central_element[index].active_cond_potassium ], 
                            numpy.arange(t - step, t, int_step), 
                            (self._num_osc + index , ));
                            
            [ next_cn_membrane[index], next_cn_active_sodium[index], next_cn_inactive_sodium[index], next_cn_active_potassium[index] ] = result[len(result) - 1][0:4];
        
        # Noise generation
        self._noise = [ 1.0 + 0.01 * (random.random() * 2.0 - 1.0) for i in range(self._num_osc)];
        
        # Updating states of PNs
        for index in range(0, self._num_osc):
            if (self._pulse_generation[index] is False):
                if (next_membrane[index] > 0.0):
                    self._pulse_generation[index] = True;
                    self._pulse_generation_time[index].append(t);
            else:
                if (next_membrane[index] < 0.0):
                    self._pulse_generation[index] = False;
            
            # Update connection from CN2 to PN
            if (self._link_weight3[index] == 0.0):
                if ( (next_membrane[index] > self._params.threshold) and (next_membrane[index] > self._params.threshold) ):
                    self._link_pulse_counter[index] += step;
                
                    if (self._link_pulse_counter[index] >= 1 / self._params.eps):
                        self._link_weight3[index] = self._params.w3;
                        self._link_activation_time[index] = t;
            else:
                if ( not ((self._link_activation_time[index] < t) and (t < self._link_activation_time[index] + self._params.deltah)) ):
                    self._link_weight3[index] = 0.0;
                    self._link_pulse_counter[index] = 0.0;
                    
        
        
        # Updation states of CN
        for index in range(0, len(self._central_element)):
            if (self._central_element[index].pulse_generation is False):
                if (next_cn_membrane[index] > 0.0):
                    self._central_element[index].pulse_generation = True;
                    self._central_element[index].pulse_generation_time.append(t);
            else:
                if (next_cn_membrane[index] < 0.0):
                    self._central_element[index].pulse_generation = False;
            
            self._central_element[index].membrane_potential = next_cn_membrane[index];
            self._central_element[index].active_cond_sodium = next_cn_active_sodium[index];
            self._central_element[index].inactive_cond_sodium = next_cn_inactive_sodium[index];
            self._central_element[index].active_cond_potassium = next_cn_active_potassium[index];
        
        self._membrane_potential = next_membrane[:];
        self._active_cond_sodium = next_active_sodium[:];
        self._inactive_cond_sodium = next_inactive_sodium[:];
        self._active_cond_potassium = next_active_potassium[:];
        
        return next_membrane + next_cn_membrane;
    
    
    def hnn_state(self, inputs, t, argv):
        "Returns new values of excitatory and inhibitory parts of oscillator and potential of oscillator."
        
        "(in) inputs        - list of states of oscillator for integration [v, m, h, n] (see description below)."
        "(in) t             - current time of simulation."
        "(in) argv          - extra arguments that are not used for integration - index of oscillator."
        
        "Returns list of new values of oscillator [v, m, h, n], where:"
        "v - membrane potantial of oscillator,"
        "m - activation conductance of the sodium channel,"
        "h - inactication conductance of the sodium channel,"
        "n - activation conductance of the potassium channel."
        
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
        
        Iext = 0.0;
        Isyn = 0.0;
        if (index < self._num_osc): 
            # PN - peripheral neuron - calculation of external current and synaptic current.
            Iext = self._stimulus[index] * self._noise[index];    # probably noise can be pre-defined for reducting compexity            
            
            memory_impact1 = 0.0;
            for i in range(0, len(self._central_element[0].pulse_generation_time)):
                # TODO: alfa function shouldn't be calculated here (long procedure)
                memory_impact1 += self.__alfa_function(t - self._central_element[0].pulse_generation_time[i], self._params.alfa_inhibitory, self._params.betta_inhibitory);
            
            memory_impact2 = 0.0;
            for i in range(0, len(self._central_element[1].pulse_generation_time)):
                # TODO: alfa function shouldn't be calculated here (long procedure)
                memory_impact2 += self.__alfa_function(t - self._central_element[1].pulse_generation_time[i], self._params.alfa_inhibitory, self._params.betta_inhibitory);        
    
            Isyn = self._params.w2 * (v - self._params.Vsyninh) * memory_impact1 + self._link_weight3[index] * (v - self._params.Vsyninh) * memory_impact2;            
        else:
            # CN - central element.
            central_index = index - self._num_osc;
            if (central_index == 0):
                Iext = self._params.Icn1;   # CN1
                
                memory_impact = 0.0;
                for index_oscillator in range(0, self._num_osc):
                    for index_generation in range(0, len(self._pulse_generation_time[index_oscillator])):
                        # TODO: alfa function shouldn't be calculated here (long procedure)
                        memory_impact += self.__alfa_function(t - self._pulse_generation_time[index_oscillator][index_generation], self._params.alfa_excitatory, self._params.betta_excitatory);
                 
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
        an = (0.1 - 0.01 * potential) / (math.exp(1.0 - 0.1 * potential) - 1.0);
        
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
        
        ignore = set();
        
        ignore.add(self._num_osc);
        ignore.add(self._num_osc + 1);
        
        return allocate_sync_ensembles(self._membrane_dynamic_pointer, tolerance, 20.0, ignore);
    
    
    def __alfa_function(self, time, alfa, betta):
        "Calculate value of alfa-function for difference between spike generation time and current simulation time."
        
        "(in) time    - difference between last spike generation time and current time."
        "(in) alfa    - alfa parameter for alfa-function."
        "(in) betta   - betta parameter for alfa-function."
        
        "Returns value of alfa-function."
        
        return alfa * time * math.exp(-betta * time);
    