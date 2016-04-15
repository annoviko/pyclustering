"""!

@brief Cluster analysis algorithm: OPTICS (Ordering Points To Identify Clustering Structure)
@details Based on article description:
         - M.Ankerst, M.Breunig, H.Kriegel, J.Sander. OPTICS: Ordering Points To Identify the Clustering Structure. 1999.

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

from pyclustering.utils import euclidean_distance;


class optics_descriptor:
    """!
    @brief Object description that used by OPTICS algorithm for cluster analysis.
    
    """
    
    def __init__(self, index, core_distance = None, reachability_distance = None):
        """!
        @brief Constructor of object description in optics terms.
        
        @param[in] index (uint): Index of the object in the data set.
        @param[in] core_distance (double): Core distance that is minimum distance to specified number of neighbors.
        @param[in] reachability_distance (double): Reachability distance to this object.
        
        """
        
        ## Reachability distance - the smallest distance to be reachable by core object.
        self.index_object = index;
        
        ## Core distance - the smallest distance to reach specified number of neighbors that is not greater then connectivity radius.
        self.core_distance = core_distance;
        
        ## Index of object from the input data.
        self.reachability_distance = reachability_distance;
        
        ## True is object has been already traversed.
        self.processed = False;
        
    def __repr__(self):
        """!
        @brief Returns string representation of the optics descriptor.
        
        """
        
        return '(%s, [c: %s, r: %s])' % (self.index_object, self.core_distance, self.reachability_distance);               


class optics:
    """!
    @brief Class represents clustering algorithm OPTICS (Ordering Points To Identify Clustering Structure).
    @details OPTICS is a density-based algorithm. Purpose of the algorithm is to provide explicit clusters, but create clustering-ordering representation of the input data. 
             Clustering-ordering information contains information about internal structures of data set in terms of density. 

    Example:
    @code
        # Read sample for clustering from some file
        sample = read_sample(path_sample);
        
        # Create OPTICS algorithm for cluster analysis
        optics_instance = optics(sample, 0.5, 6);
        
        # Run cluster analysis
        optics_instance.process();
        
        # Obtain results of clustering
        clusters = optics_instance.get_clusters();
        noise = optics_instance.get_noise();
        
        # Obtain rechability-distances
        ordering = optics_instance.get_cluster_ordering();
        
        # Visualization of cluster ordering in line with reachability distance.
        indexes = [i for i in range(0, len(ordering))];
        plt.bar(indexes, ordering);
        plt.show(); 
    @endcode
       
    """
    
    def __init__(self, sample, eps, minpts):
        """!
        @brief Constructor of clustering algorithm OPTICS.
        
        @param[in] sample (list): Input data that is presented as a list of points (objects), where each point is represented by list or tuple.
        @param[in] eps (double): Connectivity radius between points, points may be connected if distance between them less than the radius.
        @param[in] minpts (uint): Minimum number of shared neighbors that is required for establishing links between points.
        
        """
        
        self.__processed = [False] * len(sample);
        self.__optics_objects = [optics_descriptor(i) for i in range(len(sample))];     # List of OPTICS objects that corresponds to objects from input sample.
        self.__ordered_database = [];       # List of OPTICS objects in traverse order. 
        
        self.__sample_pointer = sample;     # Algorithm parameter - pointer to sample for processing.
        self.__eps = eps;                   # Algorithm parameter - connectivity radius between object for establish links between object.
        self.__minpts = minpts;             # Algorithm parameter - minimum number of neighbors that is required for establish links between object.
        
        self.__clusters = None;             # Result of clustering (list of clusters where each cluster contains indexes of objects from input data).
        self.__noise = None;                # Result of clustering (noise).


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of OPTICS algorithm.
        
        @remark Results of clustering can be obtained using corresponding gets methods.
        
        @see get_clusters()
        @see get_noise()
        @see get_cluster_ordering()
        
        """
        
        for optic_object in self.__optics_objects:
            if (optic_object.processed is False):
                self.__expand_cluster_order(optic_object);
        
        self.__extract_clusters();
    
    
    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, where each cluster contains indexes of objects and each cluster is represented by list.
        
        @return (list) List of allocated clusters.
        
        @see process()
        @see get_noise()
        @see get_cluster_ordering()
        
        """
        
        return self.__clusters;
    
    
    def get_noise(self):
        """!
        @brief Returns list of noise that contains indexes of objects that corresponds to input data.
        
        @return (list) List of allocated noise objects.
        
        @see process()
        @see get_clusters()
        @see get_cluster_ordering()
        
        """
        
        return self.__noise;
    
    
    def get_cluster_ordering(self):
        """!
        @brief Returns clustering ordering information about the input data set.
        @details Clustering ordering of data-set contains the information about the internal clustering structure in line with connectivity radius.
        
        @return (list) List of reachability distances (clustering ordering).
        
        @see process()
        @see get_clusters()
        @see get_noise()
        
        """
        
        ordering = [];
        
        for cluster in self.__clusters:
            for index_object in cluster:
                optics_object = self.__optics_objects[index_object];
                if (optics_object.reachability_distance is not None):
                    ordering.append(optics_object.reachability_distance);
                    
        return ordering;
    
    
    def __expand_cluster_order(self, optics_object):
        """!
        @brief Expand cluster order from not processed optic-object that corresponds to object from input data.
               Traverse procedure is performed until objects are reachable from core-objects in line with connectivity radius.
               Order database is updated during expanding.
               
        @param[in] optics_object (optics_descriptor): Object that hasn't been processed.
        
        """
        
        optics_object.processed = True;
        
        neighbors_descriptor = self.__neighbor_indexes(optics_object);
        optics_object.reachability_distance = None;
        
        self.__ordered_database.append(optics_object);
        
        # Check core distance
        if (len(neighbors_descriptor) >= self.__minpts):
            neighbors_descriptor.sort(key = lambda obj: obj[1]);
            optics_object.core_distance = neighbors_descriptor[self.__minpts - 1][1];
            
            # Continue processing
            order_seed = list();
            self.__update_order_seed(optics_object, neighbors_descriptor, order_seed);
            
            while(len(order_seed) > 0):
                optic_descriptor = order_seed[0];
                order_seed.remove(optic_descriptor);
                
                neighbors_descriptor = self.__neighbor_indexes(optic_descriptor);
                optic_descriptor.processed = True;
                
                self.__ordered_database.append(optic_descriptor);
                
                if (len(neighbors_descriptor) >= self.__minpts):
                    neighbors_descriptor.sort(key = lambda obj: obj[1]);
                    optic_descriptor.core_distance = neighbors_descriptor[self.__minpts - 1][1];
                    
                    self.__update_order_seed(optic_descriptor, neighbors_descriptor, order_seed);
                else:
                    optic_descriptor.core_distance = None;
                    
        else:
            optics_object.core_distance = None;

    
    def __extract_clusters(self):
        """!
        @brief Extract clusters and noise from order database.
        
        """
     
        self.__clusters = [];
        self.__noise = [];

        current_cluster = [];
        for optics_object in self.__ordered_database:
            if ((optics_object.reachability_distance is None) or (optics_object.reachability_distance > self.__eps)):
                if ((optics_object.core_distance is not None) and (optics_object.core_distance <= self.__eps)):
                    if (len(current_cluster) > 0):
                        self.__clusters.append(current_cluster);
                        current_cluster = [];
                        
                    current_cluster.append(optics_object.index_object);
                else:
                    self.__noise.append(optics_object.index_object);
            else:
                current_cluster.append(optics_object.index_object);
        
        if (len(current_cluster) > 0):
            self.__clusters.append(current_cluster);
                

    def __update_order_seed(self, optic_descriptor, neighbors_descriptors, order_seed):
        """!
        @brief Update sorted list of reachable objects (from core-object) that should be processed using neighbors of core-object.
        
        @param[in] optic_descriptor (optics_descriptor): Core-object whose neighbors should be analysed.
        @param[in] neighbors_descriptors (list): List of neighbors of core-object.
        @param[in|out] order_seed (list): List of sorted object in line with reachable distance.
        
        """
        
        for neighbor_descriptor in neighbors_descriptors:
            index_neighbor = neighbor_descriptor[0];
            current_reachable_distance = neighbor_descriptor[1];
            
            if (self.__optics_objects[index_neighbor].processed != True):
                reachable_distance = max(current_reachable_distance, optic_descriptor.core_distance);
                if (self.__optics_objects[index_neighbor].reachability_distance is None):
                    self.__optics_objects[index_neighbor].reachability_distance = reachable_distance;
                    
                    # insert element in queue O(n) - worst case.
                    index_insertion = len(order_seed);
                    for index_seed in range(0, len(order_seed)):
                        if (reachable_distance < order_seed[index_seed].reachability_distance):
                            index_insertion = index_seed;
                            break;
                    
                    order_seed.insert(index_insertion, self.__optics_objects[index_neighbor]);

                else:
                    if (reachable_distance < self.__optics_objects[index_neighbor].reachability_distance):
                        self.__optics_objects[index_neighbor].reachability_distance = reachable_distance;
                        order_seed.sort(key = lambda obj: obj.reachability_distance);


    def __neighbor_indexes(self, optic_object):
        """!
        @brief Return list of indexes of neighbors of specified point for the data.
        
        @param[in] optic_object (optics_descriptor): Object for which neighbors should be returned in line with connectivity radius.
        
        @return (list) List of indexes of neighbors in line the connectivity radius.
        
        """
              
        neighbor_description = [];
        
        for index in range(0, len(self.__sample_pointer), 1):
            if (index == optic_object.index_object):
                continue;
            
            distance = euclidean_distance(self.__sample_pointer[optic_object.index_object], self.__sample_pointer[index]);
            if (distance <= self.__eps):
                neighbor_description.append( [index, distance] );
            
        return neighbor_description;