"""!

@brief Examples of usage and demonstration of abilities of clustering algorithms from cluster module.

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

from random import random;

from pyclustering.cluster.agglomerative     import agglomerative;
from pyclustering.cluster.birch             import birch;
from pyclustering.cluster.clarans           import clarans;
from pyclustering.cluster.cure              import cure;
from pyclustering.cluster.dbscan            import dbscan;
from pyclustering.cluster.hsyncnet          import hsyncnet;
from pyclustering.cluster.kmeans            import kmeans;
from pyclustering.cluster.kmedians          import kmedians;
from pyclustering.cluster.kmedoids          import kmedoids;
from pyclustering.cluster.optics            import optics;
from pyclustering.cluster.rock              import rock;
from pyclustering.cluster.syncnet           import syncnet;
from pyclustering.cluster.syncsom           import syncsom;
from pyclustering.cluster.xmeans            import xmeans;

from pyclustering.utils import timedcall;

NUMBER_CLUSTERS = 3;

def simple_gaussian_data_clustering(cluster_sizes):
    algorithms_times = { 'agglomerative':   [],
                         'birch':           [],
                         'clarans':         [],
                         'cure':            [],
                         'dbscan':          [],
                         'hsyncnet':        [],
                         'kmeans':          [] };
#                          'kmedians':        [],
#                          'kmedoids':        [],
#                          'optics':          [],
#                          'rock':            [],
#                          'syncnet':         [],
#                          'syncsom':         [],
#                          'xmeans':          [] };

    algorithms_proc = { 'agglomerative':   process_agglomerative,
                        'birch':           process_birch,
                        'clarans':         process_clarans,
                        'cure':            process_cure,
                        'dbscan':          process_dbscan,
                        'hsyncnet':        process_hsyncnet,
                        'kmeans':          process_kmeans };
    
    for cluster_size in cluster_sizes:
        # generate data sets
        dataset = [];
        for mean in range(0, NUMBER_CLUSTERS, 1):
            dataset += [ [random() + (mean * 5), random() + (mean * 5)] for _ in range(cluster_size) ];
        
        # process data and fix time of execution
        for key in algorithms_proc:
            algorithms_times[key].append( algorithms_proc[key](dataset) );
            
    print(algorithms_times);


def process_agglomerative(sample):
    instance = agglomerative(sample, NUMBER_CLUSTERS);
    (ticks, _) = timedcall(instance.process);
    return ticks;

def process_birch(sample):
    instance = birch(sample, NUMBER_CLUSTERS);
    (ticks, _) = timedcall(instance.process);
    return ticks;

def process_clarans(sample):
    instance = clarans(sample, NUMBER_CLUSTERS, 10, 3);
    (ticks, _) = timedcall(instance.process);
    return ticks;

def process_cure(sample):
    instance = cure(sample, NUMBER_CLUSTERS);
    (ticks, _) = timedcall(instance.process);
    return ticks;

def process_dbscan(sample):
    instance = dbscan(sample, 1.0, 2);
    (ticks, _) = timedcall(instance.process);
    return ticks;

def process_hsyncnet(sample):
    instance = hsyncnet(sample, 3);
    (ticks, _) = timedcall(instance.process);
    return ticks;

def process_kmeans(sample):
    instance = kmeans(sample, [ [random() * index, random() * index] for index in range(1, NUMBER_CLUSTERS + 1, 1) ]);
    (ticks, _) = timedcall(instance.process);
    return ticks;


simple_gaussian_data_clustering([5, 8, 11, 14]);