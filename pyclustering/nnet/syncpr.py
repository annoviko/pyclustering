"""!

@brief Phase oscillatory network for patten recognition based on modified Kuramoto model.
@details Implementation based on paper @cite article::nnet::syncpr::1.

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

import math
import cmath
import numpy
import warnings

from pyclustering.nnet          import solve_type, initial_type, conn_type,conn_represent
from pyclustering.nnet.sync     import sync_network, sync_dynamic, sync_visualizer

import pyclustering.core.syncpr_wrapper as wrapper

from pyclustering.core.wrapper import ccore_library

try:
    from PIL import Image
except Exception as error_instance:
    warnings.warn("Impossible to import PIL (please, install 'PIL'), pyclustering's visualization "
                  "functionality is partially not available (details: '%s')." % str(error_instance))

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))


class syncpr_dynamic(sync_dynamic):
    """!
    @brief Represents output dynamic of syncpr (Sync for Pattern Recognition).
    
    """
    
    def __init__(self, phase, time, ccore):
        """!
        @brief Constructor of syncpr dynamic.
        
        @param[in] phase (list): Dynamic of oscillators on each step of simulation. If ccore pointer is specified than it can be ignored.
        @param[in] time (list): Simulation time.
        @param[in] ccore (ctypes.pointer): Pointer to CCORE sync_dynamic instance in memory.
        
        """
        super().__init__(phase, time, ccore);


class syncpr_visualizer(sync_visualizer):
    """!
    @brief Visualizer of output dynamic of syncpr network (Sync for Pattern Recognition).
    
    """
    
    @staticmethod
    def show_pattern(syncpr_output_dynamic, image_height, image_width):
        """!
        @brief Displays evolution of phase oscillators as set of patterns where the last one means final result of recognition.
        
        @param[in] syncpr_output_dynamic (syncpr_dynamic): Output dynamic of a syncpr network.
        @param[in] image_height (uint): Height of the pattern (image_height * image_width should be equal to number of oscillators).
        @param[in] image_width (uint): Width of the pattern.
        
        """
        number_pictures = len(syncpr_output_dynamic);
        iteration_math_step = 1.0;
        if (number_pictures > 50):
            iteration_math_step = number_pictures / 50.0;
            number_pictures = 50;
        
        number_cols = int(numpy.ceil(number_pictures ** 0.5));
        number_rows = int(numpy.ceil(number_pictures / number_cols));
        
        real_index = 0, 0;
        double_indexer = True;
        if ( (number_cols == 1) or (number_rows == 1) ):
            real_index = 0;
            double_indexer = False;
        
        (_, axarr) = plt.subplots(number_rows, number_cols);
        
        if (number_pictures > 1):
            plt.setp([ax for ax in axarr], visible = False);
            
        iteration_display = 0.0;
        for iteration in range(len(syncpr_output_dynamic)):
            if (iteration >= iteration_display):
                iteration_display += iteration_math_step;
                
                ax_handle = axarr;
                if (number_pictures > 1):
                    ax_handle = axarr[real_index];
                    
                syncpr_visualizer.__show_pattern(ax_handle, syncpr_output_dynamic, image_height, image_width, iteration);
                
                if (double_indexer is True):
                    real_index = real_index[0], real_index[1] + 1;
                    if (real_index[1] >= number_cols):
                        real_index = real_index[0] + 1, 0; 
                else:
                    real_index += 1;
    
        plt.show();
    
    
    @staticmethod
    def animate_pattern_recognition(syncpr_output_dynamic, image_height, image_width, animation_velocity = 75, title = None, save_movie = None):
        """!
        @brief Shows animation of pattern recognition process that has been preformed by the oscillatory network.
        
        @param[in] syncpr_output_dynamic (syncpr_dynamic): Output dynamic of a syncpr network.
        @param[in] image_height (uint): Height of the pattern (image_height * image_width should be equal to number of oscillators).
        @param[in] image_width (uint): Width of the pattern.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds.
        @param[in] title (string): Title of the animation that is displayed on a figure if it is specified.
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        figure = plt.figure();
        
        def init_frame():
            return frame_generation(0);
        
        def frame_generation(index_dynamic):
            figure.clf();
            
            if (title is not None):
                figure.suptitle(title, fontsize = 26, fontweight = 'bold')
            
            ax1 = figure.add_subplot(121, projection='polar');
            ax2 = figure.add_subplot(122);
            
            dynamic = syncpr_output_dynamic.output[index_dynamic];
            
            artist1, = ax1.plot(dynamic, [1.0] * len(dynamic), marker = 'o', color = 'blue', ls = '');
            artist2 = syncpr_visualizer.__show_pattern(ax2, syncpr_output_dynamic, image_height, image_width, index_dynamic);
            
            return [ artist1, artist2 ];
        
        cluster_animation = animation.FuncAnimation(figure, frame_generation, len(syncpr_output_dynamic), interval = animation_velocity, init_func = init_frame, repeat_delay = 5000);

        if (save_movie is not None):
