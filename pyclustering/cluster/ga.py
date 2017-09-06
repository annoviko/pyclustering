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


class GeneticAlgorithm:
    """!
    @brief Class represents Genetic clustering algorithm

    """

    def __init__(self, data, count_clusters,  chromosome_count, population_count, count_mutation_gens=2):

        # Initialize random
        np.random.seed()

        # Clustering data
        self.data = data

        # Count clusters
        self.count_clusters = count_clusters

        # Home many chromosome in population
        self.chromosome_count = chromosome_count

        # How many populations
        self.population_count = population_count

        # Count mutation genes
        self.count_mutation_gens = count_mutation_gens

    def clustering(self):
        """

        :return:
        """

        # Initialize population
        chromosomes = self.init_population(self.count_clusters, len(self.data), self.chromosome_count)

        # Initialize the Best solution
        best_chromosome, best_ff = self.get_best_chromosome(chromosomes, self.data, self.count_clusters)

        # Next population
        for _ in range(self.population_count):
            pass

            # Select
            chromosomes = self.select(chromosomes, self.data, self.count_clusters)

            # Crossover
            self.crossover(chromosomes)

            # Mutation
            self.mutation(chromosomes, self.count_clusters, self.count_mutation_gens)

            # Update the Best Solution
            new_best_chromosome, new_best_ff = self.get_best_chromosome(chromosomes, self.data, self.count_clusters)

            print('new best_chromosome : ', new_best_chromosome)
            print('new best_ff : ', new_best_ff)

            if new_best_ff < best_ff:
                best_ff = new_best_ff
                best_chromosome = new_best_chromosome


        print('best_chromosome : ', best_chromosome)
        print('best_ff : ', best_ff)

    @staticmethod
    def mutation(chromosomes, count_clusters, count_gen_for_mutation):
        """  """

        # Count gens in Chromosome
        count_gens = len(chromosomes[0])

        #
        for _idx_chromosome in range(len(chromosomes)):

            #
            for _ in range(count_gen_for_mutation):

                # Get random gen
                gen_num = np.random.randint(count_gens)

                # Set random cluster
                chromosomes[_idx_chromosome][gen_num] = np.random.randint(count_clusters)

    @staticmethod
    def crossover(chromosomes):
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
            crossover_mask = GeneticAlgorithm.get_crossover_mask(len(chromosomes[_idx]))

            # Crossover a pair
            GeneticAlgorithm.crossover_a_pair(chromosomes[pairs_to_crossover[_idx]],
                                              chromosomes[pairs_to_crossover[_idx + offset_in_pair]],
                                              crossover_mask)

    @staticmethod
    def crossover_a_pair(chromosome_1, chromosome_2, mask):
        """  """

        for _idx in range(len(chromosome_1)):

            if mask[_idx] == 1:
                # Swap values
                chromosome_1[_idx], chromosome_2[_idx] = chromosome_2[_idx], chromosome_1[_idx]

    @staticmethod
    def get_crossover_mask(mask_length):
        """  """

        # Initialize mask
        mask = np.zeros(mask_length)

        # Set a half of array to 1
        mask[:int(int(mask_length) / 2)] = 1

        # Random shuffle
        np.random.shuffle(mask)

        return mask

    @staticmethod
    def select(chromosomes, data, count_clusters):
        """  """

        # Calc centers
        centres = GeneticAlgorithm.get_centres(chromosomes, data, count_clusters)

        # Calc fitness functions
        fitness = GeneticAlgorithm.calc_fitness_function(centres, data)

        # Calc probability vector
        probabilities = GeneticAlgorithm.calc_probability_vector(fitness)

        # Select P chromosomes with probabilities
        new_chromosomes = np.zeros(chromosomes.shape)

        # Selecting
        for _idx in range(len(chromosomes)):
            new_chromosomes[_idx] = chromosomes[GeneticAlgorithm.get_uniform(probabilities)]

        return new_chromosomes

    @staticmethod
    def set_last_value_to_one(probabilities):
        """!
        @brief Update the last same probabilities to one.
        @details All values of probability list equals to the last element are set to 1.
        """

        # Start from the last elem
        back_idx = - 1

        # All values equal to the last elem should be set to 1
        last_val = probabilities[back_idx]

        # for all elements or if a elem not equal to the last elem
        for _idx in range(-1, -len(probabilities) - 1):
            if probabilities[back_idx] == last_val:
                probabilities[back_idx] = 1
            else:
                break

    @staticmethod
    def get_uniform(probabilities):
        """!
        @brief Returns index in probabilities.

        @param[in] probabilities (list): List with segments in increasing sequence with val in [0, 1],
                   for example, [0 0.1 0.2 0.3 1.0].
        """

        # Initialize return value
        res_idx = None

        # Get random num in range [0, 1)
        random_num = np.random.rand()

        # Find segment with  val1 < random_num < val2
        for _idx in range(len(probabilities)):
            if random_num < probabilities[_idx]:
                res_idx = _idx
                break

        if res_idx is None:
            raise AttributeError("'probabilities' should contain 1 as the end of last segment(s)")

        return res_idx

    @staticmethod
    def get_chromosome_by_probability(probabilities):
        """ """

        # Initialize return value
        res_idx = None

        # Get uniform random in [0, 1)
        random_num = np.random.rand()

        # Find element with  val1 < random_num < val2
        for _idx in range(len(probabilities)):
            if random_num < probabilities[_idx]:
                res_idx = _idx
                break

        if res_idx is None:
            raise AttributeError("List 'probabilities' should contain 1 as the end of last segment(s)")

        return res_idx

    @staticmethod
    def calc_probability_vector(fitness):
        """  """

        if len(fitness) == 0:
            raise AttributeError("Has no any fitness functions.")

        # Initialize vector
        prob = np.zeros(len(fitness))

        # Get min element
        min_elem = np.min(fitness)

        # Initialize first element
        prob[0] = fitness[0] - min_elem

        # Accumulate values in probability vector
        for _idx in range(1, len(fitness)):
            prob[_idx] = prob[_idx - 1] + fitness[_idx] - min_elem

        # Normalize
        prob /= np.sum(fitness - min_elem)

        return prob

    @staticmethod
    def init_population(count_clusters, count_data, chromosome_count):
        """ Returns first population as a uniform random choice """

        population = np.random.randint(count_clusters, size=(chromosome_count, count_data))

        return population

    @staticmethod
    def get_best_chromosome(chromosomes, data, count_clusters):
        """  """

        # Calc centers
        centres = GeneticAlgorithm.get_centres(chromosomes, data, count_clusters)

        # Calc Fitness functions
        fitness_function = GeneticAlgorithm.calc_fitness_function(centres, data)

        # Index of the best chromosome
        best_chromosome_idx = fitness_function.argmin()

        # Get chromosome with the best fitness function
        return chromosomes[best_chromosome_idx], fitness_function[best_chromosome_idx]

    @staticmethod
    def calc_fitness_function(centres, data):
        """  """

        # Get count of chromosomes and clusters
        count_chromosome = len(centres)
        count_clusters = len(centres[0])

        # Initialize fitness function values
        fitness_function = np.zeros(count_chromosome)

        # Calc fitness function for each chromosome
        for _idx_chromosome in range(count_chromosome):

            # Calc for each cluster in a chromosome
            for _idx_center in range(count_clusters):
                fitness_function[_idx_chromosome] += np.linalg.norm(data - centres[_idx_chromosome][_idx_center])

            # Normalize fitness function
            fitness_function[_idx_chromosome] /= count_clusters

        return fitness_function

    @staticmethod
    def get_centres(chromosomes, data, count_clusters):
        """ """

        # Initialize centres
        centres = np.zeros((len(chromosomes), count_clusters, len(data[0])))

        # Calc centers for next chromosome
        for _idx in range(len(chromosomes)):
            centres[_idx] = GeneticAlgorithm.calc_centers_for_chromosome(chromosomes[_idx], data, count_clusters)

        return centres

    @staticmethod
    def calc_centers_for_chromosome(chromosome, data, count_clusters):
        """ """

        # Initialize centers
        centers = np.zeros((count_clusters, len(data[0])))

        # Next cluster
        for _idx_cluster in range(count_clusters):
            centers[_idx_cluster] = GeneticAlgorithm.calc_the_center(chromosome, data, _idx_cluster)

        return centers

    @staticmethod
    def calc_the_center(chromosome, data, cluster_num):
        """ """

        # Initialize center
        center = np.zeros(len(data[0]))

        # Get count data in clusters
        count_data_in_cluster = np.sum(chromosome)

        # If has no data in cluster
        if count_data_in_cluster == 0:
            return center

        # Next data point
        for _idx in range(len(chromosome)):

            # If data associated with current cluster
            if chromosome[_idx] == cluster_num:
                center += data[_idx]

        # Normalize center
        center /= count_data_in_cluster

        return center


