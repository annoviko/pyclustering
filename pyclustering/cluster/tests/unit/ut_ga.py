"""!

@brief Unit-tests for genetic clustering algorithm.

@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
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

import unittest
import inspect

# Generate images without having a window appear.
import matplotlib
matplotlib.use('Agg')

from pyclustering.samples.definitions import SIMPLE_SAMPLES

from pyclustering.cluster.ga import genetic_algorithm, ga_observer, ga_visualizer
from pyclustering.cluster.ga_maths import ga_math
from pyclustering.utils import read_sample


class GeneticAlgorithmClusteringUnitTest(unittest.TestCase):

    # Count attempt to reach best result
    attempts = 3

    def runGeneticAlgorithm(self, test_case_name, data, count_chromosomes, count_clusters, count_populations,
                            count_mutations_gen, result_should_be):

        # Result
        best_ff = float('inf')

        # Several attempts for randomize algorithm
        for _attempt in range(GeneticAlgorithmClusteringUnitTest.attempts):

            _, best_ff, = genetic_algorithm(data=data,
                                            count_clusters=count_clusters,
                                            chromosome_count=count_chromosomes,
                                            population_count=count_populations,
                                            count_mutation_gens=count_mutations_gen).process()

            # Check result for attempt
            if best_ff == result_should_be:
                if _attempt > 0:
                    print('Test case :', test_case_name, ' success with attempts : ', _attempt + 1)
                break

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


    def templateDataClustering(self, sample_path,
                                     amount_clusters,
                                     chromosome_count,
                                     population_count,
                                     count_mutation_gens,
                                     coeff_mutation_count,
                                     expected_clusters_sizes):
        testing_result = False
        
        for _ in range(3):
            sample = read_sample(sample_path)
            
            ga_instance = genetic_algorithm(sample, amount_clusters, chromosome_count, population_count,
                                            count_mutations_gen=count_mutation_gens,
                                            coeff_mutation_count=coeff_mutation_count)
            
            ga_instance.process()
            clusters = ga_instance.get_clusters()
            
            obtained_cluster_sizes = [len(cluster) for cluster in clusters]
            if len(sample) != sum(obtained_cluster_sizes):
                continue
            
            if expected_clusters_sizes is not None:
                obtained_cluster_sizes.sort()
                expected_clusters_sizes.sort()
                if obtained_cluster_sizes != expected_clusters_sizes:
                    continue
            
            testing_result = True
            break
        
        assert testing_result is True
    
    
    def testClusteringTwoDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 20, 30, 2, 0.25, [5, 5])

    def testClusteringTwoDimensionalDataWrongAllocation(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 20, 30, 2, 0.25, [10])

    def testClusteringOneDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 20, 30, 2, 0.25, [10, 10])

    def testClusteringOneDimensionalDataWrongAllocation(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 1, 20, 30, 2, 0.25, [20])

    def testClusteringThreeDimensionalData(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, 20, 30, 2, 0.25, [10, 10])

    def testClusteringThreeDimensionalDataWrongAllocation(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 1, 20, 30, 2, 0.25, [20])

    def testTwoClustersTotallySimilarObjects(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 2, 20, 30, 2, 0.25, None)

    def testFiveClustersTotallySimilarObjects(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 5, 20, 30, 2, 0.25, None)

    def testTenClustersTotallySimilarObjects(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE12, 10, 20, 30, 2, 0.25, None)


    def templateTestObserverCollecting(self, amount_clusters, iterations, global_optimum, local_optimum, average):
        testing_result = False
        
        observer_instance = None
        sample = None
        
        for _ in range(3):
            observer_instance = ga_observer(global_optimum, local_optimum, average)
            
            assert len(observer_instance) == 0
            
            sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
            
            ga_instance = genetic_algorithm(sample, amount_clusters, 20, iterations, count_mutation_gens=2,
                                            coeff_mutation_count=0.25, observer=observer_instance)
            ga_instance.process()
            
            assert observer_instance == ga_instance.get_observer()
            
            expected_length = 0
            if (global_optimum is True):
                expected_length = iterations + 1
                assert expected_length == len(observer_instance)
            
            assert expected_length == len(observer_instance.get_global_best()['chromosome']);
            assert expected_length == len(observer_instance.get_global_best()['fitness_function']);

            expected_length = 0
            if (local_optimum is True):
                expected_length = iterations + 1
                assert expected_length == len(observer_instance);
            
            assert expected_length == len(observer_instance.get_population_best()['chromosome']);
            assert expected_length == len(observer_instance.get_population_best()['fitness_function']);
            
            expected_length = 0
            if (average is True):
                expected_length = iterations + 1
                assert expected_length == len(observer_instance);
            
            assert expected_length == len(observer_instance.get_mean_fitness_function());
            
            if (global_optimum is True):
                clusters = ga_math.get_clusters_representation(observer_instance.get_global_best()['chromosome'][-1])
                if amount_clusters != len(clusters):
                    continue
            
            testing_result = True
            break
        
        assert testing_result == True
        return sample, observer_instance


    def testObserveGlobalOptimum(self):
        self.templateTestObserverCollecting(2, 10, True, False, False)

    def testObserveLocalOptimum(self):
        self.templateTestObserverCollecting(2, 11, False, True, False)

    def testObserveAverage(self):
        self.templateTestObserverCollecting(2, 12, False, False, True)

    def testObserveAllParameters(self):
        self.templateTestObserverCollecting(2, 9, True, True, True)

    def testObserveNoCollecting(self):
        self.templateTestObserverCollecting(2, 9, False, False, False)

    def testObserveParameterCombinations(self):
        self.templateTestObserverCollecting(3, 10, True, True, False)
        self.templateTestObserverCollecting(4, 10, True, False, True)
        self.templateTestObserverCollecting(1, 10, False, True, True)


    def testNoFailureVisualizationApi(self):
        sample, observer = self.templateTestObserverCollecting(2, 10, True, True, True)
        
        ga_visualizer.show_evolution(observer)
        ga_visualizer.show_clusters(sample, observer)
        ga_visualizer.animate_cluster_allocation(sample, observer)

    def testNoFailureShowEvolution(self):
        _, observer = self.templateTestObserverCollecting(2, 10, True, True, True)
        
        ga_visualizer.show_evolution(observer, 2, 5)
        ga_visualizer.show_evolution(observer, 2, len(observer))
        ga_visualizer.show_evolution(observer, 2, len(observer), display=False)


    def testNoneObserver(self):
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)
        ga_instance = genetic_algorithm(sample, 2, 20, 20, count_mutation_gens=2,
                                        coeff_mutation_count=0.25, observer=None)
        ga_instance.process()
        assert None is ga_instance.get_observer()


    def test_incorrect_data(self):
        self.assertRaises(ValueError, genetic_algorithm, [], 1, 2, 2)

    def test_incorrect_amount_clusters(self):
        self.assertRaises(ValueError, genetic_algorithm, [[0], [1], [2]], 0, 2, 2)
