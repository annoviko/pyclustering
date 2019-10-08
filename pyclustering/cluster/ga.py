"""!

@brief Cluster analysis algorithm: Genetic clustering algorithm (GA).
@details Implementation based on papers @cite article::ga::1, @cite article::ga::2.

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


import numpy as np
import math
import warnings

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
except Exception as error_instance:
    warnings.warn("Impossible to import matplotlib (please, install 'matplotlib'), pyclustering's visualization "
                  "functionality is not available (details: '%s')." % str(error_instance))

from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.ga_maths import ga_math



class ga_observer:
    """!
    @brief Genetic algorithm observer that is used to collect information about clustering process on each iteration.
    
    """

    def __init__(self, need_global_best=False, need_population_best=False, need_mean_ff=False):
        """!
        @brief Constructs genetic algorithm observer to collect specific information.
        
        @param[in] need_global_best (bool): If 'True' then the best chromosomes and its fitness function value (global optimum) for each iteration are stored.
        @param[in] need_population_best (bool): If 'True' then current (on each iteration) best chromosomes and its fitness function value (local optimum) are stored.
        @param[in] need_mean_ff (bool): If 'True' then average value of fitness function on each iteration is stored.
        
        """

        # Global best chromosome and fitness function for each population
        self._global_best_result = {'chromosome': [], 'fitness_function': []}

        # Best chromosome and fitness function on a population
        self._best_population_result = {'chromosome': [], 'fitness_function': []}

        # Mean fitness function on each population
        self._mean_ff_result = []

        # Flags to collect
        self._need_global_best = need_global_best
        self._need_population_best = need_population_best
        self._need_mean_ff = need_mean_ff


    def __len__(self):
        """!
        @brief Returns amount of iterations that genetic algorithm was observed.
        
        """
        global_length = len(self._global_best_result['chromosome'])
        local_length = len(self._best_population_result['chromosome'])
        average_length = len(self._mean_ff_result)
        
        return max(global_length, local_length, average_length)


    def collect_global_best(self, best_chromosome, best_fitness_function):
        """!
        @brief Stores the best chromosome and its fitness function's value.
        
        @param[in] best_chromosome (list): The best chromosome that were observed.
        @param[in] best_fitness_function (float): Fitness function value of the best chromosome.
        
        """

        if not self._need_global_best:
            return

        self._global_best_result['chromosome'].append(best_chromosome)
        self._global_best_result['fitness_function'].append(best_fitness_function)


    def collect_population_best(self, best_chromosome, best_fitness_function):
        """!
        @brief Stores the best chromosome for current specific iteration and its fitness function's value.
        
        @param[in] best_chromosome (list): The best chromosome on specific iteration.
        @param[in] best_fitness_function (float): Fitness function value of the chromosome.
        
        """

        if not self._need_population_best:
            return

        self._best_population_result['chromosome'].append(best_chromosome)
        self._best_population_result['fitness_function'].append(best_fitness_function)


    def collect_mean(self, fitness_functions):
        """!
        @brief Stores average value of fitness function among chromosomes on specific iteration.
        
        @param[in] fitness_functions (float): Average value of fitness functions among chromosomes.
        
        """

        if not self._need_mean_ff:
            return

        self._mean_ff_result.append(np.mean(fitness_functions))


    def get_global_best(self):
        """!
        @return (dict) Returns dictionary with keys 'chromosome' and 'fitness_function' where evolution of the best chromosome
                 and its fitness function's value (evolution of global optimum) are stored in lists.
        
        """
        return self._global_best_result


    def get_population_best(self):
        """!
        @brief (dict) Returns dictionary with keys 'chromosome' and 'fitness_function' where evolution of the current best chromosome
                 and its fitness function's value (evolution of local optimum) are stored in lists.
        
        """
        return self._best_population_result


    def get_mean_fitness_function(self):
        """!
        @brief (list) Returns fitness function's values on each iteration.
        
        """
        return self._mean_ff_result



class ga_visualizer:
    """!
    @brief Genetic algorithm visualizer is used to show clustering results that are specific for
            this particular algorithm: clusters, evolution of global and local optimum.
    @details The visualizer requires 'ga_observer' that collects evolution of clustering process in
              genetic algorithm. The observer is created by user and passed to genetic algorithm. There
              is usage example of the visualizer using the observer:
    @code
        from pyclustering.cluster.ga import genetic_algorithm, ga_observer, ga_visualizer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import SIMPLE_SAMPLES


        # Read data for clustering
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE1)

        # Create instance of observer that will collect all information:
        observer_instance = ga_observer(True, True, True)

        # Create genetic algorithm where observer will collect information:
        ga_instance = genetic_algorithm(data=sample,
                                        count_clusters=2,
                                        chromosome_count=20,
                                        population_count=20,
                                        count_mutation_gens=1,
                                        observer=observer_instance)

        # Start processing
        ga_instance.process()

        # Obtain results
        clusters = ga_instance.get_clusters()

        # Print cluster to console
        print("Amount of clusters: '%d'. Clusters: '%s'" % (len(clusters), clusters))

        # Show cluster using observer:
        ga_visualizer.show_clusters(sample, observer_instance)
    @endcode
    
    @see cluster_visualizer
    
    """
    
    @staticmethod
    def show_evolution(observer, start_iteration = 0, stop_iteration=None, ax=None, display=True):
        """!
        @brief Displays evolution of fitness function for the best chromosome, for the current best chromosome and
                average value among all chromosomes.
        
        @param[in] observer (ga_observer): Genetic algorithm observer that was used for collecting evolution in the algorithm and
                    where whole required information for visualization is stored.
        @param[in] start_iteration (uint): Iteration from that evolution should be shown.
        @param[in] stop_iteration (uint): Iteration after that evolution shouldn't be shown.
        @param[in] ax (Axes): Canvas where evolution should be displayed.
        @param[in] display (bool): If 'True' then visualization of the evolution will be shown by the function.
                    This argument should be 'False' if you want to add something else to the canvas and display it later.
        
        @return (Axis) Canvas where evolution was shown.
        
        """
        
        if (ax is None):
            _, ax = plt.subplots(1)
            ax.set_title("Evolution")
        
        if stop_iteration is None:
            stop_iteration = len(observer)
        
        line_best, = ax.plot(observer.get_global_best()['fitness_function'][start_iteration:stop_iteration], 'r')
        line_current, = ax.plot(observer.get_population_best()['fitness_function'][start_iteration:stop_iteration], 'k')
        line_mean, = ax.plot(observer.get_mean_fitness_function()[start_iteration:stop_iteration], 'c')

        if start_iteration < (stop_iteration - 1):
            ax.set_xlim([start_iteration, (stop_iteration - 1)])
        
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Fitness function")
        ax.legend([line_best, line_current, line_mean], ["The best pop.", "Cur. best pop.", "Average"], prop={'size': 10})
        ax.grid()

        if display is True:
            plt.show()
        
        return ax


    @staticmethod
    def show_clusters(data, observer, marker='.', markersize=None):
        """!
        @brief Shows allocated clusters by the genetic algorithm.
        
        @param[in] data (list): Input data that was used for clustering process by the algorithm.
        @param[in] observer (ga_observer): Observer that was used for collection information about clustering process.
        @param[in] marker (char): Type of marker that should be used for object (point) representation.
        @param[in] markersize (uint): Size of the marker that is used for object (point) representation.
        
        @note If you have clusters instead of observer then 'cluster_visualizer' can be used for visualization purposes.
        
        @see cluster_visualizer
        
        """
        
        figure = plt.figure()
        ax1 = figure.add_subplot(121)
        
        clusters = ga_math.get_clusters_representation(observer.get_global_best()['chromosome'][-1])
        
        visualizer = cluster_visualizer(1, 2)
        visualizer.append_clusters(clusters, data, 0, marker, markersize)
        visualizer.show(figure, display=False)
        
        ga_visualizer.show_evolution(observer, 0, None, ax1, True)


    @staticmethod
    def animate_cluster_allocation(data, observer, animation_velocity=75, movie_fps=5, save_movie=None):
        """!
        @brief Animate clustering process of genetic clustering algorithm.
        @details This method can be also used for rendering movie of clustering process and 'ffmpeg' is required for that purpuse.
        
        @param[in] data (list): Input data that was used for clustering process by the algorithm.
        @param[in] observer (ga_observer): Observer that was used for collection information about clustering process.
                    Be sure that whole information was collected by the observer.
        @param[in] animation_velocity (uint): Interval between frames in milliseconds (for run-time animation only).
        @param[in] movie_fps (uint): Defines frames per second (for rendering movie only).
        @param[in] save_movie (string): If it is specified then animation will be stored to file that is specified in this parameter.
        
        """
        
        figure = plt.figure()
        
        def init_frame():
            return frame_generation(0)

        def frame_generation(index_iteration):
            figure.clf()
            
            figure.suptitle("Clustering genetic algorithm (iteration: " + str(index_iteration) + ")", fontsize=18, fontweight='bold')
            
            visualizer = cluster_visualizer(4, 2, ["The best pop. on step #" + str(index_iteration), "The best population"])
            
            local_minimum_clusters = ga_math.get_clusters_representation(observer.get_population_best()['chromosome'][index_iteration])
            visualizer.append_clusters(local_minimum_clusters, data, 0)
            
            global_minimum_clusters = ga_math.get_clusters_representation(observer.get_global_best()['chromosome'][index_iteration])
            visualizer.append_clusters(global_minimum_clusters, data, 1)
            
            ax1 = plt.subplot2grid((2, 2), (1, 0), colspan=2)
            ga_visualizer.show_evolution(observer, 0, index_iteration + 1, ax1, False)
            
            visualizer.show(figure, shift=0, display=False)
            figure.subplots_adjust(top=0.85)
            
            return [figure.gca()]
        
        iterations = len(observer)
        cluster_animation = animation.FuncAnimation(figure, frame_generation, iterations, interval=animation_velocity, init_func=init_frame, repeat_delay=5000)

        if save_movie is not None:
            cluster_animation.save(save_movie, writer='ffmpeg', fps=movie_fps, bitrate=1500)
        else:
            plt.show()


class genetic_algorithm:
    """!
    @brief Class represents Genetic clustering algorithm.
    @details The searching capability of genetic algorithms is exploited in order to search for appropriate
             cluster centres.
    
    Example of clustering using genetic algorithm:
    @code
        from pyclustering.cluster.ga import genetic_algorithm, ga_observer
        from pyclustering.utils import read_sample
        from pyclustering.samples.definitions import SIMPLE_SAMPLES


        # Read input data for clustering
        sample = read_sample(SIMPLE_SAMPLES.SAMPLE_SIMPLE4)

        # Create instance of observer that will collect all information:
        observer_instance = ga_observer(True, True, True)

        # Create genetic algorithm for clustering
        ga_instance = genetic_algorithm(data=sample,
                                        count_clusters=4,
                                        chromosome_count=100,
                                        population_count=200,
                                        count_mutation_gens=1)

        # Start processing
        ga_instance.process()

        # Obtain results
        clusters = ga_instance.get_clusters()

        # Print cluster to console
        print("Amount of clusters: '%d'. Clusters: '%s'" % (len(clusters), clusters))
    @endcode

    There is an example of clustering results (fitness function evolution and allocated clusters) that were 
    visualized by 'ga_visualizer':
    
    @image html ga_clustering_sample_simple_04.png

    @see ga_visualizer
    @see ga_observer

    """

    def __init__(self, data, count_clusters, chromosome_count, population_count, **kwargs):
        """!
        @brief Initialize genetic clustering algorithm for cluster analysis.
        
        @param[in] data (numpy.array|list): Input data for clustering that is represented by two dimensional array
                    where each row is a point, for example, [[0.0, 2.1], [0.1, 2.0], [-0.2, 2.4]].
        @param[in] count_clusters (uint): Amount of clusters that should be allocated in the data.
        @param[in] chromosome_count (uint): Amount of chromosomes in each population.
        @param[in] population_count (uint): Amount of populations.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'count_mutation_gens', 'coeff_mutation_count', 'select_coeff', 'crossover_rate', 'observer').

        <b>Keyword Args:</b><br>
            - count_mutation_gens (uint): Amount of genes in chromosome that is mutated on each step.
            - coeff_mutation_count (float): Percent of chromosomes for mutation, distributed in range (0, 1] and
               thus amount of chromosomes is defined as follows: 'chromosome_count' * 'coeff_mutation_count'.
            - select_coeff (float): Exponential coefficient for selection procedure that is used as follows:
               math.exp(1 + fitness(chromosome) * select_coeff).
            - crossover_rate (float): Crossover rate.
            - observer (ga_observer): Observer that is used for collecting information of about clustering process on each step.

        """
        
        # Initialize random
        np.random.seed()

        # Clustering data
        self._data = np.array(data)

        # Count clusters
        self._count_clusters = count_clusters

        # Home many chromosome in population
        self._chromosome_count = chromosome_count

        # How many populations
        self._population_count = population_count

        # Count mutation genes
        self._count_mutation_gens = kwargs.get('count_mutation_gens', 2)

        # Crossover rate
        self._crossover_rate = kwargs.get('crossover_rate', 1.0)

        # Count of chromosome for mutation (range [0, 1])
        self._coeff_mutation_count = kwargs.get('coeff_mutation_count', 0.25)

        # Exponential coeff for selection
        self._select_coeff = kwargs.get('select_coeff', 1.0)

        # Result of clustering : best chromosome
        self._result_clustering = {'best_chromosome': [],
                                   'best_fitness_function': 0.0}

        # Observer
        self._observer = kwargs.get('observer', ga_observer())

        self._verify_arguments()


    def process(self):
        """!
        @brief Perform clustering procedure in line with rule of genetic clustering algorithm.
        
        @see get_clusters()
        
        """

        # Initialize population
        chromosomes = self._init_population(self._count_clusters, len(self._data), self._chromosome_count)

        # Initialize the Best solution
        best_chromosome, best_ff, first_fitness_functions \
            = self._get_best_chromosome(chromosomes, self._data, self._count_clusters)

        # Save best result into observer
        if self._observer is not None:
            self._observer.collect_global_best(best_chromosome, best_ff)
            self._observer.collect_population_best(best_chromosome, best_ff)
            self._observer.collect_mean(first_fitness_functions)

        # Next population
        for _ in range(self._population_count):

            # Select
            chromosomes = self._select(chromosomes, self._data, self._count_clusters, self._select_coeff)

            # Crossover
            self._crossover(chromosomes)

            # Mutation
            self._mutation(chromosomes, self._count_clusters, self._count_mutation_gens, self._coeff_mutation_count)

            # Update the Best Solution
            new_best_chromosome, new_best_ff, fitness_functions \
                = self._get_best_chromosome(chromosomes, self._data, self._count_clusters)

            # Get best chromosome
            if new_best_ff < best_ff:
                best_ff = new_best_ff
                best_chromosome = new_best_chromosome

            # Save best result into observer
            if self._observer is not None:
                self._observer.collect_global_best(best_chromosome, best_ff)
                self._observer.collect_population_best(new_best_chromosome, new_best_ff)
                self._observer.collect_mean(fitness_functions)

        # Save result
        self._result_clustering['best_chromosome'] = best_chromosome
        self._result_clustering['best_fitness_function'] = best_ff

        return best_chromosome, best_ff


    def get_observer(self):
        """!
        @brief Returns genetic algorithm observer.
        
        """
        return self._observer


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects from the data.
        
        @return (list) List of allocated clusters.
        
        @see process()
        
        """

        return ga_math.get_clusters_representation(self._result_clustering['best_chromosome'], self._count_clusters)


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
        mask[:int(int(mask_length) / 2)] = 1

        # Random shuffle
        np.random.shuffle(mask)

        return mask


    @staticmethod
    def _init_population(count_clusters, count_data, chromosome_count):
        """!
        @brief Returns first population as a uniform random choice.
        
        @param[in] count_clusters (uint): Amount of clusters that should be allocated.
        @param[in] count_data (uint): Data size that is used for clustering process.
        @param[in] chromosome_count (uint):Amount of chromosome that is used for clustering.
        
        """

        population = np.random.randint(count_clusters, size=(chromosome_count, count_data))

        return population


    @staticmethod
    def _get_best_chromosome(chromosomes, data, count_clusters):
        """!
        @brief Returns the current best chromosome.
        
        @param[in] chromosomes (list): Chromosomes that are used for searching.
        @param[in] data (list): Input data that is used for clustering process.
        @param[in] count_clusters (uint): Amount of clusters that should be allocated.
        
        @return (list, float, list) The best chromosome, its fitness function value and fitness function values for
                 all chromosomes.
        
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
        @brief Calculate fitness function values for chromosomes.
        
        @param[in] centres (list): Cluster centers.
        @param[in] data (list): Input data that is used for clustering process.
        @param[in] chromosomes (list): Chromosomes whose fitness function's values are calculated.
        
        @return (list) Fitness function value for each chromosome correspondingly.
        
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


    def _verify_arguments(self):
        """!
        @brief Verify input parameters for the algorithm and throw exception in case of incorrectness.

        """
        if len(self._data) == 0:
            raise ValueError("Input data is empty (size: '%d')." % len(self._data))

        if self._count_clusters <= 0:
            raise ValueError("Amount of cluster (current value: '%d') for allocation should be greater than 0." %
                             self._count_clusters)
