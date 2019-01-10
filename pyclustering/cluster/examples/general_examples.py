"""!

@brief Examples of usage and demonstration of abilities of clustering algorithms from cluster module.

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

from random import random, randint
from math import floor

import matplotlib.pyplot as plt

from pyclustering.nnet import initial_type

from pyclustering.cluster.agglomerative     import agglomerative
from pyclustering.cluster.birch             import birch
from pyclustering.cluster.clarans           import clarans
from pyclustering.cluster.cure              import cure
from pyclustering.cluster.dbscan            import dbscan
from pyclustering.cluster.hsyncnet          import hsyncnet
from pyclustering.cluster.kmeans            import kmeans
from pyclustering.cluster.kmedians          import kmedians
from pyclustering.cluster.kmedoids          import kmedoids
from pyclustering.cluster.optics            import optics
from pyclustering.cluster.rock              import rock
from pyclustering.cluster.syncnet           import syncnet
from pyclustering.cluster.syncsom           import syncsom
from pyclustering.cluster.xmeans            import xmeans

from pyclustering.utils import timedcall

CLUSTER_SIZES = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
NUMBER_CLUSTERS = 4
CURRENT_CLUSTER_SIZE = None
REPEAT_MEASURE = 15

def simple_gaussian_data_clustering(cluster_sizes):
    algorithms_times = { 
                        'agglomerative':   [],
                        'birch':           [],
                        'clarans':         [],
                        'cure':            [],
                        'dbscan':          [],
                        'hsyncnet':        [],
                        'kmeans':          [],
                        'kmedians':        [], 
                        'kmedoids':        [],
                        'optics':          [],
                        'rock':            [],
                        'syncnet':         [],
                        'syncsom':         [],
                        'xmeans':          [],
                       }
                        
    algorithms_proc = { 
                        'agglomerative':    process_agglomerative,
                        'birch':            process_birch,
                        'clarans':          process_clarans,
                        'cure':             process_cure,
                        'dbscan':           process_dbscan,
                        'hsyncnet':         process_hsyncnet,
                        'kmeans':           process_kmeans,
                        'kmedians':         process_kmedians,
                        'kmedoids':         process_kmedoids,
                        'optics':           process_optics,
                        'rock':             process_rock,
                        'syncnet':          process_syncnet,
                        'syncsom':          process_syncsom,
                        'xmeans':           process_xmeans,
                      }
    
    datasizes = []
    
    for cluster_size in cluster_sizes:
        print("processing clusters with size:", cluster_size)
        
        global CURRENT_CLUSTER_SIZE
        CURRENT_CLUSTER_SIZE = cluster_size
        
        # generate data sets
        dataset = []
        for mean in range(0, NUMBER_CLUSTERS, 1):
            dataset += [ [random() + (mean * 5), random() + (mean * 5)] for _ in range(cluster_size) ]
        
        datasizes.append(len(dataset))
            
        # process data and fix time of execution
        for key in algorithms_proc:
            summary_result = 0
            print("processing clusters with size:", cluster_size, "by", key)
            
            for _ in range(REPEAT_MEASURE):
                summary_result += algorithms_proc[key](dataset)
            
            algorithms_times[key].append( summary_result / REPEAT_MEASURE )
    
    print(datasizes)
    for key in algorithms_times:
        print(key, ":", algorithms_times[key])
        plt.plot(datasizes, algorithms_times[key], label = key, linestyle = '-')
    
    plt.show()


def process_agglomerative(sample):
    instance = agglomerative(sample, NUMBER_CLUSTERS)
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_birch(sample):
    instance = birch(sample, NUMBER_CLUSTERS)
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_clarans(sample):
    instance = clarans(sample, NUMBER_CLUSTERS, 10, 3)
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_cure(sample):
    instance = cure(sample, NUMBER_CLUSTERS)
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_dbscan(sample):
    instance = dbscan(sample, 1.0, 2)
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_hsyncnet(sample):
    instance = hsyncnet(sample, CURRENT_CLUSTER_SIZE, initial_type.EQUIPARTITION, CURRENT_CLUSTER_SIZE)
    (ticks, _) = timedcall(instance.process, 0.998)
    return ticks

def process_kmeans(sample):
    instance = kmeans(sample, [ [random() + (multiplier * 5), random() + (multiplier + 5)] for multiplier in range(NUMBER_CLUSTERS) ])
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_kmedians(sample):
    instance = kmedians(sample, [ [random() + (multiplier * 5), random() + (multiplier + 5)] for multiplier in range(NUMBER_CLUSTERS) ])
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_kmedoids(sample):
    instance = kmedoids(sample, [ CURRENT_CLUSTER_SIZE * multiplier for multiplier in range(NUMBER_CLUSTERS) ])
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_optics(sample):
    instance = optics(sample, 1.0, 2)
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_rock(sample):
    instance = rock(sample, 1, NUMBER_CLUSTERS, 0.5)
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_syncnet(sample):
    instance = syncnet(sample, 3.0, initial_phases = initial_type.EQUIPARTITION)
    (ticks, _) = timedcall(instance.process)
    return ticks

def process_syncsom(sample):
    instance = syncsom(sample, 1, NUMBER_CLUSTERS)
    (ticks, _) = timedcall(instance.process, 0, False, 0.998)
    return ticks

def process_xmeans(sample):
    instance = xmeans(sample, [ [random() + (multiplier * 5), random() + (multiplier + 5)] for multiplier in range(NUMBER_CLUSTERS) ])
    (ticks, _) = timedcall(instance.process)
    return ticks


simple_gaussian_data_clustering(CLUSTER_SIZES)