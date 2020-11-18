"""!

@brief Examples of usage and demonstration of abilities of CLIQUE algorithm in cluster analysis.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import os

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.clique import clique, clique_visualizer

from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES


def template_clustering(data_path, intervals, density_threshold, **kwargs):
    print("Sample: '%s'." % os.path.basename(data_path))

    data = read_sample(data_path)

    clique_instance = clique(data, intervals, density_threshold)
    clique_instance.process()

    clusters = clique_instance.get_clusters()
    noise = clique_instance.get_noise()
    cells = clique_instance.get_cells()

    print([len(cluster) for cluster in clusters])

    clique_visualizer.show_grid(cells, data)

    visualizer = cluster_visualizer()
    visualizer.append_clusters(clusters, data)
    visualizer.append_cluster(noise, data, marker='x')
    visualizer.show()


def cluster_simple_sample():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 8, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 15, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 7, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 7, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 5, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 7, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 2, 0)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 7, 0)


def cluster_fcps():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 15, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 15, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 15, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 10, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 9, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 10, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 10, 0)
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, 10, 0)


cluster_simple_sample()
cluster_fcps()
