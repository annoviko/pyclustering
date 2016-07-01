'''
Created on Jul 1, 2016

@author: alex
'''

import unittest;

from pyclustering.cluster.ant_mean import ant_mean;


class Test(unittest.TestCase):
    
    def process(self, samples, clusters):
        
        algo = ant_mean(None)
        res = algo.process(len(clusters), samples)
        
        """
            Testing clusters
        """
        for i in range(len(res)):
            res[i].sort()
        
        for i in range(len(clusters)):
            clusters[i].sort()
            
            for j in range(len(res)):
                foundCl = True
                
                for k in range(len(clusters[i])):
                    if (clusters[i][k] != res[j][k]):
                        foundCl = False
                        break;
                
                if (foundCl):
                    break
            
            assert (foundCl)
                    
        
    
    def testSimpleTwoClusters(self):
        self.process([[ 0,0 ],[ 1,1 ],[ 10,10 ],[ 11,11 ],[ -2, -2 ],[ 0.55, -1.26 ],[ 13.25, 12.12 ]], [[0, 1, 4, 5], [2, 3, 6]])
        
        
        
         