"""!

@brief Examples of center initializer API.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES
from pyclustering.samples.definitions import FCPS_SAMPLES

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer


def template_kmeans_plusplus_initializer(path, amount, draw=True):
    sample = read_sample(path)
    centers = kmeans_plusplus_initializer(sample, amount, 1).initialize()
    
    if draw is True:
        visualizer = cluster_visualizer()
        visualizer.append_cluster(sample)
        visualizer.append_cluster(centers, marker='*', markersize=10)
        visualizer.show()
    
    return sample, centers


def kmeans_plusplus_initializer_sample_simple_01():
    template_kmeans_plusplus_initializer(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2)

def kmeans_plusplus_initializer_sample_simple_02():
    template_kmeans_plusplus_initializer(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3)

def kmeans_plusplus_initializer_sample_simple_03():
    template_kmeans_plusplus_initializer(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4)

def kmeans_plusplus_initializer_sample_simple_04():
    template_kmeans_plusplus_initializer(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5)

def kmeans_plusplus_initializer_sample_simple_05():
    template_kmeans_plusplus_initializer(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4)

def kmeans_plusplus_initializer_collection():
    (sample1, centers1) = template_kmeans_plusplus_initializer(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, False)
    (sample2, centers2) = template_kmeans_plusplus_initializer(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, False)
    (sample3, centers3) = template_kmeans_plusplus_initializer(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, False)
    (sample4, centers4) = template_kmeans_plusplus_initializer(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 2, False)
    
    visualizer = cluster_visualizer(4, 2)
    visualizer.append_cluster(sample1, canvas=0)
    visualizer.append_cluster(centers1, canvas=0, marker='*', markersize=10)
    
    visualizer.append_cluster(sample2, canvas=1)
    visualizer.append_cluster(centers2, canvas=1, marker='*', markersize=10)
    
    visualizer.append_cluster(sample3, canvas=2)
    visualizer.append_cluster(centers3, canvas=2, marker='*', markersize=10)
    
    visualizer.append_cluster(sample4, canvas=3)
    visualizer.append_cluster(centers4, canvas=3, marker='*', markersize=10)
    visualizer.show()

def kmeans_plusplus_initializer_fcps_lsun():
    template_kmeans_plusplus_initializer(FCPS_SAMPLES.SAMPLE_LSUN, 3)

def kmeans_plusplus_initializer_fcps_two_diamonds():
    template_kmeans_plusplus_initializer(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 2)


# kmeans_plusplus_initializer_sample_simple_01()
# kmeans_plusplus_initializer_sample_simple_02()
kmeans_plusplus_initializer_sample_simple_03()
kmeans_plusplus_initializer_sample_simple_03()
kmeans_plusplus_initializer_sample_simple_03()
kmeans_plusplus_initializer_sample_simple_03()
kmeans_plusplus_initializer_sample_simple_03()
kmeans_plusplus_initializer_sample_simple_03()
# kmeans_plusplus_initializer_sample_simple_04()
# kmeans_plusplus_initializer_sample_simple_05()
#
# kmeans_plusplus_initializer_collection()
#
# kmeans_plusplus_initializer_fcps_lsun()
# kmeans_plusplus_initializer_fcps_two_diamonds()
