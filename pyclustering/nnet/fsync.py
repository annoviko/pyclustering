"""!

@brief Oscillatory Neural Network based on Kuramoto model in frequency domain.
@details Implementation based on paper @cite book::chemical_oscillatorions_waves.

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
import pyclustering.utils

from scipy.integrate import odeint

from pyclustering.nnet import network, conn_type, conn_represent


class fsync_dynamic:
    """!
    @brief Represents output dynamic of Sync in frequency domain.
    
    """


    def __init__(self, amplitude, time):
        """!
        @brief Constructor of Sync dynamic in frequency domain.
        
        @param[in] amplitude (list): Dynamic of oscillators on each step of simulation.
        @param[in] time (list): Simulation time where each time-point corresponds to amplitude-point.
        
        """

        self.__amplitude = amplitude;
        self.__time = time;


    @property
    def output(self):
        """!
        @brief (list) Returns output dynamic of the Sync network (amplitudes of each oscillator in the network) during simulation.
        
        """

        return self.__amplitude;


    @property
    def time(self):
        """!
        @brief (list) Returns time-points corresponds to dynamic-points points.
        
        """

        return self.__time;


    def __len__(self):
        """!
        @brief (uint) Returns number of simulation steps that are stored in dynamic.
        
        """
        
        return len(self.__amplitude);


    def __getitem__(self, index):
        """!
        @brief Indexing of the dynamic.
        
        """
        if (index is 0):
            return self.__time;
        
        elif (index is 1):
            return self.__amplitude;
        
        else:
            raise NameError('Out of range ' + index + ': only indexes 0 and 1 are supported.');


    def allocate_sync_ensembles(self, tolerance = 0.1):
        """!
        @brief Allocate clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster.
        
        @param[in] tolerance (double): Maximum error for allocation of synchronous ensemble oscillators.
        
        @return (list) Grours of indexes of synchronous oscillators, for example, [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
        
        """
        
        return pyclustering.utils.allocate_sync_ensembles(self.__amplitude, tolerance, 0.0);


    def extract_number_oscillations(self, index, amplitude_threshold):
        """!
        @brief Extracts number of oscillations of specified oscillator.
        
        @param[in] index (uint): Index of oscillator whose dynamic is considered.
        @param[in] amplitude_threshold (double): Amplitude threshold when oscillation is taken into account, for example,
                    when oscillator amplitude is greater than threshold then oscillation is incremented.
        
        @return (uint) Number of oscillations of specified oscillator.
        
        """
        
        return pyclustering.utils.extract_number_oscillations(self.__amplitude, index, amplitude_threshold);



class fsync_visualizer:
    """!
    @brief Visualizer of output dynamic of sync network in frequency domain.
    
    """

    @staticmethod
    def show_output_dynamic(fsync_output_dynamic):
        """!
        @brief Shows output dynamic (output of each oscillator) during simulation.
        
        @param[in] fsync_output_dynamic (fsync_dynamic): Output dynamic of the fSync network.
        
        @see show_output_dynamics
        
        """
        
        pyclustering.utils.draw_dynamics(fsync_output_dynamic.time, fsync_output_dynamic.output, x_title = "t", y_title = "amplitude");


    @staticmethod
    def show_output_dynamics(fsync_output_dynamics):
        """!
        @brief Shows several output dynamics (output of each oscillator) during simulation.
        @details Each dynamic is presented on separate plot.
        
        @param[in] fsync_output_dynamics (list): list of output dynamics 'fsync_dynamic' of the fSync network.
        
        @see show_output_dynamic
        
        """
        
        pyclustering.utils.draw_dynamics_set(fsync_output_dynamics, "t", "amplitude", None, None, False, False);



class fsync_network(network):
    """!
    @brief Model of oscillatory network that uses Landau-Stuart oscillator and Kuramoto model as a synchronization mechanism.
    @details Dynamic of each oscillator in the network is described by following differential Landau-Stuart equation with feedback:
    
    \f[
    \dot{z}_{i} = (i\omega_{i} + \rho^{2}_{i} - |z_{i}|^{2} )z_{i} + \frac{1}{N}\sum_{j=0}^{N}k_{ij}(z_{j} - z_{i});
    \f]
    
    Where left part of the equation is Landau-Stuart equation and the right is a Kuramoto model for synchronization.
    For solving this equation Runge-Kutta 4 method is used by default.
    
    Example:
    @code
        # Prepare oscillatory network parameters.
        amount_oscillators = 3;
        frequency = 1.0;
        radiuses = [1.0, 2.0, 3.0];
        coupling_strength = 1.0;
        
        # Create oscillatory network
        oscillatory_network = fsync_network(amount_oscillators, frequency, radiuses, coupling_strength);
        
        # Simulate network during 200 steps on 10 time-units of time-axis.
        output_dynamic = oscillatory_network.simulate(200, 10, True);    # True is to collect whole output dynamic.
        
        # Visualize output result
        fsync_visualizer.show_output_dynamic(output_dynamic);
    @endcode
    
    Example of output dynamic of the network:
    @image html fsync_sync_examples.png
    
    """
    
    __DEFAULT_FREQUENCY_VALUE = 1.0;
    __DEFAULT_RADIUS_VALUE = 1.0;
    __DEFAULT_COUPLING_STRENGTH = 1.0;


    def __init__(self, num_osc, factor_frequency = 1.0, factor_radius = 1.0, factor_coupling = 1.0, type_conn = conn_type.ALL_TO_ALL, representation = conn_represent.MATRIX):
        """!
        @brief Constructor of oscillatory network based on synchronization Kuramoto model and Landau-Stuart oscillator.
        
        @param[in] num_osc (uint): Amount oscillators in the network.
        @param[in] factor_frequency (double|list): Frequency of oscillators, it can be specified as common value for all oscillators by
                    single double value and for each separately by list.
        @param[in] factor_radius (double|list): Radius of oscillators that affects amplitude, it can be specified as common value for all oscillators by
                    single double value and for each separately by list.
        @param[in] factor_coupling (double): Coupling strength between oscillators.
        @param[in] type_conn (conn_type): Type of connection between oscillators in the network (all-to-all, grid, bidirectional list, etc.).
        @param[in] representation (conn_represent): Internal representation of connection in the network: matrix or list.
        
        """
        
        super().__init__(num_osc, type_conn, representation);
        
        self.__frequency = factor_frequency if isinstance(factor_frequency, list) else [ fsync_network.__DEFAULT_FREQUENCY_VALUE * factor_frequency for _ in range(num_osc) ];
        self.__radius = factor_radius if isinstance(factor_radius, list) else [ fsync_network.__DEFAULT_RADIUS_VALUE * factor_radius for _ in range(num_osc) ];
        self.__coupling_strength = fsync_network.__DEFAULT_COUPLING_STRENGTH * factor_coupling;
        self.__properties = [ self.__oscillator_property(index) for index in range(self._num_osc) ];
        
        random.seed();
        self.__amplitude = [ random.random() for _ in range(num_osc) ];


    def simulate(self, steps, time, collect_dynamic = False):
        """!
        @brief Performs static simulation of oscillatory network.
        
        @param[in] steps (uint): Number simulation steps.
        @param[in] time (double): Time of simulation.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        
        @return (list) Dynamic of oscillatory network. If argument 'collect_dynamic' is True, than return dynamic for the whole simulation time,
                 otherwise returns only last values (last step of simulation) of output dynamic.
        
        @see simulate()
        @see simulate_dynamic()
        
        """
        
        dynamic_amplitude, dynamic_time = ([], []) if collect_dynamic is False else ([self.__amplitude], [0]);
        
        step = time / steps;
        int_step = step / 10.0;
        
        for t in numpy.arange(step, time + step, step):
            self.__amplitude = self.__calculate(t, step, int_step);
            
            if collect_dynamic is True:
                dynamic_amplitude.append([ numpy.real(amplitude)[0] for amplitude in self.__amplitude ]);
                dynamic_time.append(t);
        
        if collect_dynamic is False:
            dynamic_amplitude.append([ numpy.real(amplitude)[0] for amplitude in self.__amplitude ]);
            dynamic_time.append(time);

        output_sync_dynamic = fsync_dynamic(dynamic_amplitude, dynamic_time);
        return output_sync_dynamic;


    def __calculate(self, t, step, int_step):
        """!
        @brief Calculates new amplitudes for oscillators in the network in line with current step.
        
        @param[in] t (double): Time of simulation.
        @param[in] step (double): Step of solution at the end of which states of oscillators should be calculated.
        @param[in] int_step (double): Step differentiation that is used for solving differential equation.
        
        @return (list) New states (phases) for oscillators.
        
        """
        
        next_amplitudes = [0.0] * self._num_osc;
        
        for index in range (0, self._num_osc, 1):
            z = numpy.array(self.__amplitude[index], dtype = numpy.complex128, ndmin = 1);
            result = odeint(self.__calculate_amplitude, z.view(numpy.float64), numpy.arange(t - step, t, int_step), (index , ));
            next_amplitudes[index] = (result[len(result) - 1]).view(numpy.complex128);
        
        return next_amplitudes;


    def __oscillator_property(self, index):
        """!
        @brief Calculate Landau-Stuart oscillator constant property that is based on frequency and radius.
        
        @param[in] index (uint): Oscillator index whose property is calculated.
        
        @return (double) Oscillator property.
        
        """
        
        return numpy.array(1j * self.__frequency[index] + self.__radius[index]**2, dtype = numpy.complex128, ndmin = 1);


    def __landau_stuart(self, amplitude, index):
        """!
        @brief Calculate Landau-Stuart state.
        
        @param[in] amplitude (double): Current amplitude of oscillator.
        @param[in] index (uint): Oscillator index whose state is calculated. 
        
        @return (double) Landau-Stuart state.
        
        """
        
        return (self.__properties[index] - numpy.absolute(amplitude) ** 2) * amplitude;


    def __synchronization_mechanism(self, amplitude, index):
        """!
        @brief Calculate synchronization part using Kuramoto synchronization mechanism.
        
        @param[in] amplitude (double): Current amplitude of oscillator.
        @param[in] index (uint): Oscillator index whose synchronization influence is calculated.
        
        @return (double) Synchronization influence for the specified oscillator.
        
        """
        
        sync_influence = 0.0;
        
        for k in range(self._num_osc):
            if self.has_connection(index, k) is True:
                amplitude_neighbor = numpy.array(self.__amplitude[k], dtype = numpy.complex128, ndmin = 1);
                sync_influence += amplitude_neighbor - amplitude;
        
        return sync_influence * self.__coupling_strength / self._num_osc;


    def __calculate_amplitude(self, amplitude, t, argv):
        """!
        @brief Returns new amplitude value for particular oscillator that is defined by index that is in 'argv' argument.
        @details The method is used for differential calculation.
        
        @param[in] amplitude (double): Current amplitude of oscillator.
        @param[in] t (double): Current time of simulation.
        @param[in] argv (uint): Index of the current oscillator.
        
        @return (double) New amplitude of the oscillator.
        
        """
        
        z = amplitude.view(numpy.complex);
        dzdt = self.__landau_stuart(z, argv) + self.__synchronization_mechanism(z, argv);
        
        return dzdt.view(numpy.float64);