#             plt.rcParams['animation.ffmpeg_path'] = 'C:\\Users\\annoviko\\programs\\ffmpeg-win64-static\\bin\\ffmpeg.exe';
#             ffmpeg_writer = animation.FFMpegWriter();
#             cluster_animation.save(save_movie, writer = ffmpeg_writer, fps = 15);
            cluster_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();
    
    
    @staticmethod
    def __show_pattern(ax_handle, syncpr_output_dynamic, image_height, image_width, iteration):
        """!
        @brief Draws pattern on specified ax.
        
        @param[in] ax_handle (Axis): Axis where pattern should be drawn.
        @param[in] syncpr_output_dynamic (syncpr_dynamic): Output dynamic of a syncpr network.
        @param[in] image_height (uint): Height of the pattern (image_height * image_width should be equal to number of oscillators).
        @param[in] image_width (uint): Width of the pattern.
        @param[in] iteration (uint): Simulation iteration that should be used for extracting pattern.
        
        @return (matplotlib.artist) Artist (pattern) that is rendered in the canvas.
        
        """
        
        current_dynamic = syncpr_output_dynamic.output[iteration];
        stage_picture = [(255, 255, 255)] * (image_height * image_width);
        for index_phase in range(len(current_dynamic)):
            phase = current_dynamic[index_phase];
            
            pixel_color = math.floor( phase * (255 / (2 * math.pi)) );
            stage_picture[index_phase] = (pixel_color, pixel_color, pixel_color);
          
        stage = numpy.array(stage_picture, numpy.uint8);
        stage = numpy.reshape(stage, (image_height, image_width) + ((3),)); # ((3),) it's size of RGB - third dimension.
        
        image_cluster = Image.fromarray(stage);
        
        artist = ax_handle.imshow(image_cluster, interpolation = 'none');
        plt.setp(ax_handle, visible = True);
        
        ax_handle.xaxis.set_ticklabels([]);
        ax_handle.yaxis.set_ticklabels([]);
        ax_handle.xaxis.set_ticks_position('none');
        ax_handle.yaxis.set_ticks_position('none');
        
        return artist;


