"""!

@brief Chaotic Neural Network
@details Implementation based on paper @cite article::nnet::cnn::1, @cite inproceedings::nnet::cnn::1.

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
import numpy
import random
import warnings

try:
    import matplotlib.pyplot as plt

    from matplotlib import rcParams
    from matplotlib.font_manager import FontProperties
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))

from enum import IntEnum

from scipy.spatial import Delaunay

from pyclustering.utils import euclidean_distance_square, average_neighbor_distance, heaviside, draw_dynamics


class type_conn(IntEnum):
    """!
    @brief Enumeration of connection types for Chaotic Neural Network.
    
    @see cnn_network
    
    """
    
    ## All oscillators have connection with each other.
    ALL_TO_ALL  = 0,
    
    ## Connections between oscillators are created in line with Delaunay triangulation.
    TRIANGULATION_DELAUNAY = 1,


class cnn_dynamic:
    """!
    @brief Container of output dynamic of the chaotic neural network where states of each neuron during simulation are stored.
    
    @see cnn_network
    
    """
    
    def __init__(self, output=None, time=None):
        """!
        @brief Costructor of the chaotic neural network output dynamic.

        @param[in] output (list): Dynamic of oscillators on each step of simulation.
        @param[in] time (list): Simulation time.
        
        """
        
        ## Output value of each neuron on each iteration.
        self.output = output or []
        
        ## Sequence of simulation steps of the network.
        self.time = time or []


    def __len__(self):
        """!
        @brief (uint) Returns amount of simulation steps that are stored.
        
        """
        return len(self.output)


    def allocate_observation_matrix(self):
        """!
        @brief Allocates observation matrix in line with output dynamic of the network.
        @details Matrix where state of each neuron is denoted by zero/one in line with Heaviside function on each iteration.
        
        @return (list) Observation matrix of the network dynamic.
        
        """
        number_neurons = len(self.output[0])
        observation_matrix = []
        
        for iteration in range(len(self.output)):
            obervation_column = []
            for index_neuron in range(number_neurons):
                obervation_column.append(heaviside(self.output[iteration][index_neuron]))
            
            observation_matrix.append(obervation_column)
        
        return observation_matrix
    
    
    def __allocate_neuron_patterns(self, start_iteration, stop_iteration):
        """!
        @brief Allocates observation transposed matrix of neurons that is limited by specified periods of simulation.
        @details Matrix where state of each neuron is denoted by zero/one in line with Heaviside function on each iteration.
        
        @return (list) Transposed observation matrix that is limited by specified periods of simulation.
        
        """
        
        pattern_matrix = []
        for index_neuron in range(len(self.output[0])):
            pattern_neuron = []
            for iteration in range(start_iteration, stop_iteration):
                pattern_neuron.append(heaviside(self.output[iteration][index_neuron]))
            
            pattern_matrix.append(pattern_neuron)
        
        return pattern_matrix
    
    
    def allocate_sync_ensembles(self, steps):
        """!
        @brief Allocate clusters in line with ensembles of synchronous neurons where each synchronous ensemble corresponds to only one cluster.
               
        @param[in] steps (double): Amount of steps from the end that is used for analysis. During specified period chaotic neural network should have stable output
                    otherwise inccorect results are allocated.
        
        @return (list) Grours (lists) of indexes of synchronous oscillators.
                For example [ [index_osc1, index_osc3], [index_osc2], [index_osc4, index_osc5] ].
        
        """
        
        iterations = steps
        if iterations >= len(self.output):
            iterations = len(self.output)
        
        ensembles = []

        start_iteration = len(self.output) - iterations
        end_iteration = len(self.output)
        
        pattern_matrix = self.__allocate_neuron_patterns(start_iteration, end_iteration)
        
        ensembles.append( [0] )
        
        for index_neuron in range(1, len(self.output[0])):
            neuron_pattern = pattern_matrix[index_neuron][:]
            
            neuron_assigned = False
            
            for ensemble in ensembles:
                ensemble_pattern = pattern_matrix[ensemble[0]][:]

                if neuron_pattern == ensemble_pattern:
                    ensemble.append(index_neuron)
                    neuron_assigned = True
                    break
            
            if neuron_assigned is False:
                ensembles.append( [index_neuron] )
        
        return ensembles


class cnn_visualizer:
    """!
    @brief Visualizer of output dynamic of chaotic neural network (CNN).
    
    """
    
    @staticmethod
    def show_output_dynamic(cnn_output_dynamic):
        """!
        @brief Shows output dynamic (output of each neuron) during simulation.
        
        @param[in] cnn_output_dynamic (cnn_dynamic): Output dynamic of the chaotic neural network.
        
        @see show_dynamic_matrix
        @see show_observation_matrix
        
        """
        
        draw_dynamics(cnn_output_dynamic.time, cnn_output_dynamic.output, x_title="t", y_title="x")
    
    
    @staticmethod
    def show_dynamic_matrix(cnn_output_dynamic):
        """!
        @brief Shows output dynamic as matrix in grey colors.
        @details This type of visualization is convenient for observing allocated clusters.
        
        @param[in] cnn_output_dynamic (cnn_dynamic): Output dynamic of the chaotic neural network.
        
        @see show_output_dynamic
        @see show_observation_matrix
        
        """

        network_dynamic = numpy.array(cnn_output_dynamic.output)
        
        plt.imshow(network_dynamic.T, cmap=plt.get_cmap('gray'), interpolation='None', vmin=0.0, vmax=1.0)
        plt.show()
    
    
    @staticmethod
    def show_observation_matrix(cnn_output_dynamic):
        """!
        @brief Shows observation matrix as black/white blocks.
        @details This type of visualization is convenient for observing allocated clusters.
        
        @param[in] cnn_output_dynamic (cnn_dynamic): Output dynamic of the chaotic neural network.
        
        @see show_output_dynamic
        @see show_dynamic_matrix
        
        """
        
        observation_matrix = numpy.array(cnn_output_dynamic.allocate_observation_matrix())
        plt.imshow(observation_matrix.T, cmap = plt.get_cmap('gray'), interpolation='None', vmin = 0.0, vmax = 1.0)
        plt.show()


class cnn_network:
    """!
    @brief Chaotic neural network based on system of logistic map where clustering phenomenon can be observed.
    @details Here is an example how to perform cluster analysis using chaotic neural network:
    @code
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.samples.definitions import SIMPLE_SAMPLES
        from pyclustering.utils import read_sample
        from pyclustering.nnet.cnn import cnn_network, cnn_visualizer

        # Load stimulus from file.
        stimulus = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

        # Create chaotic neural network, amount of neurons should be equal to amount of stimulus.
        network_instance = cnn_network(len(stimulus))

        # Perform simulation during 100 steps.
        steps = 100
        output_dynamic = network_instance.simulate(steps, stimulus)

        # Display output dynamic of the network.
        cnn_visualizer.show_output_dynamic(output_dynamic)

        # Display dynamic matrix and observation matrix to show clustering phenomenon.
        cnn_visualizer.show_dynamic_matrix(output_dynamic)
        cnn_visualizer.show_observation_matrix(output_dynamic)

        # Visualize clustering results.
        clusters = output_dynamic.allocate_sync_ensembles(10)
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, stimulus)
        visualizer.show()
    @endcode
    
    """
    
    def __init__(self, num_osc, conn_type = type_conn.ALL_TO_ALL, amount_neighbors = 3):
        """!
        @brief Constructor of chaotic neural network.
        
        @param[in] num_osc (uint): Amount of neurons in the chaotic neural network.
        @param[in] conn_type (type_conn): CNN type connection for the network.
        @param[in] amount_neighbors (uint): k-nearest neighbors for calculation scaling constant of weights.
        
        """
        
        self.__num_osc = num_osc
        self.__conn_type = conn_type
        self.__amount_neighbors = amount_neighbors
        
        self.__average_distance = 0.0
        self.__weights = None
        self.__weights_summary = None
        
        self.__location = None     # just for network visualization
        
        random.seed()
        self.__output = [ random.random() for _ in range(num_osc) ]
    
    
    def __len__(self):
        """!
        @brief Returns size of the chaotic neural network that is defined by amount of neurons.
        
        """
        return self.__num_osc
    
    
    def simulate(self, steps, stimulus):
        """!
        @brief Simulates chaotic neural network with extrnal stimulus during specified steps.
        @details Stimulus are considered as a coordinates of neurons and in line with that weights
                 are initialized.
        
        @param[in] steps (uint): Amount of steps for simulation.
        @param[in] stimulus (list): Stimulus that are used for simulation.
        
        @return (cnn_dynamic) Output dynamic of the chaotic neural network.
        
        """
        
        self.__create_weights(stimulus)
        self.__location = stimulus
        
        dynamic = cnn_dynamic([], [])
        dynamic.output.append(self.__output)
        dynamic.time.append(0)
        
        for step in range(1, steps, 1):
            self.__output = self.__calculate_states()
            
            dynamic.output.append(self.__output)
            dynamic.time.append(step)
            
        return dynamic
    
    
    def __calculate_states(self):
        """!
        @brief Calculates new state of each neuron.
        @detail There is no any assignment.
        
        @return (list) Returns new states (output).
        
        """
        
        output = [ 0.0 for _ in range(self.__num_osc) ]
        
        for i in range(self.__num_osc):
            output[i] = self.__neuron_evolution(i)
        
        return output
    
    
    def __neuron_evolution(self, index):
        """!
        @brief Calculates state of the neuron with specified index.
        
        @param[in] index (uint): Index of neuron in the network.
        
        @return (double) New output of the specified neuron.
        
        """
        value = 0.0
        
        for index_neighbor in range(self.__num_osc):
            value += self.__weights[index][index_neighbor] * (1.0 - 2.0 * (self.__output[index_neighbor] ** 2))
        
        return value / self.__weights_summary[index]
    
    
    def __create_weights(self, stimulus):
        """!
        @brief Create weights between neurons in line with stimulus.
        
        @param[in] stimulus (list): External stimulus for the chaotic neural network.
        
        """
        
        self.__average_distance = average_neighbor_distance(stimulus, self.__amount_neighbors)
        
        self.__weights = [ [ 0.0 for _ in range(len(stimulus)) ] for _ in range(len(stimulus)) ]
        self.__weights_summary = [ 0.0 for _ in range(self.__num_osc) ]
        
        if self.__conn_type == type_conn.ALL_TO_ALL:
            self.__create_weights_all_to_all(stimulus)
        
        elif self.__conn_type == type_conn.TRIANGULATION_DELAUNAY:
            self.__create_weights_delaunay_triangulation(stimulus)
    
    
    def __create_weights_all_to_all(self, stimulus):
        """!
        @brief Create weight all-to-all structure between neurons in line with stimulus.
        
        @param[in] stimulus (list): External stimulus for the chaotic neural network.
        
        """
        
        for i in range(len(stimulus)):
            for j in range(i + 1, len(stimulus)):
                weight = self.__calculate_weight(stimulus[i], stimulus[j])
                
                self.__weights[i][j] = weight
                self.__weights[j][i] = weight
                
                self.__weights_summary[i] += weight
                self.__weights_summary[j] += weight
    
    
    def __create_weights_delaunay_triangulation(self, stimulus):
        """!
        @brief Create weight Denlauny triangulation structure between neurons in line with stimulus.
        
        @param[in] stimulus (list): External stimulus for the chaotic neural network.
        
        """
        
        points = numpy.array(stimulus)
        triangulation = Delaunay(points)
        
        for triangle in triangulation.simplices:
            for index_tri_point1 in range(len(triangle)):
                for index_tri_point2 in range(index_tri_point1 + 1, len(triangle)):
                    index_point1 = triangle[index_tri_point1]
                    index_point2 = triangle[index_tri_point2]
                    
                    weight = self.__calculate_weight(stimulus[index_point1], stimulus[index_point2])
                    
                    self.__weights[index_point1][index_point2] = weight
                    self.__weights[index_point2][index_point1] = weight
                    
                    self.__weights_summary[index_point1] += weight
                    self.__weights_summary[index_point2] += weight
    
    
    def __calculate_weight(self, stimulus1, stimulus2):
        """!
        @brief Calculate weight between neurons that have external stimulus1 and stimulus2.
        
        @param[in] stimulus1 (list): External stimulus of the first neuron.
        @param[in] stimulus2 (list): External stimulus of the second neuron.
        
        @return (double) Weight between neurons that are under specified stimulus.
        
        """
        
        distance = euclidean_distance_square(stimulus1, stimulus2)
        return math.exp(-distance / (2.0 * self.__average_distance))

    
    def show_network(self):
        """!
        @brief Shows structure of the network: neurons and connections between them.
        
        """
        
        dimension = len(self.__location[0])
        if (dimension != 3) and (dimension != 2):
            raise NameError('Network that is located in different from 2-d and 3-d dimensions can not be represented')

        (fig, axes) = self.__create_surface(dimension)
        
        for i in range(0, self.__num_osc, 1):
            if dimension == 2:
                axes.plot(self.__location[i][0], self.__location[i][1], 'bo')
                for j in range(i, self.__num_osc, 1):    # draw connection between two points only one time
                    if self.__weights[i][j] > 0.0:
                        axes.plot([self.__location[i][0], self.__location[j][0]], [self.__location[i][1], self.__location[j][1]], 'b-', linewidth = 0.5)
            
            elif dimension == 3:
                axes.scatter(self.__location[i][0], self.__location[i][1], self.__location[i][2], c = 'b', marker = 'o')
                
                for j in range(i, self.__num_osc, 1):    # draw connection between two points only one time
                    if self.__weights[i][j] > 0.0:
                        axes.plot([self.__location[i][0], self.__location[j][0]], [self.__location[i][1], self.__location[j][1]], [self.__location[i][2], self.__location[j][2]], 'b-', linewidth = 0.5)
                
        plt.grid()
        plt.show()
    
    
    def __create_surface(self, dimension):
        """!
        @brief Prepares surface for showing network structure in line with specified dimension.
        
        @param[in] dimension (uint): Dimension of processed data (external stimulus).
        
        @return (tuple) Description of surface for drawing network structure.
        
        """
        
        rcParams['font.sans-serif'] = ['Arial']
        rcParams['font.size'] = 12

        fig = plt.figure()
        axes = None
        if dimension == 2:
            axes = fig.add_subplot(111)
        elif dimension == 3:
            axes = fig.gca(projection='3d')
        
        surface_font = FontProperties()
        surface_font.set_name('Arial')
        surface_font.set_size('12')
        
        return (fig, axes)