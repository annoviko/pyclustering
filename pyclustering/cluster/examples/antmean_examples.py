"""!

@brief Integration-tests for Ant-Mean algorithm.

@authors Andrei Novikov, Kukushkin Aleksey (pyclustering@yandex.ru)
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

from pyclustering.cluster.antmean import antmean;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;

from pyclustering.cluster import cluster_visualizer;
from pyclustering.cluster.antmean import antmean_clustering_params;

from pyclustering.utils import read_sample;

import time;


def template_clustering(path, count_clusters, iterations=50, count_ants=20, pheramone_init=0.1, ro=0.9):
    params = antmean_clustering_params()
    params.iterations = iterations
    params.count_ants = count_ants
    params.pheramone_init = pheramone_init
    params.ro = ro

    sample = read_sample(path)
    algo = antmean(sample, count_clusters, params)

    start_time = time.time()

    # Clustering ...
    algo.process()
    res = algo.get_clusters();

    print("Sample: ", path, "\t\tExecution time: ", time.time() - start_time, "\n")

    visualizer = cluster_visualizer(1)
    visualizer.append_clusters(res, sample)
    visualizer.show()


def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1,
                        count_clusters=2)


def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2,
                        count_clusters=3,
                        iterations=300,
                        count_ants=200,
                        pheramone_init=0.1,
                        ro=0.9)


def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3,
                        count_clusters=4,
                        iterations=700,
                        count_ants=1000,
                        pheramone_init=0.3,
                        ro=0.85)


def cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4,
                        count_clusters=5,
                        iterations=800,
                        count_ants=1000,
                        pheramone_init=0.3,
                        ro=0.9)


def cluster_sample5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5,
                        count_clusters=4,
                        iterations=800,
                        count_ants=1000,
                        pheramone_init=0.3,
                        ro=0.9)


def cluster_sample6():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6,
                        count_clusters=2,
                        iterations=300,
                        count_ants=200,
                        pheramone_init=0.1,
                        ro=0.9)


def cluster_sample7():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7,
                        count_clusters=2,
                        iterations=300,
                        count_ants=200,
                        pheramone_init=0.1,
                        ro=0.9)


def cluster_sample11():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11,
                        count_clusters=2,
                        iterations=300,
                        count_ants=200,
                        pheramone_init=0.1,
                        ro=0.9)


cluster_sample1()
cluster_sample2()
cluster_sample3()
cluster_sample4()
cluster_sample5()
cluster_sample6()
cluster_sample7()
cluster_sample11()


