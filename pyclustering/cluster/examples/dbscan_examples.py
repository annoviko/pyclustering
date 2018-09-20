"""!

@brief Examples of usage and demonstration of abilities of DBSCAN algorithm in cluster analysis.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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
from pyclustering.cluster.dbscan import dbscan

from pyclustering.utils import read_sample
from pyclustering.utils import timedcall

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES


def template_clustering(radius, neighb, path, invisible_axes = False, ccore = True, show = True):
    sample = read_sample(path)
    
    dbscan_instance = dbscan(sample, radius, neighb, ccore)
    (ticks, _) = timedcall(dbscan_instance.process)
    
    clusters = dbscan_instance.get_clusters()
    noise = dbscan_instance.get_noise()
    
    print([len(cluster) for cluster in clusters])
    
    if show:
        visualizer = cluster_visualizer()
        visualizer.append_clusters(clusters, sample)
        visualizer.append_cluster(noise, sample, marker = 'x')
        visualizer.show()
    
    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n")
    
    return sample, clusters, noise


def cluster_sample1():
    template_clustering(0.4, 2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
    
def cluster_sample2():
    template_clustering(1, 2, SIMPLE_SAMPLES.SAMPLE_SIMPLE2)
    
def cluster_sample3():
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE3)
    
def cluster_sample4():
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE4)

def cluster_sample5():
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE5)

def cluster_sample7():
    template_clustering(1.0, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE7)

def cluster_sample8():
    template_clustering(1.0, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE8)

def cluster_elongate():
    template_clustering(0.5, 3, SIMPLE_SAMPLES.SAMPLE_ELONGATE)

def cluster_lsun():
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_LSUN)

def cluster_target():
    template_clustering(0.5, 2, FCPS_SAMPLES.SAMPLE_TARGET)

def cluster_two_diamonds():
    "It's hard to choose properly parameters, but it's OK"
    template_clustering(0.15, 7, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS)

def cluster_wing_nut():
    "It's hard to choose properly parameters, but it's OK"
    template_clustering(0.25, 2, FCPS_SAMPLES.SAMPLE_WING_NUT)

def cluster_chainlink():
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_CHAINLINK)

def cluster_hepta():
    template_clustering(1, 3, FCPS_SAMPLES.SAMPLE_HEPTA)

def cluster_golf_ball():
    "Toooooooooooo looooong"
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_GOLF_BALL)

def cluster_atom():
    template_clustering(15, 3, FCPS_SAMPLES.SAMPLE_ATOM)

def cluster_tetra():
    template_clustering(0.4, 3, FCPS_SAMPLES.SAMPLE_TETRA)

def cluster_engy_time():
    template_clustering(0.2, 20, FCPS_SAMPLES.SAMPLE_ENGY_TIME)

def experiment_execution_time(ccore = False):
    "Performance measurement"
    template_clustering(0.5, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, False, ccore)
    template_clustering(1, 2, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, False, ccore)
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE3, False, ccore)
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE4, False, ccore)
    template_clustering(0.7, 3, SIMPLE_SAMPLES.SAMPLE_SIMPLE5, False, ccore)
    template_clustering(0.5, 3, SIMPLE_SAMPLES.SAMPLE_ELONGATE, False, ccore)
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_LSUN, False, ccore)
    template_clustering(0.5, 2, FCPS_SAMPLES.SAMPLE_TARGET, False, ccore)
    template_clustering(0.15, 7, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, ccore)
    template_clustering(0.25, 2, FCPS_SAMPLES.SAMPLE_WING_NUT, False, ccore)
    template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_CHAINLINK, False, ccore)
    template_clustering(1, 3, FCPS_SAMPLES.SAMPLE_HEPTA, False, ccore)
    template_clustering(0.4, 3, FCPS_SAMPLES.SAMPLE_TETRA, False, ccore)
    template_clustering(15, 3, FCPS_SAMPLES.SAMPLE_ATOM, False, ccore)

def display_fcps_clustering_results():
    (lsun, lsun_clusters, _) = template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_LSUN, False, True, False)
    (target, target_clusters, _) = template_clustering(0.5, 2, FCPS_SAMPLES.SAMPLE_TARGET, False, True, False)
    (two_diamonds, two_diamonds_clusters, _) = template_clustering(0.15, 7, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, True, False)
    (wing_nut, wing_nut_clusters, _) = template_clustering(0.25, 2, FCPS_SAMPLES.SAMPLE_WING_NUT, False, True, False)
    (chainlink, chainlink_clusters, _) = template_clustering(0.5, 3, FCPS_SAMPLES.SAMPLE_CHAINLINK, False, True, False)
    (hepta, hepta_clusters, _) = template_clustering(1, 3, FCPS_SAMPLES.SAMPLE_HEPTA, False, True, False)
    (tetra, tetra_clusters, _) = template_clustering(0.4, 3, FCPS_SAMPLES.SAMPLE_TETRA, False, True, False)
    (atom, atom_clusters, _) = template_clustering(15, 3, FCPS_SAMPLES.SAMPLE_ATOM, False, True, False)
    
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


def display_fcps_dependence_clustering_results():
    (two_diamonds, two_diamonds_clusters_1, _) = template_clustering(0.15, 4, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, True, False)
    (two_diamonds, two_diamonds_clusters_2, _) = template_clustering(0.15, 5, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, True, False)
    (two_diamonds, two_diamonds_clusters_3, _) = template_clustering(0.15, 6, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, True, False)
    (two_diamonds, two_diamonds_clusters_4, _) = template_clustering(0.15, 7, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, True, False)

    (two_diamonds, two_diamonds_clusters_5, _) = template_clustering(0.10, 6, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, True, False)
    (two_diamonds, two_diamonds_clusters_6, _) = template_clustering(0.12, 6, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, True, False)
    (two_diamonds, two_diamonds_clusters_7, _) = template_clustering(0.15, 6, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, True, False)
    (two_diamonds, two_diamonds_clusters_8, _) = template_clustering(0.17, 6, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, False, True, False)
    
    visualizer = cluster_visualizer(8, 4)
    visualizer.append_clusters(two_diamonds_clusters_1, two_diamonds, 0)
    visualizer.append_clusters(two_diamonds_clusters_2, two_diamonds, 1)
    visualizer.append_clusters(two_diamonds_clusters_3, two_diamonds, 2)
    visualizer.append_clusters(two_diamonds_clusters_4, two_diamonds, 3)
    visualizer.append_clusters(two_diamonds_clusters_5, two_diamonds, 4)
    visualizer.append_clusters(two_diamonds_clusters_6, two_diamonds, 5)
    visualizer.append_clusters(two_diamonds_clusters_7, two_diamonds, 6)
    visualizer.append_clusters(two_diamonds_clusters_8, two_diamonds, 7)
    visualizer.show()


def clustering_random_points(amount, ccore):
    sample = [ [ random.random(), random.random() ] for _ in range(amount) ]
    
    dbscan_instance = dbscan(sample, 0.05, 20, ccore)
    (ticks, _) = timedcall(dbscan_instance.process)
    
    print("Execution time ("+ str(amount) +" 2D-points):", ticks)


def performance_measure_random_points(ccore):
    clustering_random_points(1000, ccore)
    clustering_random_points(2000, ccore)
    clustering_random_points(3000, ccore)
    clustering_random_points(4000, ccore)
    clustering_random_points(5000, ccore)
    clustering_random_points(10000, ccore)
    clustering_random_points(20000, ccore)



# cluster_sample1()
# cluster_sample2()
# cluster_sample3()
# cluster_sample4()
# cluster_sample5()
# cluster_sample7()
# cluster_sample8()
# cluster_elongate()
# cluster_lsun()
# cluster_target()
# cluster_two_diamonds()
# cluster_wing_nut()
# cluster_chainlink()
# cluster_hepta()
# cluster_golf_ball()           # it is commented due to long time of processing - it's working absolutely correct!
# cluster_atom()
# cluster_tetra()
# cluster_engy_time()
#
# experiment_execution_time(False)  # Python code
# experiment_execution_time(True)   # C++ code + Python env.
#
# display_fcps_clustering_results()
# display_fcps_dependence_clustering_results()
#
# performance_measure_random_points(False)
# performance_measure_random_points(True)


import numpy as np
import matplotlib.pyplot as plt

from pyclustering.cluster.dbscan import dbscan

def on_picker(event):
    distances = np.abs(np.linalg.norm(data - np.array([event.mouseevent.xdata, event.mouseevent.ydata]), axis=1, ord=2))
    ix = distances.argmin()

    circle = plt.Circle((data[ix, 0], data[ix, 1]), eps, edgecolor='k', linestyle='-', linewidth=0.5, fill=None)

    ax.add_artist(circle)
    event.canvas.draw()

data = np.array([[3.84883118, 7.98287654],
                 [6.15957575, 0.93742612],
                 [0.58865177, 7.34201309],
                 [6.95169446, 6.34775643],
                 [3.64920659, 1.43836441],
                 [4.98745463, 1.48505],
                 [1.50897943, 0.66372945],
                 [1.7165765, 6.51867617],
                 [3.63916014, 4.03335428],        # Point in question
                 [1.64755443, 6.91168503],
                 [5.18619498, 5.01467501],
                 [5.22841242, 4.66132755],
                 [4.46416522, 4.99414511],
                 [5.74935967, 5.19903379],
                 [4.71599415, 4.88615725],
                 [5.24744658, 4.56903919],
                 [5.19049452, 5.41090111],
                 [4.46223735, 4.4370961],
                 [4.06165299, 5.64246575],
                 [4.13648305, 5.0203021],
                 [5.0931739, 5.90484805],
                 [5.27248291, 5.10978874],
                 [4.98665978, 5.02617475],
                 [4.49543272, 3.6342554],
                 [5.49451608, 4.56799783],
                 [5.26142474, 4.99616694],
                 [5.5543285, 5.59529684],
                 [4.15108339, 4.31406758],
                 [5.12194741, 4.93568024],
                 [4.77956745, 4.73403704],
                 [5.58123982, 5.5657367],
                 [5.06730322, 4.57878869],
                 [4.58515378, 5.18852395],
                 [5.49669378, 4.8901156],
                 [5.42696559, 4.71035229],
                 [3.5934053, 4.76841482],
                 [5.60826032, 5.61143477],
                 [6.23623543, 4.93332256],
                 [5.25518697, 4.35253186],
                 [3.63467815, 5.25080737],

                 [3.63467815, 5.25080737]])

eps, minPts = 1.0, 5
dbscan_i = dbscan(data, eps, minPts, False)
dbscan_i.process()

labels = np.zeros(data.shape[0], dtype=np.int32)
for ix, cluster_indices in enumerate(dbscan_i.get_clusters()):
    labels[cluster_indices] = ix + 1

fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis("equal")
for label in labels:
    mask = labels == label
    if label == 0:
        ax.scatter(data[mask, 0], data[mask, 1], s=10, c='k', picker=True)
    else:
        ax.scatter(data[mask, 0], data[mask, 1], s=10, picker=True)
ax.set_title("Eps {}, MinPts {}".format(eps, minPts))

fig.canvas.mpl_connect("pick_event", on_picker)

plt.show()