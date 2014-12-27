'''

Cluster analysis algorithm: BIRCH

Based on article description:
 - T.Zhang, R.Ramakrishnan, M.Livny. BIRCH: An Efficient Data Clustering Method for Very Large Databases. 1996.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from support import linear_sum, square_sum;
from support.cftree import cftree, cfentry, measurement_type;

from copy import copy;

class birch:
    __pointer_data = None;
    __number_clusters = 0;
    
    __features = None;
    __tree = None;
    
    __measurement_type = None;
    __entry_size_limit = 0;
    
    __clusters = None;
    __noise = None;
    
    __ccore = False;
    
    def __init__(self, data, number_clusters, branching_factor = 5, max_node_entries = 5, initial_diameter = 0.1, type_measurement = measurement_type.CENTROID_EUCLIDIAN_DISTANCE, entry_size_limit = 200, ccore = False):
        self.__pointer_data = data;
        self.__number_clusters = number_clusters;
        
        self.__measurement_type = type_measurement;
        self.__entry_size_limit = entry_size_limit;
        self.__ccore = ccore;
        
        self.__tree = cftree(branching_factor, max_node_entries, initial_diameter, type_measurement);
               
        
    def process(self):
        self.__insert_data();
        
        # copy all leaf clustering features
        self.__features = [ copy(node.feature) for node in self.__tree.leafes ];
        
        # in line with specification modify hierarchical algorithm should be used for further clustering
        current_number_clusters = len(self.__features);
        while (current_number_clusters > self.__number_clusters):
            indexes = self.__find_nearest_cluster_features();
            
            self.__features[indexes[0]] += self.__features[indexes[1]];
            self.__features.pop(indexes[1]);
            
            current_number_clusters = len(self.__features);
            
        # decode data
        self.__clusters = [ [] for i in range(self.__number_clusters) ];
        
        for index_point in range(0, len(self.__pointer_data)):
            cluster_index = self.__get_nearest_feature(self.__pointer_data[index_point]);
            self.__clusters[cluster_index].append(index_point);
            
#         for index in range(len(self.__clusters)):
#             print("cluster:", self.__clusters[index]);
#             print("feature:", self.__features[index]);
#         
#         print();
        
    def get_clusters(self):
        return self.__clusters;
    
    
    def __insert_data(self):
        for index_point in range(0, len(self.__pointer_data)):
            point = self.__pointer_data[index_point];
            self.__tree.insert_cluster( [ point ] );
            
            if (self.__tree.amount_entries > self.__entry_size_limit):
                self.__tree = self.__rebuild_tree(index_point);
    
    
    def __rebuild_tree(self, index_point):
        rebuild_result = False;
        increased_diameter = self.__tree.threshold * 1.5;
        
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
                    increased_diameter *= 1.5;
                    continue;
            
            # Re-build is successful.
            rebuild_result = True;
        
        return tree;
    
    
    def __find_nearest_cluster_features(self):
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
    
    
    def __get_nearest_feature(self, point):
        minimum_distance = float("Inf");
        index_nearest_feature = -1;
        
        for index_entry in range(0, len(self.__features)):
            point_entry = cfentry(1, linear_sum([ point ]), square_sum([ point ]));
            
            distance = self.__features[index_entry].get_distance(point_entry, self.__measurement_type);
            if (distance < minimum_distance):
                minimum_distance = distance;
                index_nearest_feature = index_entry;
                
        return index_nearest_feature;
                
        