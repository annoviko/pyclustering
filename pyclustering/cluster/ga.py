"""!

@brief Cluster analysis algorithm: Genetic clustering algorithm (GA).

@authors Andrey Novikov, Aleksey Kukushkin (pyclustering@yandex.ru)
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


import numpy as np;
import math;

import matplotlib.pyplot as plt;
import matplotlib.animation as animation;

from pyclustering.cluster import cluster_visualizer;
from pyclustering.cluster.ga_maths import ga_math;



class ga_observer:
    """!

    """

    def __init__(self, need_global_best=False, need_population_best=False, need_mean_ff=False):
        """ """

        # Global best chromosome and fitness function for each population
        self._global_best_result = {'chromosome': [], 'fitness_function': []};

        # Best chromosome and fitness function on a population
        self._best_population_result = {'chromosome': [], 'fitness_function': []};

        # Mean fitness function on each population
        self._mean_ff_result = [];

        # Flags to collect
        self._need_global_best = need_global_best;
        self._need_population_best = need_population_best;
        self._need_mean_ff = need_mean_ff;


    def __len__(self):
        return len(self._global_best_result['chromosome']);


    def collect_global_best(self, best_chromosome, best_fitness_function):
        """ """

        if not self._need_global_best:
            return;

        self._global_best_result['chromosome'].append(best_chromosome);
        self._global_best_result['fitness_function'].append(best_fitness_function);


    def collect_population_best(self, best_chromosome, best_fitness_function):
        """ """

        if not self._need_population_best:
            return;

        self._best_population_result['chromosome'].append(best_chromosome);
        self._best_population_result['fitness_function'].append(best_fitness_function);


    def collect_mean(self, fitness_functions):
        """ """

        if not self._need_mean_ff:
            return;

        self._mean_ff_result.append(np.mean(fitness_functions));


    def get_global_best(self):
        return self._global_best_result;


    def get_population_best(self):
        return self._best_population_result;


    def get_mean_fitness_function(self):
        return self._mean_ff_result;



class ga_visualizer:
    @staticmethod
    def show_evolution(observer, start_iteration = 0, stop_iteration = None, ax = None, display = True):
        if (ax is None):
            _, ax = plt.subplots(1);
            ax.set_title("Evolution");
        
        if (stop_iteration is None):
            stop_iteration = len(observer);
        
        line_best, = ax.plot(observer.get_global_best()['fitness_function'][start_iteration:stop_iteration], 'r');
        line_current, = ax.plot(observer.get_population_best()['fitness_function'][start_iteration:stop_iteration], 'k');
        line_mean, = ax.plot(observer.get_mean_fitness_function()[start_iteration:stop_iteration], 'c');

        ax.set_xlabel("Iteration");
        ax.set_ylabel("Fitness function");
        ax.legend([line_best, line_current, line_mean], ["The best pop.", "Cur. best pop.", "Average"], prop={'size': 10});
        ax.grid();

        print(start_iteration, stop_iteration);
        if (display is True):
            plt.show();


    @staticmethod
    def show_clusters(data, observer, marker = '.', markersize = None):
        figure = plt.figure();
        ax1 = figure.add_subplot(121);
        
        clusters = ga_math.get_clusters_representation(observer.get_global_best()['chromosome'][-1]);
        
        visualizer = cluster_visualizer(1, 2);
        visualizer.append_clusters(clusters, data, 0, marker, markersize);
        visualizer.show(figure, display = False);
        
        ga_visualizer.show_evolution(observer, 0, None, ax1, True);


    @staticmethod
    def animate_cluster_allocation(data, observer, animation_velocity = 75, save_movie = None):
        figure = plt.figure();
        
        def init_frame():
            return frame_generation(0);

        def frame_generation(index_iteration):
            figure.clf();
            
            figure.suptitle("Clustering genetic algorithm (iteration: " + str(index_iteration) +")", fontsize = 20, fontweight = 'bold');
            
            visualizer = cluster_visualizer(4, 2, ["Population #" + str(index_iteration), "The best population"]);
            
            local_minimum_clusters = ga_math.get_clusters_representation(observer.get_population_best()['chromosome'][index_iteration]);
            visualizer.append_clusters(local_minimum_clusters, data, 0);
            
            global_minimum_clusters = ga_math.get_clusters_representation(observer.get_global_best()['chromosome'][index_iteration]);
            visualizer.append_clusters(global_minimum_clusters, data, 1);
            
            ax1 = plt.subplot2grid((2, 2), (1, 0), colspan = 2);
            ga_visualizer.show_evolution(observer, 0, index_iteration + 1, ax1, False);
            
            visualizer.show(figure, shift = 0, display = False);
            figure.subplots_adjust(top = 0.85);
            
            return [ figure.gca() ];
        
        iterations = len(observer);
        cluster_animation = animation.FuncAnimation(figure, frame_generation, iterations, interval = animation_velocity, init_func = init_frame, repeat_delay = 5000);

        if (save_movie is not None):
#             plt.rcParams['animation.ffmpeg_path'] = 'D:\\Program Files\\ffmpeg-3.3.1-win64-static\\bin\\ffmpeg.exe';
#             ffmpeg_writer = animation.FFMpegWriter(fps = 15);
#             cluster_animation.save(save_movie, writer = ffmpeg_writer);
            cluster_animation.save(save_movie, writer = 'ffmpeg', fps = 15, bitrate = 1500);
        else:
            plt.show();


class genetic_algorithm:
    """!
    @brief Class represents Genetic clustering algorithm.
    @details The searching capability of genetic algorithms is exploited in order to search for appropriate
             cluster centres.

    """

    def __init__(self, data, count_clusters, chromosome_count, population_count, count_mutation_gens=2,
                 coeff_mutation_count=0.25, select_coeff=1.0, observer=ga_observer()):
        """!
        @brief Initialize genetic clustering algorithm for cluster analysis.
        
        @param[in] data (numpy.array|list): Input data for clustering that is represented by two dimensional array
                    where each row is a point, for example, [[0.0, 2.1], [0.1, 2.0], [-0.2, 2.4]].
        @param[in] count_clusters (uint): Amount of clusters that should be allocated in the data.
        @param[in] chromosome_count (uint): Amount of chromosomes in each population.
        @param[in] population_count (uint): Amount of populations.
        @param[in] count_mutation_gens (uint): Amount of genes in chromosome that is mutated on each step.
        @param[in] coeff_mutation_count (float): Percent of chromosomes for mutation, destributed in range (0, 1] and
                    thus amount of chromosomes is defined as follows: 'chromosome_count' * 'coeff_mutation_count'.
        @param[in] select_coeff (float): Exponential coefficient for selection procedure that is used as follows:
                   math.exp(1 + fitness(chromosome) * select_coeff).
        
        """
        
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

        # Result of clustering : best chromosome
        self.result_clustering = {'best_chromosome': [],
                                  'best_fitness_function': 0.0}

        # Observer
        self.observer = observer

    def process(self):
        """!
        @brief Perform clustering procedure in line with rule of genetic clustering algorithm.
        
        @see get_clusters()
        
        """

        # Initialize population
        chromosomes = self._init_population(self.count_clusters, len(self.data), self.chromosome_count)

        # Initialize the Best solution
        best_chromosome, best_ff, first_fitness_functions \
            = self._get_best_chromosome(chromosomes, self.data, self.count_clusters)

        # Save best result into observer
        self.observer.collect_global_best(best_chromosome, best_ff)
        self.observer.collect_population_best(best_chromosome, best_ff)
        self.observer.collect_mean(first_fitness_functions)

        # Next population
        for _idx in range(self.population_count):

            # Select
            chromosomes = self._select(chromosomes, self.data, self.count_clusters, self.select_coeff)

            # Crossover
            self._crossover(chromosomes)

            # Mutation
            self._mutation(chromosomes, self.count_clusters, self.count_mutation_gens, self.coeff_mutation_count)

            # Update the Best Solution
            new_best_chromosome, new_best_ff, fitness_functions \
                = self._get_best_chromosome(chromosomes, self.data, self.count_clusters)

            # Get best chromosome
            if new_best_ff < best_ff:
                best_ff = new_best_ff
                best_chromosome = new_best_chromosome

            # Save best result into observer
            self.observer.collect_global_best(best_chromosome, best_ff)
            self.observer.collect_population_best(new_best_chromosome, new_best_ff)
            self.observer.collect_mean(fitness_functions)

        # Save result
        self.result_clustering['best_chromosome'] = best_chromosome
        self.result_clustering['best_fitness_function'] = best_ff

        return best_chromosome, best_ff


    def get_observer(self):
        """!
        @brief Returns genetic algorithm observer.
        
        """
        return self.observer


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects from the data.
        
        @return (list) List of allocated clusters.
        
        @see process()
        
        """

        return ga_math.get_clusters_representation(self.result_clustering['best_chromosome'], self.count_clusters)


    @staticmethod
    def _select(chromosomes, data, count_clusters, select_coeff):
        """!
        @brief Performs selection procedure where new chromosomes are calculated.
        
        @param[in] chromosomes (numpy.array): Chromosomes 
        
        """

        # Calc centers
        centres = ga_math.get_centres(chromosomes, data, count_clusters)

        # Calc fitness functions
        fitness = genetic_algorithm._calc_fitness_function(centres, data, chromosomes)

        for _idx in range(len(fitness)):
            fitness[_idx] = math.exp(1 + fitness[_idx] * select_coeff)

        # Calc probability vector
        probabilities = ga_math.calc_probability_vector(fitness)

        # Select P chromosomes with probabilities
        new_chromosomes = np.zeros(chromosomes.shape, dtype=np.int)

        # Selecting
        for _idx in range(len(chromosomes)):
            new_chromosomes[_idx] = chromosomes[ga_math.get_uniform(probabilities)]

        return new_chromosomes


    @staticmethod
    def _crossover(chromosomes):
        """!
        @brief Crossover procedure.
        
        """

        # Get pairs to Crossover
        pairs_to_crossover = np.array(range(len(chromosomes)))

        # Set random pairs
        np.random.shuffle(pairs_to_crossover)

        # Index offset ( pairs_to_crossover split into 2 parts : [V1, V2, .. | P1, P2, ...] crossover between V<->P)
        offset_in_pair = int(len(pairs_to_crossover) / 2)

        # For each pair
        for _idx in range(offset_in_pair):

            # Generate random mask for crossover
            crossover_mask = genetic_algorithm._get_crossover_mask(len(chromosomes[_idx]))

            # Crossover a pair
            genetic_algorithm._crossover_a_pair(chromosomes[pairs_to_crossover[_idx]],
                                                chromosomes[pairs_to_crossover[_idx + offset_in_pair]],
                                                crossover_mask)


    @staticmethod
    def _mutation(chromosomes, count_clusters, count_gen_for_mutation, coeff_mutation_count):
        """!
        @brief Mutation procedure.
        
        """

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
        """!
        @brief Crossovers a pair of chromosomes.
        
        @param[in] chromosome_1 (numpy.array): The first chromosome for crossover.
        @param[in] chromosome_2 (numpy.array): The second chromosome for crossover.
        @param[in] mask (numpy.array): Crossover mask that defines which genes should be swapped.
        
        """

        for _idx in range(len(chromosome_1)):

            if mask[_idx] == 1:
                # Swap values
                chromosome_1[_idx], chromosome_2[_idx] = chromosome_2[_idx], chromosome_1[_idx]


    @staticmethod
    def _get_crossover_mask(mask_length):
        """!
        @brief Crossover mask to crossover a pair of chromosomes.
        
        @param[in] mask_length (uint): Length of the mask.
        
        """

        # Initialize mask
        mask = np.zeros(mask_length)

        # Set a half of array to 1
        mask[:int(int(mask_length) / 6)] = 1

        # Random shuffle
        np.random.shuffle(mask)

        return mask


    @staticmethod
    def _init_population(count_clusters, count_data, chromosome_count):
        """!
        @brief Returns first population as a uniform random choice.
        
        @param[in] count_clusters (uint):
        @param[in] count_data (uint):
        @param[in] chromosome_count (uint): 
        
        """

        population = np.random.randint(count_clusters, size=(chromosome_count, count_data))

        return population


    @staticmethod
    def _get_best_chromosome(chromosomes, data, count_clusters):
        """!
        @brief 
        
        """

        # Calc centers
        centres = ga_math.get_centres(chromosomes, data, count_clusters)

        # Calc Fitness functions
        fitness_functions = genetic_algorithm._calc_fitness_function(centres, data, chromosomes)

        # Index of the best chromosome
        best_chromosome_idx = fitness_functions.argmin()

        # Get chromosome with the best fitness function
        return chromosomes[best_chromosome_idx], fitness_functions[best_chromosome_idx], fitness_functions


    @staticmethod
    def _calc_fitness_function(centres, data, chromosomes):
        """!
        @brief 
        
        """

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
