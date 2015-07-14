"""!

@brief Examples of usage and demonstration of abilities of Hierarchical Sync (HSyncNet) algorithm in cluster analysis.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2015
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

from pyclustering.utils import read_sample, draw_clusters;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;
from pyclustering.samples.definitions import FCPS_SAMPLES;

from pyclustering.cluster.hsyncnet import hsyncnet;
from pyclustering.nnet.sync import sync_visualizer;

def template_clustering(file, number_clusters, arg_order = 0.999, arg_collect_dynamic = True, ccore_flag = False):
        sample = read_sample(file);
        network = hsyncnet(sample, number_clusters, ccore = ccore_flag);
        
        analyser = network.process(arg_order, collect_dynamic = arg_collect_dynamic);
        clusters = analyser.allocate_clusters();
        
        if (arg_collect_dynamic == True):
            sync_visualizer.show_output_dynamic(analyser);
        
        draw_clusters(sample, clusters);
        

def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2);
    
def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3);
    
def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4);
    
def cluster_simple4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5);
    
def cluster_simple5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4);
    
def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 2, arg_collect_dynamic = False);

def cluster_lsun():
    "NOTE: Too slow"
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 3, arg_collect_dynamic = False);
    
def cluster_hepta():
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, arg_collect_dynamic = False);
    
def cluster_tetra():
    "NOTE: Too slow"
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 4, arg_collect_dynamic = False);

def cluster_target():
    "NOTE: Too slow"
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 6, arg_collect_dynamic = False);
    
def cluster_chainlink():
    "NOTE: Too slow"
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 2, arg_collect_dynamic = False);
    
def cluster_wing_nut():
    "NOTE: Too slow"
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 2, arg_collect_dynamic = False);
    
def cluster_two_diamonds():
    "NOTE: Too slow"
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 2, arg_collect_dynamic = False);    

def experiment_execution_time(show_dyn = False, ccore = False):
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 0.999, show_dyn, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 0.999, show_dyn, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, 0.999, show_dyn, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, 0.999, show_dyn, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, 0.999, show_dyn, ccore);
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 2, 0.999, show_dyn, ccore);
    
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 3, 0.999, show_dyn, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 6, 0.999, show_dyn, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 2, 0.999, show_dyn, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 2, 0.999, show_dyn, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 2, 0.999, show_dyn, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7, 0.999, show_dyn, ccore);
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 4, 0.999, show_dyn, ccore);

cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_simple4();
cluster_elongate();
cluster_lsun();
cluster_hepta();
cluster_tetra();
cluster_target();
cluster_chainlink();
cluster_wing_nut();
cluster_two_diamonds();
 
experiment_execution_time(False, False);
experiment_execution_time(False, True);