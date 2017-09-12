"""!

@brief Unit-tests for center-initializer set.

@authors Andrei Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
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

import unittest;

from pyclustering.utils import read_sample;
from pyclustering.cluster.ga import GeneticAlgorithm;

from pyclustering.samples.definitions import SIMPLE_SAMPLES;


class GeneticAlgorithmClusteringUnitTest(unittest.TestCase):

    def test1CenterClustering(self):

        data = [[0, 0], [0, 2]]

        count_chromosomes = 10
        count_clusters = 1
        count_populations = 10
        count_mutations_gen = 1

        _, best_ff = GeneticAlgorithm(data=data,
                                      count_clusters=count_clusters,
                                      chromosome_count=count_chromosomes,
                                      population_count=count_populations,
                                      count_mutation_gens=count_mutations_gen).clustering()

        self.assertEqual(best_ff, 2.0)

    def test1Center4DataClustering(self):

        data = [[0, 0], [0, 2], [2, 0], [2, 2]]

        count_chromosomes = 10
        count_clusters = 1
        count_populations = 10
        count_mutations_gen = 1

        _, best_ff = GeneticAlgorithm(data=data,
                                      count_clusters=count_clusters,
                                      chromosome_count=count_chromosomes,
                                      population_count=count_populations,
                                      count_mutation_gens=count_mutations_gen).clustering()

        self.assertEqual(best_ff, 8.0)

    def test2Center8DataClustering(self):

        data = [[0, 0], [0, 2], [2, 0], [2, 2]]
        data.extend([[6, 0], [6, 2], [8, 0], [8, 2]])

        count_chromosomes = 50
        count_clusters = 2
        count_populations = 50
        count_mutations_gen = 1

        _, best_ff = GeneticAlgorithm(data=data,
                                      count_clusters=count_clusters,
                                      chromosome_count=count_chromosomes,
                                      population_count=count_populations,
                                      count_mutation_gens=count_mutations_gen).clustering()

        self.assertEqual(best_ff, 16.0)

    # @unittest.skip("unstable test (or long : 3 - 5s)")
    def test4Center16DataClustering(self):
        testing_result = False;
        
        for _ in range(3):
            data = []
            data.extend([[0, 0], [1, 0], [0, 1], [1, 1]])
            data.extend([[5, 0], [6, 0], [5, 1], [6, 1]])
            data.extend([[0, 5], [1, 5], [0, 6], [1, 6]])
            data.extend([[4, 4], [7, 4], [4, 7], [7, 7]])
    
            count_chromosomes = 20
            count_clusters = 4
            count_populations = 100
            count_mutations_gen = 1
    
            _, best_ff = GeneticAlgorithm(data=data,
                                          count_clusters=count_clusters,
                                          chromosome_count=count_chromosomes,
                                          population_count=count_populations,
                                          count_mutation_gens=count_mutations_gen).clustering()
    
            if (best_ff != 24.0):
                continue;
            
            testing_result = True;
        
        self.assertEqual(testing_result, True);


    def templateDataClustering(self, sample_path,
                                     amount_clusters,
                                     chromosome_count,
                                     population_count,
                                     count_mutation_gens,
                                     coeff_mutation_count,
                                     expected_clusters_sizes):
        testing_result = False;
        
        for _ in range(3):
            sample = read_sample(sample_path);
            
            ga_instance = GeneticAlgorithm(sample, amount_clusters, chromosome_count,
                                    population_count, count_mutation_gens, coeff_mutation_count);
            
            best_chromosome, _ = ga_instance.clustering();
            
            clusters = [[] for _ in range(amount_clusters)]
            for _idx in range(len(best_chromosome)):
                clusters[best_chromosome[_idx]].append(_idx);
            
            obtained_cluster_sizes = [len(cluster) for cluster in clusters];
            if (len(sample) != sum(obtained_cluster_sizes)):
                continue;
            
            if (expected_clusters_sizes != None):
                obtained_cluster_sizes.sort();
                expected_clusters_sizes.sort();
                if (obtained_cluster_sizes != expected_clusters_sizes):
                    continue;
            
            testing_result = True;
        
        assert testing_result == True;
    
    
    def testClusteringSampleSimple01(self):
        # Two dimensional data
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 2, 20, 30, 2, 0.25, [5, 5]);

    def testClusteringSampleSimple01WrongAllocation(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE1, 1, 20, 30, 2, 0.25, [10]);

    def testClusteringSampleSimple07(self):
        # One dimensional data
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 2, 20, 30, 2, 0.25, [10, 10]);

    def testClusteringSampleSimple07WrongAllocation(self):
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE7, 1, 20, 30, 2, 0.25, [20]);

    def testClusteringSampleSimple11(self):
        # Three dimensional data
        self.templateDataClustering(SIMPLE_SAMPLES.SAMPLE_SIMPLE11, 2, 20, 30, 2, 0.25, [10, 10]);


if __name__ == "__main__":
    unittest.main();
