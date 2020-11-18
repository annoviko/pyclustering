"""!

@brief Examples of usage and demonstration of abilities of CLARANS algorithm in cluster analysis.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from pyclustering.cluster.clarans import clarans;

from pyclustering.utils import read_sample;
from pyclustering.utils import draw_clusters;
from pyclustering.utils import timedcall;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;


def template_clustering(number_clusters, path, iterations, maxneighbors):
    sample = read_sample(path);

    clarans_instance = clarans(sample, number_clusters, iterations, maxneighbors);
    (ticks, result) = timedcall(clarans_instance.process);

    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");

    clusters = clarans_instance.get_clusters();
    draw_clusters(sample, clusters);


def cluster_sample1():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 10, 3);

def cluster_sample2():
    template_clustering(3, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 10, 3);

def cluster_sample3():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 10, 3);

def cluster_sample4():
    template_clustering(5, SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 4);
    
def cluster_sample5():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 10, 5);

def cluster_sample6():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE6, 10, 3);

def cluster_sample7():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 10, 3);

def cluster_sample8():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 15, 5);

def cluster_elongate():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_ELONGATE, 2, 2);

def cluster_lsun():
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN, 2, 2);

def cluster_target():
    template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET, 2, 2);

def cluster_two_diamonds():
    # tooo long
    template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 2, 2);

def cluster_wing_nut():
    # too long
    template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT, 2, 2);

def cluster_chainlink():
    # too long
    template_clustering(2, FCPS_SAMPLES.SAMPLE_CHAINLINK, 2, 2);

def cluster_hepta():
    template_clustering(7, FCPS_SAMPLES.SAMPLE_HEPTA, 2, 2); 

def cluster_tetra():
    template_clustering(4, FCPS_SAMPLES.SAMPLE_TETRA, 2, 2);

def cluster_engy_time():
    # too long
    template_clustering(2, FCPS_SAMPLES.SAMPLE_ENGY_TIME, 2, 2);


cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_sample4();
cluster_sample5();
cluster_sample6();
cluster_sample7();
cluster_sample8();
cluster_elongate();
 
cluster_lsun();
cluster_target();
cluster_two_diamonds();   # too long
cluster_wing_nut();       # too long
cluster_chainlink();      # too long
cluster_hepta();
cluster_tetra();
cluster_engy_time();      # too long