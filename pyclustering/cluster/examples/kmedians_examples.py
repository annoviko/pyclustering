"""!

@brief Examples of usage and demonstration of abilities of K-Medoids algorithm in cluster analysis.

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

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from pyclustering.cluster.kmedoids import kmedoids;

from pyclustering.utils import draw_clusters;
from pyclustering.utils import read_sample;
from pyclustering.utils import timedcall;

def template_clustering(start_medoids, path, tolerance = 0.25):
    sample = read_sample(path);
    
    kmedoids_instance = kmedoids(sample, start_medoids, tolerance);
    (ticks, result) = timedcall(kmedoids_instance.process);
    
    clusters = kmedoids_instance.get_clusters();
    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");

    draw_clusters(sample, clusters);
    
def cluster_sample1():
    template_clustering([2, 9], SIMPLE_SAMPLES.SAMPLE_SIMPLE1);
    
def cluster_sample2():
    template_clustering([3, 12, 20], SIMPLE_SAMPLES.SAMPLE_SIMPLE2);
    
def cluster_sample3():
    template_clustering([4, 12, 25, 37], SIMPLE_SAMPLES.SAMPLE_SIMPLE3);
    
def cluster_sample4():
    template_clustering([4, 15, 30, 40, 50], SIMPLE_SAMPLES.SAMPLE_SIMPLE4);    
    
def cluster_sample5():
    template_clustering([4, 18, 34, 55], SIMPLE_SAMPLES.SAMPLE_SIMPLE5);    
        
def cluster_elongate():
    template_clustering([8, 56], SIMPLE_SAMPLES.SAMPLE_ELONGATE);

def cluster_lsun():
    template_clustering([10, 275, 385], FCPS_SAMPLES.SAMPLE_LSUN);  
    
def cluster_target():
    template_clustering([10, 160, 310, 460, 560, 700], FCPS_SAMPLES.SAMPLE_TARGET);     

def cluster_two_diamonds():
    template_clustering([10, 650], FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS);  

def cluster_wing_nut():
    template_clustering([19, 823], FCPS_SAMPLES.SAMPLE_WING_NUT); 
    
def cluster_chainlink():
    template_clustering([30, 900], FCPS_SAMPLES.SAMPLE_CHAINLINK);     
    
def cluster_hepta():
    template_clustering([0, 35, 86, 93, 125, 171, 194], FCPS_SAMPLES.SAMPLE_HEPTA); 
    
def cluster_tetra():
    template_clustering([0, 131, 214, 265], FCPS_SAMPLES.SAMPLE_TETRA);    
    
def cluster_engy_time():
    template_clustering([10, 3000], FCPS_SAMPLES.SAMPLE_ENGY_TIME);
    
    
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