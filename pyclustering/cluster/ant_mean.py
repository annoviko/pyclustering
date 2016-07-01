'''
Created on Jul 1, 2016

@author: alex
'''

import pyclustering.core.ant_mean_clustering_wrapper as wrapper


class ant_mean_clustering_params:
    
    def __init__(self):
        
        ## used for pheramone evaporation
        self.ro                 = 0.9
        
        ## initial value for pheramones
        self.pheramone_init     = 0.1
        
        ## amount of iterations that is used for solving
        self.iterations         = 50
        
        ## amount of ants that is used on each iteration
        self.count_ants         = 20
        
        
class ant_mean:
    
    def __init__(self, parameters):
        
        self.__parameters = None
        
        if (parameters is None):
            self.__parameters = ant_mean_clustering_params();
        else:
            self.__parameters = parameters;
            
    
    def process(self, count_clusters, samples):
        
        return wrapper.ant_mean_clustering_process(self.__parameters, count_clusters, samples)
        
        