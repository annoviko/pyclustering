"""!

@brief Examples of usage and demonstration of abilities of Fuzzy C-Means algorithm in cluster analysis.

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

import random

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES, FAMOUS_SAMPLES

from pyclustering.cluster import cluster_visualizer_multidim
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.fcm import fcm

from pyclustering.utils import read_sample
from pyclustering.utils import timedcall


def template_clustering(start_centers, path):
    sample = read_sample(path)

    fcm_instance = fcm(sample, start_centers)
    fcm_instance.process()

    clusters = fcm_instance.get_clusters()
    centers = fcm_instance.get_centers()
    membership = fcm_instance.get_membership()

    visualizer = cluster_visualizer_multidim()
    visualizer.append_clusters(clusters, sample)
    visualizer.append_cluster(centers, marker='*', markersize=10)
    visualizer.show()


def cluster_sample1():
    start_centers = [[4.7, 5.9], [5.7, 6.5]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE1)


def cluster_sample2():
    start_centers = [[3.5, 4.8], [6.9, 7], [7.5, 0.5]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE2)


def cluster_sample3():
    start_centers = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE3)


def cluster_sample4():
    start_centers = [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE4)


def cluster_sample5():
    start_centers = [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE5)


def cluster_sample6():
    start_centers = [[2.0, 6.0], [8.5, 4.5]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE6)


def cluster_sample7():
    start_centers = [[-3.0], [2.5]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE7)


def cluster_sample8():
    start_centers = [[-4.0], [3.1], [6.1], [12.0]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_SIMPLE8)


def cluster_elongate():
    "Not so applicable for this sample"
    start_centers = [[1.0, 4.5], [3.1, 2.7]]
    template_clustering(start_centers, SIMPLE_SAMPLES.SAMPLE_ELONGATE)


def cluster_lsun():
    "Not so applicable for this sample"
    start_centers = [[1.0, 3.5], [2.0, 0.5], [3.0, 3.0]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_LSUN)


def cluster_target():
    "Not so applicable for this sample"
    start_centers = [[0.2, 0.2], [0.0, -2.0], [3.0, -3.0], [3.0, 3.0], [-3.0, 3.0], [-3.0, -3.0]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TARGET)


def cluster_two_diamonds():
    start_centers = [[0.8, 0.2], [3.0, 0.0]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)


def cluster_wing_nut():
    "Almost good!"
    start_centers = [[-1.5, 1.5], [1.5, 1.5]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_WING_NUT)


def cluster_chainlink():
    start_centers = [[1.1, -1.7, 1.1], [-1.4, 2.5, -1.2]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_CHAINLINK)


def cluster_hepta():
    start_centers = [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [-2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, -3.0, 0.0],
                     [0.0, 0.0, 2.5], [0.0, 0.0, -2.5]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_HEPTA)


def cluster_tetra():
    start_centers = [[1, 0, 0], [0, 1, 0], [0, -1, 0], [-1, 0, 0]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_TETRA)


def cluster_engy_time():
    start_centers = [[0.5, 0.5], [2.3, 2.9]]
    template_clustering(start_centers, FCPS_SAMPLES.SAMPLE_ENGY_TIME)


def cluster_iris():
    start_centers = kmeans_plusplus_initializer(read_sample(FAMOUS_SAMPLES.SAMPLE_IRIS), 4).initialize()
    template_clustering(start_centers, FAMOUS_SAMPLES.SAMPLE_IRIS)

cluster_sample1()
cluster_sample2()
cluster_sample3()
cluster_sample4()
cluster_sample5()
cluster_sample6()
cluster_sample7()
cluster_sample8()
cluster_elongate()
cluster_lsun()
cluster_target()
cluster_two_diamonds()
cluster_wing_nut()
cluster_chainlink()
cluster_hepta()
cluster_tetra()
cluster_engy_time()
cluster_iris()