"""!

@brief Neural Network: Pulse Coupled Neural Network
@details Implementation based on paper @cite book::image_processing_using_pcnn.

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

import random
import numpy
import warnings

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is partially not available (details: '%s')." % str(error_instance))

try:
    from PIL import Image
except Exception as error_instance:
    warnings.warn("Impossible to import PIL (please, install 'PIL'), pyclustering's visualization "
                  "functionality is partially not available (details: '%s')." % str(error_instance))

from pyclustering.nnet import *

from pyclustering.core.wrapper import ccore_library

import pyclustering.core.pcnn_wrapper as wrapper

from pyclustering.utils import draw_dynamics


class pcnn_parameters:
    """!
    @brief Parameters for pulse coupled neural network.
    
    """
    
    def __init__(self):
        """!
        @brief    Default constructor of parameters for pulse-coupled neural network.
        @details  Constructor initializes parameters by default non-zero values that can be
                  used for simple simulation.
        """
        
        ## Multiplier for the feeding compartment at the current step.
        self.VF = 1.0
        
        ## Multiplier for the linking compartment at the current step.
        self.VL = 1.0
        
        ## Multiplier for the threshold at the current step.
        self.VT = 10.0
        
        
        ## Multiplier for the feeding compartment at the previous step.
        self.AF = 0.1
        
        ## Multiplier for the linking compartment at the previous step.
        self.AL = 0.1
        
        ## Multiplier for the threshold at the previous step.
        self.AT = 0.5
        
        
        ## Synaptic weight - neighbours influence on linking compartment.
        self.W = 1.0
        
        ## Synaptic weight - neighbours influence on feeding compartment.
        self.M = 1.0
        
        
        ## Linking strength in the network.
        self.B = 0.1
        
        ## Enable/disable Fast-Linking mode. Fast linking helps to overcome some of the effects of time quantisation. This process allows the linking wave to progress a lot faster than the feeding wave.
        self.FAST_LINKING = False
    
    
class pcnn_dynamic:
    """!
    @brief Represents output dynamic of PCNN (pulse-coupled neural network).
    
    """

    @property
    def output(self):
        """!
        @brief (list) Returns oscillato outputs during simulation.
        
        """
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_get_output(self.__ccore_pcnn_dynamic_pointer)
            
        return self.__dynamic
    
    
    @property
    def time(self):
        """!
        @brief (list) Returns sampling times when dynamic is measured during simulation.
        
        """
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_get_time(self.__ccore_pcnn_dynamic_pointer)
        
        return list(range(len(self)))
    
    
    def __init__(self, dynamic, ccore=None):
        """!
        @brief Constructor of PCNN dynamic.
        
        @param[in] dynamic (list): Dynamic of oscillators on each step of simulation. If ccore pointer is specified than it can be ignored.
        @param[in] ccore (ctypes.pointer): Pointer to CCORE pcnn_dynamic instance in memory.
        
        """
        self.__OUTPUT_TRUE = 1    # fire value for oscillators.
        self.__OUTPUT_FALSE = 0   # rest value for oscillators.
        
        self.__dynamic = dynamic
        self.__ccore_pcnn_dynamic_pointer = ccore
    
    
    def __del__(self):
        """!
        @brief Default destructor of PCNN dynamic.
        
        """
        if self.__ccore_pcnn_dynamic_pointer is not None:
            wrapper.pcnn_dynamic_destroy(self.__ccore_pcnn_dynamic_pointer)
    
    
    def __len__(self):
        """!
        @brief (uint) Returns number of simulation steps that are stored in dynamic.
        
        """
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_get_size(self.__ccore_pcnn_dynamic_pointer)
        
        return len(self.__dynamic)
    
    
    def allocate_sync_ensembles(self):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each
               synchronous ensemble corresponds to only one cluster.
        
        @return (list) Grours (lists) of indexes of synchronous oscillators. 
                For example, [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
                
        """
        
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_allocate_sync_ensembles(self.__ccore_pcnn_dynamic_pointer)
        
        sync_ensembles = []
        traverse_oscillators = set()
        
        number_oscillators = len(self.__dynamic[0])
        
        for t in range(len(self.__dynamic) - 1, 0, -1):
            sync_ensemble = []
            for i in range(number_oscillators):
                if self.__dynamic[t][i] == self.__OUTPUT_TRUE:
                    if i not in traverse_oscillators:
                        sync_ensemble.append(i)
                        traverse_oscillators.add(i)
            
            if sync_ensemble != []:
                sync_ensembles.append(sync_ensemble)
        
        return sync_ensembles


    def allocate_spike_ensembles(self):
        """!
        @brief Analyses output dynamic of network and allocates spikes on each iteration as a list of indexes of oscillators.
        @details Each allocated spike ensemble represents list of indexes of oscillators whose output is active.
        
        @return (list) Spike ensembles of oscillators.
        
        """
        
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_allocate_spike_ensembles(self.__ccore_pcnn_dynamic_pointer)
        
        spike_ensembles = []
        number_oscillators = len(self.__dynamic[0])
        
        for t in range(len(self.__dynamic)):
            spike_ensemble = []
            
            for index in range(number_oscillators):
                if self.__dynamic[t][index] == self.__OUTPUT_TRUE:
                    spike_ensemble.append(index)
            
            if len(spike_ensemble) > 0:
                spike_ensembles.append(spike_ensemble)
        
        return spike_ensembles
    
    
    def allocate_time_signal(self):
        """!
        @brief Analyses output dynamic and calculates time signal (signal vector information) of network output.
           
        @return (list) Time signal of network output.
        
        """
        
        if self.__ccore_pcnn_dynamic_pointer is not None:
            return wrapper.pcnn_dynamic_allocate_time_signal(self.__ccore_pcnn_dynamic_pointer)
        
        signal_vector_information = []
        for t in range(0, len(self.__dynamic)):
            signal_vector_information.append(sum(self.__dynamic[t]))
        
        return signal_vector_information


