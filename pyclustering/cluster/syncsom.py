"""!

@brief Cluster analysis algorithm: SYNC-SOM
@details Implementation based on paper @cite article::syncsom::1.

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


from pyclustering.cluster.encoder import type_encoding
from pyclustering.cluster.syncnet import syncnet

from pyclustering.nnet.som import som, type_conn
from pyclustering.nnet import initial_type

from pyclustering.utils import euclidean_distance_square


class syncsom:
    """!
    @brief Class represents clustering algorithm SYNC-SOM. SYNC-SOM is bio-inspired algorithm that is based on oscillatory network 
           that uses self-organized feature map as the first layer.
           
    Example:
    @code
        # read sample for clustering
        sample = read_sample(file);
        
        # create oscillatory network for cluster analysis where the first layer has 
        # size 10x10 and connectivity radius for objects 1.0.
        network = syncsom(sample, 10, 10, 1.0);
        
        # simulate network (perform cluster analysis) and collect output dynamic
        (dyn_time, dyn_phase) = network.process(True, 0.998);
        
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

    @property
    def som_layer(self):
        """!
        @brief The first layer of the oscillatory network - self-organized feature map.
        
        """
        return self._som


    @property
    def sync_layer(self):
        """!
        @brief The second layer of the oscillatory network based on Kuramoto model.
        
        """
        return self._sync


    def __init__(self, data, rows, cols, radius):
        """!
        @brief Constructor of the double layer oscillatory network SYNC-SOM.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] rows (uint): Rows of neurons (number of neurons in column) in the input layer (self-organized feature map).
        @param[in] cols (uint): Columns of neurons (number of neurons in row) in the input later (self-organized feature map).
        @param[in] radius (double): Connectivity radius between objects that defines connection between oscillators in the second layer.
        
        """
        
        self._data = data
        self._radius = radius * radius
        
        self._som = som(rows, cols, conn_type=type_conn.grid_four, ccore=False)   # The first (input) later - SOM layer.
        self._som_osc_table = list()
        
        self._sync = None       # The second (output) layer - Sync layer.
        self._struct = None     # Structure of connections between oscillators in the second layer - Sync layer.
        
        # For convenience
        self._analyser = None


    def process(self, collect_dynamic=False, order=0.999):
        """!
        @brief Performs simulation of the oscillatory network.
        
        @param[in] collect_dynamic (bool): If True - returns whole dynamic of oscillatory network, otherwise returns only last values of dynamics.
        @param[in] order (double): Order of process synchronization that should be considered as end of clustering, destributed 0..1.
        
        @return (tuple) Dynamic of oscillatory network. If argument 'collect_dynamic' = True, than return dynamic for the whole simulation time,
                otherwise returns only last values (last step of simulation) of dynamic.
        
        @see get_som_clusters()
        @see get_clusters()
        """
        
        # train self-organization map.
        self._som.train(self._data, 100)
        
        # prepare to build list.
        weights = list()
        self._som_osc_table.clear()       # must be cleared, if it's used before.
        for i in range(self._som.size):
            if self._som.awards[i] > 0:
                weights.append(self._som.weights[i])
                self._som_osc_table.append(i)
        
        # create oscillatory neural network.
        self._sync = self.__create_sync_layer(weights)
        self._analyser = self._sync.process(order, collect_dynamic=collect_dynamic)
        
        return self._analyser.time, self._analyser.output


    def __create_sync_layer(self, weights):
        """!
        @brief Creates second layer of the network.
        
        @param[in] weights (list): List of weights of SOM neurons.
        
        @return (syncnet) Second layer of the network.
        
        """
        sync_layer = syncnet(weights, 0.0, initial_phases = initial_type.RANDOM_GAUSSIAN, ccore=False)
        
        for oscillator_index1 in range(0, len(sync_layer)):
            for oscillator_index2 in range(oscillator_index1 + 1, len(sync_layer)):
                if self.__has_object_connection(oscillator_index1, oscillator_index2):
                    sync_layer.set_connection(oscillator_index1, oscillator_index2)
        
        return sync_layer


    def __has_object_connection(self, oscillator_index1, oscillator_index2):
        """!
        @brief Searches for pair of objects that are encoded by specified neurons and that are connected in line with connectivity radius.
        
        @param[in] oscillator_index1 (uint): Index of the first oscillator in the second layer.
        @param[in] oscillator_index2 (uint): Index of the second oscillator in the second layer.
        
        @return (bool) True - if there is pair of connected objects encoded by specified oscillators.
        
        """
        som_neuron_index1 = self._som_osc_table[oscillator_index1]
        som_neuron_index2 = self._som_osc_table[oscillator_index2]
        
        for index_object1 in self._som.capture_objects[som_neuron_index1]:
            for index_object2 in self._som.capture_objects[som_neuron_index2]:
                distance = euclidean_distance_square(self._data[index_object1], self._data[index_object2])
                if distance <= self._radius:
                    return True
        
        return False


    def get_som_clusters(self):
        """!
        @brief Returns clusters with SOM neurons that encode input features in line with result of synchronization in the second (Sync) layer.
        
        @return (list) List of clusters that are represented by lists of indexes of neurons that encode input data.
        
        @see process()
        @see get_clusters()
        
        """
        
        sync_clusters = self._analyser.allocate_clusters()
        
        # Decode it to indexes of SOM neurons
        som_clusters = list()
        for oscillators in sync_clusters:
            cluster = list()
            for index_oscillator in oscillators:
                index_neuron = self._som_osc_table[index_oscillator]
                cluster.append(index_neuron)
                
            som_clusters.append(cluster)
            
        return som_clusters


    def get_clusters(self, eps=0.1):
        """!
        @brief Returns clusters in line with ensembles of synchronous oscillators where each synchronous ensemble corresponds to only one cluster.
        
        @param[in] eps (double): Maximum error for allocation of synchronous ensemble oscillators.
        
        @return (list) List of grours (lists) of indexes of synchronous oscillators that corresponds to index of objects.
        
        @see process()
        @see get_som_clusters()
        
        """
        
        sync_clusters = self._analyser.allocate_clusters(eps)       # it isn't indexes of SOM neurons
        
        clusters = list()
        for oscillators in sync_clusters:
            cluster = list()
            for index_oscillator in oscillators:
                index_neuron = self._som_osc_table[index_oscillator]
                
                cluster += self._som.capture_objects[index_neuron]
                
            clusters.append(cluster)
        
        return clusters


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION


    def show_som_layer(self):
        """!
        @brief Shows visual representation of the first (SOM) layer.
        
        """
        
        self._som.show_network()


    def show_sync_layer(self):
        """!
        @brief Shows visual representation of the second (Sync) layer.
        
        """
        
        self._sync.show_network()
