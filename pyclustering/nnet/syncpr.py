"""!

@brief Phase oscillatory network for patten recognition based on modified Kuramoto model.
@details Based on article description:
         - R.Follmann, E.E.N.Macau, E.Rosa, Jr., J.R.C.Piqueira. Phase Oscillatory Network and Visual Pattern Recognition. 2014.
         
@authors Andrei Novikov (pyclustering@yandex.ru)
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

from pyclustering.nnet          import solve_type, initial_type, conn_type;
from pyclustering.nnet.sync     import sync_network, sync_dynamic, sync_visualizer;
from pyclustering.utils         import draw_dynamics;

from PIL import Image;

import matplotlib.pyplot as plt;

import math;
import numpy;


class syncpr_dynamic(sync_dynamic):
    """!
    @brief Represents output dynamic of syncpr (Sync for Pattern Recognition).
    
    """
    
    def __init__(self, phase, time):
        """!
        @brief Constructor of syncpr dynamic.
        
        @param[in] phase (list): Dynamic of oscillators on each step of simulation. If ccore pointer is specified than it can be ignored.
        @param[in] time (list): Simulation time.
        
        """     
        super().__init__(phase, time, None);
        
        
    def __len__(self):
        """!
        @brief (uint) Returns number of simulation steps that are stored in dynamic.
        
        """
        
        return len(self._dynamic);        


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
            
        image_size = image_height * image_width;
        
        number_cols = int(numpy.ceil(number_pictures ** 0.5));
        number_rows = int(numpy.ceil(number_pictures / number_cols));
        
        real_index = 0, 0;
        double_indexer = True;
        if ( (number_cols == 1) or (number_rows == 1) ):
            real_index = 0;
            double_indexer = False;
        
        (fig, axarr) = plt.subplots(number_rows, number_cols);
        
        if (number_pictures > 1):
            plt.setp([ax for ax in axarr], visible = False);
            
        iteration_display = 0.0;
        for iteration in range(len(syncpr_output_dynamic)):
            if (iteration >= iteration_display):
                iteration_display += iteration_math_step;
                
                current_dynamic = syncpr_output_dynamic.output[iteration];
                stage_picture = [(255, 255, 255)] * image_size;
                for index_phase in range(len(current_dynamic)):
                    phase = current_dynamic[index_phase];
                    
                    pixel_color = math.floor( phase * (255 / (2 * math.pi)) );
                    stage_picture[index_phase] = (pixel_color, pixel_color, pixel_color);
                  
                stage = numpy.array(stage_picture, numpy.uint8);
                stage = numpy.reshape(stage, (image_height, image_width) + ((3),)); # ((3),) it's size of RGB - third dimension.
                
                image_cluster = Image.fromarray(stage, 'RGB');
                
                ax_handle = axarr;
                if (number_pictures > 1):
                    ax_handle = axarr[real_index];
                    
                ax_handle.imshow(image_cluster, interpolation = 'none');
                plt.setp(ax_handle, visible = True);
                
                ax_handle.xaxis.set_ticklabels([]);
                ax_handle.yaxis.set_ticklabels([]);
                ax_handle.xaxis.set_ticks_position('none');
                ax_handle.yaxis.set_ticks_position('none');
                
                if (double_indexer is True):
                    real_index = real_index[0], real_index[1] + 1;
                    if (real_index[1] >= number_cols):
                        real_index = real_index[0] + 1, 0; 
                else:
                    real_index += 1;
    
        plt.show();


class syncpr(sync_network):
    """!
    @brief Model of phase oscillatory network for pattern recognition that is based on the Kuramoto model.
    @details The model uses second-order and third-order modes of the Fourier components.
    
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
    
    _increase_strength1 = 0.0;
    _increase_strength2 = 0.0;
    _coupling = None;
    
    def __init__(self, num_osc, increase_strength1, increase_strength2):
        """!
        @brief Constructor of oscillatory network for pattern recognition based on Kuramoto model.
        
        @param[in] num_osc (uint): Number of oscillators in the network.
        @param[in] increase_strength1 (double): Parameter for increasing strength of the second term of the Fourier component.
        @param[in] increase_strength2 (double): Parameter for increasing strength of the third term of the Fourier component.
        
        """
        self._increase_strength1 = increase_strength1;
        self._increase_strength2 = increase_strength2;
        self._coupling = [ [0.0 for i in range(num_osc)] for j in range(num_osc) ];
    
        super().__init__(num_osc, 1, 0, conn_type.NONE, initial_type.RANDOM_GAUSSIAN);
        
        
    def train(self, samples):
        """!
        @brief Trains syncpr network using Hebbian rule for adjusting strength of connections between oscillators during training.
        
        @param[in] samples (list): list of patterns where each pattern is represented by list of features that are equal to [-1; 1].
        
        """
        
        length = float(len(self));
        
        for i in range(0, len(self), 1):
            for j in range(i + 1, len(self), 1):
                
                # go through via all patterns
                for p in range(len(samples)):
                    self.__validate_pattern(samples[p]);
                    
                    value1 = samples[p][i];
                    value2 = samples[p][j];
                    
                    self._coupling[i][j] += value1 * value2;
                
                self._coupling[i][j] /= length;
                self._coupling[j][i] = self._coupling[i][j];
    
    
    def simulate(self, steps, time, pattern, solution = solve_type.FAST, collect_dynamic = True):
        """!
        @brief Performs static simulation of syncpr oscillatory network.
        
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
        
        self.__validate_pattern(pattern);
        
        for i in range(0, len(pattern), 1):
            if (pattern[i] > 0.0):
                self._phases[i] = 0.0;
            else:
                self._phases[i] = math.pi / 2.0;
                    
        return self.simulate_static(steps, time, solution, collect_dynamic);
    
    
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
                
        return ( phase + (1.0 / len(self)) * term );
    
    
    def __validate_pattern(self, pattern):
        """!
        @brief Validates pattern.
        @details Throws exception if length of pattern is not equal to size of the network or if it consists feature with value that are not equal to [-1; 1]
        
        @param[in] pattern (list): Pattern for recognition represented by list of features that are equal to [-1; 1].
        
        """
        if (len(pattern) != len(self)):
            raise NameError('syncpr: length of the pattern (' + len(pattern) + ') should be equal to size of the network');
        
        for feature in pattern:
            if ( (feature != -1.0) and (feature != 1.0) ):
                raise NameError('syncpr: patten feature (' + feature + ') should be distributed in [-1; 1]');