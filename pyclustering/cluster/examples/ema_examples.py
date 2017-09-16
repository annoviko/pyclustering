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

from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer;
from pyclustering.cluster.kmeans import kmeans;
from pyclustering.cluster.ema import ema, ema_visualizer;

from pyclustering.utils import read_sample;

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES;


def template_clustering(sample_file_path, amount_clusters):
    sample = read_sample(sample_file_path);
    
    ema_instance = ema(sample, amount_clusters);
    ema_instance.process();
    
    clusters = ema_instance.get_clusters();
    covariances = ema_instance.get_covariances();
    means = ema_instance.get_centers();

    ema_visualizer.show_clusters(clusters, sample, covariances, means);


def cluster_sample01():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2);

def cluster_sample02():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3);

def cluster_sample03():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4);

def cluster_sample04():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5);

def cluster_sample05():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4);

def cluster_sample08():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8, 4);

def cluster_sample11():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2);

def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 2);

def cluster_lsun():
    template_clustering(FCPS_SAMPLES.SAMPLE_LSUN, 3);


cluster_sample01();
cluster_sample02();
cluster_sample03();
cluster_sample04();
cluster_sample05();
cluster_sample08();
cluster_sample11();
cluster_elongate();
cluster_lsun();