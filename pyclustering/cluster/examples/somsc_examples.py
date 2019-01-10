"""!

@brief Examples of usage and demonstration of abilities of SOM-SC algorithm in cluster analysis.

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


from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;

from pyclustering.cluster import cluster_visualizer;
from pyclustering.cluster.somsc import somsc;

from pyclustering.utils import read_sample;
from pyclustering.utils import timedcall;

def template_clustering(path, amount_clusters, epouch = 100, ccore = True):
    sample = read_sample(path);
    
    somsc_instance = somsc(sample, amount_clusters, epouch, ccore);
    (ticks, _) = timedcall(somsc_instance.process);
    
    clusters = somsc_instance.get_clusters();
    
    print("Sample: ", path, "\t\tExecution time: ", ticks, "\n");

    visualizer = cluster_visualizer();
    visualizer.append_clusters(clusters, sample);
    visualizer.show();


def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2);
    
def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3);
    
def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4);
    
def cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5);
    
def cluster_sample5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 6);

def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 2);

def cluster_lsun():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 3);
    
def cluster_target():
    template_clustering(FCPS_SAMPLES.SAMPLE_TARGET, 6);

def cluster_two_diamonds():
    template_clustering(FCPS_SAMPLES.SAMPLE_TWO_DIAMONDS, 2);

def cluster_wing_nut():
    template_clustering(FCPS_SAMPLES.SAMPLE_WING_NUT, 2); 
    
def cluster_chainlink():
    template_clustering(FCPS_SAMPLES.SAMPLE_CHAINLINK, 2);
    
def cluster_hepta():
    template_clustering(FCPS_SAMPLES.SAMPLE_HEPTA, 7); 
    
def cluster_tetra():
    template_clustering(FCPS_SAMPLES.SAMPLE_TETRA, 4);
    
def cluster_engy_time():
    template_clustering(FCPS_SAMPLES.SAMPLE_ENGY_TIME, 2);


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