"""!

@brief Examples of usage and demonstration of abilities of BIRCH algorithm in cluster analysis.

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

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.birch import birch

from pyclustering.container.cftree import measurement_type

from pyclustering.utils import read_sample

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES


def template_clustering(number_clusters, path, branching_factor=50, max_node_entries=100, initial_diameter=0.5, type_measurement=measurement_type.CENTROID_EUCLIDEAN_DISTANCE, entry_size_limit=200, diameter_multiplier=1.5, show_result=True):
    print("Sample: ", path)

    sample = read_sample(path)

    birch_instance = birch(sample, number_clusters, branching_factor, max_node_entries, initial_diameter,
                           type_measurement, entry_size_limit, diameter_multiplier)
    birch_instance.process()
    clusters = birch_instance.get_clusters()

    if show_result is True:
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.show()
    
    return sample, clusters


def cluster_sample1():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 5, 5, 0.1, measurement_type.CENTROID_EUCLIDEAN_DISTANCE, 2)      # only two entries available

def cluster_sample2():
    template_clustering(3, SIMPLE_SAMPLES.SAMPLE_SIMPLE2)

def cluster_sample3():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE3)

def cluster_sample4():
    template_clustering(5, SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
    
def cluster_sample5():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE5)

def cluster_sample7():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE7)

def cluster_sample8():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE8)

def cluster_elongate():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_ELONGATE)

def cluster_lsun():
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN)

def cluster_lsun_rebuilt():
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN, entry_size_limit=20, diameter_multiplier=1.5)

def cluster_target():
    template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET)

def cluster_two_diamonds():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

def cluster_wing_nut():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT)

def cluster_chainlink():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_CHAINLINK)

def cluster_hepta():
    template_clustering(7, FCPS_SAMPLES.SAMPLE_HEPTA)

def cluster_tetra():
    template_clustering(4, FCPS_SAMPLES.SAMPLE_TETRA)

def cluster_engy_time():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_ENGY_TIME)


def experiment_execution_time(ccore=False):
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
    template_clustering(3, SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
    template_clustering(5, SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE5)
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_ELONGATE)
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN)
    template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET)
    template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)
    template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT)
    template_clustering(2, FCPS_SAMPLES.SAMPLE_CHAINLINK)
    template_clustering(7, FCPS_SAMPLES.SAMPLE_HEPTA)
    template_clustering(4, FCPS_SAMPLES.SAMPLE_TETRA)
    template_clustering(2, FCPS_SAMPLES.SAMPLE_ATOM)


def display_fcps_clustering_results():
    (lsun, lsun_clusters) = template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN, show_result=False)
    (target, target_clusters) = template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET, show_result=False)
    (two_diamonds, two_diamonds_clusters) = template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, show_result=False)
    (wing_nut, wing_nut_clusters) = template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT, show_result=False)
    (chainlink, chainlink_clusters) = template_clustering(2, FCPS_SAMPLES.SAMPLE_CHAINLINK, show_result=False)
    (hepta, hepta_clusters) = template_clustering(7, FCPS_SAMPLES.SAMPLE_HEPTA, show_result=False)
    (tetra, tetra_clusters) = template_clustering(4, FCPS_SAMPLES.SAMPLE_TETRA, show_result=False)
    (atom, atom_clusters) = template_clustering(2, FCPS_SAMPLES.SAMPLE_ATOM, show_result=False)
    
    visualizer = cluster_visualizer(8, 4)
    visualizer.append_clusters(lsun_clusters, lsun, 0)
    visualizer.append_clusters(target_clusters, target, 1)
    visualizer.append_clusters(two_diamonds_clusters, two_diamonds, 2)
    visualizer.append_clusters(wing_nut_clusters, wing_nut, 3)
    visualizer.append_clusters(chainlink_clusters, chainlink, 4)
    visualizer.append_clusters(hepta_clusters, hepta, 5)
    visualizer.append_clusters(tetra_clusters, tetra, 6)
    visualizer.append_clusters(atom_clusters, atom, 7)
    visualizer.show()


cluster_sample1()
cluster_sample2()
cluster_sample3()
cluster_sample4()
cluster_sample5()
cluster_sample7()
cluster_sample8()
cluster_elongate()
cluster_lsun()
cluster_lsun_rebuilt()
cluster_target()
cluster_two_diamonds()
cluster_wing_nut()
cluster_chainlink()
cluster_hepta()
cluster_tetra()
cluster_engy_time()

experiment_execution_time(True)    # C++ code + Python env.

display_fcps_clustering_results()
