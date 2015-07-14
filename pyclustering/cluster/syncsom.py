"""!

@brief Cluster analysis algorithm: SYNC-SOM
@details Based on article description:
         - A.Novikov, E.Benderskaya. SYNC-SOM Double-layer Oscillatory Network for Cluster Analysis. 2014.

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

from pyclustering.nnet.som import som, type_conn;
from pyclustering.nnet import initial_type;

from pyclustering.cluster.syncnet import syncnet;

from pyclustering.utils import average_neighbor_distance;


class syncsom:
    """!
    @brief Class represents clustering algorithm SYNC-SOM. SYNC-SOM is bio-inspired algorithm that is based on oscillatory network 
           that uses self-organized feature map as the first layer.
           
    Example:
    @code
        # read sample for clustering
        sample = read_sample(file);
        
        # create oscillatory network for cluster analysis where the first layer has size 10x10
        network = syncsom(sample, 10, 10);
        
        # simulate network (perform cluster analysis) and collect output dynamic
        (dyn_time, dyn_phase) = network.process(5, True, 0.998);
        
        # obtain encoded clusters
        encoded_clusters = network.get_som_clusters();
        
        # obtain real clusters
        clusters = network.get_clusters();
        
        # show the first layer of the network
        network.show_som_layer();
        
        # show the second layer of the network
        network.show_sync_layer();
    @endcode
    
    """
    _som = None;        # The first (input) later - SOM layer.
    _data = None;       # Pointer to input data.
    _sync = None;       # The second (output) layer - Sync layer.
    _struct = None;     # Structure of connections between oscillators in the second layer - Sync layer.
    
    # For convenience
    _som_osc_table = None;
    _analyser = None;
    
    @property
    def som_layer(self):
        """!
        @brief The first layer of the oscillatory network - self-organized feature map.
        
        """
        return self._som;
    
    @property
    def sync_layer(self):
        """!
        @brief The second layer of the oscillatory network based on Kuramoto model.
        
        """
        return self._sync;
    
    def __init__(self, data, rows, cols):
        """!
        @brief Constructor of the double layer oscillatory network SYNC-SOM.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] rows (uint): Rows of neurons (number of neurons in column) in the input layer (self-organized feature map).
        @param[in] cols (uint): Columns of neurons (number of neurons in row) in the input later (self-organized feature map).
        
        """
        
        self._data = data;
        
        self._som = som(rows, cols, conn_type = type_conn.grid_four);
        self._som_osc_table = list();        
    
    def process(self, number_neighbours, collect_dynamic = False, order = 0.999):
        """!
        @brief Performs simulation of the oscillatory network.
        
        @param[in] number_neighbours (uint): Number of neighbours that should be used for calculation average distance and creation connections between oscillators.
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        @param[in] order (double): Order of process synchronization that should be considered as end of clustering, destributed 0..1.
        
        @return (tuple) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see get_som_clusters()
        @see get_clusters()
        """
        
        # train self-organization map.
        self._som.train(self._data, 100);
        
        # prepare to build list.
        weights = list();
        self._som_osc_table.clear();        # must be cleared, if it's used before.
        for i in range(self._som.size):
            if (self._som.awards[i] > 0):
                weights.append(self._som.weights[i]);
                self._som_osc_table.append(i);
        
        # calculate trusted distance between objects.
        radius = 0;
        if (len(weights) >= number_neighbours):
            radius = average_neighbor_distance(weights, number_neighbours);
        else:
            radius = 0;
        
        # create oscillatory neural network.
        self._sync = syncnet(weights, radius, initial_phases = initial_type.EQUIPARTITION);
        self._analyser = self._sync.process(order, collect_dynamic = collect_dynamic);
        
        # Draw SOM clusters.
        #clusters = self._sync.get_clusters();
        #draw_clusters(weights, clusters);
        #self._som.show_network(awards = False, belongs = True);
        
        # return dynamic if it was requested.
        return (self._analyser.time, self._analyser.output);   
    
    def get_som_clusters(self, eps = 0.1):
        """!
        @brief Returns clusters with SOM neurons that encode input features in line with result of synchronization in the second (Sync) layer.
        
        @param[in] eps (double): Maximum error for allocation of synchronous ensemble oscillators.
        
        @return (list) List of clusters that are represented by lists of indexes of neurons that encode input data.
        
        @see process()
        @see get_clusters()
        
        """
        
        sync_clusters = self._analyser.allocate_clusters();
        
        # Decode it to indexes of SOM neurons
        som_clusters = list();
        for oscillators in sync_clusters:
            cluster = list();
            for index_oscillator in oscillators:
                index_neuron = self._som_osc_table[index_oscillator];
                cluster.append(index_neuron);
                
            som_clusters.append(cluster);
            
        return som_clusters;
            
    
    def get_clusters(self, eps = 0.1):
        """!
        @brief Returns clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster.
        
        @param[in] eps (double): Maximum error for allocation of synchronous ensemble oscillators.
        
        @return (list) List of grours (lists) of indexes of synchronous oscillators that corresponds to index of objects.
        
        @see process()
        @see get_som_clusters()
        
        """
        
        sync_clusters = self._analyser.allocate_clusters(eps);       # NOTE: it isn't indexes of SOM neurons
        
        clusters = list();
        total_winners = 0;
        total_number_points = 0;
        for oscillators in sync_clusters:
            cluster = list();
            for index_oscillator in oscillators:
                index_neuron = self._som_osc_table[index_oscillator];
                assert self._som.awards[index_neuron] == len(self._som.capture_objects[index_neuron]);      # TODO: Should be moved to unit-test
                assert self._som.awards[index_neuron] > 0;              # TODO: Should be moved to unit-test
                
                cluster += self._som.capture_objects[index_neuron];
                total_number_points += len(self._som.capture_objects[index_neuron]);
                total_winners += 1;
                
            clusters.append(cluster);
        
        assert self._som.get_winner_number() == total_winners;      # TODO: Should be moved to unit-test
        assert len(self._data) == total_number_points;              # TODO: Should be moved to unit-test
        
        # TODO: Should be moved to unit-test
        capture_points = 0;
        for points in clusters:
            capture_points += len(points);
        # print("[POINTS] Capture: ", capture_points, ", Real: ", len(self._data));
        assert capture_points == len(self._data);
        
        return clusters;


    def show_som_layer(self):
        """!
        @brief Shows visual representation of the first (SOM) layer.
        
        """
        
        self._som.show_network();
    
    
    def show_sync_layer(self):
        """!
        @brief Shows visual representation of the second (Sync) layer.
        
        """
        
        self._sync.show_network();
        