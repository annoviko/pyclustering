"""!

@brief Examples of usage and demonstration of abilities of BANG algorithm in cluster analysis.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import os

from pyclustering.cluster.bang import bang, bang_visualizer, bang_animator

from pyclustering.utils import draw_image_mask_segments, read_sample, read_image

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES


def template_clustering(data_path, levels, **kwargs):
    print("Sample: '%s'." % os.path.basename(data_path))

    density_threshold = kwargs.get("density_threshold", 0.0)
    amount_threshold = kwargs.get("amount_threshold", 0)
    data = read_sample(data_path)

    bang_instance = bang(data, levels, density_threshold=density_threshold, amount_threshold=amount_threshold)
    bang_instance.process()

    clusters = bang_instance.get_clusters()
    noise = bang_instance.get_noise()
    directory = bang_instance.get_directory()
    dendrogram = bang_instance.get_dendrogram()

    bang_visualizer.show_blocks(directory)
    bang_visualizer.show_dendrogram(dendrogram)
    bang_visualizer.show_clusters(data, clusters, noise)

    if len(data[0]) == 2:
        animator = bang_animator(directory, clusters)
        animator.animate()
        # movie_filename = os.path.basename(data_path) + ".mp4"
        # animator.animate(movie_filename=movie_filename)


def template_segmentation(source, levels, threshold):
    data = read_image(source)

    bang_instance = bang(data, levels, threshold)
    bang_instance.process()

    clusters = bang_instance.get_clusters()

    draw_image_mask_segments(source, clusters)



def cluster_simple_sample():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 3)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 7)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 7)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, density_threshold=2.5)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 8)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 8)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, 7)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 4)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 7)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 7)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10, 7)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 7)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 7)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13, 7)
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 7)


def cluster_fcps():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 9)
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 11)
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 11)
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 10)
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 10)
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 11)
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 13)
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, 11)


cluster_simple_sample()
cluster_fcps()
