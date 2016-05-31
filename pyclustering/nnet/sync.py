"""!

@brief Neural Network: Oscillatory Neural Network based on Kuramoto model
@details Based on article description:
         - A.Arenas, Y.Moreno, C.Zhou. Synchronization in complex networks. 2008.
         - X.B.Lu. Adaptive Cluster Synchronization in Coupled Phase Oscillators. 2009.
         - X.Lou. Adaptive Synchronizability of Coupled Oscillators With Switching. 2012.
         - A.Novikov, E.Benderskaya. Oscillatory Neural Networks Based on the Kuramoto Model. 2014.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

import matplotlib.pyplot as plt;
import matplotlib.animation as animation;

import numpy;
import random;

import pyclustering.core.sync_wrapper as wrapper;

from scipy import pi;
from scipy.integrate import odeint;

from pyclustering.nnet import *;

from pyclustering.utils import draw_dynamics, draw_dynamics_set;


class sync_dynamic:
    """!
    @brief Represents output dynamic of Sync.
    
    """
    
    @property
    def output(self):
        """!
        @brief (list) Returns outputs of oscillator during simulation.
        
        """
        if (self._ccore_sync_dynamic_pointer is not None):
            return wrapper.sync_dynamic_get_output(self._ccore_sync_dynamic_pointer);
        
        return self._dynamic;
    
    
    @property
    def time(self):
        """!
        @brief (list) Returns sampling times when dynamic is measured during simulation.
        
        """
        if (self._ccore_sync_dynamic_pointer is not None):
            return wrapper.sync_dynamic_get_time(self._ccore_sync_dynamic_pointer);
        
        return self._time;
    
    
    def __init__(self, phase, time, ccore = None):
        """!
        @brief Constructor of Sync dynamic.
        
        @param[in] phase (list): Dynamic of oscillators on each step of simulation. If ccore pointer is specified than it can be ignored.
        @param[in] time (list): Simulation time.
        @param[in] ccore (ctypes.pointer): Pointer to CCORE sync_dynamic instance in memory.
        
        """
        
        self._dynamic = phase;
        self._time = time;
        self._ccore_sync_dynamic_pointer = ccore;
    
    
    def __del__(self):
        """!
        @brief Default destructor of Sync dynamic.
        
        """
        if (self._ccore_sync_dynamic_pointer is not None):
            wrapper.sync_dynamic_destroy(self._ccore_sync_dynamic_pointer);
    
    
    def __len__(self):
        """!
        @brief (uint) Returns number of simulation steps that are stored in dynamic.
        
        """
        if (self._ccore_sync_dynamic_pointer is not None):
            return wrapper.sync_dynamic_get_size(self._ccore_sync_dynamic_pointer);
        
        return len(self._dynamic);
    
    
    def __getitem__(self, index):
        """!
        @brief Indexing of the dynamic.
        
        """
        if (index is 0):
            return self.time;
        
        elif (index is 1):
            return self.output;
        
        else:
            raise NameError('Out of range ' + index + ': only indexes 0 and 1 are supported.');


    def allocate_sync_ensembles(self, tolerance = 0.01, indexes = None, iteration = None):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster.
               
        @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
        @param[in] indexes (list): List of real object indexes and it should be equal to amount of oscillators (in case of 'None' - indexes are in range [0; amount_oscillators]).
        @param[in] iteration (uint): Iteration of simulation that should be used for allocation.
        
        @return (list) Grours (lists) of indexes of synchronous oscillators.
                For example [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
        
        """
        
        if (self._ccore_sync_dynamic_pointer is not None):
            ensembles = wrapper.sync_dynamic_allocate_sync_ensembles(self._ccore_sync_dynamic_pointer, tolerance, iteration);
            
            if (indexes is not None):
                for ensemble in ensembles:
                    for index in range(len(ensemble)):
                        ensemble[index] = indexes[ ensemble[index] ];
                
            return ensembles;
        
        if ( (self._dynamic is None) or (len(self._dynamic) == 0) ):
            return [];
        
        number_oscillators = len(self._dynamic[0]);
        last_state = None;
        
        if (iteration is None):
            last_state = self._dynamic[len(self._dynamic) - 1];
        else:
            last_state = self._dynamic[iteration];
        
        clusters = [];
        if (number_oscillators > 0):
            clusters.append([0]);
        
        for i in range(1, number_oscillators, 1):
            cluster_allocated = False;
            for cluster in clusters:
                for neuron_index in cluster:
                    last_state_shifted = abs(last_state[i] - 2 * pi);
                    
                    if ( ( (last_state[i] < (last_state[neuron_index] + tolerance)) and (last_state[i] > (last_state[neuron_index] - tolerance)) ) or
                         ( (last_state_shifted < (last_state[neuron_index] + tolerance)) and (last_state_shifted > (last_state[neuron_index] - tolerance)) ) ):
                        cluster_allocated = True;
                        
                        real_index = i;
                        if (indexes is not None):
                            real_index = indexes[i];
                        
                        cluster.append(real_index);
                        break;
                
                if (cluster_allocated == True):
                    break;
            
            if (cluster_allocated == False):
                clusters.append([i]);
        
        return clusters;
    
    
    def allocate_correlation_matrix(self, iteration = None):
        """!
        @brief Allocate correlation matrix between oscillators at the specified step of simulation.
               
        @param[in] iteration (uint): Number of iteration of simulation for which correlation matrix should be allocated.
                                      If iternation number is not specified, the last step of simulation is used for the matrix allocation.
        
        @return (list) Correlation matrix between oscillators with size [number_oscillators x number_oscillators].
        
        """
        
        if (self._ccore_sync_dynamic_pointer is not None):
            return wrapper.sync_dynamic_allocate_correlation_matrix(self._ccore_sync_dynamic_pointer, iteration);
        
        if ( (self._dynamic is None) or (len(self._dynamic) == 0) ):
            return [];
        
        dynamic = self._dynamic;
        current_dynamic = dynamic[len(dynamic) - 1];
        
        if (iteration is not None):
            current_dynamic = dynamic[iteration];
        
        number_oscillators = len(dynamic[0]);
        affinity_matrix = [ [ 0.0 for i in range(number_oscillators) ] for j in range(number_oscillators) ];  
        
        for i in range(number_oscillators):
            for j in range(number_oscillators):
                phase1 = current_dynamic[i];
                phase2 = current_dynamic[j];
                
                affinity_matrix[i][j] = abs(math.sin(phase1 - phase2));
                
        return affinity_matrix;


