"""!

@brief Cluster analysis algorithm: Sync
@details Implementation based on paper @cite article::syncnet::1.

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
import warnings

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))

from pyclustering.cluster.encoder import type_encoding
from pyclustering.cluster import cluster_visualizer

from pyclustering.core.syncnet_wrapper import syncnet_create_network, syncnet_process, syncnet_destroy_network, syncnet_analyser_destroy
from pyclustering.core.sync_wrapper import sync_connectivity_matrix
from pyclustering.core.wrapper import ccore_library

from pyclustering.nnet.sync import sync_dynamic, sync_network, sync_visualizer
from pyclustering.nnet import conn_represent, initial_type, conn_type, solve_type

from pyclustering.utils import euclidean_distance


class syncnet_analyser(sync_dynamic):
    """!
    @brief Performs analysis of output dynamic of the oscillatory network syncnet to extract information about cluster allocation.
    
    """
    
    def __init__(self, phase, time, pointer_sync_analyser):
        """!
        @brief Constructor of the analyser.
        
        @param[in] phase (list): Output dynamic of the oscillatory network, where one iteration consists of all phases of oscillators.
        @param[in] time (list): Simulation time.
        @param[in] pointer_sync_analyser (POINTER): Pointer to CCORE analyser, if specified then other arguments can be omitted.
        
        """
        super().__init__(phase, time, pointer_sync_analyser)


    def __del__(self):
        """!
        @brief Desctructor of the analyser.
        
        """
        
        if self._ccore_sync_dynamic_pointer is not None:
            syncnet_analyser_destroy(self._ccore_sync_dynamic_pointer)
            self._ccore_sync_dynamic_pointer = None
    
    
    def allocate_clusters(self, eps = 0.01, indexes = None, iteration = None):
        """!
        @brief Returns list of clusters in line with state of ocillators (phases).
        
        @param[in] eps (double): Tolerance level that define maximal difference between phases of oscillators in one cluster.
        @param[in] indexes (list): List of real object indexes and it should be equal to amount of oscillators (in case of 'None' - indexes are in range [0; amount_oscillators]).
        @param[in] iteration (uint): Iteration of simulation that should be used for allocation.
        
        @return (list) List of clusters, for example [ [cluster1], [cluster2], ... ].)
        
        """
        
        return self.allocate_sync_ensembles(eps, indexes, iteration)


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION



class syncnet_visualizer(sync_visualizer):
    """!
    @brief Visualizer of output dynamic of oscillatory network 'syncnet' for cluster analysis.
    
    """
    
    @staticmethod
    def animate_cluster_allocation(dataset, analyser, animation_velocity = 75, tolerance = 0.1, save_movie = None, title = None):
        """!
        @brief Shows animation of output dynamic (output of each oscillator) during simulation on a circle from [0; 2pi].
        
        @param[in] dataset (list): Input data that was used for processing by the network.
        @param[in] analyser (syncnet_analyser): Output dynamic analyser of the Sync network.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds.
        @param[in] tolerance (double): Tolerance level that define maximal difference between phases of oscillators in one cluster.
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        @param[in] title (string): If it is specified then title will be displayed on the animation plot.
        
        """
        
        figure = plt.figure()
        
        def init_frame():
            return frame_generation(0)
        
        def frame_generation(index_dynamic):
            figure.clf()
            if title is not None:
                figure.suptitle(title, fontsize = 26, fontweight = 'bold')
            
            ax1 = figure.add_subplot(121, projection='polar')
            
            clusters = analyser.allocate_clusters(eps = tolerance, iteration = index_dynamic)
            dynamic = analyser.output[index_dynamic]
            
            visualizer = cluster_visualizer(size_row = 2)
            visualizer.append_clusters(clusters, dataset)
            
            artist1, = ax1.plot(dynamic, [1.0] * len(dynamic), marker = 'o', color = 'blue', ls = '')
            
            visualizer.show(figure, display = False)
            artist2 = figure.gca()
            
            return [ artist1, artist2 ]
        
        cluster_animation = animation.FuncAnimation(figure, frame_generation, len(analyser), interval = animation_velocity, init_func = init_frame, repeat_delay = 5000);

        if save_movie is not None:
#             plt.rcParams['animation.ffmpeg_path'] = 'D:\\Program Files\\ffmpeg-3.3.1-win64-static\\bin\\ffmpeg.exe';
#             ffmpeg_writer = animation.FFMpegWriter(fps = 15);
#             cluster_animation.save(save_movie, writer = ffmpeg_writer);
            cluster_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500)
        else:
            plt.show()


class syncnet(sync_network):
    """!
    @brief Class represents clustering algorithm SyncNet. 
    @details SyncNet is bio-inspired algorithm that is based on oscillatory network that uses modified Kuramoto model. Each attribute of a data object
             is considered as a phase oscillator.
    
    Example:
    @code
        from pyclustering.cluster import cluster_visualizer
        from pyclustering.cluster.syncnet import syncnet, solve_type
        from pyclustering.samples.definitions import SIMPLE_SAMPLES
        from pyclustering.utils import read_sample

        # Read sample for clustering from some file.
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

        # Create oscillatory network with connectivity radius 1.0.
        network = syncnet(sample, 1.0)

        # Run cluster analysis and collect output dynamic of the oscillatory network.
        # Network simulation is performed by Runge Kutta 4.
        analyser = network.process(0.998, solve_type.RK4)

        # Show oscillatory network.
        network.show_network()

        # Obtain clustering results.
        clusters = analyser.allocate_clusters()

        # Visualize clustering results.
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    @endcode
    
    """
    
    def __init__(self, sample, radius, conn_repr=conn_represent.MATRIX, initial_phases=initial_type.RANDOM_GAUSSIAN,
                 enable_conn_weight=False, ccore=True):
        """!
        @brief Contructor of the oscillatory network SYNC for cluster analysis.
        
        @param[in] sample (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] radius (double): Connectivity radius between points, points should be connected if distance between them less then the radius.
        @param[in] conn_repr (conn_represent): Internal representation of connection in the network: matrix or list. Ignored in case of usage of CCORE library.
        @param[in] initial_phases (initial_type): Type of initialization of initial phases of oscillators (random, uniformly distributed, etc.).
        @param[in] enable_conn_weight (bool): If True - enable mode when strength between oscillators depends on distance between two oscillators.
              If False - all connection between oscillators have the same strength that equals to 1 (True).
        @param[in] ccore (bool): Defines should be CCORE C++ library used instead of Python code or not.
        
        """
        
        self._ccore_network_pointer = None
        self._osc_loc = sample
        self._num_osc = len(sample)

        self._verify_arguments()

        if (ccore is True) and ccore_library.workable():
            self._ccore_network_pointer = syncnet_create_network(sample, radius, initial_phases, enable_conn_weight)
            
            # Default representation that is returned by CCORE is matrix.
            self._conn_represent = conn_represent.MATRIX

        else:
            super().__init__(len(sample), 1, 0, conn_type.DYNAMIC, conn_repr, initial_phases, False)
            
            self._conn_weight = None
            self._ena_conn_weight = enable_conn_weight
            
            # Create connections.
            if radius is not None:
                self._create_connections(radius)


    def __del__(self):
        """!
        @brief Destructor of oscillatory network is based on Kuramoto model.
        
        """
        
        if self._ccore_network_pointer is not None:
            syncnet_destroy_network(self._ccore_network_pointer)
            self._ccore_network_pointer = None


    def _verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if self._num_osc <= 0:
            raise ValueError("Input data is empty (size: '%d')." % self._num_osc)


    def _create_connections(self, radius):
        """!
        @brief Create connections between oscillators in line with input radius of connectivity.
        
        @param[in] radius (double): Connectivity radius between oscillators.
        
        """
        
        if self._ena_conn_weight is True:
            self._conn_weight = [[0] * self._num_osc for _ in range(0, self._num_osc, 1)]
        
        maximum_distance = 0
        minimum_distance = float('inf')
        
        # Create connections
        for i in range(0, self._num_osc, 1):
            for j in range(i + 1, self._num_osc, 1):
                    dist = euclidean_distance(self._osc_loc[i], self._osc_loc[j])
                    
                    if self._ena_conn_weight is True:
                        self._conn_weight[i][j] = dist
                        self._conn_weight[j][i] = dist
                        
                        if (dist > maximum_distance): maximum_distance = dist
                        if (dist < minimum_distance): minimum_distance = dist
                    
                    if dist <= radius:
                        self.set_connection(i, j)
        
        if self._ena_conn_weight is True:
            multiplier = 1
            subtractor = 0
            
            if maximum_distance != minimum_distance:
                multiplier = (maximum_distance - minimum_distance)
                subtractor = minimum_distance
            
            for i in range(0, self._num_osc, 1):
                for j in range(i + 1, self._num_osc, 1):
                    value_conn_weight = (self._conn_weight[i][j] - subtractor) / multiplier
                    
                    self._conn_weight[i][j] = value_conn_weight
                    self._conn_weight[j][i] = value_conn_weight


    def process(self, order = 0.998, solution=solve_type.FAST, collect_dynamic=True):
        """!
        @brief Peforms cluster analysis using simulation of the oscillatory network.
        
        @param[in] order (double): Order of synchronization that is used as indication for stopping processing.
        @param[in] solution (solve_type): Specified type of solving diff. equation.
        @param[in] collect_dynamic (bool): Specified requirement to collect whole dynamic of the network.
        
        @return (syncnet_analyser) Returns analyser of results of clustering.
        
        """
        
        if self._ccore_network_pointer is not None:
            pointer_output_dynamic = syncnet_process(self._ccore_network_pointer, order, solution, collect_dynamic)
            return syncnet_analyser(None, None, pointer_output_dynamic)
        else:
            output_sync_dynamic = self.simulate_dynamic(order, solution, collect_dynamic)
            return syncnet_analyser(output_sync_dynamic.output, output_sync_dynamic.time, None)
    
    
    def _phase_kuramoto(self, teta, t, argv):
        """!
        @brief Overrided method for calculation of oscillator phase.
        
        @param[in] teta (double): Current value of phase.
        @param[in] t (double): Time (can be ignored).
        @param[in] argv (uint): Index of oscillator whose phase represented by argument teta.
        
        @return (double) New value of phase of oscillator with index 'argv'.
        
        """
        
        index = argv   # index of oscillator
        phase = 0.0      # phase of a specified oscillator that will calculated in line with current env. states.
        
        neighbors = self.get_neighbors(index)
        for k in neighbors:
            conn_weight = 1.0
            if self._ena_conn_weight is True:
                conn_weight = self._conn_weight[index][k]
                
            phase += conn_weight * self._weight * math.sin(self._phases[k] - teta)
        
        divider = len(neighbors)
        if divider == 0:
            divider = 1.0
            
        return self._freq[index] + (phase / divider)
    
    
    def show_network(self):
        """!
        @brief Shows connections in the network. It supports only 2-d and 3-d representation.
        
        """
        
        if (self._ccore_network_pointer is not None) and (self._osc_conn is None):
            self._osc_conn = sync_connectivity_matrix(self._ccore_network_pointer)
        
        dimension = len(self._osc_loc[0])
        if (dimension != 3) and (dimension != 2):
            raise NameError('Network that is located in different from 2-d and 3-d dimensions can not be represented');
        
        from matplotlib.font_manager import FontProperties
        from matplotlib import rcParams
    
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
        
        for i in range(0, self._num_osc, 1):
            if dimension == 2:
                axes.plot(self._osc_loc[i][0], self._osc_loc[i][1], 'bo')
                if self._conn_represent == conn_represent.MATRIX:
                    for j in range(i, self._num_osc, 1):    # draw connection between two points only one time
                        if self.has_connection(i, j) is True:
                            axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], 'b-', linewidth = 0.5)
                            
                else:
                    for j in self.get_neighbors(i):
                        if (self.has_connection(i, j) is True) and (i > j):     # draw connection between two points only one time
                            axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], 'b-', linewidth = 0.5)
            
            elif dimension == 3:
                axes.scatter(self._osc_loc[i][0], self._osc_loc[i][1], self._osc_loc[i][2], c = 'b', marker = 'o')
                
                if self._conn_represent == conn_represent.MATRIX:
                    for j in range(i, self._num_osc, 1):    # draw connection between two points only one time
                        if self.has_connection(i, j) is True:
                            axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], [self._osc_loc[i][2], self._osc_loc[j][2]], 'b-', linewidth = 0.5)
                        
                else:
                    for j in self.get_neighbors(i):
                        if (self.has_connection(i, j) == True) and (i > j):     # draw connection between two points only one time
                            axes.plot([self._osc_loc[i][0], self._osc_loc[j][0]], [self._osc_loc[i][1], self._osc_loc[j][1]], [self._osc_loc[i][2], self._osc_loc[j][2]], 'b-', linewidth = 0.5)

        plt.grid()
        plt.show()