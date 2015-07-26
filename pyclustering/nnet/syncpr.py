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
    _energy = None;
    
    @property
    def energy(self):
        return self._energy;
    
    def __init__(self, phase, energy, time):
        self._energy = energy;
        
        super().__init__(phase, time, None);


class syncpr_visualizer(sync_visualizer):
    @staticmethod
    def show_energy(syncpr_output_dynamic):
        if (syncpr_output_dynamic.energy is None):
            return;
        
        draw_dynamics(syncpr_output_dynamic.time, syncpr_output_dynamic.energy, x_title = "t", y_title = "L");
    
    
    @staticmethod
    def show_pattern(syncpr_output_dynamic, image_height, image_width):
        number_pictures = len(syncpr_output_dynamic);
        iteration_math_step = 1.0;
        if (number_pictures > 50):
            iteration_math_step = math.ceil(number_pictures / 50.0);
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
        plt.setp([ax for ax in axarr], visible = False);
        
        axarr[real_index].xaxis.set_ticklabels([]);
        axarr[real_index].yaxis.set_ticklabels([]);
        axarr[real_index].xaxis.set_ticks_position('none');
        axarr[real_index].yaxis.set_ticks_position('none');
                
        if (double_indexer is True):
            real_index = 0, 1;
        else:
            real_index += 1;
        
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
                
                axarr[real_index].imshow(image_cluster, interpolation = 'none');
                plt.setp(axarr[real_index], visible = True);
                
                axarr[real_index].xaxis.set_ticklabels([]);
                axarr[real_index].yaxis.set_ticklabels([]);
                    
                axarr[real_index].xaxis.set_ticks_position('none');
                axarr[real_index].yaxis.set_ticks_position('none');
                
                if (double_indexer is True):
                    real_index = real_index[0], real_index[1] + 1;
                    if (real_index[1] >= number_cols):
                        real_index = real_index[0] + 1, 0; 
                else:
                    real_index += 1;
    
        plt.show();


class syncpr(sync_network):
    _increase_strength1 = 0.0;
    _increase_strength2 = 0.0;
    _coupling = None;
    
    def __init__(self, num_osc, increase_strength1, increase_strength2):
        self._increase_strength1 = increase_strength1;
        self._increase_strength2 = increase_strength2;
        self._coupling = [ [0.0 for i in range(num_osc)] for j in range(num_osc) ];
    
        super().__init__(num_osc, 1, 0, conn_type.NONE, initial_type.RANDOM_GAUSSIAN);
        
        
    def train(self, samples):
        length = float(len(self));
        
        for i in range(0, len(self), 1):
            for j in range(i + 1, len(self), 1):
                
                # go through via all patterns
                for p in range(len(samples)):
                    value1 = 1.0;
                    if (samples[p][i] > 0.0):
                        value1 = -1.0;
                    
                    value2 = 1.0;
                    if (samples[p][j] > 0.0):
                        value2 = -1.0;
                    
                    self._coupling[i][j] += value1 * value2;
                
                self._coupling[i][j] /= length;
                self._coupling[j][i] = self._coupling[i][j];
    
    
    def simulate(self, steps, time, pattern, solution = solve_type.FAST, collect_dynamic = True):
        for i in range(0, len(pattern), 1):
            if (pattern[i] > 0.0):
                self._phases[i] = 0.0;
            else:
                self._phases[i] = math.pi / 2.0;
                    
        return self.simulate_static(steps, time, solution, collect_dynamic);
    
    
    def simulate_static(self, steps, time, solution = solve_type.FAST, collect_dynamic = False):
        dyn_phase = None;
        dyn_time = None;
        dyn_energy = None;
        
        if (collect_dynamic == True):
            dyn_phase = [];
            dyn_time = [];
            dyn_energy = [];
            
            dyn_phase.append(self._phases);
            dyn_time.append(0);
            dyn_energy.append( self.__calculate_energy(self._phases) );
        
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._phases = self._calculate_phases(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_phase.append(self._phases);
                dyn_time.append(t);
                # dyn_energy.append( self.__calculate_energy(self._phases) );
            else:
                dyn_phase = [ self._phases ];
                dyn_time = t;
                # dyn_energy = [ self.__calculate_energy(self._phases) ];
        
        output_sync_dynamic = syncpr_dynamic(dyn_phase, None, dyn_time);
        return output_sync_dynamic;     
    
    
    def __calculate_energy(self, phases):
        energy = [0.0] * len(self);
        length = float(len(self));
        
        for i in range(len(self)):
            energy_oscillator = 0.0;
            term_oscillator = 0.0;
            
            for j in range(len(self)):
                phase_delta = phases[j] - phases[i];
                
                term1 = 3.0 * self._increase_strength1 * math.cos(2.0 * phase_delta);
                term2 = 2.0 * self._increase_strength2 * math.cos(3.0 * phase_delta);
                
                term_oscillator += (term1 - term2);
                energy_oscillator += self._coupling[i][j] * math.cos(phase_delta);
            
            energy[i] = -0.5 * energy_oscillator - ( 0.08333 / length ) * term_oscillator;
        
        return energy;
    
    
    def _phase_kuramoto(self, teta, t, argv):
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