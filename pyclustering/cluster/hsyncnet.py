"""!

@brief Cluster analysis algorithm: Hierarchical Sync (HSyncNet)
@details Implementation based on paper @cite artcile::hsyncnet::1.

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


import pyclustering.core.hsyncnet_wrapper as wrapper

from pyclustering.core.wrapper import ccore_library

from pyclustering.nnet import initial_type, solve_type

from pyclustering.cluster.syncnet import syncnet, syncnet_analyser

from pyclustering.utils import average_neighbor_distance


class hsyncnet(syncnet):
    """!
    @brief Class represents clustering algorithm HSyncNet. HSyncNet is bio-inspired algorithm that is based on oscillatory network that uses modified Kuramoto model.
    
    Example:
    @code
        from pyclustering.cluster.hsyncnet import hsyncnet
        from pyclustering.nnet.sync import sync_visualizer
        from pyclustering.utils import read_sample, draw_clusters
        from pyclustering.samples.definitions import SIMPLE_SAMPLES

        # Read list of points for cluster analysis.
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)

        # Create network for allocation of three clusters.
        network = hsyncnet(sample, 3)

        # Run cluster analysis and output dynamic of the network.
        analyser = network.process(0.995, collect_dynamic=True)

        # Get allocated clusters.
        clusters = analyser.allocate_clusters(eps=0.1)

        # Show output dynamic of the network.
        sync_visualizer.show_output_dynamic(analyser)

        # Show allocated clusters.
        draw_clusters(sample, clusters)
    @endcode
    """
    
    def __init__(self, source_data, number_clusters, osc_initial_phases=initial_type.RANDOM_GAUSSIAN,
                 initial_neighbors=3, increase_persent=0.15, ccore=True):
        """!
        @brief Costructor of the oscillatory network hSyncNet for cluster analysis.

        @param[in] source_data (list): Input data set defines structure of the network.
        @param[in] number_clusters (uint): Number of clusters that should be allocated.
        @param[in] osc_initial_phases (initial_type): Type of initialization of initial values of phases of oscillators.
        @param[in] initial_neighbors (uint): Defines initial radius connectivity by calculation average distance to connect specify number of oscillators.
        @param[in] increase_persent (double): Percent of increasing of radius connectivity on each step (input values in range (0.0; 1.0) correspond to (0%; 100%)).
        @param[in] ccore (bool): If True than DLL CCORE (C++ solution) will be used for solving.
        
        """
        
        self.__ccore_network_pointer = None
        
        if initial_neighbors >= len(source_data):
            initial_neighbors = len(source_data) - 1

        if (ccore is True) and ccore_library.workable():
            self.__ccore_network_pointer = wrapper.hsyncnet_create_network(source_data, number_clusters, osc_initial_phases, initial_neighbors, increase_persent)
        else: 
            super().__init__(source_data, 0, initial_phases=osc_initial_phases, ccore=False)
            
            self.__initial_neighbors = initial_neighbors
            self.__increase_persent = increase_persent
            self._number_clusters = number_clusters
    
    
    def __del__(self):
        """!
        @brief Destructor of oscillatory network HSyncNet.
        
        """
        
        if self.__ccore_network_pointer is not None:
            wrapper.hsyncnet_destroy_network(self.__ccore_network_pointer)
            self.__ccore_network_pointer = None
            
            
    def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False):
        """!
        @brief Performs clustering of input data set in line with input parameters.
        
        @param[in] order (double): Level of local synchronization between oscillator that defines end of synchronization process, range [0..1].
        @param[in] solution (solve_type) Type of solving differential equation.
        @param[in] collect_dynamic (bool): If True - returns whole history of process synchronization otherwise - only final state (when process of clustering is over).
        
        @return (tuple) Returns dynamic of the network as tuple of lists on each iteration (time, oscillator_phases) that depends on collect_dynamic parameter. 
        
        @see get_clusters()
        
        """
        
        if self.__ccore_network_pointer is not None:
            analyser = wrapper.hsyncnet_process(self.__ccore_network_pointer, order, solution, collect_dynamic)
            return syncnet_analyser(None, None, analyser)
        
        number_neighbors = self.__initial_neighbors
        current_number_clusters = float('inf')
        
        dyn_phase = []
        dyn_time = []
        
        radius = average_neighbor_distance(self._osc_loc, number_neighbors)
        
        increase_step = int(len(self._osc_loc) * self.__increase_persent)
        if increase_step < 1:
            increase_step = 1
        
        
        analyser = None
        while current_number_clusters > self._number_clusters:
            self._create_connections(radius)
        
            analyser = self.simulate_dynamic(order, solution, collect_dynamic)
            if collect_dynamic == True:
                if len(dyn_phase) == 0:
                    self.__store_dynamic(dyn_phase, dyn_time, analyser, True)
                
                self.__store_dynamic(dyn_phase, dyn_time, analyser, False)
            
            clusters = analyser.allocate_sync_ensembles(0.05)
            
            # Get current number of allocated clusters
            current_number_clusters = len(clusters)
            
            # Increase number of neighbors that should be used
            number_neighbors += increase_step
            
            # Update connectivity radius and check if average function can be used anymore
            radius = self.__calculate_radius(number_neighbors, radius)
        
        if (collect_dynamic != True):
            self.__store_dynamic(dyn_phase, dyn_time, analyser, False)
        
        return syncnet_analyser(dyn_phase, dyn_time, None)


    def __calculate_radius(self, number_neighbors, radius):
        """!
        @brief Calculate new connectivity radius.
        
        @param[in] number_neighbors (uint): Average amount of neighbors that should be connected by new radius.
        @param[in] radius (double): Current connectivity radius.
        
        @return New connectivity radius.
        
        """
        
        if (number_neighbors >= len(self._osc_loc)):
            return radius * self.__increase_persent + radius;
        
        return average_neighbor_distance(self._osc_loc, number_neighbors);


    def __store_dynamic(self, dyn_phase, dyn_time, analyser, begin_state):
        """!
        @brief Store specified state of Sync network to hSync.
        
        @param[in] dyn_phase (list): Output dynamic of hSync where state should be stored.
        @param[in] dyn_time (list): Time points that correspond to output dynamic where new time point should be stored.
        @param[in] analyser (syncnet_analyser): Sync analyser where Sync states are stored.
        @param[in] begin_state (bool): If True the first state of Sync network is stored, otherwise the last state is stored.
        
        """
        
        if (begin_state is True):
            dyn_time.append(0);
            dyn_phase.append(analyser.output[0]);
        
        else:
            dyn_phase.append(analyser.output[len(analyser.output) - 1]);
            dyn_time.append(len(dyn_time));