class syncpr(sync_network):
    """!
    @brief Model of phase oscillatory network for pattern recognition that is based on the Kuramoto model.
    @details The model uses second-order and third-order modes of the Fourier components.
             
             CCORE option can be used to use the pyclustering core - C/C++ shared library for processing that significantly increases performance.
             
    Example:
    @code
        # Network size should be equal to size of pattern for learning.
        net = syncpr(size_network, 0.3, 0.3);
        
        # Train network using list of patterns (input images).
        net.train(image_samples);
        
        # Recognize image using 10 steps during 10 seconds of simulation.
        sync_output_dynamic = net.simulate(10, 10, pattern, solve_type.RK4, True);
        
        # Display output dynamic.
        syncpr_visualizer.show_output_dynamic(sync_output_dynamic);
        
        # Display evolution of recognition of the pattern.
        syncpr_visualizer.show_pattern(sync_output_dynamic, image_height, image_width);
    
    @endcode
    
    """

    def __init__(self, num_osc, increase_strength1, increase_strength2, ccore = True):
        """!
        @brief Constructor of oscillatory network for pattern recognition based on Kuramoto model.
        
        @param[in] num_osc (uint): Number of oscillators in the network.
        @param[in] increase_strength1 (double): Parameter for increasing strength of the second term of the Fourier component.
        @param[in] increase_strength2 (double): Parameter for increasing strength of the third term of the Fourier component.
        @param[in] ccore (bool): If True simulation is performed by CCORE library (C++ implementation of pyclustering).
        
        """
        
        if ( (ccore is True) and ccore_library.workable() ):
            self._ccore_network_pointer = wrapper.syncpr_create(num_osc, increase_strength1, increase_strength2);
            
        else:
            self._increase_strength1 = increase_strength1;
            self._increase_strength2 = increase_strength2;
            self._coupling = [ [0.0 for i in range(num_osc)] for j in range(num_osc) ];

            super().__init__(num_osc, 1, 0, conn_type.ALL_TO_ALL, conn_represent.MATRIX, initial_type.RANDOM_GAUSSIAN, ccore)
    
    
    def __del__(self):
        """!
        @brief Default destructor of syncpr.
        
        """
        
        if (self._ccore_network_pointer is not None):
            wrapper.syncpr_destroy(self._ccore_network_pointer);
            self._ccore_network_pointer = None;


    def __len__(self):
        """!
        @brief Returns size of the network.
        
        """        
        if (self._ccore_network_pointer is not None):
            return wrapper.syncpr_get_size(self._ccore_network_pointer);
        
        else:
            return self._num_osc;
    
    
    def train(self, samples):
        """!
        @brief Trains syncpr network using Hebbian rule for adjusting strength of connections between oscillators during training.
        
        @param[in] samples (list): list of patterns where each pattern is represented by list of features that are equal to [-1; 1].
        
        """
        
        # Verify pattern for learning
        for pattern in samples:
            self.__validate_pattern(pattern);
        
        if (self._ccore_network_pointer is not None):
            return wrapper.syncpr_train(self._ccore_network_pointer, samples);
        
        length = len(self);
        number_samples = len(samples);
        
        for i in range(length):
            for j in range(i + 1, len(self), 1):
                
                # go through via all patterns
                for p in range(number_samples):
                    value1 = samples[p][i];
                    value2 = samples[p][j];
                    
                    self._coupling[i][j] += value1 * value2;
                
                self._coupling[i][j] /= length;
                self._coupling[j][i] = self._coupling[i][j];
    
    
    def simulate(self, steps, time, pattern, solution = solve_type.RK4, collect_dynamic = True):
        """!
        @brief Performs static simulation of syncpr oscillatory network.
        @details In other words network performs pattern recognition during simulation.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        @param[in] solution (solve_type): Type of solver that should be used for simulation.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see simulate_dynamic()
        @see simulate_static()
        
        """
                    
        return self.simulate_static(steps, time, pattern, solution, collect_dynamic);
    
    
    def simulate_dynamic(self, pattern, order = 0.998, solution = solve_type.RK4, collect_dynamic = False, step = 0.1, int_step = 0.01, threshold_changes = 0.0000001):
        """!
        @brief Performs dynamic simulation of the network until stop condition is not reached.
        @details In other words network performs pattern recognition during simulation. 
                 Stop condition is defined by input argument 'order' that represents memory order, but
                 process of simulation can be stopped if convergance rate is low whose threshold is defined
                 by the argument 'threshold_changes'.
        
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        @param[in] order (double): Order of process synchronization, distributed 0..1.
        @param[in] solution (solve_type): Type of solution.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        @param[in] step (double): Time step of one iteration of simulation.
        @param[in] int_step (double): Integration step, should be less than step.
        @param[in] threshold_changes (double): Additional stop condition that helps prevent infinite simulation, defines limit of changes of oscillators between current and previous steps.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see simulate()
        @see simulate_static()
        
        """
        
        self.__validate_pattern(pattern);
        
        if (self._ccore_network_pointer is not None):
            ccore_instance_dynamic = wrapper.syncpr_simulate_dynamic(self._ccore_network_pointer, pattern, order, solution, collect_dynamic, step);
            return syncpr_dynamic(None, None, ccore_instance_dynamic);
        
        for i in range(0, len(pattern), 1):
            if (pattern[i] > 0.0):
                self._phases[i] = 0.0;
            else:
                self._phases[i] = math.pi / 2.0;
        
        # For statistics and integration
        time_counter = 0;
        
        # Prevent infinite loop. It's possible when required state cannot be reached.
        previous_order = 0;
        current_order = self.__calculate_memory_order(pattern);
        
        # If requested input dynamics
        dyn_phase = [];
        dyn_time = [];
        if (collect_dynamic == True):
            dyn_phase.append(self._phases);
            dyn_time.append(0);
        
        # Execute until sync state will be reached
        while (current_order < order):
            # update states of oscillators
            self._phases = self._calculate_phases(solution, time_counter, step, int_step);
            
            # update time
            time_counter += step;
            
            # if requested input dynamic
            if (collect_dynamic == True):
                dyn_phase.append(self._phases);
                dyn_time.append(time_counter);
                
            # update orders
            previous_order = current_order;
            current_order = self.__calculate_memory_order(pattern);
            
            # hang prevention
            if (abs(current_order - previous_order) < threshold_changes):
                break;
        
        if (collect_dynamic != True):
            dyn_phase.append(self._phases);
            dyn_time.append(time_counter);
        
        output_sync_dynamic = syncpr_dynamic(dyn_phase, dyn_time, None);
        return output_sync_dynamic;


    def simulate_static(self, steps, time, pattern, solution = solve_type.FAST, collect_dynamic = False):
        """!
        @brief Performs static simulation of syncpr oscillatory network.
        @details In other words network performs pattern recognition during simulation.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        @param[in] solution (solve_type): Type of solution.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see simulate()
        @see simulate_dynamic()
        
        """
        
        self.__validate_pattern(pattern);
        
        if (self._ccore_network_pointer is not None):
            ccore_instance_dynamic = wrapper.syncpr_simulate_static(self._ccore_network_pointer, steps, time, pattern, solution, collect_dynamic);
            return syncpr_dynamic(None, None, ccore_instance_dynamic);
        
        for i in range(0, len(pattern), 1):
            if (pattern[i] > 0.0):
                self._phases[i] = 0.0;
            else:
                self._phases[i] = math.pi / 2.0;
                
        return super().simulate_static(steps, time, solution, collect_dynamic);
    
    
    def memory_order(self, pattern):
        """!
        @brief Calculates function of the memorized pattern.
        @details Throws exception if length of pattern is not equal to size of the network or if it consists feature with value that are not equal to [-1; 1].
        
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        
        @return (double) Order of memory for the specified pattern.
        
        """
        
        self.__validate_pattern(pattern);
        
        if (self._ccore_network_pointer is not None):
            return wrapper.syncpr_memory_order(self._ccore_network_pointer, pattern);
        
        else:
            return self.__calculate_memory_order(pattern);

    
    def __calculate_memory_order(self, pattern):
        """!
        @brief Calculates function of the memorized pattern without any pattern validation.
        
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        
        @return (double) Order of memory for the specified pattern.
                
        """
        
        memory_order = 0.0;
        for index in range(len(self)):
            memory_order += pattern[index] * cmath.exp( 1j * self._phases[index] );
        
        memory_order /= len(self);
        return abs(memory_order);
        
    
    def _phase_kuramoto(self, teta, t, argv):
        """!
        @brief Returns result of phase calculation for specified oscillator in the network.
        
        @param[in] teta (double): Phase of the oscillator that is differentiated.
        @param[in] t (double): Current time of simulation.
        @param[in] argv (tuple): Index of the oscillator in the list.
        
        @return (double) New phase for specified oscillator (don't assign it here).
        
        """
        
        index = argv;
        
        phase = 0.0;
        term = 0.0;
        
        for k in range(0, self._num_osc):
            if (k != index):
                phase_delta = self._phases[k] - teta;
                
                phase += self._coupling[index][k] * math.sin(phase_delta);
                
                term1 = self._increase_strength1 * math.sin(2.0 * phase_delta);
                term2 = self._increase_strength2 * math.sin(3.0 * phase_delta);
                
                term += (term1 - term2);
                
        return ( phase + term / len(self) );
    
    
    def __validate_pattern(self, pattern):
        """!
        @brief Validates pattern.
        @details Throws exception if length of pattern is not equal to size of the network or if it consists feature with value that are not equal to [-1; 1].
        
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        
        """
        if (len(pattern) != len(self)):
            raise NameError('syncpr: length of the pattern (' + len(pattern) + ') should be equal to size of the network');
        
        for feature in pattern:
            if ( (feature != -1.0) and (feature != 1.0) ):
                raise NameError('syncpr: patten feature (' + feature + ') should be distributed in [-1; 1]');