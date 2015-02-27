"""!

@brief Neural Network: Local Excitatory Global Inhibitory Oscillatory Network (LEGION)
@details Based on article description:
         - D.Wang, D.Terman. Image Segmentation Based on Oscillatory Correlation. 1997.
         - D.Wang, D.Terman. Locally Excitatory Globally Inhibitory Oscillator Networks. 1995.

@authors Andrei Novikov (spb.andr@yandex.ru)
@version 1.0
@date 2014-2015
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

import numpy;
import math;
import random;

from pyclustering.nnet import *;  

from pyclustering.support import heaviside, allocate_sync_ensembles;

from scipy.integrate import odeint;

class legion_parameters:
    """!
    @brief Describes parameters of LEGION.
    
    @see legion_network
    
    """  
    
    eps         = 0.02;
    alpha       = 0.005;
    gamma       = 6.0;
    betta       = 0.1;
    lamda       = 0.1;
    teta        = 0.9;
    teta_x      = -1.5;
    teta_p      = 1.5;
    teta_xz     = 0.1;
    teta_zx     = 0.1;
    T           = 2.0;          # value of permanent connections
    mu          = 0.01;
    Wz          = 1.5;          # value of global inhibitory connections
    Wt          = 8.0;
    fi          = 3.0;
    ro          = 0.02;         # multiplier of oscillator noise
    I           = 0.2;          # value of stimulus


class legion_network(network, network_interface):
    """!
    @brief Local excitatory global inhibitory oscillatory network (LEGION) that uses relaxation oscillator
           based on Van der Pol model. The model uses global inhibitor to de-synchronize synchronous ensembles
           of oscillators.
           
    """
    
    _name = "Local excitatory global inhibitory oscillatory network (LEGION)"
    
    _excitatory = None;         # excitatory state of each oscillator
    _inhibitory = None;         # inhibitory state of each oscillator
    _potential = None;          # potential of each oscillator
    
    _stimulus = None;           # stimulus of each oscillator
    _coupling_term = None;      # coupling term of each oscillator
    _global_inhibitor = 0;      # value of global inhibitory
    
    _buffer_coupling_term = None;   # coupling terms on previous step of simulation
    _dynamic_coupling = None;       # dynamic connection between oscillators
    
    _params = None;                 # parameters of the network
    
    _noise = None;                  # noise of each oscillator
    
    _dyn_exc = None;                # save pointer to the excitatory dynamic of the network of the last simulation
    
    def __init__(self, num_osc, stimulus = None, parameters = None, type_conn = conn_type.ALL_TO_ALL, type_conn_represent = conn_represent.MATRIX):
        """!
        @brief Constructor of oscillatory network LEGION (local excitatory global inhibitory oscillatory network).
        
        @param[in] num_osc (uint): Number of oscillators in the network.
        @param[in] stimulus (list): Stimulus for oscillators, number of stimulus should be equal to number of oscillators,
                           example of stimulus for 5 oscillators [0, 0, 1, 1, 0], value of stimulus is defined by parameter 'I'.
        @param[in] parameters (legion_parameters): Parameters of the network that are defined by structure 'legion_parameters'.
        @param[in] type_conn (conn_type): Type of connection between oscillators in the network.
        @param[in] type_conn_represent (conn_represent): Internal representation of connection in the network: matrix or list.
        
        """
        
        super().__init__(num_osc, type_conn, type_conn_represent);
        
        # set parameters of the network
        if (parameters is not None):
            self._params = parameters;
        else:
            self._params = legion_parameters();
            
        # initial states
        self._excitatory = [ random.random() for i in range(self._num_osc) ];
        self._inhibitory = [0.0] * self._num_osc;
        self._potential = [0.0] * self._num_osc;
        
        self._coupling_term = [0.0] * self._num_osc;
        self._buffer_coupling_term = [0.0] * self._num_osc;
        
        # set stimulus
        self.__create_stimulus(stimulus);
        
        # calculate dynamic weights
        self.__create_dynamic_connections();
            
        # generate first noises
        self._noise = [random.random() * self._params.ro for i in range(self._num_osc)];
    
    
    def __create_stimulus(self, stimulus):
        """!
        @brief Create stimulus for oscillators in line with stimulus map and parameters.
        
        @param[in] stimulus (list): Stimulus for oscillators that is represented by list, number of stimulus should be equal number of oscillators.
        
        """
        
        if (stimulus is None):
            self._stimulus = [0] * self._num_osc;
        else:
            if (len(stimulus) != self._num_osc):
                raise NameError("Number of stimulus should be equal number of oscillators in the network.");
            else:
                self._stimulus = [];
                 
                for val in stimulus:
                    if (val > 0): self._stimulus.append(self._params.I);
                    else: self._stimulus.append(0);
    
    
    def __create_dynamic_connections(self):
        """!
        @brief Create dynamic connection in line with input stimulus.
        
        """
        
        if (self._stimulus is None):
            raise NameError("Stimulus should initialed before creation of the dynamic connections in the network.");
        
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
    
    
    def simulate(self, steps, time, solution = solve_type.RK4, collect_dynamic = True):
        """!
        @brief Performs static simulation of LEGION oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solution (solving).
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        """
        
        return self.simulate_static(steps, time, solution, collect_dynamic);
    
    
    def simulate_dynamic(self, order, solution, collect_dynamic, step, int_step, threshold_changes):
        """!
        @brief Performs dynamic simulation, when time simulation is not specified, only stop condition.
        
        @warning The method is not supported.
        
        """
        
        raise NameError("Dynamic simulation is not supported due to lack of stop conditions for the model.");
    
    
    def simulate_static(self, steps, time, solution = solve_type.RK4, collect_dynamic = False):
        """!
        @brief Performs static simulation of LEGION oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solution (only RK4 is supported for python implementation).
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        """  
        
        # Check solver before simulation
        if (solution == solve_type.FAST):
            raise NameError("Solver FAST is not support due to low accuracy that leads to huge error.");
        elif (solution == solve_type.RKF45):
            raise NameError("Solver RKF45 is not support in python version.");
        
        if (self._dyn_exc is not None):
            del self._dyn_exc;
            self._dyn_exc = None;
        
        dyn_exc = None;
        dyn_time = None;
        dyn_ginh = None;
        
        # Store only excitatory of the oscillator
        if (collect_dynamic == True):
            dyn_exc = [];
            dyn_time = [];
            dyn_ginh = [];
            
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._excitatory = self._calculate_states(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_exc.append(self._excitatory);
                dyn_time.append(t);
                dyn_ginh.append(self._global_inhibitor);
            else:
                dyn_exc = self._excitatory;
                dyn_time = t;
                dyn_ginh = self._global_inhibitor;
        
        self._dyn_exc = dyn_exc;
        return (dyn_time, dyn_exc, dyn_ginh); 
    
    
    def _calculate_states(self, solution, t, step, int_step):
        """!
        @brief Calculates new state of each oscillator in the network. Returns only excitatory state of oscillators.
        
        @param[in] solution (solve_type): Type solver of the differential equation.
        @param[in] t (double): Current time of simulation.
        @param[in] step (double): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Step differentiation that is used for solving differential equation.
        
        @return (list) New state of excitatory parts of oscillators.
        
        """
        
        next_excitatory = [0.0] * self._num_osc;
        next_inhibitory = [0.0] * self._num_osc;
        next_potential = [0.0] * self._num_osc;
        
        # Update states of oscillators
        for index in range (0, self._num_osc, 1):
            result = odeint(self._legion_state, [self._excitatory[index], self._inhibitory[index], self._potential[index]], numpy.arange(t - step, t, int_step), (index , ));
            [ next_excitatory[index], next_inhibitory[index], next_potential[index] ] = result[len(result) - 1][0:3];
            
            # Update coupling term
            neighbors = self.get_neighbors(index);
            
            coupling = 0
            for index_neighbor in neighbors:
                coupling += self._dynamic_coupling[index][index_neighbor] * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
            
            self._buffer_coupling_term[index] = coupling - self._params.Wz * heaviside(self._global_inhibitor - self._params.teta_xz);
        
        # Update state of global inhibitory
        result = odeint(self._global_inhibitor_state, self._global_inhibitor, numpy.arange(t - step, t, int_step), (None, ));
        self._global_inhibitor = result[len(result) - 1][0];
        
        self._noise = [random.random() * self._params.ro for i in range(self._num_osc)];
        self._coupling_term = self._buffer_coupling_term[:];
        self._inhibitory = next_inhibitory[:];
        self._potential = next_potential[:];
        
        return next_excitatory;
    
    
    def _global_inhibitor_state(self, z, t, argv):
        """!
        @brief Returns new value of global inhibitory
        
        @param[in] z (dobule): Current value of inhibitory.
        @param[in] t (double): Current time of simulation.
        @param[in] argv (tuple): It's not used, can be ignored.
        
        @return (double) New value if global inhibitory (not assign).
        
        """
        
        sigma = 0.0;
        
        for x in self._excitatory:
            if (x > self._params.teta_zx):
                sigma = 1.0;
                break;
        
        return self._params.fi * (sigma - z);
    
    
    def _legion_state(self, inputs, t, argv):
        """!
        @brief Returns new values of excitatory and inhibitory parts of oscillator and potential of oscillator.
        
        @param[in] inputs (list): Initial values (current) of oscillator [excitatory, inhibitory, potential].
        @param[in] t (double): Current time of simulation.
        @param[in] argv (uint): Extra arguments that are not used for integration - index of oscillator.
        
        @return (list) New values of excitatoty and inhibitory part of oscillator and new value of potential (not assign).
        
        """
        
        index = argv;
        
        x = inputs[0];  # excitatory
        y = inputs[1];  # inhibitory
        p = inputs[2];  # potential
        
        potential_influence = heaviside(p + math.exp(-self._params.alpha * t) - self._params.teta);
        
        dx = 3 * x - x ** 3 + 2 - y + self._stimulus[index] * potential_influence + self._coupling_term[index] - self._noise[index];
        dy = self._params.eps * (self._params.gamma * (1 + math.tanh(x / self._params.betta)) - y);
        
        neighbors = self.get_neighbors(index);
        potential = 0;
        
        for index_neighbor in neighbors:
            potential += self._params.T * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
        
        dp = self._params.lamda * (1 - p) * heaviside(potential - self._params.teta_p) - self._params.mu * p;
        
        return [dx, dy, dp];
    
    
    def allocate_sync_ensembles(self, tolerance = 0.1):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster.
        
        @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
        
        @return (list) Grours of indexes of synchronous oscillators, for example, [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
        
        """

        return allocate_sync_ensembles(self._dyn_exc, tolerance);