class pcnn_visualizer:
    """!
    @brief Visualizer of output dynamic of pulse-coupled neural network (PCNN).
    
    """
    
    @staticmethod
    def show_time_signal(pcnn_output_dynamic):
        """!
        @brief Shows time signal (signal vector information) using network dynamic during simulation.
        
        @param[in] pcnn_output_dynamic (pcnn_dynamic): Output dynamic of the pulse-coupled neural network.
        
        """
        
        time_signal = pcnn_output_dynamic.allocate_time_signal()
        time_axis = range(len(time_signal))
        
        plt.subplot(1, 1, 1)
        plt.plot(time_axis, time_signal, '-')
        plt.ylabel("G (time signal)")
        plt.xlabel("t (iteration)")
        plt.grid(True)
        
        plt.show()
        
    @staticmethod
    def show_output_dynamic(pcnn_output_dynamic, separate_representation = False):
        """!
        @brief Shows output dynamic (output of each oscillator) during simulation.
        
        @param[in] pcnn_output_dynamic (pcnn_dynamic): Output dynamic of the pulse-coupled neural network.
        @param[in] separate_representation (list): Consists of lists of oscillators where each such list consists of oscillator indexes that will be shown on separated stage.
        
        """
        
        draw_dynamics(pcnn_output_dynamic.time, pcnn_output_dynamic.output, x_title = "t", y_title = "y(t)", separate = separate_representation)
    
    @staticmethod
    def animate_spike_ensembles(pcnn_output_dynamic, image_size):
        """!
        @brief Shows animation of output dynamic (output of each oscillator) during simulation.
        
        @param[in] pcnn_output_dynamic (pcnn_dynamic): Output dynamic of the pulse-coupled neural network.
        @param[in] image_size (tuple): Image size represented as (height, width).
        
        """
        
        figure = plt.figure()
        
        time_signal = pcnn_output_dynamic.allocate_time_signal()
        spike_ensembles = pcnn_output_dynamic.allocate_spike_ensembles()
        
        spike_animation = []
        ensemble_index = 0
        for t in range(len(time_signal)):
            image_color_segments = [(255, 255, 255)] * (image_size[0] * image_size[1])
            
            if time_signal[t] > 0:
                for index_pixel in spike_ensembles[ensemble_index]:
                    image_color_segments[index_pixel] = (0, 0, 0)
                
                ensemble_index += 1

            stage = numpy.array(image_color_segments, numpy.uint8)
            stage = numpy.reshape(stage, image_size + ((3),)) # ((3),) it's size of RGB - third dimension.
            image_cluster = Image.fromarray(stage, 'RGB')
            
            spike_animation.append( [ plt.imshow(image_cluster, interpolation='none') ] )
            
        
        im_ani = animation.ArtistAnimation(figure, spike_animation, interval=75, repeat_delay=3000, blit=True)
        plt.show()


