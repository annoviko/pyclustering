'''

Cluster analysis algorithm: BIRCH

Based on article description:
 - T.Zhang, R.Ramakrishnan, M.Livny. BIRCH: An Efficient Data Clustering Method for Very Large Databases. 1996.

Implementation: Andrei Novikov (spb.andr@yandex.ru)

'''

from support import euclidean_distance_sqrt;
from support.cftree import cftree;
from scipy.stats.mstats_basic import threshold

class birch:
    __pointer_data = None;
    __tree = None;
    
    __entry_size_limit = 0;
    
    __clusters = None;
    
    __ccore = False;
    
    def __init__(self, data, branching_factor, max_node_entries, initial_diameter, type_measurement, entry_size_limit = 400, ccore = False):
        self.__pointer_data = data;
        
        self.__entry_size_limit = entry_size_limit;
        self.__ccore = ccore;
        
        self.__tree = cftree(branching_factor, max_node_entries, initial_diameter, type_measurement);
        
    def process(self):
        self.__insert_data();
        
    
    def get_clusters(self):
        return self.__clusters;
    
    def __insert_data(self):
        for index_point in range(0, len(self.__pointer_data)):
            point = self.__pointer_data[index_point];
            self.__tree.insert_cluster(point);
            
            if (self.__tree.amount_entries > self.__entry_size_limit):
                self.__tree = self.__rebuild_tree(index_point);
    
    
    def __rebuild_tree(self, index_end_point):
        rebuild_result = False;
        increased_diameter = self.__tree.threshold * 1.5;
        
        tree = None;
        
        while(rebuild_result is False):
            # increase diameter and rebuild tree
            if (increased_diameter == 0.0):
                increased_diameter = 1.0;
            
            # build tree with update parameters
            tree = cftree(self.__tree.branch_factor, self.__tree.max_entries, increased_diameter, self.__tree.type_measurement);
            
            for index_point in range(0, index_end_point):
                point = self.__pointer_data[index_point];
                tree.insert_cluster(point);
            
                if (tree.amount_entries > self.__entry_size_limit):
                    increased_diameter *= 1.5;
                    continue;
            
            # Re-build is successful.
            rebuild_result = True;
        
        return tree;
            
            
            
                
                