"""!

@brief Neural Network: Pulse Coupled Neural Network
@details Based on book description:
         - T.Lindblad, J.M.Kinser. Image Processing Using Pulse-Coupled Neural Networks (2nd edition). 2005.

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

from pyclustering.nnet import *;

class pcnn_parameters:
    """!
    @brief Parameters for pulse coupled neural network.
    
    """
    
    VF = 1.0;   # multiplier for the feeding compartment at the current step
    VL = 1.0;   # multiplier for the linking compartment at the current step
    VT = 10.0;  # multiplier for the threshold at the current step
    
    AF = 0.1;   # multiplier for the feeding compartment at the previous step
    AL = 0.1;   # multiplier for the linking compartment at the previous step
    AT = 0.5;   # multiplier for the threshold at the previous step
    
    W = 1.0;    # neighbours influence on linking compartment
    M = 1.0;    # neighbours influence on feeding compartment
    
    B = 0.1;    # linking strength in the network.
    
    OUTPUT_TRUE = 1;    # fire value for oscillators.
    OUTPUT_FALSE = 0;   # rest value for oscillators.

class pcnn_network(network, network_interface):
    """!
    @brief Model of oscillatory network that is based on the Eckhorn model.
    
    """
    
    # Protected members:
    _name = "Pulse Coupled Neural Network";
    _stimulus = None;           # stimulus of each oscillator.
    _outputs = None;            # list of outputs of oscillors.
    _pointer_dynamic = None;    # pointer to output dynamics.
    
    _feeding = None;            # feeding compartment of each oscillator.    
    _linking = None;            # linking compartment of each oscillator. 
    _threshold = None;          # threshold of each oscillator.
    
    _params = None;
    
    
    def __init__(self, num_osc, stimulus = None, parameters = None, type_conn = conn_type.ALL_TO_ALL, type_conn_represent = conn_represent.MATRIX):
        """!
        @brief Constructor of oscillatory network is based on Kuramoto model.
        
        @param[in] num_osc (uint): Number of oscillators in the network.
        @param[in] stimulus (list): Stimulus for oscillators, number of stimulus should be equal to number of oscillators.
        @param[in] parameters (pcnn_parameters): Parameters of the network.
        @param[in] type_conn (conn_type): Type of connection between oscillators in the network (all-to-all, grid, bidirectional list, etc.).
        @param[in] type_conn_represent (conn_represent): Internal representation of connection in the network: matrix or list.
        
        """
        
        super().__init__(num_osc, type_conn, type_conn_represent);
        
        # set parameters of the network
        if (parameters is not None):
            self._params = parameters;
        else:
            self._params = pcnn_parameters();
        
        self._outputs = [0.0] * self._num_osc;
        
        self._feeding = [0.0] * self._num_osc;    
        self._linking = [0.0] * self._num_osc;        
        self._threshold = [0.0] * self._num_osc;
        
        if (stimulus is None):
            self._stimulus = [0.0] * self._num_osc;
        else:
            if (len(stimulus) != self._num_osc):
                raise NameError('Number of the stimulus should be equal to number of oscillators.');
            else:
                self._stimulus = stimulus;
    
    
    def simulate(self, steps, time = None, solution = solve_type.RK4, collect_dynamic = False):
        """!
        @brief Performs static simulation of pulse coupled neural network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Can be ingored - steps are used instead of time of simulation.
        @param[in] solution (solve_type): Type of solution (solving).
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        """
        
        return self.simulate_static(steps, time, solution, collect_dynamic);
        
        
    def simulate_static(self, steps, time = None, solution = solve_type.RK4, collect_dynamic = False):
        """!
        @brief Performs static simulation of pulse coupled neural network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Can be ingored - steps are used instead of time of simulation.
        @param[in] solution (solve_type): Type of solution (solving).
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        """
        
        dyn_output = None;
        # dyn_threshold = None;
        # dyn_feeding = None;
        # dyn_linking = None;
        
        dyn_time = None;
        
        if (collect_dynamic == True):
            dyn_output = [];
            # dyn_threshold = [];
            # dyn_feeding = [];
            # dyn_linking = [];
            
            dyn_time = [];
            
            dyn_output.append(self._outputs);
            # dyn_threshold.append(self._threshold);
            # dyn_feeding.append(self._feeding);
            # dyn_linking.append(self._linking);
            dyn_time.append(0);
        
        for step in range(0, steps, 1):
            self._outputs = self._calculate_states(step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_output.append(self._outputs);
                # dyn_threshold.append(self._threshold);
                # dyn_feeding.append(self._feeding);
                # dyn_linking.append(self._linking);
                
                dyn_time.append(step);
            else:
                dyn_output = self._outputs;
                dyn_time = step;
        
        self._pointer_dynamic = dyn_output;
        #return (dyn_time, dyn_output, dyn_threshold, dyn_feeding, dyn_linking);
        return (dyn_time, dyn_output);
    
    
    def simulate_dynamic(self, order, solution, collect_dynamic, step, int_step, threshold_changes):
        """!
        @brief Performs dynamic simulation, when time simulation is not specified, only stop condition.
        
        @warning The method is not supported.
        
        """
        
        raise NameError("Dynamic simulation is not supported due to lack of stop conditions for the model.");
    
        
    def _calculate_states(self, t):
        """!
        @brief Calculates states of oscillators in the network for current step and stored them except outputs of oscillators.
        
        @param[in] t (double): Can be ignored, current step of simulation.
        
        @return (list) New outputs for oscillators (do not stored it).
        
        """
        
        feeding = [0.0] * self._num_osc;
        linking = [0.0] * self._num_osc;
        outputs = [0.0] * self._num_osc;
        threshold = [0.0] * self._num_osc;
        
        for index in range(0, self._num_osc, 1):
            neighbors = self.get_neighbors(index);
            
            feeding_influence = 0.0;
            linking_influence = 0.0;
            
            for index_neighbour in neighbors:
                feeding_influence += self._outputs[index_neighbour] * self._params.M;
                linking_influence += self._outputs[index_neighbour] * self._params.W;
            
            feeding_influence *= self._params.VF;
            linking_influence *= self._params.VL;
            
            # feeding[index] = math.exp(-self._params.AF) * self._feeding[index] + self._stimulus[index];
            # linking[index] = math.exp(-self._params.AL) * self._linking[index];
            
            feeding[index] = self._params.AF * self._feeding[index] + self._stimulus[index] + feeding_influence;
            linking[index] = self._params.AL * self._linking[index] + linking_influence;
            
            # calculate internal activity
            internal_activity = feeding[index] * (1.0 + self._params.B * linking[index]);
            
            # calculate output of the oscillator
            if (internal_activity > self._threshold[index]):
                outputs[index] = self._params.OUTPUT_TRUE;
            else:
                outputs[index] = self._params.OUTPUT_FALSE;
                
            # threshold[index] = math.exp(-self._params.AT) * self._threshold[index] + self._params.VT * outputs[index];
            threshold[index] = self._params.AT * self._threshold[index] + self._params.VT * outputs[index];
            
        self._feeding = feeding[:];
        self._linking = linking[:];
        self._threshold = threshold[:];
        
        return outputs;
    
    
    def allocate_sync_ensembles(self, tolerance = 10):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each
               synchronous ensemble corresponds to only one cluster.
               
        @param[in] (double): Is not used, can be ignored.
        
        @return (list) Grours (lists) of indexes of synchronous oscillators. 
                For example, [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
                
        """
        
        sync_ensembles = [];
        traverse_oscillators = set();
        
        if (isinstance(self._pointer_dynamic[0], list) is not True):
            return None;
        
        lower_boundary = 0;
#         lower_boundary = len(self._pointer_dynamic) - 1 - tolerance;
#         if (lower_boundary < 0):
#             lower_boundary = 0;
        
        for t in range(len(self._pointer_dynamic) - 1, lower_boundary, -1):
            sync_ensemble = [];
            for i in range(self._num_osc):
                if (self._pointer_dynamic[t][i] == self._params.OUTPUT_TRUE):
                    if (i not in traverse_oscillators):
                        sync_ensemble.append(i);
                        traverse_oscillators.add(i);
            
            if (sync_ensemble != []):
                sync_ensembles.append(sync_ensemble);
        
        return sync_ensembles;
