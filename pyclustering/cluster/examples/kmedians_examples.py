"""!

@brief Examples of usage and demonstration of abilities of K-Medians algorithm in cluster analysis.

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
from pyclustering.cluster.kmedians import kmedians

from pyclustering.utils import draw_clusters
from pyclustering.utils import read_sample
from pyclustering.utils import timedcall

def template_clustering(start_medians, path, tolerance = 0.25):
    sample = read_sample(path)
    
    kmedians_instance = kmedians(sample, start_medians, tolerance)
    (ticks, result) = timedcall(kmedians_instance.process)
    
    clusters = kmedians_instance.get_clusters()
    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n")

    draw_clusters(sample, clusters)
    
def cluster_sample1():
    start_medians = [[3.7, 5.5], [6.7, 7.5]]
    template_clustering(start_medians, SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
    
def cluster_sample2():
    start_medians = [[3.5, 4.8], [6.9, 7], [7.5, 0.5]]
    template_clustering(start_medians, SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
    
def cluster_sample3():
    start_medians = [[0.2, 0.1], [4.0, 1.0], [2.0, 2.0], [2.3, 3.9]]
    template_clustering(start_medians, SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
    
def cluster_sample4():
    start_medians = [[1.5, 0.0], [1.5, 2.0], [1.5, 4.0], [1.5, 6.0], [1.5, 8.0]]
    template_clustering(start_medians, SIMPLE_SAMPLES.SAMPLE_SIMPLE4)
    
def cluster_sample5():
    start_medians = [[0.0, 1.0], [0.0, 0.0], [1.0, 1.0], [1.0, 0.0]]
    template_clustering(start_medians, SIMPLE_SAMPLES.SAMPLE_SIMPLE5)
        
def cluster_elongate():
    start_medians = [[1.0, 4.5], [3.1, 2.7]]
    template_clustering(start_medians, SIMPLE_SAMPLES.SAMPLE_ELONGATE)

def cluster_lsun():
    start_medians = [[1.0, 3.5], [2.0, 0.5], [3.0, 3.0]]
    template_clustering(start_medians, FCPS_SAMPLES.SAMPLE_LSUN)
    
def cluster_target():
    start_medians = [[0.2, 0.2], [0.0, -2.0], [3.0, -3.0], [3.0, 3.0], [-3.0, 3.0], [-3.0, -3.0]]
    template_clustering(start_medians, FCPS_SAMPLES.SAMPLE_TARGET)

def cluster_two_diamonds():
    start_medians = [[0.8, 0.2], [3.0, 0.0]]
    template_clustering(start_medians, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

def cluster_wing_nut():
    start_medians = [[-1.5, 1.5], [1.5, 1.5]]
    template_clustering(start_medians, FCPS_SAMPLES.SAMPLE_WING_NUT)
    
def cluster_chainlink():
    start_medians = [[1.1, -1.7, 1.1], [-1.4, 2.5, -1.2]]
    template_clustering(start_medians, FCPS_SAMPLES.SAMPLE_CHAINLINK)
    
def cluster_hepta():
    start_medians = [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0], [-2.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, -3.0, 0.0], [0.0, 0.0, 2.5], [0.0, 0.0, -2.5]]
    template_clustering(start_medians, FCPS_SAMPLES.SAMPLE_HEPTA)
    
def cluster_tetra():
    start_medians = [[1, 0, 0], [0, 1, 0], [0, -1, 0], [-1, 0, 0]]
    template_clustering(start_medians, FCPS_SAMPLES.SAMPLE_TETRA)
    
def cluster_engy_time():
    start_medians = [[0.5, 0.5], [2.3, 2.9]]
    template_clustering(start_medians, FCPS_SAMPLES.SAMPLE_ENGY_TIME)

def cluster_atom():
    start_medians = [[-0.5, -0.5, -0.5], [0.5, 0.5, 0.5]]
    template_clustering(start_medians, FCPS_SAMPLES.SAMPLE_ATOM)


cluster_sample1()
cluster_sample2()
cluster_sample3()
cluster_sample4()
cluster_sample5()
cluster_elongate()
cluster_lsun()
cluster_target()
cluster_two_diamonds()
cluster_wing_nut()
cluster_chainlink()
cluster_hepta()
cluster_tetra()
cluster_atom()
cluster_engy_time()
