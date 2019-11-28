"""!
@brief Examples of usage and demonstration of abilities of agglomerative algorithm in cluster analysis.
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
from pyclustering.cluster.agglomerative import agglomerative, type_link

from pyclustering.utils import read_sample
from pyclustering.utils import timedcall

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES


def template_clustering(number_clusters, path, links):
    sample = read_sample(path)
    
    clusters_centroid_link = None
    clusters_single_link = None
    clusters_complete_link = None
    clusters_average_link = None
    
    visualizer = cluster_visualizer(len(links), len(links));
    index_canvas = 0;
    
    if (type_link.CENTROID_LINK in links):
        agglomerative_centroid_link = agglomerative(sample, number_clusters, type_link.CENTROID_LINK, True);
        
        (ticks, result) = timedcall(agglomerative_centroid_link.process);
        clusters_centroid_link = agglomerative_centroid_link.get_clusters();
        
        visualizer.append_clusters(clusters_centroid_link, sample, index_canvas);
        visualizer.set_canvas_title('Link: Centroid', index_canvas);
        index_canvas += 1;
        
        print("Sample: ", path, "Link: Centroid", "\tExecution time: ", ticks, "\n");
    
    if (type_link.SINGLE_LINK in links):
        agglomerative_simple_link = agglomerative(sample, number_clusters, type_link.SINGLE_LINK);
        
        (ticks, result) = timedcall(agglomerative_simple_link.process);
        clusters_single_link = agglomerative_simple_link.get_clusters();
        
        visualizer.append_clusters(clusters_single_link, sample, index_canvas);
        visualizer.set_canvas_title('Link: Single', index_canvas);
        index_canvas += 1;
        
        print("Sample: ", path, "Link: Single", "\tExecution time: ", ticks, "\n");
    
    if (type_link.COMPLETE_LINK in links):
        agglomerative_complete_link = agglomerative(sample, number_clusters, type_link.COMPLETE_LINK);
        
        (ticks, result) = timedcall(agglomerative_complete_link.process);
        clusters_complete_link = agglomerative_complete_link.get_clusters();
        
        visualizer.append_clusters(clusters_complete_link, sample, index_canvas);
        visualizer.set_canvas_title('Link: Complete', index_canvas);
        index_canvas += 1;
        
        print("Sample: ", path, "Link: Complete", "\tExecution time: ", ticks, "\n");
    
    if (type_link.AVERAGE_LINK in links):
        agglomerative_average_link = agglomerative(sample, number_clusters, type_link.AVERAGE_LINK);
        
        (ticks, result) = timedcall(agglomerative_average_link.process);
        clusters_average_link = agglomerative_average_link.get_clusters();
        
        visualizer.append_clusters(clusters_average_link, sample, index_canvas);
        visualizer.set_canvas_title('Link: Average', index_canvas);
        index_canvas += 1;
        
        print("Sample: ", path, "Link: Average", "\tExecution time: ", ticks, "\n");
    
    visualizer.show();
    
    
def cluster_sample1():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [type_link.CENTROID_LINK, type_link.SINGLE_LINK, type_link.AVERAGE_LINK, type_link.COMPLETE_LINK]);
    
def cluster_sample2():
    template_clustering(3, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [type_link.CENTROID_LINK, type_link.SINGLE_LINK, type_link.AVERAGE_LINK, type_link.COMPLETE_LINK]);
    
def cluster_sample3():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [type_link.CENTROID_LINK, type_link.SINGLE_LINK, type_link.AVERAGE_LINK, type_link.COMPLETE_LINK]);
    
def cluster_sample4():
    template_clustering(5, SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [type_link.CENTROID_LINK, type_link.SINGLE_LINK, type_link.AVERAGE_LINK, type_link.COMPLETE_LINK]);
    
def cluster_sample5():
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [type_link.CENTROID_LINK, type_link.SINGLE_LINK, type_link.AVERAGE_LINK, type_link.COMPLETE_LINK]);
    
def cluster_elongate():
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_ELONGATE, [type_link.CENTROID_LINK, type_link.SINGLE_LINK, type_link.AVERAGE_LINK, type_link.COMPLETE_LINK]);

def cluster_lsun():
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN, [type_link.CENTROID_LINK, type_link.SINGLE_LINK, type_link.AVERAGE_LINK, type_link.COMPLETE_LINK]);
    
def cluster_target():
    template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET, [ type_link.CENTROID_LINK ]);

def cluster_two_diamonds():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [ type_link.CENTROID_LINK ]);

def cluster_wing_nut():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT, [type_link.CENTROID_LINK ]); 
    
def cluster_chainlink():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_CHAINLINK, [ type_link.CENTROID_LINK ]);
    
def cluster_hepta():
    template_clustering(7, FCPS_SAMPLES.SAMPLE_HEPTA, [ type_link.CENTROID_LINK ]);
    
def cluster_tetra():
    template_clustering(4, FCPS_SAMPLES.SAMPLE_TETRA, [ type_link.CENTROID_LINK ]);
    
def cluster_engy_time():
    template_clustering(2, FCPS_SAMPLES.SAMPLE_ENGY_TIME, [ type_link.CENTROID_LINK ]);
    
    
def experiment_execution_time(ccore = False):
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, [type_link.SINGLE_LINK]);
    template_clustering(3, SIMPLE_SAMPLES.SAMPLE_SIMPLE2, [type_link.SINGLE_LINK]);
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE3, [type_link.SINGLE_LINK]);
    template_clustering(5, SIMPLE_SAMPLES.SAMPLE_SIMPLE4, [type_link.SINGLE_LINK]);
    template_clustering(4, SIMPLE_SAMPLES.SAMPLE_SIMPLE5, [type_link.SINGLE_LINK]);
    template_clustering(2, SIMPLE_SAMPLES.SAMPLE_ELONGATE, [type_link.SINGLE_LINK]);
    template_clustering(3, FCPS_SAMPLES.SAMPLE_LSUN, [type_link.SINGLE_LINK]);
    template_clustering(6, FCPS_SAMPLES.SAMPLE_TARGET, [type_link.SINGLE_LINK]);
    template_clustering(2, FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, [type_link.SINGLE_LINK]);
    template_clustering(2, FCPS_SAMPLES.SAMPLE_WING_NUT, [type_link.SINGLE_LINK]);
    template_clustering(2, FCPS_SAMPLES.SAMPLE_CHAINLINK, [type_link.SINGLE_LINK]);
    template_clustering(7, FCPS_SAMPLES.SAMPLE_HEPTA, [type_link.SINGLE_LINK]);
    template_clustering(4, FCPS_SAMPLES.SAMPLE_TETRA, [type_link.SINGLE_LINK]);
    template_clustering(2, FCPS_SAMPLES.SAMPLE_ATOM, [type_link.SINGLE_LINK]);


cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_sample4();
cluster_sample5();
cluster_elongate();
cluster_lsun();
cluster_target();
cluster_two_diamonds();
cluster_wing_nut();
cluster_chainlink();
cluster_hepta();
cluster_tetra();
cluster_engy_time();


experiment_execution_time(False);   # Python code