class sync_visualizer:
    """!
    @brief Visualizer of output dynamic of sync network (Sync).
    
    """
        
    @staticmethod
    def show_output_dynamic(sync_output_dynamic):
        """!
        @brief Shows output dynamic (output of each oscillator) during simulation.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        
        @see show_output_dynamics
        
        """
        
        draw_dynamics(sync_output_dynamic.time, sync_output_dynamic.output, x_title = "t", y_title = "phase", y_lim = [0, 2 * 3.14]);
    
    
    @staticmethod
    def show_output_dynamics(sync_output_dynamics):
        """!
        @brief Shows several output dynamics (output of each oscillator) during simulation.
        @details Each dynamic is presented on separate plot.
        
        @param[in] sync_output_dynamics (list): list of output dynamics 'sync_dynamic' of the Sync network.
        
        @see show_output_dynamic
        
        """
        
        draw_dynamics_set(sync_output_dynamics, "t", "phase", None, [0, 2 * 3.14], False, False);
    
    
    @staticmethod
    def show_correlation_matrix(sync_output_dynamic, iteration = None):
        """!
        @brief Shows correlation matrix between oscillators at the specified iteration.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] iteration (uint): Number of interation of simulation for which correlation matrix should be allocated.
                                      If iternation number is not specified, the last step of simulation is used for the matrix allocation.
        
        """
        
        _ = plt.figure();
        correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(iteration);
        
        plt.imshow(correlation_matrix, cmap = plt.get_cmap('cool'), interpolation='kaiser'); 
        plt.show();
        
    
    
    @staticmethod
    def animate_output_dynamic(sync_output_dynamic, animation_velocity = 75, save_movie = None):
        """!
        @brief Shows animation of output dynamic (output of each oscillator) during simulation on a circle from [0; 2pi].
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds.
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        figure = plt.figure();
        
        dynamic = sync_output_dynamic.output[0];
        artist, = plt.polar(dynamic, [1.0] * len(dynamic), 'o', color = 'blue');
        
        def init_frame():
            return [ artist ];
        
        def frame_generation(index_dynamic):
            dynamic = sync_output_dynamic.output[index_dynamic];
            artist.set_data(dynamic, [1.0] * len(dynamic));
            
            return [ artist ];
        
        phase_animation = animation.FuncAnimation(figure, frame_generation, len(sync_output_dynamic), interval = animation_velocity, init_func = init_frame, repeat_delay = 5000);

        if (save_movie is not None):
            phase_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();


    @staticmethod
    def animate_correlation_matrix(sync_output_dynamic, animation_velocity = 75, colormap = 'cool', save_movie = None):
        """!
        @brief Shows animation of correlation matrix between oscillators during simulation.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds.
        @param[in] colormap (string): Name of colormap that is used by matplotlib ('gray', 'pink', 'cool', spring', etc.).
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        figure = plt.figure();
        
        correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(0);
        artist = plt.imshow(correlation_matrix, cmap = plt.get_cmap(colormap), interpolation='kaiser', hold = True);
        
        def init_frame(): 
            return [ artist ];
        
        def frame_generation(index_dynamic):
            correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(index_dynamic);
            artist.set_data(correlation_matrix);
            
            return [ artist ];

        correlation_animation = animation.FuncAnimation(figure, frame_generation, len(sync_output_dynamic), init_func = init_frame, interval = animation_velocity , repeat_delay = 1000, blit = True);
        
        if (save_movie is not None):
            correlation_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();


    @staticmethod
    def animate(sync_output_dynamic, title = None, save_movie = None):
        """!
        @brief Shows animation of phase coordinates and animation of correlation matrix together for the Sync dynamic output on the same figure.
        
        @param[in] sync_output_dynamic (sync_dynamic): Output dynamic of the Sync network.
        @param[in] title (string): Title of the animation that is displayed on a figure if it is specified.
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        dynamic = sync_output_dynamic.output[0];
        correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(0);
        
        figure = plt.figure(1);
        if (title is not None):
            figure.suptitle(title, fontsize = 26, fontweight = 'bold')
        
        ax1 = figure.add_subplot(121, projection='polar');
        ax2 = figure.add_subplot(122);
        
        artist1, = ax1.plot(dynamic, [1.0] * len(dynamic), marker = 'o', color = 'blue', ls = '');
        artist2 = ax2.imshow(correlation_matrix, cmap = plt.get_cmap('Accent'), interpolation='kaiser');
        
        def init_frame():
            return [ artist1, artist2 ];

        def frame_generation(index_dynamic):
            dynamic = sync_output_dynamic.output[index_dynamic];
            artist1.set_data(dynamic, [1.0] * len(dynamic));
            
            correlation_matrix = sync_output_dynamic.allocate_correlation_matrix(index_dynamic);
            artist2.set_data(correlation_matrix);
            
            return [ artist1, artist2 ];
        
        dynamic_animation = animation.FuncAnimation(figure, frame_generation, len(sync_output_dynamic), interval = 75, init_func = init_frame, repeat_delay = 5000);
        
        if (save_movie is not None):
            dynamic_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();


class sync_network(network):
    """!
    @brief Model of oscillatory network that is based on the Kuramoto model of synchronization.
    
    """

    def __init__(self, num_osc, weight = 1, frequency = 0, type_conn = conn_type.ALL_TO_ALL, representation = conn_represent.MATRIX, initial_phases = initial_type.RANDOM_GAUSSIAN, ccore = False):
        """!
        @brief Constructor of oscillatory network is based on Kuramoto model.
        
        @param[in] num_osc (uint): Number of oscillators in the network.
        @param[in] weight (double): Coupling strength of the links between oscillators.
        @param[in] frequency (double): Multiplier of internal frequency of the oscillators.
        @param[in] type_conn (conn_type): Type of connection between oscillators in the network (all-to-all, grid, bidirectional list, etc.).
        @param[in] representation (conn_represent): Internal representation of connection in the network: matrix or list.
        @param[in] initial_phases (initial_type): Type of initialization of initial phases of oscillators (random, uniformly distributed, etc.).
        @param[in] ccore (bool): If True simulation is performed by CCORE library (C++ implementation of pyclustering).
        
        """
        
        self._ccore_network_pointer = None;      # Pointer to CCORE Sync implementation of the network.
        
        if (ccore is True):
            self._ccore_network_pointer = wrapper.sync_create_network(num_osc, weight, frequency, type_conn, initial_phases);
        else:   
            super().__init__(num_osc, type_conn, representation);
            
            self._weight = weight;
            
            self._phases = list();
            self._freq = list();
            
            random.seed();
            for index in range(0, num_osc, 1):
                if (initial_phases == initial_type.RANDOM_GAUSSIAN):
                    self._phases.append(random.random() * pi);
                
                elif (initial_phases == initial_type.EQUIPARTITION):
                    self._phases.append( pi / num_osc * index);
                
                self._freq.append(random.random() * frequency);


    def __del__(self):
        """!
        @brief Destructor of oscillatory network is based on Kuramoto model.
        
        """
        
        if (self._ccore_network_pointer is not None):
            wrapper.sync_destroy_network(self._ccore_network_pointer);
            self._ccore_network_pointer = None;
    
    
    def sync_order(self):
        """!
        @brief Calculates level of global synchorization in the network.
        
        @return (double) Level of global synchronization.
        
        @see sync_local_order()
        
        """
        
        if (self._ccore_network_pointer is not None):
            return wrapper.sync_order(self._ccore_network_pointer);
        
        exp_amount = 0;
        average_phase = 0;
        
        for index in range(0, self._num_osc, 1):
            exp_amount += math.expm1( abs(1j * self._phases[index]) );
            average_phase += self._phases[index];
        
        exp_amount /= self._num_osc;
        average_phase = math.expm1( abs(1j * (average_phase / self._num_osc)) );
        
        return abs(average_phase) / abs(exp_amount);    
    
    
    def sync_local_order(self):
        """!
        @brief Calculates level of local (partial) synchronization in the network.
        
        @return (double) Level of local (partial) synchronization.
        
        @see sync_order()
        
        """
        
        if (self._ccore_network_pointer is not None):
            return wrapper.sync_local_order(self._ccore_network_pointer);
        
        exp_amount = 0.0;
        num_neigh = 0;
        
        for i in range(0, self._num_osc, 1):
            for j in range(0, self._num_osc, 1):
                if (self.has_connection(i, j) == True):
                    exp_amount += math.exp(-abs(self._phases[j] - self._phases[i]));
                    num_neigh += 1;
        
        if (num_neigh == 0):
            num_neigh = 1;
        
        return exp_amount / num_neigh;
    
    
    def _phase_kuramoto(self, teta, t, argv):
        """!
        @brief Returns result of phase calculation for specified oscillator in the network.
        
        @param[in] teta (double): Phase of the oscillator that is differentiated.
        @param[in] t (double): Current time of simulation.
        @param[in] argv (tuple): Index of the oscillator in the list.
        
        @return (double) New phase for specified oscillator (don't assign here).
        
        """
        
        index = argv;
        phase = 0;
        for k in range(0, self._num_osc):
            if (self.has_connection(index, k) == True):
                phase += math.sin(self._phases[k] - teta);
            
        return ( self._freq[index] + (phase * self._weight / self._num_osc) );
        
    
    def simulate(self, steps, time, solution = solve_type.FAST, collect_dynamic = True):
        """!
        @brief Performs static simulation of Sync oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solution (solving).
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see simulate_dynamic()
        @see simulate_static()
        
        """
        
        return self.simulate_static(steps, time, solution, collect_dynamic);


    def simulate_dynamic(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False, step = 0.1, int_step = 0.01, threshold_changes = 0.0000001):
        """!
        @brief Performs dynamic simulation of the network until stop condition is not reached. Stop condition is defined by input argument 'order'.
        
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
        
        if (self._ccore_network_pointer is not None):
            ccore_instance_dynamic = wrapper.sync_simulate_dynamic(self._ccore_network_pointer, order, solution, collect_dynamic, step, int_step, threshold_changes);
            return sync_dynamic(None, None, ccore_instance_dynamic);
        
        # For statistics and integration
        time_counter = 0;
        
        # Prevent infinite loop. It's possible when required state cannot be reached.
        previous_order = 0;
        current_order = self.sync_local_order();
        
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
            current_order = self.sync_local_order();
            
            # hang prevention
            if (abs(current_order - previous_order) < threshold_changes):
                # print("Warning: sync_network::simulate_dynamic - simulation is aborted due to low level of convergence rate (order = " + str(current_order) + ").");
                break;
            
        if (collect_dynamic != True):
            dyn_phase.append(self._phases);
            dyn_time.append(time_counter);

        output_sync_dynamic = sync_dynamic(dyn_phase, dyn_time, None);
        return output_sync_dynamic;


    def simulate_static(self, steps, time, solution = solve_type.FAST, collect_dynamic = False):
        """!
        @brief Performs static simulation of oscillatory network.
        
        @param[in] steps (uint): Number steps of simulations during simulation.
        @param[in] time (double): Time of simulation.
        @param[in] solution (solve_type): Type of solution.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see simulate()
        @see simulate_dynamic()
        
        """
        
        if (self._ccore_network_pointer is not None):
            ccore_instance_dynamic = wrapper.sync_simulate_static(self._ccore_network_pointer, steps, time, solution, collect_dynamic);
            return sync_dynamic(None, None, ccore_instance_dynamic);
        
        dyn_phase = [];
        dyn_time = [];
        
        if (collect_dynamic == True):
            dyn_phase.append(self._phases);
            dyn_time.append(0);
        
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            # update states of oscillators
            self._phases = self._calculate_phases(solution, t, step, int_step);
            
            # update states of oscillators
            if (collect_dynamic == True):
                dyn_phase.append(self._phases);
                dyn_time.append(t);
        
        if (collect_dynamic != True):
            dyn_phase.append(self._phases);
            dyn_time.append(time);
                        
        output_sync_dynamic = sync_dynamic(dyn_phase, dyn_time);
        return output_sync_dynamic;     


    def _calculate_phases(self, solution, t, step, int_step):
        """!
        @brief Calculates new phases for oscillators in the network in line with current step.
        
        @param[in] solution (solve_type): Type solver of the differential equation.
        @param[in] t (double): Time of simulation.
        @param[in] step (double): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Step differentiation that is used for solving differential equation.
        
        @return (list) New states (phases) for oscillators.
        
        """
        
        next_phases = [0] * self._num_osc;    # new oscillator _phases
        
        for index in range (0, self._num_osc, 1):
            if (solution == solve_type.FAST):
                result = self._phases[index] + self._phase_kuramoto(self._phases[index], 0, index);
                next_phases[index] = self._phase_normalization(result);
                
            elif (solution == solve_type.RK4):
                result = odeint(self._phase_kuramoto, self._phases[index], numpy.arange(t - step, t, int_step), (index , ));
                next_phases[index] = self._phase_normalization(result[len(result) - 1][0]);
            
            else:
                raise NameError("Solver '" + solution + "' is not supported");
        
        return next_phases;
        

    def _phase_normalization(self, teta):
        """!
        @brief Normalization of phase of oscillator that should be placed between [0; 2 * pi].
        
        @param[in] teta (double): phase of oscillator.
        
        @return (double) Normalized phase.
        
        """
        
        norm_teta = teta;
        while (norm_teta > (2.0 * pi)) or (norm_teta < 0):
            if (norm_teta > (2.0 * pi)):
                norm_teta -= 2.0 * pi;
            else:
                norm_teta += 2.0 * pi;
        
        return norm_teta;
