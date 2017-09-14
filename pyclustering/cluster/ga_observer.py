

import numpy as np


class genetic_algorithm_observer:
    """!

    """

    def __init__(self, need_global_best=False, need_population_best=False, need_mean_ff=False):
        """ """

        # Global best chromosome and fitness function for each population
        self.global_best_result = {'chromosome': [], 'fitness_function': []}

        # Best chromosome and fitness function on a population
        self.best_population_result = {'chromosome': [], 'fitness_function': []}

        # Mean fitness function on each population
        self.mean_ff_result = []

        # Flags to collect
        self.need_global_best = need_global_best
        self.need_population_best = need_population_best
        self.need_mean_ff = need_mean_ff

    def collect_global_best(self, best_chromosome, best_fitness_function):
        """ """

        if not self.need_global_best:
            return

        self.global_best_result['chromosome'].append(best_chromosome)
        self.global_best_result['fitness_function'].append(best_fitness_function)

    def collect_population_best(self, best_chromosome, best_fitness_function):
        """ """

        if not self.need_population_best:
            return

        self.best_population_result['chromosome'].append(best_chromosome)
        self.best_population_result['fitness_function'].append(best_fitness_function)

    def collect_mean(self, fitness_functions):
        """ """

        if not self.need_mean_ff:
            return

        self.mean_ff_result.append(np.mean(fitness_functions))

    def get_global_best(self):
        return self.global_best_result

    def get_population_best(self):
        return self.best_population_result

    def get_mean_fitness_function(self):
        return self.mean_ff_result


