"""!

@brief Examples of usage and demonstration of abilities of Local Excitatory Global Inhibitory Oscillatory Network (LEGION).

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

from pyclustering.utils import draw_dynamics;

from pyclustering.nnet.legion import legion_network, legion_parameters;
from pyclustering.nnet import *;

def template_dynamic_legion(num_osc, steps, time, conn_type, stimulus, params = None, separate_repr = True, ccore_flag = True):
    net = legion_network(num_osc, params, conn_type, ccore = ccore_flag);
    print("Created");
    
    dynamic = net.simulate(steps, time, stimulus, solution = solve_type.RK4);
    print("Simulated");
    
    draw_dynamics(dynamic.time, dynamic.output, x_title = "Time", y_title = "x(t)", separate = separate_repr);
    draw_dynamics(dynamic.time, dynamic.inhibitor, x_title = "Time", y_title = "z(t)");
    
    ensembles = dynamic.allocate_sync_ensembles(0.1);
    print(ensembles);
    
    
def one_oscillator_unstimulated():
    parameters = legion_parameters();
    parameters.teta = 0;    # because no neighbors at all
    
    template_dynamic_legion(1, 2000, 500, conn_type.NONE, [0], parameters);

def one_oscillator_stimulated():
    parameters = legion_parameters();
    parameters.teta = 0;    # because no neighbors at all
    
    template_dynamic_legion(1, 2000, 500, conn_type.NONE, [1], parameters);
    
def three_oscillator_unstimulated_list():
    parameters = legion_parameters();
    parameters.teta = 0;    # because no stmulated neighbors
    
    template_dynamic_legion(3, 2000, 200, conn_type.LIST_BIDIR, [0, 0, 0], parameters);
    
def three_oscillator_stimulated_list():
    template_dynamic_legion(3, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1]);
    
def three_oscillator_mix_stimulated_list():
    parameters = legion_parameters();
    parameters.Wt = 4.0;
    template_dynamic_legion(3, 1200, 1200, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 0, 1], params = parameters);
    
def ten_oscillator_stimulated_list():
    template_dynamic_legion(10, 1000, 750, conn_type = conn_type.LIST_BIDIR, stimulus = [1] * 10);
    
def ten_oscillator_mix_stimulated_list():
    template_dynamic_legion(10, 1500, 1500, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1, 0, 0, 0, 1, 1, 0, 0], separate_repr = [ [0, 1, 2], [3, 4, 5, 8, 9], [6, 7] ]);
    
def thirteen_oscillator_three_stimulated_ensembles_list():
    "Good example of three synchronous ensembels"
    "Not accurate due to false skipes are observed"
    parameters = legion_parameters();
    parameters.Wt = 4.0;
    parameters.fi = 10.0;
    template_dynamic_legion(15, 1000, 1000, conn_type = conn_type.LIST_BIDIR, stimulus = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1], params = parameters, separate_repr = [ [0, 1, 2], [3, 4, 5, 9, 10], [6, 7, 8], [11, 12, 13, 14] ]);
    

def thirteen_simplify_oscillator_three_stimulated_ensembles_list():
    "Good example of three synchronous ensembels"
    "Not accurate due to false skipes are observed"
    parameters = legion_parameters();
    parameters.Wt = 4.0;
    parameters.fi = 0.8;
    parameters.ENABLE_POTENTIONAL = False;
    template_dynamic_legion(15, 1000, 1000, conn_type = conn_type.LIST_BIDIR, 
                            stimulus = [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1], 
                            params = parameters, 
                            separate_repr = [ [0, 1, 2], [3, 4, 5, 9, 10], [6, 7, 8], [11, 12, 13, 14] ]);
    

def sixteen_oscillator_two_stimulated_ensembles_grid():
    "Not accurate false due to spikes are observed"
    parameters = legion_parameters();
    parameters.teta_x = -1.1;
    template_dynamic_legion(16, 2000, 1500, conn_type = conn_type.GRID_FOUR, params = parameters, stimulus = [1, 1, 1, 0, 
                                                                                                              1, 1, 1, 0, 
                                                                                                              0, 0, 0, 1, 
                                                                                                              0, 0, 1, 1]);
                                                                                                              

def simple_segmentation_example():
    "Perfect results!"
    parameters = legion_parameters();
    parameters.eps = 0.02;
    parameters.alpha = 0.005;
    parameters.betta = 0.1;
    parameters.gamma = 7.0;
    parameters.teta = 0.9;
    parameters.lamda = 0.1;
    parameters.teta_x = -0.5;
    parameters.teta_p = 7.0;
    parameters.Wz = 0.7;
    parameters.mu = 0.01;
    parameters.fi = 3.0;
    parameters.teta_xz = 0.1;
    parameters.teta_zx = 0.1;
    
    parameters.ENABLE_POTENTIONAL = False;
    template_dynamic_legion(81, 2500, 2500, 
                            conn_type = conn_type.GRID_FOUR, 
                            params = parameters, 
                            stimulus = [1, 1, 1, 0, 0, 0, 0, 0, 0, 
                                        1, 1, 1, 0, 0, 1, 1, 1, 1, 
                                        1, 1, 1, 0, 0, 1, 1, 1, 1, 
                                        0, 0, 0, 0, 0, 0, 1, 1, 1,
                                        0, 0, 0, 0, 0, 0, 1, 1, 1,
                                        1, 1, 1, 1, 0, 0, 1, 1, 1,
                                        1, 1, 1, 1, 0, 0, 0, 0, 0,
                                        1, 1, 1, 1, 0, 0, 0, 0, 0,
                                        1, 1, 1, 1, 0, 0, 0, 0, 0],
                            separate_repr = [ [0, 1, 2, 9, 10, 11, 18, 19, 20], 
                                              [14, 15, 16, 17, 23, 24, 25, 26, 33, 34, 35, 42, 43, 44, 51, 52, 53], 
                                              [45, 46, 47, 48, 54, 55, 56, 57, 63, 64, 65, 66, 72, 73, 74, 75] ]);

    
one_oscillator_unstimulated();
one_oscillator_stimulated();
three_oscillator_unstimulated_list();
three_oscillator_stimulated_list();
three_oscillator_mix_stimulated_list();
ten_oscillator_stimulated_list();
ten_oscillator_mix_stimulated_list();
thirteen_oscillator_three_stimulated_ensembles_list();
thirteen_simplify_oscillator_three_stimulated_ensembles_list();
sixteen_oscillator_two_stimulated_ensembles_grid();
simple_segmentation_example();