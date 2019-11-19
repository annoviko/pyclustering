"""!

@brief Neural Network: Local Excitatory Global Inhibitory Oscillatory Network (LEGION)
@details Implementation based on paper @cite article::legion::1, @cite article::legion::2.

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
import random

import pyclustering.core.legion_wrapper as wrapper

from pyclustering.core.wrapper import ccore_library

from pyclustering.nnet import *

from pyclustering.utils import heaviside, allocate_sync_ensembles

from scipy.integrate import odeint


class legion_parameters:
    """!
    @brief Describes parameters of LEGION.
    @details Contained parameters affect on output dynamic of each oscillator of the network.
    
    @see legion_network
    
    """  
    
    def __init__(self):
        """!
        @brief    Default constructor of parameters for LEGION (local excitatory global inhibitory oscillatory network).
        @details  Constructor initializes parameters by default non-zero values that can be
                  used for simple simulation.
        """
        
        ## Coefficient that affects intrinsic inhibitor of each oscillator. Should be the same as 'alpha'.
        self.eps         = 0.02;
        
        ## Coefficient is chosen to be on the same order of magnitude as 'eps'. Affects on exponential function that decays on a slow time scale.
        self.alpha       = 0.005;
        
        ## Coefficient that is used to control the ratio of the times that the solution spends in these two phases. For a larger value of g, the solution spends a shorter time in the active phase.
        self.gamma       = 6.0;
        
        ## Coefficient that affects on intrinsic inhibitor of each oscillator. Specifies the steepness of the sigmoid function.
        self.betta       = 0.1;
        
        ## Scale coefficient that is used by potential, should be greater than 0.
        self.lamda       = 0.1;
        
        ## Threshold that should be exceeded by a potential to switch on potential.
        self.teta        = 0.9;
        
        ## Threshold that should be exceeded by a single oscillator to affect its neighbors.
        self.teta_x      = -1.5;
        
        ## Threshold that should be exceeded to activate potential. If potential less than the threshold then potential is relaxed to 0 on time scale 'mu'.
        self.teta_p      = 1.5;
        
        ## Threshold that should be exceeded by any oscillator to activate global inhibitor.
        self.teta_xz     = 0.1;
        
        ## Threshold that should be exceeded to affect on a oscillator by the global inhibitor.
        self.teta_zx     = 0.1;
        
        ## Weight of permanent connections.
        self.T           = 2.0;
        
        ## Defines time scaling of relaxing of oscillator potential.
        self.mu          = 0.01;
        
        ## Weight of global inhibitory connections.
        self.Wz          = 1.5;
        
        ## Total dynamic weights to a single oscillator from neighbors. Sum of weights of dynamic connections to a single oscillator can not be bigger than Wt.
        self.Wt          = 8.0;
        
        ## Rate at which the global inhibitor reacts to the stimulation from the oscillator network.
        self.fi          = 3.0;
        
        ## Multiplier of oscillator noise. Plays important role in desynchronization process.
        self.ro          = 0.02;
        
        ## Value of external stimulus.
        self.I           = 0.2;
        
        ## Defines whether to use potentional of oscillator or not.
        self.ENABLE_POTENTIONAL = True;


class legion_dynamic:
    """!
    @brief Represents output dynamic of LEGION.
    
    """
    
    @property
    def output(self):
        """!
        @brief Returns output dynamic of the network.
        
        """
        if (self.__ccore_legion_dynamic_pointer is not None):
            return wrapper.legion_dynamic_get_output(self.__ccore_legion_dynamic_pointer);
            
        return self.__output;
    

    @property
    def inhibitor(self):
        """!
        @brief Returns output dynamic of the global inhibitor of the network.
        
        """
        
        if (self.__ccore_legion_dynamic_pointer is not None):
            return wrapper.legion_dynamic_get_inhibitory_output(self.__ccore_legion_dynamic_pointer);
            
        return self.__inhibitor;
    
    
    @property
    def time(self):
        """!
        @brief Returns simulation time.
        
        """
        if (self.__ccore_legion_dynamic_pointer is not None):
            return wrapper.legion_dynamic_get_time(self.__ccore_legion_dynamic_pointer);
        
        return list(range(len(self)));
    
    
    def __init__(self, output, inhibitor, time, ccore = None):
        """!
        @brief Constructor of legion dynamic.
        
        @param[in] output (list): Output dynamic of the network represented by excitatory values of oscillators.
        @param[in] inhibitor (list): Output dynamic of the global inhibitor of the network.
        @param[in] time (list): Simulation time.
        @param[in] ccore (POINTER): Pointer to CCORE legion_dynamic. If it is specified then others arguments can be omitted.
        
        """
        
        self.__output = output;
        self.__inhibitor = inhibitor;
        self._time = time;
        
        self.__ccore_legion_dynamic_pointer = ccore;
        
        
    def __del__(self):
        """!
        @brief Destructor of the dynamic of the legion network.
        
        """
        if (self.__ccore_legion_dynamic_pointer is not None):
            wrapper.legion_dynamic_destroy(self.__ccore_legion_dynamic_pointer);


    def __len__(self):
        """!
        @brief Returns length of output dynamic.
        
        """
        if (self.__ccore_legion_dynamic_pointer is not None):
            return wrapper.legion_dynamic_get_size(self.__ccore_legion_dynamic_pointer);
        
        return len(self._time);


    def allocate_sync_ensembles(self, tolerance = 0.1):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster.
        
        @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
        
        @return (list) Grours of indexes of synchronous oscillators, for example, [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
        
        """

        if (self.__ccore_legion_dynamic_pointer is not None):
            self.__output = wrapper.legion_dynamic_get_output(self.__ccore_legion_dynamic_pointer);
            
        return allocate_sync_ensembles(self.__output, tolerance);


