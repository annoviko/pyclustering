"""!

@brief Examples of usage and demonstration of abilities of TTSAS algorithm in cluster analysis.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

from pyclustering.cluster.bsas import bsas_visualizer;
from pyclustering.cluster.ttsas import ttsas;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from pyclustering.utils import read_sample;
from pyclustering.utils.metric import distance_metric, type_metric;


def template_clustering(path, threshold1, threshold2, **kwargs):
    metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE));
    ccore = kwargs.get('ccore', False);
    draw = kwargs.get('draw', True);

    sample = read_sample(path);

    print("Sample: ", path);

    ttsas_instance = ttsas(sample, threshold1, threshold2, ccore=ccore, metric=metric);
    ttsas_instance.process();

    clusters = ttsas_instance.get_clusters();
    representatives = ttsas_instance.get_representatives();

    if draw is True:
        bsas_visualizer.show_clusters(sample, clusters, representatives);


def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1.0, 2.0);

def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1.0, 2.0);

def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.0, 2.0);

def cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1.0, 2.0);

def cluster_sample5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1.0, 2.0);

def cluster_sample6():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, 1.0, 2.0);

def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 1.0, 2.0);

def cluster_two_diamonds():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1.0, 2.0);


cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_sample4();
cluster_sample5();
cluster_sample6();
cluster_elongate();
cluster_two_diamonds();