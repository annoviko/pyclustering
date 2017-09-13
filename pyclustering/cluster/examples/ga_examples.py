

from pyclustering.samples.definitions import SIMPLE_SAMPLES, FCPS_SAMPLES

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.ga import GeneticAlgorithm

from pyclustering.utils import read_sample
from pyclustering.utils import timedcall

import time

import matplotlib.pyplot as plt


def template_clustering(path,
                        count_clusters,
                        chromosome_count,
                        population_count,
                        count_mutation_gens,
                        coeff_mutation_count=0.25,
                        select_coeff=1.0):

    sample = read_sample(path)

    algo_instance = GeneticAlgorithm(sample, count_clusters, chromosome_count,
                                     population_count, count_mutation_gens, coeff_mutation_count)

    start_time = time.time()
    best_chromosome, best_ff, arr_best_ff = algo_instance.clustering()

    print("Sample: ", path, "\t\tExecution time: ", time.time() - start_time, "\n")

    # clusters = kmeans_instance.get_clusters()
    # centers = kmeans_instance.get_centers()

    # print("Sample: ", path, "\t\tExecution time: ", ticks, "\n")

    clusters = [[] for _ in range(count_clusters)]

    for _idx in range(len(best_chromosome)):
        clusters[best_chromosome[_idx]].append(_idx)

    visualizer = cluster_visualizer()
    visualizer.append_clusters(clusters, sample)
    visualizer.show()

    plt.plot(arr_best_ff)
    plt.show()


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
                        population_count=150,
                        count_mutation_gens=1,
                        coeff_mutation_count=1.0,
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


# def cluster_sample8():
#     template_clustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE8,
#                         count_clusters=4,
#                         chromosome_count=50,
#                         population_count=200,
#                         count_mutation_gens=2,
#                         coeff_mutation_count=0.15,
#                         select_coeff=1.0)


# cluster_sample1()
# cluster_sample2()
cluster_sample3()
# cluster_sample4()
# cluster_sample5()
# cluster_sample6()
# cluster_sample7()
# cluster_sample8()
