"""!

@brief Examples of usage and demonstration of abilities of SYNC-SOM algorithm in cluster analysis.

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

from random import random;

from pyclustering.cluster import cluster_visualizer;
from pyclustering.cluster.syncsom import syncsom;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.samples.definitions import FCPS_SAMPLES;

from pyclustering.utils import read_sample, draw_dynamics;
from pyclustering.utils import timedcall;


def template_clustering(file, map_size, radius, sync_order = 0.999, show_dyn = False, show_layer1 = False, show_layer2 = False, show_clusters = True):
    # Read sample
    sample = read_sample(file);

    # Create network
    network = syncsom(sample, map_size[0], map_size[1], radius);
    
    # Run processing
    (ticks, (dyn_time, dyn_phase)) = timedcall(network.process, show_dyn, sync_order);
    print("Sample: ", file, "\t\tExecution time: ", ticks, "\n");
    
    # Show dynamic of the last layer.
    if (show_dyn == True):
        draw_dynamics(dyn_time, dyn_phase, x_title = "Time", y_title = "Phase", y_lim = [0, 3.14]);
    
    if (show_clusters == True):
        clusters = network.get_som_clusters();
        
        visualizer = cluster_visualizer();
        visualizer.append_clusters(clusters, network.som_layer.weights);
        visualizer.show();
    
    # Show network stuff.
    if (show_layer1 == True):
        network.show_som_layer();
    
    if (show_layer2 == True):
        network.show_sync_layer();
    
    if (show_clusters == True):
        clusters = network.get_clusters();
        
        visualizer = cluster_visualizer();
        visualizer.append_clusters(clusters, sample);
        visualizer.show();

def cluster_simple1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [4, 4], 1.0, 0.999, True, True, True, True);

def cluster_simple1_as_som():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [1, 2], 1.0, 0.999, True, True, True, True);
  
def cluster_simple2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [4, 4], 1.0, 0.999, True, True, True, True);

def cluster_simple2_as_som():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [1, 3], 1.0, 0.999, True, True, True, True);

def cluster_simple3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [5, 5], 1.0, 0.999, True, True, True, True);
    
def cluster_simple4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [5, 5], 1.0, 0.999, True, True, True);
    
def cluster_simple5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [5, 5], 1.0, 0.999, True, True, True);

def cluster_lsun():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, [9, 9], 0.45, 0.999, True, True, True);
     
def cluster_target():
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, [9, 9], 0.9, 0.999, True, True, True);

def cluster_two_diamonds():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [10, 10], 0.15, 0.999, True, True, True);

def cluster_wing_nut():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, [10, 10], 0.25, 0.999, True, True, True);

def cluster_chainlink():
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, [10, 10], 0.5, 0.999, True, True, True);

def cluster_hepta():
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, [7, 7], 1.0, 0.999, True, True, True);

def cluster_tetra():
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, [7, 7], 0.4, 0.998, True, True, True);

def experiment_execution_time():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, [4, 4], 0.45, 0.999, False, False, False, False);
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, [4, 4], 0.9, 0.998, False, False, False, False);
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, [4, 4], 0.25, 0.999, False, False, False, False);
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, [4, 4], 0.5, 0.998, False, False, False, False);
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, [4, 4], 0.4, 0.998, False, False, False, False);
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, [6, 6], 1.0, 0.998, False, False, False, False);
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [4, 4], 0.15, 0.998, False, False, False, False);
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, [4, 4], 15, 0.998, False, False, False, False);


def experiment_execution_one_cluster_dependence(layer_first_size, radius, order):
    print("Experiment: map size =", layer_first_size[0] * layer_first_size[1], "radius =", radius, "order =", order);
    cluster_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150];
    
    for cluster_size in cluster_sizes:
        # generate data sets
        dataset = [];
        dataset += [ [random(), random()] for _ in range(cluster_size) ];
        
        general_value = 0.0;
        amount_attempt = 5;
        for _ in range(amount_attempt):
            network = syncsom(dataset, layer_first_size[0], layer_first_size[1], radius);
            (ticks, (dyn_time, dyn_phase)) = timedcall(network.process, False, order);
            general_value += ticks;
                
        print("Sample: ", cluster_size, "\t\tExecution time: ", general_value / float(amount_attempt));
        
    print("\n");


cluster_simple1();
cluster_simple1_as_som();
cluster_simple2();
cluster_simple2_as_som();
cluster_simple3();
cluster_simple4();
cluster_simple5();
cluster_lsun();
cluster_target();
cluster_two_diamonds();
cluster_chainlink();
cluster_hepta();
cluster_tetra();

experiment_execution_time();

experiment_execution_one_cluster_dependence([5, 5], 0.6, 0.998);
experiment_execution_one_cluster_dependence([6, 6], 0.6, 0.998);
experiment_execution_one_cluster_dependence([7, 7], 0.6, 0.998);
experiment_execution_one_cluster_dependence([8, 8], 0.6, 0.998);
experiment_execution_one_cluster_dependence([9, 9], 0.6, 0.998);
experiment_execution_one_cluster_dependence([10, 10], 0.6, 0.998);