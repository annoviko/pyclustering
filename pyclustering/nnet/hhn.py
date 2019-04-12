"""!

@brief Oscillatory Neural Network based on Hodgkin-Huxley Neuron Model
@details Implementation based on paper @cite article::nnet::hnn::1.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
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

from scipy.integrate import odeint

from pyclustering.core.wrapper import ccore_library

import pyclustering.core.hhn_wrapper as wrapper

from pyclustering.nnet import *

from pyclustering.utils import allocate_sync_ensembles

import numpy
import random

class hhn_parameters:
    """!
    @brief Describes parameters of Hodgkin-Huxley Oscillatory Network.
    
    @see hhn_network
    
    """
    
    def __init__(self):
        """!
        @brief    Default constructor of parameters for Hodgkin-Huxley Oscillatory Network.
        @details  Constructor initializes parameters by default non-zero values that can be
                  used for simple simulation.
        """
        
        ## Intrinsic noise.
        self.nu      = random.random() * 2.0 - 1.0;
        
        ## Maximal conductivity for sodium current.
        self.gNa     = 120.0 * (1 + 0.02 * self.nu);
        
        ## Maximal conductivity for potassium current.
        self.gK      = 36.0 * (1 + 0.02 * self.nu);
        
        ## Maximal conductivity for leakage current.
        self.gL      = 0.3 * (1 + 0.02 * self.nu);
        
        
        ## Reverse potential of sodium current [mV].
        self.vNa     = 50.0;
        
        ## Reverse potential of potassium current [mV].
        self.vK      = -77.0;
        
        ## Reverse potential of leakage current [mV].
        self.vL      = -54.4;
        
        ## Rest potential [mV].
        self.vRest   = -65.0;    
        
        
        ## External current [mV] for central element 1.
        self.Icn1    = 5.0;
        
        ## External current [mV] for central element 2.
        self.Icn2    = 30.0;
        
        
        ## Synaptic reversal potential [mV] for inhibitory effects.
        self.Vsyninh = -80.0;    
        
        ## Synaptic reversal potential [mV] for exciting effects.
        self.Vsynexc = 0.0;
        
        ## Alfa-parameter for alfa-function for inhibitory effect.
        self.alfa_inhibitory     = 6.0;
        
        ## Betta-parameter for alfa-function for inhibitory effect.
        self.betta_inhibitory    = 0.3;
        
        
        ## Alfa-parameter for alfa-function for excitatory effect.
        self.alfa_excitatory     = 40.0;
        
        ## Betta-parameter for alfa-function for excitatory effect.
        self.betta_excitatory    = 2.0;
        
        
        ## Strength of the synaptic connection from PN to CN1.
        self.w1 = 0.1;
        
        ## Strength of the synaptic connection from CN1 to PN.
        self.w2 = 9.0;
        
        ## Strength of the synaptic connection from CN2 to PN.
        self.w3 = 5.0;
        
        
        ## Period of time [ms] when high strength value of synaptic connection exists from CN2 to PN.
        self.deltah = 650.0;
        
        ## Threshold of the membrane potential that should exceeded by oscillator to be considered as an active.
        self.threshold = -10;
        
        ## Affects pulse counter.
        self.eps = 0.16;


class central_element:
    """!
    @brief Central element consist of two central neurons that are described by a little bit different dynamic than peripheral.
    
    @see hhn_network
    
    """
    
    def __init__(self):
        """!
        @brief Constructor of central element.
        
        """
        
        ## Membrane potential of cenral neuron (V).
        self.membrane_potential      = 0.0;
        
        ## Activation conductance of the sodium channel (m).
        self.active_cond_sodium      = 0.0;
        
        ## Inactivaton conductance of the sodium channel (h).
        self.inactive_cond_sodium    = 0.0;
        
        ## Activaton conductance of the sodium channel (h).
        self.active_cond_potassium   = 0.0;
        
        ## Spike generation of central neuron.
        self.pulse_generation = False;
        
        ## Timestamps of generated pulses.
        self.pulse_generation_time = [];
    
    def __repr__(self):
        """!
        @brief Returns string that represents central element.
        
        """
        return "%s, %s" % (self.membrane_potential, self.pulse_generation_time);


class hhn_network(network):
    """!
    @brief Oscillatory Neural Network with central element based on Hodgkin-Huxley neuron model.
    @details Interaction between oscillators is performed via central element (no connection between oscillators that
              are called as peripheral). Peripheral oscillators receive external stimulus. Central element consist of
              two oscillators: the first is used for synchronization some ensemble of oscillators and the second
              controls synchronization of the first central oscillator with various ensembles.
    
    Usage example where oscillatory network with 6 oscillators is used for simulation. The first two oscillators
    have the same stimulus, as well as the third and fourth oscillators and the last two. Thus three synchronous
    ensembles are expected after simulation.
    @code
        from pyclustering.nnet.hhn import hhn_network, hhn_parameters
        from pyclustering.nnet.dynamic_visualizer import dynamic_visualizer

        # Change period of time when high strength value of synaptic connection exists from CN2 to PN.
        params = hhn_parameters()
        params.deltah = 400

        # Create Hodgkin-Huxley oscillatory network with stimulus.
        net = hhn_network(6, [0, 0, 25, 25, 47, 47], params)

        # Simulate network.
        (t, dyn_peripheral, dyn_central) = net.simulate(2400, 600)

        # Visualize network's output (membrane potential of peripheral and central neurons).
        amount_canvases = 6 + 2  # 6 peripheral oscillator + 2 central elements
        visualizer = dynamic_visualizer(amount_canvases, x_title="Time", y_title="V", y_labels=False)
        visualizer.append_dynamics(t, dyn_peripheral, 0, True)
        visualizer.append_dynamics(t, dyn_central, amount_canvases - 2, True)
        visualizer.show()
    @endcode

    There is visualized result of simulation where three synchronous ensembles of oscillators can be observed. The
    first and the second oscillators form the first ensemble, the third and the fourth form the second ensemble and
    the last two oscillators form the third ensemble.
    @image html hhn_three_ensembles.png
    
    """
    
    def __init__(self, num_osc, stimulus = None, parameters = None, type_conn = None, type_conn_represent = conn_represent.MATRIX, ccore = True):
        """!
        @brief Constructor of oscillatory network based on Hodgkin-Huxley neuron model.
        
        @param[in] num_osc (uint): Number of peripheral oscillators in the network.
        @param[in] stimulus (list): List of stimulus for oscillators, number of stimulus should be equal to number of peripheral oscillators.
        @param[in] parameters (hhn_parameters): Parameters of the network.
        @param[in] type_conn (conn_type): Type of connections between oscillators in the network (ignored for this type of network).
        @param[in] type_conn_represent (conn_represent): Internal representation of connection in the network: matrix or list.
        @param[in] ccore (bool): If 'True' then CCORE is used (C/C++ implementation of the model).
        
        """
          
        super().__init__(num_osc, conn_type.NONE, type_conn_represent);
        
        if (stimulus is None):
            self._stimulus = [0.0] * num_osc;
        else:
            self._stimulus = stimulus;
        
        if (parameters is not None):
            self._params = parameters;
        else:
            self._params = hhn_parameters();
        
        self.__ccore_hhn_pointer = None;
        self.__ccore_hhn_dynamic_pointer = None;
        
        if ( (ccore is True) and ccore_library.workable() ):
            self.__ccore_hhn_pointer = wrapper.hhn_create(num_osc, self._params);
        else:
            self._membrane_dynamic_pointer = None;        # final result is stored here.
            
            self._membrane_potential        = [0.0] * self._num_osc;
            self._active_cond_sodium        = [0.0] * self._num_osc;
            self._inactive_cond_sodium      = [0.0] * self._num_osc;
            self._active_cond_potassium     = [0.0] * self._num_osc;
            self._link_activation_time      = [0.0] * self._num_osc;
            self._link_pulse_counter        = [0.0] * self._num_osc;
            self._link_deactivation_time    = [0.0] * self._num_osc;
            self._link_weight3              = [0.0] * self._num_osc;
            self._pulse_generation_time     = [ [] for i in range(self._num_osc) ];
            self._pulse_generation          = [False] * self._num_osc;
            
            self._noise = [random.random() * 2.0 - 1.0 for i in range(self._num_osc)];
            
            self._central_element = [central_element(), central_element()];


    def __del__(self):
        """!
        @brief Destroy dynamically allocated oscillatory network instance in case of CCORE usage.

        """
        if self.__ccore_hhn_pointer:
            wrapper.hhn_destroy(self.__ccore_hhn_pointer)


    def simulate(self, steps, time, solution = solve_type.RK4):
        """!
        @brief Performs static simulation of oscillatory network based on Hodgkin-Huxley neuron model.
        @details Output dynamic is sensible to amount of steps of simulation and solver of differential equation.
                  Python implementation uses 'odeint' from 'scipy', CCORE uses classical RK4 and RFK45 methods,
                  therefore in case of CCORE HHN (Hodgkin-Huxley network) amount of steps should be greater than in
                  case of Python HHN.

        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solver for differential equations.
        
        @return (tuple) Dynamic of oscillatory network represented by (time, peripheral neurons dynamic, central elements
                dynamic), where types are (list, list, list).
        
        """
        
        return self.simulate_static(steps, time, solution)
    
    
    def simulate_static(self, steps, time, solution = solve_type.RK4):
        """!
        @brief Performs static simulation of oscillatory network based on Hodgkin-Huxley neuron model.
        @details Output dynamic is sensible to amount of steps of simulation and solver of differential equation.
                  Python implementation uses 'odeint' from 'scipy', CCORE uses classical RK4 and RFK45 methods,
                  therefore in case of CCORE HHN (Hodgkin-Huxley network) amount of steps should be greater than in
                  case of Python HHN.

        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solver for differential equations.
        
        @return (tuple) Dynamic of oscillatory network represented by (time, peripheral neurons dynamic, central elements
                dynamic), where types are (list, list, list).
        
        """
        
        # Check solver before simulation
        if (solution == solve_type.FAST):
            raise NameError("Solver FAST is not support due to low accuracy that leads to huge error.");
        
        self._membrane_dynamic_pointer = None;
        
        if (self.__ccore_hhn_pointer is not None):
            self.__ccore_hhn_dynamic_pointer = wrapper.hhn_dynamic_create(True, False, False, False);
            wrapper.hhn_simulate(self.__ccore_hhn_pointer, steps, time, solution, self._stimulus, self.__ccore_hhn_dynamic_pointer);
            
            peripheral_membrane_potential = wrapper.hhn_dynamic_get_peripheral_evolution(self.__ccore_hhn_dynamic_pointer, 0);
            central_membrane_potential = wrapper.hhn_dynamic_get_central_evolution(self.__ccore_hhn_dynamic_pointer, 0);
            dynamic_time = wrapper.hhn_dynamic_get_time(self.__ccore_hhn_dynamic_pointer);
            
            self._membrane_dynamic_pointer = peripheral_membrane_potential;

            wrapper.hhn_dynamic_destroy(self.__ccore_hhn_dynamic_pointer);
            
            return (dynamic_time, peripheral_membrane_potential, central_membrane_potential);
        
        if (solution == solve_type.RKF45):
            raise NameError("Solver RKF45 is not support in python version.");
        
        dyn_peripheral = [ self._membrane_potential[:] ];
        dyn_central = [ [0.0, 0.0] ];
        dyn_time = [ 0.0 ];
        
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            (memb_peripheral, memb_central) = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            dyn_peripheral.append(memb_peripheral);
            dyn_central.append(memb_central);
            dyn_time.append(t);
        
        self._membrane_dynamic_pointer = dyn_peripheral;
        return (dyn_time, dyn_peripheral, dyn_central);
    
    
    def _calculate_states(self, solution, t, step, int_step):
        """!
        @brief Caclculates new state of each oscillator in the network. Returns only excitatory state of oscillators.
        
        @param[in] solution (solve_type): Type solver of the differential equations.
        @param[in] t (double): Current time of simulation.
        @param[in] step (uint): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Differentiation step that is used for solving differential equation.
        
        @return (list) New states of membrance potentials for peripheral oscillators and for cental elements as a list where
                the last two values correspond to central element 1 and 2.
                 
        """
        
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
        self.__update_peripheral_neurons(t, step, next_membrane, next_active_sodium, next_inactive_sodium, next_active_potassium);
        
        # Updation states of CN
        self.__update_central_neurons(t, next_cn_membrane, next_cn_active_sodium, next_cn_inactive_sodium, next_cn_active_potassium);
        
        return (next_membrane, next_cn_membrane);
    
    
    def __update_peripheral_neurons(self, t, step, next_membrane, next_active_sodium, next_inactive_sodium, next_active_potassium):
        """!
        @brief Update peripheral neurons in line with new values of current in channels.
        
        @param[in] t (doubles): Current time of simulation.
        @param[in] step (uint): Step (time duration) during simulation when states of oscillators should be calculated.
        @param[in] next_membrane (list): New values of membrane potentials for peripheral neurons.
        @Param[in] next_active_sodium (list): New values of activation conductances of the sodium channels for peripheral neurons.
        @param[in] next_inactive_sodium (list): New values of inactivaton conductances of the sodium channels for peripheral neurons.
        @param[in] next_active_potassium (list): New values of activation conductances of the potassium channel for peripheral neurons.
        
        """
        
        self._membrane_potential = next_membrane[:];
        self._active_cond_sodium = next_active_sodium[:];
        self._inactive_cond_sodium = next_inactive_sodium[:];
        self._active_cond_potassium = next_active_potassium[:];
        
        for index in range(0, self._num_osc):
            if (self._pulse_generation[index] is False):
                if (self._membrane_potential[index] >= 0.0):
                    self._pulse_generation[index] = True;
                    self._pulse_generation_time[index].append(t);
            elif (self._membrane_potential[index] < 0.0):
                self._pulse_generation[index] = False;
            
            # Update connection from CN2 to PN
            if (self._link_weight3[index] == 0.0):
                if (self._membrane_potential[index] > self._params.threshold):
                    self._link_pulse_counter[index] += step;
                
                    if (self._link_pulse_counter[index] >= 1 / self._params.eps):
                        self._link_weight3[index] = self._params.w3;
                        self._link_activation_time[index] = t;
            elif ( not ((self._link_activation_time[index] < t) and (t < self._link_activation_time[index] + self._params.deltah)) ):
                self._link_weight3[index] = 0.0;
                self._link_pulse_counter[index] = 0.0;
    
    
    def __update_central_neurons(self, t, next_cn_membrane, next_cn_active_sodium, next_cn_inactive_sodium, next_cn_active_potassium):
        """!
        @brief Update of central neurons in line with new values of current in channels.
        
        @param[in] t (doubles): Current time of simulation.
        @param[in] next_membrane (list): New values of membrane potentials for central neurons.
        @Param[in] next_active_sodium (list): New values of activation conductances of the sodium channels for central neurons.
        @param[in] next_inactive_sodium (list): New values of inactivaton conductances of the sodium channels for central neurons.
        @param[in] next_active_potassium (list): New values of activation conductances of the potassium channel for central neurons.
        
        """
        
        for index in range(0, len(self._central_element)):
            self._central_element[index].membrane_potential = next_cn_membrane[index];
            self._central_element[index].active_cond_sodium = next_cn_active_sodium[index];
            self._central_element[index].inactive_cond_sodium = next_cn_inactive_sodium[index];
            self._central_element[index].active_cond_potassium = next_cn_active_potassium[index];
            
            if (self._central_element[index].pulse_generation is False):
                if (self._central_element[index].membrane_potential >= 0.0):
                    self._central_element[index].pulse_generation = True;
                    self._central_element[index].pulse_generation_time.append(t);
            elif (self._central_element[index].membrane_potential < 0.0):
                self._central_element[index].pulse_generation = False;
    
    
    def hnn_state(self, inputs, t, argv):
        """!
        @brief Returns new values of excitatory and inhibitory parts of oscillator and potential of oscillator.
        
        @param[in] inputs (list): States of oscillator for integration [v, m, h, n] (see description below).
        @param[in] t (double): Current time of simulation.
        @param[in] argv (tuple): Extra arguments that are not used for integration - index of oscillator.
        
        @return (list) new values of oscillator [v, m, h, n], where:
                v - membrane potantial of oscillator,
                m - activation conductance of the sodium channel,
                h - inactication conductance of the sodium channel,
                n - activation conductance of the potassium channel.
        
        """
        
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
                memory_impact1 += self.__alfa_function(t - self._central_element[0].pulse_generation_time[i], self._params.alfa_inhibitory, self._params.betta_inhibitory);
            
            memory_impact2 = 0.0;
            for i in range(0, len(self._central_element[1].pulse_generation_time)):
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
        """!
        @brief Allocates clusters in line with ensembles of synchronous oscillators where each. Synchronous ensemble corresponds to only one cluster.
        
        @param[in] tolerance (double): maximum error for allocation of synchronous ensemble oscillators.
        
        @return (list) Grours (lists) of indexes of synchronous oscillators. For example [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
        
        """
        
        return allocate_sync_ensembles(self._membrane_dynamic_pointer, tolerance, 20.0, None);
    
    
    def __alfa_function(self, time, alfa, betta):
        """!
        @brief Calculates value of alfa-function for difference between spike generation time and current simulation time.
        
        @param[in] time (double): Difference between last spike generation time and current time.
        @param[in] alfa (double): Alfa parameter for alfa-function.
        @param[in] betta (double): Betta parameter for alfa-function.
        
        @return (double) Value of alfa-function.
        
        """
        
        return alfa * time * math.exp(-betta * time);
    