class legion_network(network):
    """!
    @brief Local excitatory global inhibitory oscillatory network (LEGION) that uses relaxation oscillator
           based on Van der Pol model. 
           
    @details The model uses global inhibitor to de-synchronize synchronous ensembles of oscillators.
             
             CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
    Example:
    @code
        # Create parameters of the network
        parameters = legion_parameters();
        parameters.Wt = 4.0;
        
        # Create stimulus
        stimulus = [1, 1, 0, 0, 0, 1, 1, 1];
        
        # Create the network (use CCORE for fast solving)
        net = legion_network(len(stimulus), parameters, conn_type.GRID_FOUR, ccore = True);
        
        # Simulate network - result of simulation is output dynamic of the network
        output_dynamic = net.simulate(1000, 750, stimulus);
        
        # Draw output dynamic
        draw_dynamics(output_dynamic.time, output_dynamic.output, x_title = "Time", y_title = "x(t)");
    @endcode
    
    """

    def __init__(self, num_osc, parameters = None, type_conn = conn_type.ALL_TO_ALL, type_conn_represent = conn_represent.MATRIX, ccore = True):
        """!
        @brief Constructor of oscillatory network LEGION (local excitatory global inhibitory oscillatory network).
        
        @param[in] num_osc (uint): Number of oscillators in the network.
        @param[in] parameters (legion_parameters): Parameters of the network that are defined by structure 'legion_parameters'.
        @param[in] type_conn (conn_type): Type of connection between oscillators in the network.
        @param[in] type_conn_represent (conn_represent): Internal representation of connection in the network: matrix or list.
        @param[in] ccore (bool): If True then all interaction with object will be performed via CCORE library (C++ implementation of pyclustering).
        
        """
        
        self._params = None;                 # parameters of the network
    
        self.__ccore_legion_pointer = None;
        self._params = parameters;
        
        # set parameters of the network
        if (self._params is None):
            self._params = legion_parameters();
        
        if ( (ccore is True) and ccore_library.workable() ):
            self.__ccore_legion_pointer = wrapper.legion_create(num_osc, type_conn, self._params);
            
        else: 
            super().__init__(num_osc, type_conn, type_conn_represent);
                
            # initial states
            self._excitatory = [ random.random() for _ in range(self._num_osc) ];
            self._inhibitory = [0.0] * self._num_osc;
            self._potential = [0.0] * self._num_osc;
            
            self._coupling_term = None;      # coupling term of each oscillator
            self._global_inhibitor = 0;      # value of global inhibitory
            self._stimulus = None;           # stimulus of each oscillator
            
            self._dynamic_coupling = None;   # dynamic connection between oscillators
            self._coupling_term = [0.0] * self._num_osc;
            self._buffer_coupling_term = [0.0] * self._num_osc;
                
            # generate first noises
            self._noise = [random.random() * self._params.ro for i in range(self._num_osc)];


    def __del__(self):
        """!
        @brief Default destructor of LEGION.
        
        """
        if (self.__ccore_legion_pointer is not None):
            wrapper.legion_destroy(self.__ccore_legion_pointer);
            self.__ccore_legion_pointer = None;


    def __len__(self):
        """!
        @brief (uint) Returns size of LEGION.
        
        """
        
        if (self.__ccore_legion_pointer is not None):
            return wrapper.legion_get_size(self.__ccore_legion_pointer);
        
        return self._num_osc;


    def __create_stimulus(self, stimulus):
        """!
        @brief Create stimulus for oscillators in line with stimulus map and parameters.
        
        @param[in] stimulus (list): Stimulus for oscillators that is represented by list, number of stimulus should be equal number of oscillators.
        
        """
        
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
        
        if self._stimulus is None:
            raise NameError("Stimulus should initialed before creation of the dynamic connections in the network.");
        
        self._dynamic_coupling = [ [0] * self._num_osc for i in range(self._num_osc)];
        
        for i in range(self._num_osc):
            neighbors = self.get_neighbors(i)
            
            if (len(neighbors) > 0) and (self._stimulus[i] > 0):
                number_stimulated_neighbors = 0.0
                for j in neighbors:
                    if self._stimulus[j] > 0:
                        number_stimulated_neighbors += 1.0
                
                if (number_stimulated_neighbors > 0):
                    dynamic_weight = self._params.Wt / number_stimulated_neighbors
                    
                    for j in neighbors:
                        self._dynamic_coupling[i][j] = dynamic_weight
    
    
    def simulate(self, steps, time, stimulus, solution=solve_type.RK4, collect_dynamic=True):
        """!
        @brief Performs static simulation of LEGION oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] stimulus (list): Stimulus for oscillators, number of stimulus should be equal to number of oscillators,
                   example of stimulus for 5 oscillators [0, 0, 1, 1, 0], value of stimulus is defined by parameter 'I'.
        @param[in] solution (solve_type): Method that is used for differential equation.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        """
        
        if self.__ccore_legion_pointer is not None:
            pointer_dynamic = wrapper.legion_simulate(self.__ccore_legion_pointer, steps, time, solution, collect_dynamic, stimulus)
            return legion_dynamic(None, None, None, pointer_dynamic)
        
        # Check solver before simulation
        if solution == solve_type.FAST:
            raise NameError("Solver FAST is not support due to low accuracy that leads to huge error.")
        
        elif solution == solve_type.RKF45:
            raise NameError("Solver RKF45 is not support in python version. RKF45 is supported in CCORE implementation.")
        
        # set stimulus
        self.__create_stimulus(stimulus)
            
        # calculate dynamic weights
        self.__create_dynamic_connections()
        
        dyn_exc = None
        dyn_time = None
        dyn_ginh = None
        
        # Store only excitatory of the oscillator
        if collect_dynamic is True:
            dyn_exc = []
            dyn_time = []
            dyn_ginh = []
            
        step = time / steps
        int_step = step / 10.0
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._calculate_states(solution, t, step, int_step)
            
            # update states of oscillators
            if collect_dynamic is True:
                dyn_exc.append(self._excitatory)
                dyn_time.append(t)
                dyn_ginh.append(self._global_inhibitor)
            else:
                dyn_exc = self._excitatory
                dyn_time = t
                dyn_ginh = self._global_inhibitor
        
        return legion_dynamic(dyn_exc, dyn_ginh, dyn_time);
    
    
    def _calculate_states(self, solution, t, step, int_step):
        """!
        @brief Calculates new state of each oscillator in the network.
        
        @param[in] solution (solve_type): Type solver of the differential equation.
        @param[in] t (double): Current time of simulation.
        @param[in] step (double): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Step differentiation that is used for solving differential equation.
        
        """
        
        next_excitatory = [0.0] * self._num_osc;
        next_inhibitory = [0.0] * self._num_osc;
        
        next_potential = [];
        if (self._params.ENABLE_POTENTIONAL is True):
            next_potential = [0.0] * self._num_osc;
        
        # Update states of oscillators
        for index in range (0, self._num_osc, 1):
            if (self._params.ENABLE_POTENTIONAL is True):
                result = odeint(self._legion_state, [self._excitatory[index], self._inhibitory[index], self._potential[index]], numpy.arange(t - step, t, int_step), (index , ));
                [ next_excitatory[index], next_inhibitory[index], next_potential[index] ] = result[len(result) - 1][0:3];
                
            else:
                result = odeint(self._legion_state_simplify, [self._excitatory[index], self._inhibitory[index] ], numpy.arange(t - step, t, int_step), (index , ));
                [ next_excitatory[index], next_inhibitory[index] ] = result[len(result) - 1][0:2];
            
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
        self._excitatory = next_excitatory[:];
        
        if (self._params.ENABLE_POTENTIONAL is True):
            self._potential = next_potential[:];
            
    
    
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
    
    
    def _legion_state_simplify(self, inputs, t, argv):
        """!
        @brief Returns new values of excitatory and inhibitory parts of oscillator of oscillator.
        @details Simplify model doesn't consider oscillator potential.
        
        @param[in] inputs (list): Initial values (current) of oscillator [excitatory, inhibitory].
        @param[in] t (double): Current time of simulation.
        @param[in] argv (uint): Extra arguments that are not used for integration - index of oscillator.
        
        @return (list) New values of excitatoty and inhibitory part of oscillator (not assign).
        
        """
        
        index = argv;
        
        x = inputs[0];  # excitatory
        y = inputs[1];  # inhibitory
        
        dx = 3.0 * x - x ** 3.0 + 2.0 - y + self._stimulus[index] + self._coupling_term[index] + self._noise[index];
        dy = self._params.eps * (self._params.gamma * (1.0 + math.tanh(x / self._params.betta)) - y);
        
        neighbors = self.get_neighbors(index);
        potential = 0.0;
        
        for index_neighbor in neighbors:
            potential += self._params.T * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
        
        return [dx, dy];    
    
    
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
        
        dx = 3.0 * x - x ** 3.0 + 2.0 - y + self._stimulus[index] * potential_influence + self._coupling_term[index] + self._noise[index];
        dy = self._params.eps * (self._params.gamma * (1.0 + math.tanh(x / self._params.betta)) - y);
        
        neighbors = self.get_neighbors(index);
        potential = 0.0;
        
        for index_neighbor in neighbors:
            potential += self._params.T * heaviside(self._excitatory[index_neighbor] - self._params.teta_x);
        
        dp = self._params.lamda * (1.0 - p) * heaviside(potential - self._params.teta_p) - self._params.mu * p;
        
        return [dx, dy, dp];