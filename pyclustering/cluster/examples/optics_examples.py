"""!

@brief Examples of usage and demonstration of abilities of OPTICS algorithm in cluster analysis.

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

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.optics import optics, ordering_analyser, ordering_visualizer

from pyclustering.utils import read_sample, timedcall

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES


def template_clustering(path_sample, eps, minpts, amount_clusters = None, visualize = True, ccore = False):
    sample = read_sample(path_sample)
    
    optics_instance = optics(sample, eps, minpts, amount_clusters, ccore)
    (ticks, _) = timedcall(optics_instance.process)
    
    print("Sample: ", path_sample, "\t\tExecution time: ", ticks, "\n")
    
    if (visualize is True):
        clusters = optics_instance.get_clusters()
        noise = optics_instance.get_noise()

        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.append_cluster(noise, sample, marker = 'x')
        visualizer.show()
    
        ordering = optics_instance.get_ordering()
        analyser = ordering_analyser(ordering)
        
        ordering_visualizer.show_ordering_diagram(analyser, amount_clusters)
    
    
def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 0.5, 3)
    
def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3.0, 3)
    
def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 0.7, 3)
    
def cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 0.7, 3)

def cluster_sample5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 0.7, 3)
    
def cluster_sample6():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, 1.0, 3)
 
def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 0.5, 3)

def cluster_lsun():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 0.5, 3)

def cluster_lsun_radius_calculation():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 1.0, 3, 3)

def cluster_target():
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 0.5, 2)

def cluster_target_radius_calculation():
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 10.0, 2, 6)

def cluster_two_diamonds():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 0.15, 7)

def cluster_two_diamonds_radius_calculation():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1.0, 7, 2)

def cluster_wing_nut():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 0.25, 2)

def cluster_wing_nut_radius_calculation():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 1.0, 2, 2)

def cluster_chainlink():
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 0.15, 3)
    
def cluster_hepta():
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3)
    
def cluster_golf_ball():
    template_clustering(FCPS_SAMPLES.SAMPLE_GOLF_BALL, 0.5, 3)
    
def cluster_atom():
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, 15, 3)

def cluster_tetra():
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 0.4, 3)
     
def cluster_engy_time():
    template_clustering(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 0.2, 20)


def experiment_execution_time(ccore):
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 1.0, 3, 3, False, ccore)
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 10.0, 2, 6, False, ccore)
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 1.0, 7, 2, False, ccore)
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 2.0, 3, 2, False, ccore)
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 1.0, 2, 2, False, ccore)
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 3, None, False, ccore)
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 1.0, 3, 4, False, ccore)
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, 30, 3, 2, False, ccore)


def clustering_random_points(amount, ccore):
    sample = [ [ random.random(), random.random() ] for _ in range(amount) ]
    
    optics_instance = optics(sample, 0.05, 20, None, ccore)
    (ticks, _) = timedcall(optics_instance.process)
    
    print("Execution time ("+ str(amount) +" 2D-points):", ticks)


def performance_measure_random_points(ccore):
    clustering_random_points(1000, ccore)
    clustering_random_points(2000, ccore)
    clustering_random_points(3000, ccore)
    clustering_random_points(4000, ccore)
    clustering_random_points(5000, ccore)
    clustering_random_points(10000, ccore)
    clustering_random_points(20000, ccore)


cluster_sample1()
cluster_sample2()
cluster_sample3()
cluster_sample4()
cluster_sample5()
cluster_sample6()
cluster_elongate()
cluster_lsun()
cluster_lsun_radius_calculation()
cluster_target()
cluster_target_radius_calculation()
cluster_two_diamonds()
cluster_two_diamonds_radius_calculation()
cluster_wing_nut()
cluster_wing_nut_radius_calculation()
cluster_chainlink()
cluster_hepta()
cluster_golf_ball()
cluster_atom()
cluster_tetra()
cluster_engy_time()


experiment_execution_time(False)
experiment_execution_time(True)

performance_measure_random_points(False)
performance_measure_random_points(True)