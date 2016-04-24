"""!

@brief Cluster analysis algorithm: Hierarchical Sync (HSyncNet)
@details Based on article description:
         - J.Shao, X.He, C.Bohm, Q.Yang, C.Plant. Synchronization-Inspired Partitioning and Hierarchical Clustering. 2013.

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

import pyclustering.core.wrapper as wrapper;

from pyclustering.nnet import initial_type, solve_type;

from pyclustering.cluster.syncnet import syncnet, syncnet_analyser;
from pyclustering.utils import average_neighbor_distance;

class hsyncnet(syncnet):
    """!
    @brief Class represents clustering algorithm HSyncNet. HSyncNet is bio-inspired algorithm that is based on oscillatory network that uses modified Kuramoto model.
    
    Example:
    @code
        # read list of points for cluster analysis
        sample = read_sample(file);
        
        # create network for allocation three clusters using CCORE (C++ implementation)
        network = hsyncnet(sample, 3, ccore = True);
        
        # run cluster analysis and output dynamic of the network
        (time, dynamic) = network.process(0.995, collect_dynamic = True);
        
        # get allocated clusters
        clusters = network.get_clusters();
        
        # show output dynamic of the network
        draw_dynamics(time, dynamic);
    @endcode
    """
    
    def __init__(self, source_data, number_clusters, osc_initial_phases = initial_type.RANDOM_GAUSSIAN, initial_neighbors = 3, increase_persent = 0.15, ccore = False):
        """!
        @brief Costructor of the oscillatory network hSyncNet for cluster analysis.

        @param[in] source_data (list): Input data set defines structure of the network.
        @param[in] number_clusters (uint): Number of clusters that should be allocated.
        @param[in] osc_initial_phases (initial_type): Type of initialization of initial values of phases of oscillators.
        @param[in] initial_neighbors (uint): Defines initial radius connectivity by calculation average distance to connect specify number of oscillators.
        @param[in] increase_persent (double): Percent of increasing of radius connectivity on each step (input values in range (0.0; 1.0) correspond to (0%; 100%)).
        @param[in] ccore (bool): If True than DLL CCORE (C++ solution) will be used for solving.
        
        """
        
        self.__ccore_network_pointer = None;
        
        if (initial_neighbors >= len(source_data)):
            initial_neighbors = len(source_data) - 1;
        
        if (ccore is True):
            self.__ccore_network_pointer = wrapper.hsyncnet_create_network(source_data, number_clusters, osc_initial_phases, initial_neighbors, increase_persent);
        else: 
            super().__init__(source_data, 0, initial_phases = osc_initial_phases);
            
            self.__initial_neighbors = initial_neighbors;
            self.__increase_persent = increase_persent;
            self._number_clusters = number_clusters;
    
    
    def __del__(self):
        """!
        @brief Destructor of oscillatory network HSyncNet.
        
        """
        
        if (self.__ccore_network_pointer is not None):
            wrapper.hsyncnet_destroy_network(self.__ccore_network_pointer);
            self.__ccore_network_pointer = None;
            
            
    def process(self, order = 0.998, solution = solve_type.FAST, collect_dynamic = False):
        """!
        @brief Performs clustering of input data set in line with input parameters.
        
        @param[in] order (double): Level of local synchronization between oscillator that defines end of synchronization process, range [0..1].
        @param[in] solution (solve_type) Type of solving differential equation.
        @param[in] collect_dynamic (bool): If True - returns whole history of process synchronization otherwise - only final state (when process of clustering is over).
        
        @return (tuple) Returns dynamic of the network as tuple of lists on each iteration (time, oscillator_phases) that depends on collect_dynamic parameter. 
        
        @see get_clusters()
        
        """
        
        if (self.__ccore_network_pointer is not None):
            analyser = wrapper.hsyncnet_process(self.__ccore_network_pointer, order, solution, collect_dynamic);
            return syncnet_analyser(None, None, analyser);
        
        number_neighbors = self.__initial_neighbors;
        current_number_clusters = float('inf');
        
        dyn_phase = [];
        dyn_time = [];
        
        radius = average_neighbor_distance(self._osc_loc, number_neighbors);
        
        increase_step = int(len(self._osc_loc) * self.__increase_persent);
        if (increase_step < 1):
            increase_step = 1;
        
        
        analyser = None;
        while(current_number_clusters > self._number_clusters):
            self._create_connections(radius);
        
            analyser = self.simulate_dynamic(order, solution, collect_dynamic);
            if (collect_dynamic == True):
                dyn_phase += analyser.output;
                
                if (len(dyn_time) > 0):
                    point_time_last = dyn_time[len(dyn_time) - 1];
                    dyn_time += [time_point + point_time_last for time_point in analyser.time];
                else:
                    dyn_time += analyser.time;
            
            clusters = analyser.allocate_sync_ensembles(0.05);
            
            # Get current number of allocated clusters
            current_number_clusters = len(clusters);
            
            # Increase number of neighbors that should be used
            number_neighbors += increase_step;
            
            # Update connectivity radius and check if average function can be used anymore
            if (number_neighbors >= len(self._osc_loc)):
                radius = radius * self.__increase_persent + radius;
            else:
                radius = average_neighbor_distance(self._osc_loc, number_neighbors);
        
        if (collect_dynamic != True):
            dyn_phase = analyser.output;
            dyn_time = analyser.time;
        
        return syncnet_analyser(dyn_phase, dyn_time, None);
    