"""!

@brief Examples of usage and demonstration of abilities of G-Means algorithm in cluster analysis.

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


from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.gmeans import gmeans

from pyclustering.utils import read_sample


def template_clustering(sample_path, k_init=1, ccore=True, **kwargs):
    sample = read_sample(sample_path)

    gmeans_instance = gmeans(sample, k_init, ccore, repeat=5).process()
    clusters = gmeans_instance.get_clusters()
    centers = gmeans_instance.get_centers()

    visualize = kwargs.get('visualize', True)
    if visualize:
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.append_cluster(centers, None, marker='*', markersize=10)
        visualizer.show()

    return sample, clusters


def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)

def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2)

def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

def cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)

def cluster_sample5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5)

def cluster_sample6():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6)

def cluster_sample7():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7)

def cluster_sample8():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8)

def cluster_sample9():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9)

def cluster_sample10():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE10)

def cluster_sample11():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11)

def cluster_sample12():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12)

def cluster_sample13():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE13)

def cluster_sample14():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE14)

def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE)

def cluster_lsun():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN)

def cluster_tetra():
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA)

def cluster_hepta():
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA)

def cluster_two_diamonds():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

def cluster_chainlink():
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK)

def cluster_wingnut():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT)

def cluster_atom():
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM)

def cluster_engytime():
    template_clustering(FCPS_SAMPLES.SAMPLE_ENGY_TIME)


def display_simple_clustering_results():
    (simple1, simple1_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, visualize=False)
    (simple2, simple2_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, visualize=False)
    (simple3, simple3_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, visualize=False)
    (simple4, simple4_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, visualize=False)
    (simple5, simple5_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, visualize=False)
    (simple6, simple6_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, visualize=False)
    (simple7, simple7_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, visualize=False)
    (simple8, simple8_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, visualize=False)
    (simple9, simple9_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, visualize=False)

    visualizer = cluster_visualizer(9, 3)
    visualizer.append_clusters(simple1_clusters, simple1, 0, markersize=3)
    visualizer.append_clusters(simple2_clusters, simple2, 1, markersize=3)
    visualizer.append_clusters(simple3_clusters, simple3, 2, markersize=3)
    visualizer.append_clusters(simple4_clusters, simple4, 3, markersize=3)
    visualizer.append_clusters(simple5_clusters, simple5, 4, markersize=3)
    visualizer.append_clusters(simple6_clusters, simple6, 5, markersize=6)
    visualizer.append_clusters(simple7_clusters, simple7, 6, markersize=6)
    visualizer.append_clusters(simple8_clusters, simple8, 7, markersize=6)
    visualizer.append_clusters(simple9_clusters, simple9, 8, markersize=6)
    visualizer.show()


def display_fcps_clustering_results():
    (simple3, simple3_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, visualize=False)
    (lsun, lsun_clusters) = template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, visualize=False)
    (target, target_clusters) = template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, visualize=False)
    (two_diamonds, two_diamonds_clusters) = template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, visualize=False)
    (wing_nut, wing_nut_clusters) = template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, visualize=False)
    (chainlink, chainlink_clusters) = template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, visualize=False)
    (hepta, hepta_clusters) = template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, visualize=False)
    (tetra, tetra_clusters) = template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, visualize=False)
    (atom, atom_clusters) = template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, visualize=False)

    visualizer = cluster_visualizer(9, 3)
    visualizer.append_clusters(simple3_clusters, simple3, 0, markersize=3)
    visualizer.append_clusters(lsun_clusters, lsun, 1, markersize=3)
    visualizer.append_clusters(target_clusters, target, 2, markersize=3)
    visualizer.append_clusters(two_diamonds_clusters, two_diamonds, 3, markersize=3)
    visualizer.append_clusters(wing_nut_clusters, wing_nut, 4, markersize=3)
    visualizer.append_clusters(chainlink_clusters, chainlink, 5, markersize=6)
    visualizer.append_clusters(hepta_clusters, hepta, 6, markersize=6)
    visualizer.append_clusters(tetra_clusters, tetra, 7, markersize=6)
    visualizer.append_clusters(atom_clusters, atom, 8, markersize=6)
    visualizer.show()


cluster_sample1()
cluster_sample2()
cluster_sample3()
cluster_sample4()
cluster_sample5()
cluster_sample6()
cluster_sample7()
cluster_sample8()
cluster_sample9()
cluster_sample10()
cluster_sample11()
cluster_sample12()
cluster_sample13()
cluster_sample14()
cluster_elongate()
cluster_lsun()
cluster_tetra()
cluster_hepta()
cluster_two_diamonds()
cluster_chainlink()
cluster_wingnut()
cluster_atom()
cluster_engytime()

# display_simple_clustering_results()
# display_fcps_clustering_results()
