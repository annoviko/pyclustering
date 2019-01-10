"""!

@brief Examples of usage and demonstration of abilities of Sync algorithm in cluster analysis.

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

from pyclustering.cluster import cluster_visualizer;
from pyclustering.cluster.syncnet import syncnet, syncnet_visualizer;
 
from pyclustering.nnet.sync import sync_visualizer;
from pyclustering.nnet import initial_type, solve_type;
 
from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.samples.definitions import FCPS_SAMPLES;
 
from pyclustering.utils import draw_clusters;
from pyclustering.utils import read_sample;
from pyclustering.utils import timedcall;


def template_clustering(file, radius, order, show_dyn = False, show_conn = False, show_clusters = True, ena_conn_weight = False, ccore_flag = True, tolerance = 0.1):
    sample = read_sample(file)
    syncnet_instance = syncnet(sample, radius, enable_conn_weight = ena_conn_weight, ccore = ccore_flag)

    (ticks, analyser) = timedcall(syncnet_instance.process, order, solve_type.FAST, show_dyn)
    print("Sample: ", file, "\t\tExecution time: ", ticks)

    if show_dyn == True:
        sync_visualizer.show_output_dynamic(analyser)
        sync_visualizer.animate(analyser)
        sync_visualizer.show_local_order_parameter(analyser, syncnet_instance)
        #sync_visualizer.animate_output_dynamic(analyser);
        #sync_visualizer.animate_correlation_matrix(analyser, colormap = 'hsv')
     
    if show_conn == True:
        syncnet_instance.show_network()
     
    if show_clusters == True:
        clusters = analyser.allocate_clusters(tolerance)
        print("Amount of allocated clusters: ", len(clusters))
        draw_clusters(sample, clusters)
    
    print("----------------------------\n")
    return (sample, clusters)


def cluster_simple1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, show_dyn = True, show_conn = True);

def cluster_simple2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, show_dyn = True, show_conn = True);

def cluster_simple3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, show_dyn = True, show_conn = True);

def cluster_simple4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0.999, show_dyn = True, show_conn = True);

def cluster_simple5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0.999, show_dyn = True, show_conn = True);

def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 0.5, 0.999, show_dyn = True, show_conn = True);

def cluster_lsun():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 0.45, 0.9995, show_dyn = True, show_conn = True);

def cluster_target():
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 0.95, 0.99995, show_dyn = False, show_conn = True);

def cluster_hepta():
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 0.999, show_dyn = True, show_conn = True);

def cluster_chainlink():
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 0.8, 0.999, show_dyn = True, show_conn = True);

def cluster_two_diamonds():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 0.3, 0.999, show_dyn = False, show_conn = False);  

def cluster_atom():
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, 25, 0.999, show_dyn = False, show_conn = False); 

def cluster_wing_nut():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 0.28, 0.999, show_dyn = False, show_conn = False); 


def experiment_execution_time(show_dyn = False, ccore = False):
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1, 0.999, show_dyn, False, True, False, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 0.5, 0.999, show_dyn, False, True, False, ccore);
    
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 0.45, 0.98, show_dyn, False, False, True, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 0.4, 0.98, show_dyn, False, False, True, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 0.3, 0.98, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 0.28, 0.98, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 0.8, 0.98, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 0.98, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 0.3, 0.98, show_dyn, False, True, False, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_ATOM, 25, 0.98, show_dyn, False, True, False, ccore);

def cluster_simple1_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True); 

def cluster_simple2_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 2, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True);   

def cluster_simple3_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 2, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True);

def cluster_simple4_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 10, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True);

def cluster_simple5_conn_weight():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 10, 0.999, show_dyn = True, show_conn = True, ena_conn_weight = True);


def template_animated_clustering(file, radius, order, expected_cluster_amount, title_animation = None):
    sample = read_sample(file);
    expected_result_obtained = False;
     
    analyser = None;
     
    while (expected_result_obtained == False):
        network = syncnet(sample, radius, initial_phases = initial_type.RANDOM_GAUSSIAN, ccore = True);
     
        analyser = network.process(order, solve_type.FAST, True);
        clusters = analyser.allocate_clusters(0.1);
     
        if (len(clusters) == expected_cluster_amount):
            print("Expected result is obtained - start rendering...")
            expected_result_obtained = True;
             
            visualizer = cluster_visualizer();
            visualizer.append_clusters(clusters, sample);
            visualizer.show();
             
        else:
            print("Expected result is NOT obtained - rendering is NOT started ( actual:", len(clusters), ")...");
     
    syncnet_visualizer.animate_cluster_allocation(sample, analyser, tolerance = 0.1, save_movie = "clustering_animation.mp4", title = title_animation);
 
def animation_cluster_allocation_sample_simple3():
    template_animated_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 1.0, 0.999, 4);
 
def animation_cluster_allocation_sample_simple5():
    template_animated_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 1.0, 0.999, 4);
 
def animation_cluster_allocation_elongate():
    template_animated_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 0.5, 0.999, 2);
 
def animation_cluster_allocation_lsun():
    template_animated_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 0.45, 0.999, 3);
 
def animation_cluster_allocation_target():
    template_animated_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 0.95, 0.9999, 6);

def animation_cluster_allocation_hepta():
    template_animated_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 1, 0.995, 7, "Sync clustering\nOscillatory based algorithm");


def display_fcps_clustering_results():
    (simple4, simple4_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 1, 0.999, show_dyn = False, show_conn = False, ccore_flag = True);
    (simple_elongate, simple_elongate_clusters) = template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 0.5, 0.999, show_dyn = False, show_conn = False, ccore_flag = True);
    (lsun, lsun_clusters) = template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 0.45, 0.9995, show_dyn = False, show_conn = False, ccore_flag = True, tolerance = 0.2);

    visualizer = cluster_visualizer(1, 3);
    visualizer.append_clusters(simple4_clusters, simple4, 0);
    visualizer.append_clusters(simple_elongate_clusters, simple_elongate, 1);
    visualizer.append_clusters(lsun_clusters, lsun, 2);

    visualizer.show();


cluster_simple1();
cluster_simple2();
cluster_simple3();
cluster_simple4();
cluster_simple5();
cluster_elongate();
cluster_lsun();
cluster_target();
cluster_hepta();
cluster_chainlink();
cluster_two_diamonds();
cluster_atom();
cluster_wing_nut();


cluster_simple1_conn_weight();
cluster_simple2_conn_weight();
cluster_simple3_conn_weight();
cluster_simple4_conn_weight();
cluster_simple5_conn_weight();


experiment_execution_time(False, False);
experiment_execution_time(False, True);


animation_cluster_allocation_sample_simple3();
animation_cluster_allocation_sample_simple5();
animation_cluster_allocation_elongate();
animation_cluster_allocation_lsun();
animation_cluster_allocation_target();
animation_cluster_allocation_hepta();


display_fcps_clustering_results();