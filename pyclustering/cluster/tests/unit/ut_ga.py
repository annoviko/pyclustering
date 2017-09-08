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

import unittest

from pyclustering.cluster.ga import GeneticAlgorithm


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

    @unittest.skip("unstable test (or long : 3 - 5s)")
    def DISABLED4Center16DataClustering(self):

        data = []
        data.extend([[0, 0], [1, 0], [0, 1], [1, 1]])
        data.extend([[5, 0], [6, 0], [5, 1], [6, 1]])
        data.extend([[0, 5], [1, 5], [0, 6], [1, 6]])
        data.extend([[4, 4], [7, 4], [4, 7], [7, 7]])

        count_chromosomes = 100
        count_clusters = 4
        count_populations = 150
        count_mutations_gen = 1

        _, best_ff = GeneticAlgorithm(data=data,
                                      count_clusters=count_clusters,
                                      chromosome_count=count_chromosomes,
                                      population_count=count_populations,
                                      count_mutation_gens=count_mutations_gen).clustering()

        self.assertEqual(best_ff, 24.0)
