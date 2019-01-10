"""!

@brief Neural Network: Hysteresis Oscillatory Network
@details Implementation based on paper @cite article::nnet::hysteresis::1.

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

import numpy

from scipy.integrate import odeint

from pyclustering.nnet import *

from pyclustering.utils import draw_dynamics


class hysteresis_dynamic:
    """!
    @brief Represents output dynamic of hysteresis oscillatory network.
    
    """
    
    @property
    def output(self):
        """!
        @brief (list) Returns outputs of oscillator during simulation.
        
        """
        return self._dynamic;
    
    
    @property
    def time(self):
        """!
        @brief (list) Returns sampling times when dynamic is measured during simulation.
        
        """
        
        return self._time;
    
    
    def __init__(self, amplitudes, time):
        """!
        @brief Constructor of hysteresis neural network dynamic.
        
        @param[in] amplitudes (list): Dynamic (amplitudes) of oscillators on each step of simulation.
        @param[in] time (list): Simulation time (timestamps of simulation steps) when amplitudes are stored.
        
        """
        
        if (len(amplitudes) != len(time)):
            raise NameError("Length of list of dynamics of oscillators should be equal to length of simulation timestamps of steps.");
        
        self._dynamic = amplitudes;
        
        self._time = time;


    def __len__(self):
        """!
        @brief (uint) Returns number of simulation steps that are stored in dynamic.
        
        """
        
        return len(self._dynamic);
    
    
    def allocate_sync_ensembles(self, tolerance = 0.1, threshold_steps = 1):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each
               synchronous ensemble corresponds to only one cluster.
               
        @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
        @param[in] threshold_steps (uint): Number of steps from the end of simulation that should be analysed for ensemble allocation.
                    If amout of simulation steps has been less than threshold steps than amount of steps will be reduced to amout
                    of simulation steps.
        
        @return (list) Grours of indexes of synchronous oscillators, for example, [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ]."
        
        """
        
        clusters = [ [0] ];
        
        number_oscillators = len(self._dynamic[0]);
        
        for i in range(1, number_oscillators, 1):
            captured_neuron = True;
            for cluster in clusters:
                neuron_index = cluster[0];
                
                analysis_steps = threshold_steps;
                if (len(self._dynamic) < analysis_steps):
                    analysis_steps = len(self._dynamic);
                
                analysis_start_step_index = len(self._dynamic) - 1;
                
                for step in range(analysis_start_step_index, analysis_start_step_index - analysis_steps, -1):
                    neuron_amplitude = self._dynamic[step][neuron_index];
                    candidate_amplitude = self._dynamic[step][i];
                    
                    if ( not (candidate_amplitude < (neuron_amplitude + tolerance)) or not (candidate_amplitude > (neuron_amplitude - tolerance)) ):
                        captured_neuron = False;
                        break;
                    
                if ( captured_neuron is True ):
                    cluster.append(i);
                    break;
            
            if (captured_neuron is False):
                clusters.append([i]);
        
        return clusters;


class hysteresis_visualizer:
    """!
    @brief Visualizer of output dynamic of hysteresis oscillatory network.
    
    """
        
    @staticmethod
    def show_output_dynamic(hysteresis_output_dynamic):
        """!
        @brief Shows output dynamic (output of each oscillator) during simulation.
        
        @param[in] hysteresis_output_dynamic (hysteresis_dynamic): Output dynamic of the hysteresis oscillatory network.
        
        """
        
        draw_dynamics(hysteresis_output_dynamic.time, hysteresis_output_dynamic.output, x_title = "Time", y_title = "x(t)");


