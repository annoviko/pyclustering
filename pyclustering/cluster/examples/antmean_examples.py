

from pyclustering.cluster.antmean import antmean

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.antmean import antmean
from pyclustering.cluster.antmean import antmean_clustering_params

from pyclustering.utils import read_sample

import time

import matplotlib.pyplot as plt


def template_clustering(path, count_clusters, iterations=50, count_ants=20, pheramone_init=0.1, ro=0.9):
    """ """

    params = antmean_clustering_params()
    params.iterations = iterations
    params.count_ants = count_ants
    params.pheramone_init = pheramone_init
    params.ro = ro

    #
    algo = antmean(params)

    #
    sample = read_sample(path)

    start_time = time.time()

    # Clustering ...
    res = algo.process(count_clusters, sample)

    print("Sample: ", path, "\t\tExecution time: ", time.time() - start_time, "\n")

    visualizer = cluster_visualizer(1)
    visualizer.append_clusters(res, sample)
    visualizer.show()


def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1,
                        count_clusters=2)


def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2,
                        count_clusters=3,
                        iterations=300,
                        count_ants=200,
                        pheramone_init=0.1,
                        ro=0.9)


def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3,
                        count_clusters=4,
                        iterations=700,
                        count_ants=1000,
                        pheramone_init=0.3,
                        ro=0.85)


def cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4,
                        count_clusters=5,
                        iterations=800,
                        count_ants=1000,
                        pheramone_init=0.3,
                        ro=0.9)


def cluster_sample5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5,
                        count_clusters=4,
                        iterations=800,
                        count_ants=1000,
                        pheramone_init=0.3,
                        ro=0.9)


def cluster_sample6():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6,
                        count_clusters=2,
                        iterations=300,
                        count_ants=200,
                        pheramone_init=0.1,
                        ro=0.9)


def cluster_sample7():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7,
                        count_clusters=2,
                        iterations=300,
                        count_ants=200,
                        pheramone_init=0.1,
                        ro=0.9)


def cluster_sample11():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11,
                        count_clusters=2,
                        iterations=300,
                        count_ants=200,
                        pheramone_init=0.1,
                        ro=0.9)

cluster_sample1()
cluster_sample2()
cluster_sample3()
cluster_sample4()
cluster_sample5()
cluster_sample6()
cluster_sample7()
cluster_sample11()


