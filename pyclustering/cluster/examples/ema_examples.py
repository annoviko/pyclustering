"""!

@brief Examples of usage and demonstration of abilities of expectation maximization algorithm.

@authors Andrey Novikov (pyclustering@yandex.ru)
@date 2014-2017
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


import numpy;

from pyclustering.cluster import cluster_visualizer;
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer;
from pyclustering.cluster.kmeans import kmeans;
from pyclustering.cluster.ema import ema;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;


def template_clustering(sample_file_path, amount_clusters, kmeans_initializer = True):
    sample = read_sample(sample_file_path);
    
    means = None;
    covariances = None;
    
    if (kmeans_initializer is True):
        initial_centers = kmeans_plusplus_initializer(sample, amount_clusters).initialize();
        kmeans_instance = kmeans(sample, initial_centers, ccore = True);
        kmeans_instance.process();
        
        means = kmeans_instance.get_centers();
        
        covariances = [];
        initial_clusters = kmeans_instance.get_clusters();
        for initial_cluster in initial_clusters:
            cluster_sample = [];
            for index_point in initial_cluster:
                cluster_sample.append(sample[index_point]);
            
            covariances.append(numpy.cov(cluster_sample, rowvar = False));
    
    ema_instance = ema(sample, amount_clusters, means, covariances);
    ema_instance.process();
    
    clusters = ema_instance.get_clusters();

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
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4);

def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 2);

def cluster_lsun():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 3);


cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_sample4();
cluster_sample5();
cluster_elongate();
cluster_lsun();