class hysteresis_network(network):
    """!
    @brief Hysteresis oscillatory network that uses relaxation oscillators that are represented by objective hysteresis neurons whose output in range [-1, +1].
    
    Examples:
    @code
        # create hysteresis oscillatory network with 5 oscillators.
        network = hysteresis_network(5);
        
        # set initial states (from range [-1, +1]).
        network.states = [1 0 1 0 1];
        
        # set initial outputs.
        network.outputs = [1 1 1 1 1];
        
        # perform simulation of the network during 1000 steps in 10 time units.
        output_dynamic = network.simulate(1000, 10);
        
        # show output dynamic of the network.
        hysteresis_visualizer.show_output_dynamic(output_dynamic);
        
        # obtain synchronous ensembles.
        ensembles = output_dynamic.allocate_sync_ensembles(tolerance = 0.5, threshold_steps = 5);
        print(ensembles);
    @endcode
    
    """
    
    @property
    def outputs(self):
        """!
        @brief Returns current outputs of neurons.
        
        @return (list) Current outputs of neurons.
        
        """
        
        return self._outputs;
    
    @outputs.setter
    def outputs(self, values):
        """!
        @brief Sets outputs of neurons.
        
        """
        
        self._outputs = [val for val in values];
        self._outputs_buffer = [val for val in values];
    
    @property
    def states(self):
        """!
        @brief Return current states of neurons.
        
        @return (list) States of neurons.
        
        """
        
        return self._states;
    
    @states.setter
    def states(self, values):
        """!
        @brief Set current states of neurons.
        
        """
        
        self._states = [val for val in values];
   
    
    def __init__(self, num_osc, own_weight = -4, neigh_weight = -1, type_conn = conn_type.ALL_TO_ALL, type_conn_represent = conn_represent.MATRIX):
        """!
        @brief Constructor of hysteresis oscillatory network.
        
        @param[in] num_osc (uint): Number of oscillators in the network.
        @param[in] own_weight (double): Weight of connection from oscillator to itself - own weight.
        @param[in] neigh_weight (double): Weight of connection between oscillators.
        @param[in] type_conn (conn_type): Type of connection between oscillators in the network.
        @param[in] type_conn_represent (conn_represent): Internal representation of connection in the network: matrix or list.
        
        """
        
        super().__init__(num_osc, type_conn, type_conn_represent);
        
        # list of states of neurons.
        self._states = [0] * self._num_osc;
        
        # list of current outputs of neurons.
        self._outputs = [-1] * self._num_osc;
        
        # list of previous outputs of neurons
        self._outputs_buffer = [-1] * self._num_osc;
        
        # matrix of connection weights between neurons.
        self._weight = list();
        for index in range(0, self._num_osc, 1):
            self._weight.append( [neigh_weight] * self._num_osc);
            self._weight[index][index] = own_weight;

    
    def _neuron_states(self, inputs, t, argv):
        """!
        @brief Returns new value of the neuron (oscillator).
        
        @param[in] inputs (list): Initial values (current) of the neuron - excitatory.
        @param[in] t (double): Current time of simulation.
        @param[in] argv (tuple): Extra arguments that are not used for integration - index of the neuron.
        
        @return (double) New value of the neuron.
        
        """
        
        xi = inputs[0];
        index = argv;
        
        # own impact
        impact = self._weight[index][index] * self._outputs[index];
        
        for i in range(0, self._num_osc, 1):
            if (self.has_connection(i, index)):
                impact += self._weight[index][i] * self._outputs[i];

        x = -xi + impact;
                
        if (xi > 1): self._outputs_buffer[index] = 1; 
        if (xi < -1): self._outputs_buffer[index] = -1;
       
        return x;
        
    
    def simulate(self, steps, time, solution = solve_type.RK4, collect_dynamic = True):
        """!
        @brief Performs static simulation of hysteresis oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solution (solving).
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (hysteresis_dynamic) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        """
                
        return self.simulate_static(steps, time, solution, collect_dynamic);
    
    
    def simulate_static(self, steps, time, solution = solve_type.RK4, collect_dynamic = False):
        """!
        @brief Performs static simulation of hysteresis oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solution (solving).
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (hysteresis_dynamic) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        """

        # Check solver before simulation
        if (solution == solve_type.FAST):
            raise NameError("Solver FAST is not support due to low accuracy that leads to huge error.");
        elif (solution == solve_type.RKF45):
            raise NameError("Solver RKF45 is not support in python version.");

        dyn_state = None;
        dyn_time = None;
        
        if (collect_dynamic == True):
            dyn_state = [];
            dyn_time = [];
            
            dyn_state.append(self._states);
            dyn_time.append(0);
        
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._states = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic is True):
                dyn_state.append(self._states);
                dyn_time.append(t);
        
        if (collect_dynamic is False):
            dyn_state.append(self._states);
            dyn_time.append(time);
        
        return hysteresis_dynamic(dyn_state, dyn_time);


    def _calculate_states(self, solution, t, step, int_step):
        """!
        @brief Calculates new states for neurons using differential calculus. Returns new states for neurons.
        
        @param[in] solution (solve_type): Type solver of the differential equation.
        @param[in] t (double): Current time of simulation.
        @param[in] step (double): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Step differentiation that is used for solving differential equation.
        
        @return (list) New states for neurons.
        
        """
        
        next_states = [0] * self._num_osc;
        
        for index in range (0, self._num_osc, 1):            
            result = odeint(self._neuron_states, self._states[index], numpy.arange(t - step, t, int_step), (index , ));
            next_states[index] = result[len(result) - 1][0];
        
        self._outputs = [val for val in self._outputs_buffer];
        return next_states;