class pcnn_network(network):
    """!
    @brief Model of oscillatory network that is based on the Eckhorn model.
    
    @details CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
    
    Here is an example how to perform PCNN simulation:
    @code
        from pyclustering.nnet.pcnn import pcnn_network, pcnn_visualizer

        # Create Pulse-Coupled neural network with 10 oscillators.
        net = pcnn_network(10)

        # Perform simulation during 100 steps using binary external stimulus.
        dynamic = net.simulate(50, [1, 1, 1, 0, 0, 0, 0, 1, 1, 1])

        # Allocate synchronous ensembles from the output dynamic.
        ensembles = dynamic.allocate_sync_ensembles()

        # Show output dynamic.
        pcnn_visualizer.show_output_dynamic(dynamic, ensembles)
    @endcode
    
    """
    
    __OUTPUT_TRUE = 1    # fire value for oscillators.
    __OUTPUT_FALSE = 0   # rest value for oscillators.
    
    def __init__(self, num_osc, parameters=None, type_conn=conn_type.ALL_TO_ALL, type_conn_represent=conn_represent.MATRIX, height=None, width=None, ccore=True):
        """!
        @brief Constructor of oscillatory network is based on Kuramoto model.
        
        @param[in] num_osc (uint): Number of oscillators in the network.
        @param[in] parameters (pcnn_parameters): Parameters of the network.
        @param[in] type_conn (conn_type): Type of connection between oscillators in the network (all-to-all, grid, bidirectional list, etc.).
        @param[in] type_conn_represent (conn_represent): Internal representation of connection in the network: matrix or list.
        @param[in] height (uint): Number of oscillators in column of the network, this argument is used 
                    only for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types this argument is ignored.
        @param[in] width (uint): Number of oscillotors in row of the network, this argument is used only 
                    for network with grid structure (GRID_FOUR, GRID_EIGHT), for other types this argument is ignored.
        @param[in] ccore (bool): If True then all interaction with object will be performed via CCORE library (C++ implementation of pyclustering).
        
        """
        
        self._outputs = None            # list of outputs of oscillators.
    
        self._feeding = None            # feeding compartment of each oscillator.
        self._linking = None            # linking compartment of each oscillator.
        self._threshold = None          # threshold of each oscillator.
        
        self._params = None
        
        self.__ccore_pcnn_pointer = None
        
        # set parameters of the network
        if parameters is not None:
            self._params = parameters
        else:
            self._params = pcnn_parameters()
        
        if (ccore is True) and ccore_library.workable():
            network_height = height
            network_width = width
            
            if (type_conn == conn_type.GRID_FOUR) or (type_conn == conn_type.GRID_EIGHT):
                if (network_height is None) or (network_width is None):
                    side_size = num_osc ** (0.5)
                    if side_size - math.floor(side_size) > 0:
                        raise NameError('Invalid number of oscillators in the network in case of grid structure')
                
                    network_height = int(side_size)
                    network_width = int(side_size)
            else:
                network_height = 0
                network_width = 0
                
            self.__ccore_pcnn_pointer = wrapper.pcnn_create(num_osc, type_conn, network_height, network_width, self._params)
        else:
            super().__init__(num_osc, type_conn, type_conn_represent, height, width)
            
            self._outputs = [0.0] * self._num_osc
            
            self._feeding = [0.0] * self._num_osc
            self._linking = [0.0] * self._num_osc
            self._threshold = [ random.random() for i in range(self._num_osc) ]
    
    
    def __del__(self):
        """!
        @brief Default destructor of PCNN.
        
        """
        if self.__ccore_pcnn_pointer is not None:
            wrapper.pcnn_destroy(self.__ccore_pcnn_pointer)
            self.__ccore_pcnn_pointer = None
    
    
    def __len__(self):
        """!
        @brief (uint) Returns size of oscillatory network.
        
        """
        
        if self.__ccore_pcnn_pointer is not None:
            return wrapper.pcnn_get_size(self.__ccore_pcnn_pointer)
        
        return self._num_osc
    
        
    def simulate(self, steps, stimulus):
        """!
        @brief Performs static simulation of pulse coupled neural network using.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] stimulus (list): Stimulus for oscillators, number of stimulus should be equal to number of oscillators.
        
        @return (pcnn_dynamic) Dynamic of oscillatory network - output of each oscillator on each step of simulation.
        
        """
        
        if len(stimulus) != len(self):
            raise NameError('Number of stimulus should be equal to number of oscillators. Each stimulus corresponds to only one oscillators.')
        
        if self.__ccore_pcnn_pointer is not None:
            ccore_instance_dynamic = wrapper.pcnn_simulate(self.__ccore_pcnn_pointer, steps, stimulus)
            return pcnn_dynamic(None, ccore_instance_dynamic)
        
        dynamic = []
        dynamic.append(self._outputs)
        
        for step in range(1, steps, 1):
            self._outputs = self._calculate_states(stimulus)
            
            dynamic.append(self._outputs)
        
        return pcnn_dynamic(dynamic)
    
    
    def _calculate_states(self, stimulus):
        """!
        @brief Calculates states of oscillators in the network for current step and stored them except outputs of oscillators.
        
        @param[in] stimulus (list): Stimulus for oscillators, number of stimulus should be equal to number of oscillators.
        
        @return (list) New outputs for oscillators (do not stored it).
        
        """
        
        feeding = [0.0] * self._num_osc
        linking = [0.0] * self._num_osc
        outputs = [0.0] * self._num_osc
        threshold = [0.0] * self._num_osc
        
        for index in range(0, self._num_osc, 1):
            neighbors = self.get_neighbors(index)
            
            feeding_influence = 0.0
            linking_influence = 0.0
            
            for index_neighbour in neighbors:
                feeding_influence += self._outputs[index_neighbour] * self._params.M
                linking_influence += self._outputs[index_neighbour] * self._params.W
            
            feeding_influence *= self._params.VF
            linking_influence *= self._params.VL
            
            feeding[index] = self._params.AF * self._feeding[index] + stimulus[index] + feeding_influence
            linking[index] = self._params.AL * self._linking[index] + linking_influence
            
            # calculate internal activity
            internal_activity = feeding[index] * (1.0 + self._params.B * linking[index])
            
            # calculate output of the oscillator
            if internal_activity > self._threshold[index]:
                outputs[index] = self.__OUTPUT_TRUE
            else:
                outputs[index] = self.__OUTPUT_FALSE
            
            # In case of Fast Linking we should calculate threshold until output is changed.
            if self._params.FAST_LINKING is not True:
                threshold[index] = self._params.AT * self._threshold[index] + self._params.VT * outputs[index]

        # In case of Fast Linking we need to wait until output is changed.
        if self._params.FAST_LINKING is True:
            output_change = True    # Set it True for the for the first iteration.
            previous_outputs = outputs[:]

            while output_change is True:
                current_output_change = False

                for index in range(0, self._num_osc, 1):
                    linking_influence = 0.0

                    neighbors = self.get_neighbors(index)
                    for index_neighbour in neighbors:
                        linking_influence += previous_outputs[index_neighbour] * self._params.W
                    
                    linking_influence *= self._params.VL
                    linking[index] = linking_influence
                    
                    internal_activity = feeding[index] * (1.0 + self._params.B * linking[index])
                    
                    # calculate output of the oscillator
                    if internal_activity > self._threshold[index]:
                        outputs[index] = self.__OUTPUT_TRUE
                    else:
                        outputs[index] = self.__OUTPUT_FALSE

                    current_output_change |= (outputs[index] != previous_outputs[index])
                
                output_change = current_output_change
                
                if output_change is True:
                    previous_outputs = outputs[:]
        
        # In case of Fast Linking threshold should be calculated after fast linking.
        if self._params.FAST_LINKING is True:
            for index in range(0, self._num_osc, 1):
                threshold[index] = self._params.AT * self._threshold[index] + self._params.VT * outputs[index]
        
        self._feeding = feeding[:]
        self._linking = linking[:]
        self._threshold = threshold[:]
        
        return outputs