# --------------------------  Unit tests  -----------------------------------

# # Count Clusters and Data points
# COUNT_CHROMOSOMES = 4
# COUNT_CLUSTERS = 4
# COUNT_DATA_POINTS = 10
# DATA_DIMENSION = 2
#
# # Chromosome for test
# test_chromosomes = np.random.randint(COUNT_CLUSTERS, size=(COUNT_CHROMOSOMES, COUNT_DATA_POINTS))
#
# # Data points
# test_data = np.random.rand(COUNT_DATA_POINTS, DATA_DIMENSION)
#
# # Current cluster
# test_cluster_num = 2
#
# test_center = GeneticAlgorithm.get_centres(test_chromosomes, test_data, test_cluster_num)
#
# test_fitness = GeneticAlgorithm.calc_fitness_function(test_center, test_data)
#
# print('chromosome : ', test_chromosomes)
# print('data : ', test_data)
# print('center : ', test_center)
#
# print('center shape : ', test_center.shape)
#
# print('subtract : ', test_data - test_center[0][0])
#
# print('test_fitness : ', test_fitness)
#
# a = np.zeros(10)
# a[0] = -1
# a[1] = -1
#
# print('test_fitness min: ', GeneticAlgorithm.get_best_chromosome(test_chromosomes, test_data, COUNT_CLUSTERS))
#
# GeneticAlgorithm.crossover(test_chromosomes)


COUNT_CHROMOSOMES = 20
COUNT_CLUSTERS = 4
COUNT_POPULATIONS = 20
COUNT_MUTATIONS_GEN = 2

data_set_1 = []
data_set_1.extend([[0, 0], [1, 0], [0, 1], [1, 1]])
data_set_1.extend([[5, 0], [6, 0], [5, 1], [6, 1]])
data_set_1.extend([[0, 5], [1, 5], [0, 6], [1, 6]])
data_set_1.extend([[4, 4], [7, 4], [4, 7], [7, 7]])

test_data_2 = np.array(data_set_1)

GeneticAlgorithm(data=test_data_2,
                 count_clusters=COUNT_CLUSTERS,
                 chromosome_count=COUNT_CHROMOSOMES,
                 population_count=COUNT_POPULATIONS,
                 count_mutation_gens=COUNT_MUTATIONS_GEN).clustering()
