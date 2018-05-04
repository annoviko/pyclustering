"""!

@brief Cluster analysis algorithm: BIRCH
@details Implementation based on paper @cite article::birch::1.
         
@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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


from pyclustering.utils import linear_sum, square_sum;

from pyclustering.cluster.encoder import type_encoding;

from pyclustering.container.cftree import cftree, cfentry, measurement_type;


class birch:
    """!
    @brief Class represents clustering algorithm BIRCH.
    
    Example:
    @code
        # sample for cluster analysis (represented by list)
        sample = read_sample(path_to_sample);
        
        # create object of birch that uses CCORE for processing
        birch_instance = birch(sample, 2, 5, 5, 0.05, measurement_type.CENTROID_EUCLIDIAN_DISTANCE, 200, True);
        
        # cluster analysis
        birch_instance.process();
        
        # obtain results of clustering
        clusters = birch_instance.get_clusters();
    @endcode
    
    """
    
    def __init__(self, data, number_clusters, branching_factor = 5, max_node_entries = 5, initial_diameter = 0.1, type_measurement = measurement_type.CENTROID_EUCLIDEAN_DISTANCE, entry_size_limit = 200, diameter_multiplier = 1.5, ccore = True):
        """!
        @brief Constructor of clustering algorithm BIRCH.
        
        @param[in] data (list): Input data presented as list of points (objects), where each point should be represented by list or tuple.
        @param[in] number_clusters (uint): Number of clusters that should be allocated.
        @param[in] branching_factor (uint): Maximum number of successor that might be contained by each non-leaf node in CF-Tree.
        @param[in] max_node_entries (uint): Maximum number of entries that might be contained by each leaf node in CF-Tree.
        @param[in] initial_diameter (double): Initial diameter that used for CF-Tree construction, it can be increase if entry_size_limit is exceeded.
        @param[in] type_measurement (measurement_type): Type measurement used for calculation distance metrics.
        @param[in] entry_size_limit (uint): Maximum number of entries that can be stored in CF-Tree, if it is exceeded during creation then diameter is increased and CF-Tree is rebuilt.
        @param[in] diameter_multiplier (double): Multiplier that is used for increasing diameter when entry_size_limit is exceeded.
        @param[in] ccore (bool): If True than DLL CCORE (C++ solution) will be used for solving the problem.
        
        @remark Despite eight arguments only the first two is mandatory, others can be ommitted. In this case default values are used for instance creation.
        
        Example:
        @code
            birch_instance1 = birch(sample1, 2);    # two clusters should be allocated
            birch_instance2 = birch(sample2, 5);    # five clusters should be allocated
            
            # three clusters should be allocated, but also each leaf node can have maximum 5 
            # entries and each entry can have maximum 5 descriptors with initial diameter 0.05.
            birch_instance3 = birch(sample3, 3, 5, 5, 0.05);
        @endcode
        
        """
        
        self.__pointer_data = data;
        self.__number_clusters = number_clusters;
        
        self.__measurement_type = type_measurement;
        self.__entry_size_limit = entry_size_limit;
        self.__diameter_multiplier = diameter_multiplier;
        self.__ccore = ccore;
        
        self.__features = None;
        self.__tree = cftree(branching_factor, max_node_entries, initial_diameter, type_measurement);
        
        self.__clusters = [];
        self.__noise = [];


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of BIRCH algorithm.
        
        @remark Results of clustering can be obtained using corresponding gets methods.
        
        @see get_clusters()
        
        """
        
        self.__insert_data();
        self.__extract_features();

        # in line with specification modify hierarchical algorithm should be used for further clustering
        current_number_clusters = len(self.__features);
        
        while (current_number_clusters > self.__number_clusters):
            indexes = self.__find_nearest_cluster_features();
            
            self.__features[indexes[0]] += self.__features[indexes[1]];
            self.__features.pop(indexes[1]);
            
            current_number_clusters = len(self.__features);
            
        # decode data
        self.__decode_data();
    
    
    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @remark Allocated noise can be returned only after data processing (use method process() before). Otherwise empty list is returned.
        
        @return (list) List of allocated clusters.
        
        @see process()
        @see get_noise()
        
        """
        
        return self.__clusters;


    def get_cluster_encoding(self):
        """!
        @brief Returns clustering result representation type that indicate how clusters are encoded.
        
        @return (type_encoding) Clustering result representation.
        
        @see get_clusters()
        
        """
        
        return type_encoding.CLUSTER_INDEX_LIST_SEPARATION;


    def __extract_features(self):
        """!
        @brief Extracts features from CF-tree cluster.
        
        """
        
        self.__features = [];
        
        if (len(self.__tree.leafes) == 1):
            # parameters are too general, copy all entries
            for entry in self.__tree.leafes[0].entries:
                self.__features.append(entry);

        else:
            # copy all leaf clustering features
            for node in self.__tree.leafes:
                self.__features.append(node.feature);
    
    
    def __decode_data(self):
        """!
        @brief Decodes data from CF-tree features.
        
        """
        
        self.__clusters = [ [] for _ in range(self.__number_clusters) ];
        self.__noise = [];
        
        for index_point in range(0, len(self.__pointer_data)):
            (_, cluster_index) = self.__get_nearest_feature(self.__pointer_data[index_point], self.__features);
            
            self.__clusters[cluster_index].append(index_point);
    
    
    def __insert_data(self):
        """!
        @brief Inserts input data to the tree.
        
        @remark If number of maximum number of entries is exceeded than diameter is increased and tree is rebuilt.
        
        """
        
        for index_point in range(0, len(self.__pointer_data)):
            point = self.__pointer_data[index_point];
            self.__tree.insert_cluster( [ point ] );
            
            if (self.__tree.amount_entries > self.__entry_size_limit):
                self.__tree = self.__rebuild_tree(index_point);
        
        #self.__tree.show_feature_destibution(self.__pointer_data);
    
    
    def __rebuild_tree(self, index_point):
        """!
        @brief Rebuilt tree in case of maxumum number of entries is exceeded.
        
        @param[in] index_point (uint): Index of point that is used as end point of re-building.
        
        @return (cftree) Rebuilt tree with encoded points till specified point from input data space.
        
        """
        
        rebuild_result = False;
        increased_diameter = self.__tree.threshold * self.__diameter_multiplier;
        
        tree = None;
        
        while(rebuild_result is False):
            # increase diameter and rebuild tree
            if (increased_diameter == 0.0):
                increased_diameter = 1.0;
            
            # build tree with update parameters
            tree = cftree(self.__tree.branch_factor, self.__tree.max_entries, increased_diameter, self.__tree.type_measurement);
            
            for index_point in range(0, index_point + 1):
                point = self.__pointer_data[index_point];
                tree.insert_cluster([point]);
            
                if (tree.amount_entries > self.__entry_size_limit):
                    increased_diameter *= self.__diameter_multiplier;
                    continue;
            
            # Re-build is successful.
            rebuild_result = True;
        
        return tree;
    
    
    def __find_nearest_cluster_features(self):
        """!
        @brief Find pair of nearest CF entries.
        
        @return (list) List of two nearest enties that are represented by list [index_point1, index_point2].
        
        """
        
        minimum_distance = float("Inf");
        index1 = 0;
        index2 = 0;
        
        for index_candidate1 in range(0, len(self.__features)):
            feature1 = self.__features[index_candidate1];
            for index_candidate2 in range(index_candidate1 + 1, len(self.__features)):
                feature2 = self.__features[index_candidate2];
                
                distance = feature1.get_distance(feature2, self.__measurement_type);
                if (distance < minimum_distance):
                    minimum_distance = distance;
                    
                    index1 = index_candidate1;
                    index2 = index_candidate2;
        
        return [index1, index2];
    
    
    def __get_nearest_feature(self, point, feature_collection):
        """!
        @brief Find nearest entry for specified point.
        
        @param[in] point (list): Pointer to point from input dataset.
        @param[in] feature_collection (list): Feature collection that is used for obtaining nearest feature for the specified point.
        
        @return (double, uint) Tuple of distance to nearest entry to the specified point and index of that entry.
        
        """
        
        minimum_distance = float("Inf");
        index_nearest_feature = -1;
        
        for index_entry in range(0, len(feature_collection)):
            point_entry = cfentry(1, linear_sum([ point ]), square_sum([ point ]));
            
            distance = feature_collection[index_entry].get_distance(point_entry, self.__measurement_type);
            if (distance < minimum_distance):
                minimum_distance = distance;
                index_nearest_feature = index_entry;
                
        return (minimum_distance, index_nearest_feature);
