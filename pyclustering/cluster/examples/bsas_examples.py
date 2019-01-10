"""!

@brief Examples of usage and demonstration of abilities of BSAS algorithm in cluster analysis.

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
from pyclustering.cluster.bsas import bsas, bsas_visualizer;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.utils import read_sample;
from pyclustering.utils.metric import distance_metric, type_metric;


def template_clustering(path, amount, threshold, **kwargs):
    metric = kwargs.get('metric', distance_metric(type_metric.EUCLIDEAN_SQUARE));
    ccore = kwargs.get('ccore', False);
    draw = kwargs.get('draw', True);

    sample = read_sample(path);

    print("Sample: ", path);

    bsas_instance = bsas(sample, amount, threshold, ccore=ccore, metric=metric);
    bsas_instance.process();

    clusters = bsas_instance.get_clusters();
    representatives = bsas_instance.get_representatives();

    if draw is True:
        bsas_visualizer.show_clusters(sample, clusters, representatives);


def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 1.0);

def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 1.0);

def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3, 4, 1.0);

def cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4, 5, 1.0);

def cluster_sample5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5, 4, 1.0);

def cluster_sample6():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6, 2, 1.0);

def cluster_elongate():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_ELONGATE, 2, 1.0);


cluster_sample1();
cluster_sample2();
cluster_sample3();
cluster_sample4();
cluster_sample5();
cluster_sample6();
cluster_elongate();