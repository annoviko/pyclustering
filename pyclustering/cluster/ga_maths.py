"""!

@brief Genetic algorithm math API.

@authors Aleksey Kukushkin (pyclustering@yandex.ru)
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


class ga_math:
    """
    @brief Genetic algorithm math API.
    
    """

    @staticmethod
    def calc_count_centers(chromosome):
        return chromosome[chromosome.argmax()] + 1

    @staticmethod
    def get_clusters_representation(chromosome, count_clusters=None):
        """ Convert chromosome to cluster representation:
                chromosome : [0, 1, 1, 0, 2, 3, 3]
                clusters: [[0, 3], [1, 2], [4], [5, 6]]
        """

        if count_clusters is None:
            count_clusters = ga_math.calc_count_centers(chromosome)

        # Initialize empty clusters
        clusters = [[] for _ in range(count_clusters)]

        # Fill clusters with index of data
        for _idx_data in range(len(chromosome)):
            clusters[chromosome[_idx_data]].append(_idx_data)

        return clusters

    @staticmethod
    def get_centres(chromosomes, data, count_clusters):
        """!
        """

        centres = ga_math.calc_centers(chromosomes, data, count_clusters)

        return centres

    @staticmethod
    def calc_centers(chromosomes, data, count_clusters=None):
        """!
        """

        if count_clusters is None:
            count_clusters = ga_math.calc_count_centers(chromosomes[0])

        # Initialize center
        centers = np.zeros(shape=(len(chromosomes), count_clusters, len(data[0])))

        for _idx_chromosome in range(len(chromosomes)):

            # Get count data in clusters
            count_data_in_cluster = np.zeros(count_clusters)

            # Next data point
            for _idx in range(len(chromosomes[_idx_chromosome])):

                cluster_num = chromosomes[_idx_chromosome][_idx]

                centers[_idx_chromosome][cluster_num] += data[_idx]
                count_data_in_cluster[cluster_num] += 1

            for _idx_cluster in range(count_clusters):
                if count_data_in_cluster[_idx_cluster] != 0:
                    centers[_idx_chromosome][_idx_cluster] /= count_data_in_cluster[_idx_cluster]

        return centers

    @staticmethod
    def calc_probability_vector(fitness):
        """!
        """

        if len(fitness) == 0:
            raise AttributeError("Has no any fitness functions.")

        # Get 1/fitness function
        inv_fitness = np.zeros(len(fitness))

        #
        for _idx in range(len(inv_fitness)):

            if fitness[_idx] != 0.0:
                inv_fitness[_idx] = 1.0 / fitness[_idx]
            else:
                inv_fitness[_idx] = 0.0

        # Initialize vector
        prob = np.zeros(len(fitness))

        # Initialize first element
        prob[0] = inv_fitness[0]

        # Accumulate values in probability vector
        for _idx in range(1, len(inv_fitness)):
            prob[_idx] = prob[_idx - 1] + inv_fitness[_idx]

        # Normalize
        prob /= prob[-1]

        ga_math.set_last_value_to_one(prob)

        return prob

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
        for _ in range(-1, -len(probabilities) - 1):
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
            print('Probabilities : ', probabilities)
            raise AttributeError("'probabilities' should contain 1 as the end of last segment(s)")

        return res_idx

