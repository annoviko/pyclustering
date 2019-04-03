"""!

@brief Examples of usage and demonstration of abilities of genetic algorithm for cluster analysis.

@authors Aleksey Kukushkin (pyclustering@yandex.ru)
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


from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.cluster.ga import genetic_algorithm, ga_observer, ga_visualizer

from pyclustering.utils import read_sample

import time


def template_clustering(path,
                        count_clusters,
                        chromosome_count,
                        population_count,
                        count_mutation_gens,
                        coeff_mutation_count=0.25,
                        select_coeff=1.0,
                        fps=15,
                        animation=False):

    sample = read_sample(path)

    algo_instance = genetic_algorithm(data=sample,
                                      count_clusters=count_clusters,
                                      chromosome_count=chromosome_count,
                                      population_count=population_count,
                                      count_mutation_gens=count_mutation_gens,
                                      coeff_mutation_count=coeff_mutation_count,
                                      select_coeff=select_coeff,
                                      observer=ga_observer(True, True, True))

    start_time = time.time()

    algo_instance.process()

    print("Sample: ", path, "\t\tExecution time: ", time.time() - start_time, "\n")

    observer = algo_instance.get_observer()
    
    ga_visualizer.show_clusters(sample, observer)
    
    if (animation is True):
        ga_visualizer.animate_cluster_allocation(sample, observer, movie_fps=fps, save_movie="clustering_animation.mp4")
#         ga_visualizer.animate_cluster_allocation(sample, observer);


def cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1,
                        count_clusters=2,
                        chromosome_count=20,
                        population_count=20,
                        count_mutation_gens=2)


def cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2,
                        count_clusters=3,
                        chromosome_count=40,
                        population_count=120,
                        count_mutation_gens=2)


def cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3,
                        count_clusters=4,
                        chromosome_count=100,
                        population_count=200,
                        count_mutation_gens=2,
                        coeff_mutation_count=0.8,
                        select_coeff=0.3)


def cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4,
                        count_clusters=5,
                        chromosome_count=100,
                        population_count=200,
                        count_mutation_gens=1)


def cluster_sample5():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE5,
                        count_clusters=4,
                        chromosome_count=40,
                        population_count=140,
                        count_mutation_gens=1)


def cluster_sample6():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE6,
                        count_clusters=2,
                        chromosome_count=20,
                        population_count=100,
                        count_mutation_gens=1)


def cluster_sample7():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7,
                        count_clusters=2,
                        chromosome_count=20,
                        population_count=30,
                        count_mutation_gens=1)


def cluster_sample11():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11,
                        count_clusters=2,
                        chromosome_count=20,
                        population_count=30,
                        count_mutation_gens=2)


def cluster_sample8():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8,
                        count_clusters=4,
                        chromosome_count=50,
                        population_count=200,
                        count_mutation_gens=2,
                        coeff_mutation_count=0.15,
                        select_coeff=1.0)


def animation_cluster_sample1():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1,
                        count_clusters=2,
                        chromosome_count=10,
                        population_count=50,
                        count_mutation_gens=2,
                        select_coeff=0.02,
                        fps=5,
                        animation=True)

def animation_cluster_sample2():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2,
                        count_clusters=3,
                        chromosome_count=30,
                        population_count=150,
                        count_mutation_gens=2,
                        select_coeff=0.02,
                        fps=8,
                        animation=True)

def animation_cluster_sample3():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE3,
                        count_clusters=4,
                        chromosome_count=100,
                        population_count=150,
                        count_mutation_gens=2,
                        coeff_mutation_count=0.8,
                        select_coeff=0.3,
                        fps=5,
                        animation=True)

def animation_cluster_sample4():
    template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE4,
                        count_clusters=5,
                        chromosome_count=50,
                        population_count=500,
                        count_mutation_gens=2,
                        select_coeff=0.1,
                        fps=15,
                        animation=True)


cluster_sample1()
cluster_sample2()
cluster_sample3()
cluster_sample4()
cluster_sample5()
cluster_sample6()
cluster_sample7()
cluster_sample11()

animation_cluster_sample1()
animation_cluster_sample2()
animation_cluster_sample3()
animation_cluster_sample4()
