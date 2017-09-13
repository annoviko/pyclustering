"""!

@brief Clustering by Genetic Algorithm

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

import numpy as np
import math

from pyclustering.cluster.ga_maths import GAMath


class GeneticAlgorithm:
    """!
    @brief Class represents Genetic clustering algorithm

    """

    def __init__(self, data, count_clusters,  chromosome_count, population_count, count_mutation_gens=2,
                 coeff_mutation_count=0.25, select_coeff=1.0):

        # Initialize random
        np.random.seed()

        # Clustering data
        if type(data) is list:
            self.data = np.array(data)
        else:
            self.data = data

        # Count clusters
        self.count_clusters = count_clusters

        # Home many chromosome in population
        self.chromosome_count = chromosome_count

        # How many populations
        self.population_count = population_count

        # Count mutation genes
        self.count_mutation_gens = count_mutation_gens

        # Crossover rate
        self.crossover_rate = 1.0

        # Count of chromosome for mutation (range [0, 1])
        self.coeff_mutation_count = coeff_mutation_count

        # Exponential coeff for selection
        self.select_coeff = select_coeff

    def clustering(self):
        """

        :return:
        """

        # Initialize population
        chromosomes = self._init_population(self.count_clusters, len(self.data), self.chromosome_count)

        # Initialize the Best solution
        best_chromosome, best_ff = self._get_best_chromosome(chromosomes, self.data, self.count_clusters)

        # Accumulate best_ff
        arr_best_ff = np.zeros(self.population_count)

        # Next population
        for _idx in range(self.population_count):

            arr_best_ff[_idx] = best_ff

            # Select
            chromosomes = self._select(chromosomes, self.data, self.count_clusters, self.select_coeff)

            # Crossover
            self._crossover(chromosomes)

            # Mutation
            self._mutation(chromosomes, self.count_clusters, self.count_mutation_gens, self.coeff_mutation_count)

            # Update the Best Solution
            new_best_chromosome, new_best_ff = self._get_best_chromosome(chromosomes, self.data, self.count_clusters)

            # Get best chromosome
            if new_best_ff < best_ff:
                best_ff = new_best_ff
                best_chromosome = new_best_chromosome

        return best_chromosome, best_ff, arr_best_ff

    @staticmethod
    def _select(chromosomes, data, count_clusters, select_coeff):
        """  """

        # Calc centers
        centres = GAMath.get_centres(chromosomes, data, count_clusters)

        # Calc fitness functions
        fitness = GeneticAlgorithm._calc_fitness_function(centres, data, chromosomes)

        for _idx in range(len(fitness)):
            fitness[_idx] = math.exp(1 + fitness[_idx] * select_coeff)

        # Calc probability vector
        probabilities = GAMath.calc_probability_vector(fitness)

        # Select P chromosomes with probabilities
        new_chromosomes = np.zeros(chromosomes.shape, dtype=np.int)

        # Selecting
        for _idx in range(len(chromosomes)):
            new_chromosomes[_idx] = chromosomes[GAMath.get_uniform(probabilities)]

        return new_chromosomes

    @staticmethod
    def _crossover(chromosomes):
        """  """

        # Get pairs to Crossover
        pairs_to_crossover = np.array(range(len(chromosomes)))

        # Set random pairs
        np.random.shuffle(pairs_to_crossover)

        # Index offset ( pairs_to_crossover split into 2 parts : [V1, V2, .. | P1, P2, ...] crossover between V<->P)
        offset_in_pair = int(len(pairs_to_crossover) / 2)

        # For each pair
        for _idx in range(offset_in_pair):

            # Generate random mask for crossover
            crossover_mask = GeneticAlgorithm._get_crossover_mask(len(chromosomes[_idx]))

            # Crossover a pair
            GeneticAlgorithm._crossover_a_pair(chromosomes[pairs_to_crossover[_idx]],
                                               chromosomes[pairs_to_crossover[_idx + offset_in_pair]],
                                               crossover_mask)

    @staticmethod
    def _mutation(chromosomes, count_clusters, count_gen_for_mutation, coeff_mutation_count):
        """  """

        # Count gens in Chromosome
        count_gens = len(chromosomes[0])

        # Get random chromosomes for mutation
        random_idx_chromosomes = np.array(range(len(chromosomes)))
        np.random.shuffle(random_idx_chromosomes)

        #
        for _idx_chromosome in range(int(len(random_idx_chromosomes) * coeff_mutation_count)):

            #
            for _ in range(count_gen_for_mutation):

                # Get random gen
                gen_num = np.random.randint(count_gens)

                # Set random cluster
                chromosomes[random_idx_chromosomes[_idx_chromosome]][gen_num] = np.random.randint(count_clusters)

    @staticmethod
    def _crossover_a_pair(chromosome_1, chromosome_2, mask):
        """  """

        for _idx in range(len(chromosome_1)):

            if mask[_idx] == 1:
                # Swap values
                chromosome_1[_idx], chromosome_2[_idx] = chromosome_2[_idx], chromosome_1[_idx]

    @staticmethod
    def _get_crossover_mask(mask_length):
        """  """

        # Initialize mask
        mask = np.zeros(mask_length)

        # Set a half of array to 1
        mask[:int(int(mask_length) / 6)] = 1

        # Random shuffle
        np.random.shuffle(mask)

        return mask

    @staticmethod
    def _init_population(count_clusters, count_data, chromosome_count):
        """ Returns first population as a uniform random choice """

        population = np.random.randint(count_clusters, size=(chromosome_count, count_data))

        return population

    @staticmethod
    def _get_best_chromosome(chromosomes, data, count_clusters):
        """  """

        # Calc centers
        centres = GAMath.get_centres(chromosomes, data, count_clusters)

        # Calc Fitness functions
        fitness_function = GeneticAlgorithm._calc_fitness_function(centres, data, chromosomes)

        # Index of the best chromosome
        best_chromosome_idx = fitness_function.argmin()

        # Get chromosome with the best fitness function
        return chromosomes[best_chromosome_idx], fitness_function[best_chromosome_idx]

    @staticmethod
    def _calc_fitness_function(centres, data, chromosomes):
        """  """

        # Get count of chromosomes and clusters
        count_chromosome = len(chromosomes)

        # Initialize fitness function values
        fitness_function = np.zeros(count_chromosome)

        # Calc fitness function for each chromosome
        for _idx_chromosome in range(count_chromosome):

            # Get centers for a selected chromosome
            centres_data = np.zeros(data.shape)

            # Fill data centres
            for _idx in range(len(data)):
                centres_data[_idx] = centres[_idx_chromosome][chromosomes[_idx_chromosome][_idx]]

            # Get City Block distance for a chromosome
            fitness_function[_idx_chromosome] += np.sum(abs(data - centres_data))

        return fitness_function
