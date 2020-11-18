"""!

@brief Unit-tests for genetic clustering algorithm.

@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import unittest
import inspect
import numpy

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.cluster.ga import genetic_algorithm, ga_observer, ga_visualizer
from pyclustering.cluster.ga_maths import ga_math
from pyclustering.utils import read_sample


class GeneticAlgorithmClusteringUnitTest(unittest.TestCase):
    def runGeneticAlgorithm(self, test_case_name, data, count_chromosomes, count_clusters, count_populations,
                            count_mutations_gen, result_should_be):

        _, best_ff, = genetic_algorithm(data=data,
                                        count_clusters=count_clusters,
                                        chromosome_count=count_chromosomes,
                                        population_count=count_populations,
                                        count_mutation_gens=count_mutations_gen, random_state=1000).process()

        # Check result
        self.assertEqual(best_ff, result_should_be)

    def test1CenterClustering(self):

        data = [[0, 0], [0, 2]]

        self.runGeneticAlgorithm(test_case_name=inspect.stack()[0][3],
                                 data=data,
                                 count_chromosomes=10,
                                 count_clusters=1,
                                 count_populations=10,
                                 count_mutations_gen=1,
                                 result_should_be=2.0)

    def test1Center4DataClustering(self):

        data = [[0, 0], [0, 2], [2, 0], [2, 2]]

        self.runGeneticAlgorithm(test_case_name=inspect.stack()[0][3],
                                 data=data,
                                 count_chromosomes=10,
                                 count_clusters=1,
                                 count_populations=10,
                                 count_mutations_gen=1,
                                 result_should_be=8.0)

    def test2Center8DataClustering(self):

        data = [[0, 0], [0, 2], [2, 0], [2, 2]]
        data.extend([[6, 0], [6, 2], [8, 0], [8, 2]])

        self.runGeneticAlgorithm(test_case_name=inspect.stack()[0][3],
                                 data=data,
                                 count_chromosomes=50,
                                 count_clusters=2,
                                 count_populations=50,
                                 count_mutations_gen=1,
                                 result_should_be=16.0)

    def test4Center16DataClustering(self):

        data = []
        data.extend([[0, 0], [1, 0], [0, 1], [1, 1]])
        data.extend([[5, 0], [6, 0], [5, 1], [6, 1]])
        data.extend([[0, 5], [1, 5], [0, 6], [1, 6]])
        data.extend([[4, 4], [7, 4], [4, 7], [7, 7]])

        self.runGeneticAlgorithm(test_case_name=inspect.stack()[0][3],
                                 data=data,
                                 count_chromosomes=20,
                                 count_clusters=4,
                                 count_populations=100,
                                 count_mutations_gen=1,
                                 result_should_be=24.0)


    def templateDataClustering(self,
                               sample_path,
                               amount_clusters,
                               chromosome_count,
                               population_count,
                               count_mutation_gens,
                               coeff_mutation_count,
                               expected_clusters_sizes,
                               **kwargs):

        scale_points = kwargs.get('scale_points', None)

        sample = numpy.array(read_sample(sample_path))
        if scale_points is not None:
            sample = sample * scale_points

        ga_instance = genetic_algorithm(sample, amount_clusters, chromosome_count, population_count,
                                        count_mutations_gen=count_mutation_gens,
                                        coeff_mutation_count=coeff_mutation_count,
                                        **kwargs)

        ga_instance.process()
        clusters = ga_instance.get_clusters()

        obtained_cluster_sizes = [len(cluster) for cluster in clusters]
        self.assertEqual(len(sample), sum(obtained_cluster_sizes))

        if expected_clusters_sizes is not None:
            obtained_cluster_sizes.sort()
            expected_clusters_sizes.sort()

            self.assertEqual(obtained_cluster_sizes, expected_clusters_sizes)


    def testClusteringTwoDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 20, 20, 2, 0.25, [5, 5], random_state=1000)

    def testClusteringTwoDimensionalDataWrongAllocation(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 20, 20, 2, 0.25, [10], random_state=1000)

    def testClusteringNonNormalizedValues(self):
        self.assertRaises(ValueError, self.templateDataClustering, SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 20, 20, 2, 0.25, [5, 5], random_state=1000, scale_points=1000)

    def testClusteringSimple02(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE2, 3, 20, 40, 2, 0.25, [5, 8, 10], random_state=1000)

    def testClusteringSimple09(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE9, 2, 20, 20, 2, 0.25, [10, 20], random_state=1000)

    def testClusteringOneDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 20, 20, 2, 0.25, [10, 10], random_state=1000)

    def testClusteringOneDimensionalDataWrongAllocation(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 1, 20, 20, 2, 0.25, [20], random_state=1000)

    def testClusteringThreeDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, 20, 20, 2, 0.25, [10, 10], random_state=1000)

    def testClusteringThreeDimensionalDataWrongAllocation(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, 20, 20, 2, 0.25, [20], random_state=1000)

    def testTwoClustersTotallySimilarObjects(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, 20, 20, 2, 0.25, None, random_state=1000)

    def testFiveClustersTotallySimilarObjects(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, 20, 20, 2, 0.25, None, random_state=1000)

    def testTenClustersTotallySimilarObjects(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 10, 20, 20, 2, 0.25, None, random_state=1000)


    def templateTestObserverCollecting(self, amount_clusters, iterations, global_optimum, local_optimum, average, **kwargs):
        observer_instance = ga_observer(global_optimum, local_optimum, average)

        self.assertEqual(0, len(observer_instance))

        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)

        ga_instance = genetic_algorithm(sample, amount_clusters, 20, iterations, count_mutation_gens=2,
                                        coeff_mutation_count=0.25, observer=observer_instance, **kwargs)
        ga_instance.process()

        self.assertEqual(observer_instance, ga_instance.get_observer())

        expected_length = 0
        if global_optimum is True:
            expected_length = iterations + 1
            self.assertEqual(expected_length, len(observer_instance))

        self.assertEqual(expected_length, len(observer_instance.get_global_best()['chromosome']))
        self.assertEqual(expected_length, len(observer_instance.get_global_best()['fitness_function']))

        expected_length = 0
        if local_optimum is True:
            expected_length = iterations + 1
            self.assertEqual(expected_length, len(observer_instance))

        self.assertEqual(expected_length, len(observer_instance.get_population_best()['chromosome']))
        self.assertEqual(expected_length, len(observer_instance.get_population_best()['fitness_function']))

        expected_length = 0
        if average is True:
            expected_length = iterations + 1
            self.assertEqual(expected_length, len(observer_instance))

        self.assertEqual(expected_length, len(observer_instance.get_mean_fitness_function()))

        if global_optimum is True:
            clusters = ga_math.get_clusters_representation(observer_instance.get_global_best()['chromosome'][-1])
            self.assertEqual(amount_clusters, len(clusters))

        return sample, observer_instance


    def testObserveGlobalOptimum(self):
        self.templateTestObserverCollecting(2, 10, True, False, False, random_state=1000)

    def testObserveLocalOptimum(self):
        self.templateTestObserverCollecting(2, 11, False, True, False, random_state=1000)

    def testObserveAverage(self):
        self.templateTestObserverCollecting(2, 12, False, False, True, random_state=1000)

    def testObserveAllParameters(self):
        self.templateTestObserverCollecting(2, 9, True, True, True, random_state=1000)

    def testObserveNoCollecting(self):
        self.templateTestObserverCollecting(2, 9, False, False, False, random_state=1000)

    def testObserveParameterCombinations(self):
        self.templateTestObserverCollecting(3, 10, True, True, False, random_state=1000)
        self.templateTestObserverCollecting(4, 10, True, False, True, random_state=1000)
        self.templateTestObserverCollecting(1, 10, False, True, True, random_state=1000)


    def testNoFailureVisualizationApi(self):
        sample, observer = self.templateTestObserverCollecting(2, 10, True, True, True, random_state=1000)
        
        ga_visualizer.show_evolution(observer)
        ga_visualizer.show_clusters(sample, observer)
        ga_visualizer.animate_cluster_allocation(sample, observer)

    def testNoFailureShowEvolution(self):
        _, observer = self.templateTestObserverCollecting(2, 10, True, True, True, random_state=1000)
        
        ga_visualizer.show_evolution(observer, 2, 5)
        ga_visualizer.show_evolution(observer, 2, len(observer))
        ga_visualizer.show_evolution(observer, 2, len(observer), display=False)


    def testNoneObserver(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        ga_instance = genetic_algorithm(sample, 2, 20, 20, count_mutation_gens=2,
                                        coeff_mutation_count=0.25, observer=None)
        ga_instance.process()

        self.assertIsNone(ga_instance.get_observer())


    def test_incorrect_data(self):
        self.assertRaises(ValueError, genetic_algorithm, [], 1, 2, 2)

    def test_incorrect_amount_clusters(self):
        self.assertRaises(ValueError, genetic_algorithm, [[0], [1], [2]], 0, 2, 2)
